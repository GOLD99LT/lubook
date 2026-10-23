#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_sources_online.py —— sources.list.yaml 的联网复核（零第三方依赖，不依赖搜索 API）。

为什么需要它
  `verify:all` 证明的是「本地能构建、渲染契约没破」，证明不了「引用的文档还在、还是那一篇」。
  2026-10-23 首次全量复核就查出 12 条硬失败：TI/ADI 文档下架（404/410）、
  两条书目 ISBN 指向完全不同的书、一条 SparkFun 链接 302 到了别的教程。

三条策略（全部走直连 HTTP，不需要任何搜索 key）
  A 有 url      → GET（浏览器 UA / 跟随跳转 / 重试），抽标题（PDF DocInfo、XMP、HTML <title>），
                  与条目名做 token 匹配；
  B 有厂商编号  → 定点 URL：TI `https://www.ti.com/lit/pdf/<ID>`、ADI `MT-xxx` 的 PDF 模板；
  C 有 isbn     → openlibrary.org/api/books。
  死链再查 archive.org 快照，给出可替换的存档链接，避免「引用消失」变成「无据可查」。

判定
  OK          200 且标题至少命中 2 个词
  WEAK        200 但只命中 1 个词（多为措辞差异，人工扫一眼）
  MISMATCH    200 但标题完全对不上（典型：链接退化成聚合页/索引页）
  NO-TITLE    拿不到可用标题（PDF 元数据是 `Logo_final_v4` 这类垃圾）→ 人工
  DEAD        HTTP 4xx/5xx
  GONE        HTTP 410
  BLOCKED     反爬（401/403/429/202 无正文）→ 人工
  ERROR       网络层失败（超时 / DNS / TLS）→ 人工
  ISBN-OK / ISBN-MISMATCH / ISBN-MISSING
  NO-LINK     既无 url 也无 isbn 也无厂商编号 → 只能人工

退出码
  0  没有硬失败（DEAD / GONE / ISBN-MISMATCH）
  1  有硬失败；加 `--strict` 后 WEAK / MISMATCH / NO-TITLE / BLOCKED / ERROR / ISBN-MISSING 也算失败

为什么不进 `verify:all`
  外部站点的 403、改版、超时会让质量门禁无故变红，重演「门禁红但工程没问题」。
  本工具是「手动 / 定时」体检：红了开 issue，不拦内容提交。

用法
  python packages/tooling/src/check_sources_online.py --self-test
  python packages/tooling/src/check_sources_online.py                       # 全量
  python packages/tooling/src/check_sources_online.py --only hard            # 只看要修的
  python packages/tooling/src/check_sources_online.py --json .generated/sources-online.json
  python packages/tooling/src/check_sources_online.py --limit 10 --verbose   # 抽样
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths_util import REPO_ROOT  # noqa: E402

SOURCES_PATH = os.path.join(REPO_ROOT, 'sources.list.yaml')
DEFAULT_JSON = os.path.join(REPO_ROOT, '.generated', 'sources-online.json')

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0 Safari/537.36')
ACCEPT = 'text/html,application/pdf;q=0.9,*/*;q=0.8'
MAX_BODY = 4 * 1024 * 1024          # 标题只可能在前几 MB；PDF 的 DocInfo 常在尾部，留 4MB 余量
TI_PDF = 'https://www.ti.com/lit/pdf/%s'
ADI_PDF = 'https://www.analog.com/media/en/training-seminars/tutorials/%s.pdf'
ONSEMI_PDF = 'https://www.onsemi.com/pub/Collateral/%s-D.PDF'
WAYBACK = 'https://archive.org/wayback/available?url=%s'
OPENLIBRARY = ('https://openlibrary.org/api/books?bibkeys=ISBN:%s'
               '&format=json&jscmd=data')

# 硬失败：仓库侧一定要修（引用死了 / ISBN 指错书）
HARD = {'DEAD', 'GONE', 'ISBN-MISMATCH'}
# 人工档：反爬、超时、标题对不上；`--strict` 时也算失败
SOFT = {'WEAK', 'MISMATCH', 'NO-TITLE', 'BLOCKED', 'ERROR', 'ISBN-MISSING',
        'NO-LINK', 'SKIPPED'}

STOPWORDS = {
    'with', 'from', 'and', 'the', 'for', 'that', 'this', 'your', 'into', 'over',
    'after', 'their', 'about', 'using', 'based', 'design', 'guide', 'note',
    'notes', 'application', 'report', 'tutorial', 'series', 'handbook', 'edition',
}

