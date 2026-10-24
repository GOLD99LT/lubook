#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check-content.py — 内容标准机械项检查（docs/CONTENT-STANDARD.md §1 的 H1/H3/H5/H6/H7/H8）。

只做"可自动判定"的部分；数字复算与技术正确性由主审核人工完成（§4）。
零第三方依赖。

用法：
  python scripts/check-content.py --app hardware
  python scripts/check-content.py --app hardware --dir basics
  python scripts/check-content.py --app hardware --min 4500 --strict
"""
import os, re, sys, json, argparse, xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'packages', 'tooling', 'src'))

# 两套章型标准（docs/CONTENT-STANDARD.md §2）：概念/原理章 vs 电路/器件章
PROFILES = {
    'concept': [
        ('动机', ('设计动机', '为什么', '动机', '适用')),
        ('定义与直观', ('定义', '原理', '直观', '基本概念', '是什么')),
        ('定量关系', ('定量', '公式', '关系式', '推导', '定律')),
        ('典型计算', ('计算', '示例', '算例', '例题')),
        ('工程含义', ('工程含义', '工程实践', '取值', '选型', '权衡', '影响')),
        ('常见坑', ('常见坑', '常见问题', '误区', '故障现象', '注意')),
        ('自测题', ('自测', '练习', '思考题', '习题')),
        ('参考资料', ('参考资料', '参考文献', '来源', '延伸阅读')),
    ],
    'circuit': [
        ('动机', ('设计动机', '为什么需要', '动机')),
        ('原理图', ('原理图', '电路图', '电路结构')),
        ('静态分析', ('静态分析', '直流分析', '静态工作点')),
        ('动态分析', ('动态分析', '交流分析', '瞬态', '频率响应')),
        ('环路/稳定性', ('环路', '稳定性', '相位裕度', '补偿')),
        ('取值与权衡', ('取值', '元件选择', '工程权衡', '选型')),
        ('设计示例', ('设计示例', '完整设计', '算例', '实例')),
        ('仿真与实验', ('仿真', '实验', '测量')),
        ('常见坑', ('常见坑', '常见问题', '故障现象', '掉坑')),
        ('自测题', ('自测', '练习', '思考题', '习题')),
        ('参考资料', ('参考资料', '参考文献', '来源', '延伸阅读')),
    ],
}
SKIP_FILES = {'index.md', 'SUMMARY.md', 'LICENSE-docs.md'}


def cjk_count(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def split_fm(text):
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end > 0:
            return text[3:end], text[end + 4:]
    return '', text


def first_value(fm, key):
    m = re.search(r'^%s:\s*(.+)$' % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else ''


QUICK = 'quick'


def check_chapter(path, src, min_chars, min_imgs, profile="concept"):
    rel = os.path.relpath(path, src).replace(os.sep, '/')
    text = open(path, encoding='utf-8-sig').read()
    fm, body = split_fm(text)
    issues = []
    # quick = 速查/题库档（docs/CONTENT-STANDARD.md §0.5）：
    # 不查字数、模块顺序、配图数量、折叠题数量、常见坑——
    # 这几项是"正文主干章"的指标，套到附录/题库上只会产出永远为红的假告警。
    # 但**图片存在性、SVG 合法性、来源条数、手写章号、绝对化表述**照查，这些与章型无关。
    quick = (profile == QUICK)

    chars = cjk_count(body)
    if not quick and chars < min_chars:
        issues.append('字数 %d < %d' % (chars, min_chars))

    # 模块顺序
    heads = [h.strip() for h in re.findall(r'^#{2,3}\s+(.+)$', body, re.M)]
    pos, missing = -1, []
    if not quick:
        for name, keys in PROFILES[profile]:
            found = -1
            for i, h in enumerate(heads):
                if i > pos and any(k in h for k in keys):
                    found = i
                    break
            if found < 0:
                missing.append(name)
            else:
                pos = found
    if missing:
        issues.append('缺模块: ' + '、'.join(missing))

    imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', body)
    local_imgs = [i for i in imgs if not i.startswith(('http', 'data:'))]
    if not quick and len(local_imgs) < min_imgs:
        issues.append('配图 %d < %d' % (len(local_imgs), min_imgs))
    for i in local_imgs:
        p = os.path.normpath(os.path.join(os.path.dirname(path), i.split()[0]))
        if not os.path.exists(p):
            issues.append('图片缺失: %s' % i)
        elif p.endswith('.svg'):
            # 历史上两张 SVG 因正文里有裸 & / < 而 XML 非法，线上直接破图，
            # 而 validate/scan_svg_order/manifest 对账全都发现不了。这里补上。
            try:
                ET.parse(p)
            except Exception as e:
                issues.append('SVG 不是合法 XML: %s (%s)' % (os.path.basename(p), e.__class__.__name__))

    details = len(re.findall(r'<details', body))
    if not quick and details < 4:
        issues.append('自测题 %d < 4' % details)

    # 常见坑：pitfall 容器 + 「现象/原因/解决」关键词
    pits = len(re.findall(r':::\s*pitfall', body))
    triad = len(re.findall(r'现象', body))
    if not quick and pits == 0 and triad < 3:
        issues.append('常见坑不足（pitfall=%d，现象=%d）' % (pits, triad))

    sources = re.findall(r'^\s*-\s+(.+)$', fm, re.M) if 'sources:' in fm else []
    if 'sources:' in fm:
        tail = fm.split('sources:', 1)[1]
        sources = [l.strip(' -') for l in tail.splitlines() if l.strip().startswith('-')]
    if len(sources) < 3:
        issues.append('来源 %d < 3' % len(sources))

    for m in re.finditer(r'第\s*[0-9一二三四五六七八九十]+\s*章|全书的第一章|本书第一章', body):
        issues.append('手写章号: %s' % m.group(0))
        break

    # 绝对化表述（安全相关只提示，不判死）
    for m in re.finditer(r'绝对安全|一定不会|唯一(?:的)?(?:办法|方法|手段)', body):
        issues.append('绝对化表述: %s' % m.group(0))
        break

    return {
        'rel': rel, 'chars': chars, 'imgs': len(local_imgs), 'details': details,
        'pitfalls': pits, 'sources': len(sources), 'issues': issues
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', default='hardware')
    ap.add_argument('--dir', default='')
    ap.add_argument('--min', type=int, default=4500,
                    help='最小中文字数（默认按内容标准 H1=4500）')
    ap.add_argument('--min-imgs', type=int, default=1)
    ap.add_argument('--profile', choices=['concept', 'circuit', 'all', 'quick'], default='concept',
                    help='章型标准：concept=概念/原理章，circuit=电路/器件章，'
                         'all=两套都试取通过者，quick=速查/题库档（不查字数与模块结构，'
                         '只查图片/SVG/来源/章号/绝对化表述）')
    ap.add_argument('--strict', action='store_true', help='有任何 issue 即非零退出')
    ap.add_argument('--by-dir', action='store_true',
                    help='按目录自动选口径：--quick-dirs 里的子目录走 quick（不查字数/模块），'
                         '其余按 --profile 检查。用于门禁：一本分册一条命令跑完，速查档不再恒红。')
    ap.add_argument('--quick-dirs', default='appendix,quizbank',
                    help='--by-dir 模式下按速查档口径检查的子目录，逗号分隔')
    ap.add_argument('--json', default='', help='把结果写成 JSON')
    args = ap.parse_args()

    src = os.path.join(ROOT, 'apps', args.app, 'docs')
    if args.dir:
        src = os.path.join(src, args.dir)
    if not os.path.isdir(src):
        print('目录不存在: %s' % src)
        return 2

    base = os.path.join(ROOT, 'apps', args.app, 'docs')
    quick_dirs = [d.strip() for d in args.quick_dirs.split(',') if d.strip()]
    rows = []
    for root, _d, files in os.walk(src):
        for f in sorted(files):
            if not f.endswith('.md') or f in SKIP_FILES:
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, base).replace(os.sep, '/')
            # --by-dir：速查/题库走 quick，其余按 --profile
            if args.by_dir and any(rel.startswith(d + '/') for d in quick_dirs):
                rows.append(check_chapter(p, base, args.min, args.min_imgs, QUICK))
                continue
            if args.profile == 'all':
                a = check_chapter(p, base, args.min, args.min_imgs, 'concept')
                b = check_chapter(p, base, args.min, args.min_imgs, 'circuit')
                rows.append(a if len(a['issues']) <= len(b['issues']) else b)
            else:
                rows.append(check_chapter(p, base, args.min, args.min_imgs, args.profile))

    rows.sort(key=lambda r: r['chars'])
    bad = [r for r in rows if r['issues']]

    print('%-46s %6s %4s %5s %5s %4s  %s' % ('章节', '字数', '图', '折叠题', 'pitfall', '来源', '问题'))
    print('-' * 120)
    for r in rows:
        print('%-46s %6d %4d %5d %5d %4d  %s'
              % (r['rel'], r['chars'], r['imgs'], r['details'], r['pitfalls'], r['sources'],
                 '; '.join(r['issues']) if r['issues'] else 'OK'))
    print('-' * 120)
    print('共 %d 章，达标 %d，未达标 %d；中位数 %d 字'
          % (len(rows), len(rows) - len(bad), len(bad), sorted(r['chars'] for r in rows)[len(rows) // 2] if rows else 0))

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print('明细已写入 %s' % args.json)

    return 1 if (args.strict and bad) else 0


if __name__ == '__main__':
    sys.exit(main())
