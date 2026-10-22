#!/usr/bin/env node
/**
 * 以指定堆上限运行 VitePress CLI。
 *
 * 为什么需要它：`.npmrc` 的 `node-options` 在本仓的 pnpm 版本下**不会被传给子进程**
 * （实测 `pnpm exec node -p process.env.NODE_OPTIONS` 为 UNSET，堆上限仍是默认值），
 * 而 `package.json` 里写 `NODE_OPTIONS=... vitepress build` 在 Windows 的 cmd/pwsh 下不生效。
 * 所以用这个包装器显式带 `--max-old-space-size` 重新起一个 node 进程。
 *
 * 用法（与 vitepress CLI 一致）：
 *   node ../../packages/tooling/bin/vitepress-with-heap.mjs build docs
 *
 * 堆上限默认 8192 MB，可用环境变量 VITEPRESS_HEAP_MB 覆盖。
 * 依据见 docs/adr/ADR-0011.md。
 */
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import path from 'node:path';

const HEAP_MB = process.env.VITEPRESS_HEAP_MB || '8192';

// 从**当前工作目录**解析 vitepress，这样各 app 用自己的 devDependency。
const requireFromCwd = createRequire(path.join(process.cwd(), 'package.json'));

let cli;
try {
  const pkgJson = requireFromCwd.resolve('vitepress/package.json');
  cli = path.join(path.dirname(pkgJson), 'dist', 'node', 'cli.js');
} catch {
  console.error('[vitepress-with-heap] 在当前目录解析不到 vitepress，请确认已安装依赖。');
  process.exit(1);
}

const result = spawnSync(
  process.execPath,
  [`--max-old-space-size=${HEAP_MB}`, cli, ...process.argv.slice(2)],
  { stdio: 'inherit', env: process.env },
);

if (result.error) {
  console.error('[vitepress-with-heap] 启动失败：', result.error.message);
  process.exit(1);
}
process.exit(result.status ?? 1);