# PDF / HTML 里常见的垃圾标题：不是文档名，不能当作「标题匹配」依据
JUNK_TITLE_RE = re.compile(
    r'^(?:logo|untitled|description|document|microsoft word|powerpoint|slide\s*\d|'
    r'table of contents|contents|1\s+introduction|introduction|index|home)(?![A-Za-z])',
    re.I)

TI_ID_RE = re.compile(r'\b(SL[A-Z]{2}\d{3}[A-Z]?)\b')
TI_ALT_ID_RE = re.compile(r'\b(TIDU\d{3,4}[A-Z]?|TIDA-\d{4,5}|SBOA\d{3}[A-Z]?)\b')
ADI_MT_RE = re.compile(r'\bMT-(\d{3})\b')
ONSEMI_AND_RE = re.compile(r'\bAND(\d{3,4})[-/]?([A-Z]?)\b')
CJK_RE = re.compile(r'[\u4e00-\u9fff]+')

BUCKET_RE = re.compile(r'^([a-z][a-z0-9_-]*):\s*$')
ENTRY_RE = re.compile(r'^- name:\s*(.*)$')
FIELD_RE = re.compile(r'^\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$')


# ---------------------------------------------------------------- 解析 sources

def parse_entries(path):
    """解析 sources.list.yaml 的条目（字段：name/url/isbn/type/vendor/rating）。

    只认本文件实际使用的形状：分桶（`official:` 等）+ 行首 `- name:` + 两空格缩进字段。
    刻意不引入 PyYAML —— 本仓 tooling 是「零第三方依赖」约定（见 paths_util.py 注释）。
    """
    entries = []
    bucket = ''
    cur = None
    with open(path, encoding='utf-8') as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            mb = BUCKET_RE.match(line)
            if mb:
                bucket = mb.group(1)
                cur = None
                continue
            me = ENTRY_RE.match(line)
            if me:
                cur = {'name': me.group(1).strip(), 'bucket': bucket, 'line': lineno,
                       'url': '', 'isbn': '', 'type': '', 'vendor': ''}
                entries.append(cur)
                continue
            if cur is None:
                continue
            mf = FIELD_RE.match(line)
            if not mf:
                continue
            key, val = mf.group(1), mf.group(2).strip()
            if key in ('url', 'isbn', 'type', 'vendor'):
                cur[key] = val.strip('"\'')
    return entries


def clean_name(name):
    """去掉括号里的补充说明，只留标题主体用于匹配。"""
    return re.sub(r'[（(][^）)]*[）)]', ' ', name).strip()


def tokens(text):
    """英文词元（>=4 字母、去停用词）。"""
    words = re.sub(r'[^A-Za-z0-9]+', ' ', text.lower()).split()
    return [w for w in words if len(w) >= 4 and w not in STOPWORDS]


def cjk_fragments(text):
    """中文片段（>=2 字），用于中英混排条目的兜底匹配。"""
    out = []
    for run in CJK_RE.findall(text):
        if len(run) >= 2:
            out.append(run)
    return out


# ---------------------------------------------------------------- 定点 URL

def derive_candidates(entry):
    """从条目名里的厂商编号推出可直连的定点 URL（顺序即优先级）。"""
    name = entry['name']
    urls = []
    for m in TI_ID_RE.finditer(name):
        urls.append(TI_PDF % m.group(1))
    for m in TI_ALT_ID_RE.finditer(name):
        urls.append(TI_PDF % m.group(1))
    for m in ADI_MT_RE.finditer(name):
        urls.append(ADI_PDF % ('MT-%s' % m.group(1)))
    for m in ONSEMI_AND_RE.finditer(name):
        urls.append(ONSEMI_PDF % ('AND%s%s' % (m.group(1), m.group(2))))
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


# ---------------------------------------------------------------- HTTP

class Result:
    __slots__ = ('status', 'final_url', 'ctype', 'body', 'error', 'elapsed')

    def __init__(self):
        self.status = 0
        self.final_url = ''
        self.ctype = ''
        self.body = b''
        self.error = ''
        self.elapsed = 0.0


def fetch(url, timeout=25.0, retries=1):
    res = Result()
    started = time.time()
    last = ''
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': ACCEPT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                res.status = resp.status
                res.final_url = resp.geturl()
                res.ctype = (resp.headers.get('content-type') or '').split(';')[0].strip().lower()
                res.body = resp.read(MAX_BODY)
            res.elapsed = time.time() - started
            return res
        except urllib.error.HTTPError as exc:
            res.status = exc.code
            res.final_url = exc.geturl() if hasattr(exc, 'geturl') else url
            res.ctype = (exc.headers.get('content-type') or '').split(';')[0].strip().lower() if exc.headers else ''
            try:
                res.body = exc.read(64 * 1024)
            except Exception:
                res.body = b''
            res.elapsed = time.time() - started
            return res
        except Exception as exc:  # URLError / timeout / TLS
            last = '%s: %s' % (type(exc).__name__, exc)
            res.error = last
            if attempt < retries:
                time.sleep(1.0 + attempt)
                continue
    res.elapsed = time.time() - started
    return res


def _decode_pdf_string(blob):
    """PDF 字面串：可能是 UTF-16BE（带 BOM）、UTF-8 BOM 或 latin-1。"""
    if blob.startswith(b'\xfe\xff'):
        try:
            return blob[2:].decode('utf-16-be', 'ignore').strip()
        except Exception:
            return ''
    if blob.startswith(b'\xef\xbb\xbf'):
        return blob[3:].decode('utf-8', 'ignore').strip()
    try:
        return blob.decode('utf-8').strip()
    except UnicodeDecodeError:
        return blob.decode('latin-1', 'ignore').strip()


def pdf_title(body):
    """从 DocInfo /Title 或 XMP dc:title 取标题。"""
    m = re.search(rb'/Title\s*\(((?:\\.|[^\\()]){2,400})\)', body, re.S)
    if m:
        raw = re.sub(rb'\\([()\\])', rb'\1', m.group(1))
        title = _decode_pdf_string(raw)
        title = re.sub(r'\s+', ' ', title).strip()
        if len(title) >= 3:
            return title
    m = re.search(rb'<dc:title>[\s\S]{0,400}?<rdf:li[^>]*>([^<]{3,300})</rdf:li>',
                  body, re.I)
    if m:
        return re.sub(r'\s+', ' ', m.group(1).decode('utf-8', 'ignore')).strip()
    return ''


def html_title(body):
    head = body[:400_000].decode('utf-8', 'ignore')
    m = re.search(r'<title[^>]*>([^<]{2,300})</title>', head, re.I)
    if not m:
        return ''
    return re.sub(r'\s+', ' ', m.group(1)).strip()


def extract_title(res):
    if 'pdf' in res.ctype or res.body[:5] == b'%PDF-':
        return pdf_title(res.body)
    if 'html' in res.ctype or res.body[:200].lstrip()[:9].lower() == b'<!doctype':
        return html_title(res.body)
    return ''


def is_junk_title(title):
    t = (title or '').strip()
    if len(t) < 3:
        return True
    if JUNK_TITLE_RE.match(t):
        return True
    # 纯符号/纯数字的标题没有辨识度
    return not re.search(r'[A-Za-z\u4e00-\u9fff]', t)


def title_hits(entry_name, title):
    """返回命中数：英文词元命中 + 中文片段命中。"""
    name = clean_name(entry_name)
    want = tokens(name)
    got = set(tokens(title))
    hits = sum(1 for w in want if w in got)
    for frag in cjk_fragments(name)[:2]:
        if frag in title:
            hits += 1
    return hits


def wayback_snapshot(url, timeout=20.0):
    try:
        res = fetch(WAYBACK % urllib.parse.quote(url, safe=''), timeout=timeout, retries=0)
        if res.status != 200:
            return ''
        data = json.loads(res.body.decode('utf-8', 'ignore') or '{}')
        closest = (data.get('archived_snapshots') or {}).get('closest') or {}
        return closest.get('url') or ''
    except Exception:
        return ''


def openlibrary_isbn(isbn, timeout=20.0):
    """返回 (state, title, authors)：state ∈ {'ok', 'missing', 'error'}。

    'missing'（200 但没有该 ISBN 记录）和 'error'（429/5xx/超时）必须分开：
    前者说明 ISBN 可能抄错，后者只是 OpenLibrary 限流，不能当成「书不存在」。
    """
    key = isbn.replace('-', '').strip()
    res = fetch(OPENLIBRARY % key, timeout=timeout, retries=2)
    if res.error and not res.status:
        return ('error', '', res.error[:120])
    if res.status != 200:
        return ('error', '', 'HTTP %d' % res.status)
    time.sleep(0.3)  # 开放 API 有并发限流，小步退让
    try:
        data = json.loads(res.body.decode('utf-8', 'ignore') or '{}')
    except Exception:
        return ('error', '', 'JSON 解析失败')
    rec = data.get('ISBN:%s' % key)
    if not rec:
        return ('missing', '', '')
    authors = ', '.join(a.get('name', '') for a in rec.get('authors') or [])
    return ('ok', rec.get('title') or '', authors)


def doc_id_in_url(name, url):
    """条目名里的厂商编号是否出现在最终 URL 里（PDF 元数据不可用时的兜底判据）。

    TI 的修订后缀会变（SLVA477A → slva477c.pdf），所以比对时去掉修订字母，
    只比 `slva477` 这样的主干。
    """
    u = (url or '').lower()
    for m in TI_ID_RE.finditer(name):
        base = m.group(1)
        stem = base[:-1] if (base[-1].isalpha() and base[-2].isdigit()) else base
        if stem.lower() in u:
            return True
    for m in TI_ALT_ID_RE.finditer(name):
        if m.group(1).lower() in u:
            return True
    for m in ADI_MT_RE.finditer(name):
        if ('mt-%s' % m.group(1)) in u:
            return True
    return False


# ---------------------------------------------------------------- 判定

def classify_entry(entry, do_wayback=True, timeout=25.0):
    rec = {'name': entry['name'], 'bucket': entry['bucket'], 'line': entry['line'],
           'url': entry['url'], 'isbn': entry['isbn'], 'verdict': '', 'status': 0,
           'ctype': '', 'title': '', 'final_url': '', 'detail': '', 'snapshot': '',
           'hits': 0}

    if entry['isbn']:
        state, title, authors = openlibrary_isbn(entry['isbn'], timeout=timeout)
        if state == 'error':
            rec['verdict'] = 'ERROR'
            rec['detail'] = 'OpenLibrary 查询失败：%s' % (authors or '未知错误')
            return rec
        if state == 'missing':
            rec['verdict'] = 'ISBN-MISSING'
            rec['detail'] = 'OpenLibrary 无此 ISBN 记录（也可能就是 ISBN 抄错）'
            return rec
        hits = title_hits(entry['name'], '%s %s' % (title, authors))
        rec['title'] = title
        rec['detail'] = ('%s — %s' % (title, authors)).strip(' —')
        rec['hits'] = hits
        rec['verdict'] = 'ISBN-OK' if hits >= 1 else 'ISBN-MISMATCH'
        return rec

    candidates = []
    if entry['url']:
        candidates.append(entry['url'])
    candidates.extend(derive_candidates(entry))
    if not candidates:
        rec['verdict'] = 'NO-LINK'
        rec['detail'] = '无 url / isbn / 厂商编号，只能人工'
        return rec

    first_error = ''
    for cand in candidates:
        res = fetch(cand, timeout=timeout)
        rec['status'] = res.status
        rec['ctype'] = res.ctype
        rec['final_url'] = res.final_url or cand
        if res.error and not res.status:
            first_error = res.error
            continue
        if res.status in (401, 403, 429) or (res.status == 202 and len(res.body) < 64):
            rec['verdict'] = 'BLOCKED'
            rec['detail'] = 'HTTP %d（反爬，需人工打开一次）' % res.status
            return rec
        if res.status == 410:
            rec['verdict'] = 'GONE'
            rec['detail'] = 'HTTP 410 已下线'
            if do_wayback:
                rec['snapshot'] = wayback_snapshot(rec['url'] or cand, timeout=timeout)
            return rec
        if res.status >= 400:
            rec['verdict'] = 'DEAD'
            rec['detail'] = 'HTTP %d' % res.status
            if do_wayback:
                rec['snapshot'] = wayback_snapshot(rec['url'] or cand, timeout=timeout)
            return rec
        title = extract_title(res)
        if is_junk_title(title):
            # PDF 元数据经常是 `Table of Contents` / `1 Introduction` 这类垃圾，
            # 但编号与 URL 一致就足以证明「还是那一篇」（TI 的修订后缀会变）。
            if 'pdf' in rec['ctype'] and doc_id_in_url(entry['name'], rec['final_url']):
                rec['title'] = title
                rec['verdict'] = 'OK'
                rec['detail'] = 'PDF 元数据不可用（%s），但编号与 URL 一致：%s' % (
                    title or '空', short_url(rec['final_url']))
                return rec
            # HTML 的长标题通常是 `Table of Contents | 站点名`，仍可用于匹配
            if not ('html' in rec['ctype'] and len(title) > 20):
                rec['verdict'] = 'NO-TITLE'
                rec['detail'] = '%s %dB，标题不可用：%s' % (rec['ctype'] or res.ctype,
                                                         len(res.body), title or '(空)')
                return rec
        hits = title_hits(entry['name'], title)
        rec['title'] = title
        rec['hits'] = hits
        moved = bool(rec['final_url']) and rec['final_url'] != cand
        rec['detail'] = title[:120] + ('  →%s' % short_url(rec['final_url']) if moved else '')
        rec['verdict'] = 'OK' if hits >= 2 else ('WEAK' if hits == 1 else 'MISMATCH')
        return rec

    rec['verdict'] = 'ERROR'
    rec['detail'] = (first_error or '网络失败')[:120]
    return rec


def short_url(url, limit=64):
    u = re.sub(r'^https?://(www\.)?', '', url or '')
    return u if len(u) <= limit else u[:limit - 1] + '…'


# ---------------------------------------------------------------- 报告

VERDICT_ORDER = ['DEAD', 'GONE', 'ISBN-MISMATCH', 'BLOCKED', 'ERROR',
                 'MISMATCH', 'WEAK', 'NO-TITLE', 'ISBN-MISSING', 'NO-LINK',
                 'SKIPPED', 'OK', 'ISBN-OK']


def summarize(records):
    counts = {}
    for rec in records:
        counts[rec['verdict']] = counts.get(rec['verdict'], 0) + 1
    return counts


def print_report(records, only='all', verbose=False):
    hard = [r for r in records if r['verdict'] in HARD]
    soft = [r for r in records if r['verdict'] in SOFT]
    ok = [r for r in records if r not in hard and r not in soft]

    def dump(rows, header):
        if not rows:
            return
        print('\n== %s（%d）' % (header, len(rows)))
        for r in sorted(rows, key=lambda x: VERDICT_ORDER.index(x['verdict'])
                        if x['verdict'] in VERDICT_ORDER else 99):
            line = '%-13s %-6s %s' % (r['verdict'], r['status'] or '-', r['name'][:56])
            print(line)
            if r['detail'] or verbose:
                print('   %s' % (r['detail'] or ''))
            if r['snapshot']:
                print('   快照：%s' % r['snapshot'])

    if only in ('all', 'hard'):
        dump(hard, '硬失败（仓库侧必修）')
    if only in ('all', 'manual'):
        dump(soft, '需人工确认')
    if only == 'all' and verbose:
        dump(ok, '通过')
    elif only == 'all':
        print('\n通过：%d 条（%s）' % (len(ok), ', '.join(sorted({r['verdict'] for r in ok})) or '-'))

    counts = summarize(records)
    print('\n==== 共 %d 条：%s ====' % (
        len(records), ', '.join('%s=%d' % (k, counts[k]) for k in VERDICT_ORDER if k in counts)))
    return hard, soft


def write_json(path, records):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    payload = {
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'tool': 'check_sources_online.py',
        'sources': SOURCES_PATH,
        'counts': summarize(records),
        'records': records,
    }
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print('JSON 报告：%s' % path)


# ---------------------------------------------------------------- 自测

def self_test():
    """纯函数自测（不联网）。任何一条失败都以非零退出，供 CI / 手工快速回归。"""
    checks = []

    def eq(label, got, want):
        checks.append((label, got == want, 'got=%r want=%r' % (got, want)))

    sample = '''
official:
- name: Op Amps for Everyone (Ron Mancini, TI, SLOD006B)
  url: https://www.ti.com/lit/an/slod006b/slod006b.pdf
  type: app-note
  vendor: Texas Instruments
- name: MT-035 Op Amp Inputs (ADI)
  type: app-note
books:
- name: The Art of Electronics (3rd Edition)
  author: Horowitz
  isbn: 9780521809269
'''.strip('\n')
    import tempfile
    with tempfile.NamedTemporaryFile('w+', suffix='.yaml', delete=False, encoding='utf-8') as fh:
        fh.write(sample)
        tmp = fh.name
    try:
        entries = parse_entries(tmp)
    finally:
        os.unlink(tmp)
    eq('parse.count', len(entries), 3)
    eq('parse.bucket', entries[0]['bucket'], 'official')
    eq('parse.url', entries[0]['url'], 'https://www.ti.com/lit/an/slod006b/slod006b.pdf')
    eq('parse.isbn', entries[2]['isbn'], '9780521809269')
    eq('parse.name', entries[1]['name'], 'MT-035 Op Amp Inputs (ADI)')

    eq('derive.ti', 'https://www.ti.com/lit/pdf/SLOD006B' in derive_candidates(entries[0]), True)
    eq('derive.adi', 'https://www.analog.com/media/en/training-seminars/tutorials/MT-035.pdf'
       in derive_candidates(entries[1]), True)
    eq('derive.none', derive_candidates({'name': 'Plain book', 'url': '', 'isbn': ''}), [])

    eq('junk.logo', is_junk_title('Logo_final_v4'), True)
    eq('junk.toc', is_junk_title('Table of Contents'), True)
    eq('junk.good', is_junk_title('Op Amps for Everyone, 3rd Edition'), False)
    eq('junk.empty', is_junk_title(''), True)

    eq('hits.same', title_hits('Op Amps for Everyone (TI, SLOD006B)',
                               'Op Amps for Everyone, 3rd Edition'), 2)
    eq('hits.none', title_hits('Op Amps for Everyone', 'Switching Power Supply Design'), 0)
    eq('hits.cjk', title_hits('NEETS (Navy Electricity and Electronics)', 'NEETS 海军电气'), 1)

    eq('short_url', short_url('https://www.ti.com/lit/pdf/SLVA654'), 'ti.com/lit/pdf/SLVA654')

    eq('id.url.ti',
       doc_id_in_url('TI SLVA477A — Basic Calculation',
                     'https://www.ti.com/lit/an/slva477c/slva477c.pdf'), True)
    eq('id.url.adi',
       doc_id_in_url('MT-035 Op Amp Inputs',
                     'https://www.analog.com/x/MT-035.pdf'), True)
    eq('id.url.none',
       doc_id_in_url('Op Amps for Everyone', 'https://example.com/a.pdf'), False)

    failed = [c for c in checks if not c[1]]
    for label, ok, msg in checks:
        if not ok:
            print('FAIL %-14s %s' % (label, msg))
    print('self-test: %d/%d passed' % (len(checks) - len(failed), len(checks)))
    return 1 if failed else 0


# ---------------------------------------------------------------- main

def main(argv=None):
    # Windows 控制台默认 cp936，标题里常有非 GBK 字符；统一按 UTF-8 输出，避免为编码问题中断体检
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, OSError):
            pass
    ap = argparse.ArgumentParser(description='sources.list.yaml 联网复核（不依赖搜索 API）')
    ap.add_argument('--sources', default=SOURCES_PATH, help='来源清单路径')
    ap.add_argument('--only', choices=['all', 'hard', 'manual'], default='all',
                    help='输出过滤：只看硬失败 / 只看需人工')
    ap.add_argument('--json', nargs='?', const=DEFAULT_JSON, default='',
                    help='写 JSON 报告（不给路径则写 .generated/sources-online.json）')
    ap.add_argument('--limit', type=int, default=0, help='只查前 N 条（抽样）')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--timeout', type=float, default=25.0)
    ap.add_argument('--no-wayback', action='store_true', help='死链不查 archive.org 快照')
    ap.add_argument('--strict', action='store_true', help='需人工档也算失败')
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--self-test', action='store_true', help='只跑纯函数自测（不联网）')
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if not os.path.exists(args.sources):
        print('找不到来源清单：%s' % args.sources, file=sys.stderr)
        return 2

    entries = parse_entries(args.sources)
    if args.limit:
        entries = entries[:args.limit]
    print('复核 %d 条来源（并发 %d，超时 %.0fs）…' % (len(entries), args.workers, args.timeout),
          file=sys.stderr)

    started = time.time()
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        records = list(pool.map(
            lambda e: classify_entry(e, do_wayback=not args.no_wayback, timeout=args.timeout),
            entries))

    hard, soft = print_report(records, only=args.only, verbose=args.verbose)
    print('耗时 %.1fs' % (time.time() - started))

    if args.json:
        write_json(args.json, records)

    if hard or (args.strict and soft):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
