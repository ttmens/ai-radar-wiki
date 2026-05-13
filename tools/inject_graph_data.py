#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 graph.json 注入 graph.html 中 <script id="graph-data"> 的内联 JSON，
不改动其余 HTML/JS/CSS —— 与 debd0e5 起的设计一致，避免 Cron 用整页模板覆盖丢失自定义 UI。

    建议在 Hermes 的 generate_graph_html() 中改为调用本脚本，或复制其逻辑。

    Chrome / 导航壳层（简报 / 探索、订阅、问 AI）：编辑 graph_template.html 后须保持与 graph.html 一致。
    可运行「仅 UTF-8 安全」的补充脚本：
        python tools/patch_graph_template_chrome.py [--regenerate-from-graph-html] [--ensure-regex]
        python tools/ensure_graph_js_regexes.py
    再配合本脚本的 --from-template 重写 graph.html。
    快速清单：tools/GRAPHPAGE_UTF8.md；展开说明：tools/README_GRAPH_UTF8.md。

用法：
    python tools/inject_graph_data.py [--wiki-root PATH] [--dry-run]
    python tools/inject_graph_data.py [--wiki-root PATH] --from-template [--dry-run]

默认 wiki-root 为脚本所在仓库根目录（含 graph.html / graph.json）。

--from-template
    用 graph_template.html 作为完整壳，将 graph.json 写入 {{DATA}} 后整体写入 graph.html。
    在改完模板、准备推送前运行一次，可避免 graph.html 与 graph_template.html 长期分叉。
    （定时任务 / Hermes 日常同步应仍使用默认模式：仅替换已有 graph.html 内 #graph-data JSON，见 §6.4。）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
from check_graph_utf8 import check_files as _check_graph_utf8_files  # noqa: E402

GRAPH_DATA_SCRIPT_RE = re.compile(
    r'(<script\s+id="graph-data"\s+type="application/json"\s*>)'
    r'(.*?)'
    r'(</script>)',
    re.DOTALL,
)


def _strip_illegal_controls(obj):
    """递归去掉字符串中会破坏 HTML/JS 内联 JSON 解析的 ASCII 控制字符（保留 \\t \\n \\r 由 json 转义）。"""
    if isinstance(obj, str):
        out = []
        for ch in obj:
            o = ord(ch)
            if o < 32 and ch not in '\t\n\r':
                out.append(' ')
            elif o == 0x7F:
                out.append(' ')
            else:
                out.append(ch)
        return ''.join(out)
    if isinstance(obj, list):
        return [_strip_illegal_controls(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _strip_illegal_controls(v) for k, v in obj.items()}
    return obj


def load_graph(path: Path) -> dict:
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return _strip_illegal_controls(data)


def inject_into_html(html: str, data_json: str) -> str:
    m = GRAPH_DATA_SCRIPT_RE.search(html)
    if not m:
        raise ValueError(
            'graph.html 中未找到 <script id="graph-data" type="application/json"> … </script>，'
            '无法安全注入；请勿回退到整文件模板覆盖。'
        )
    return html[: m.start()] + m.group(1) + data_json + m.group(3) + html[m.end() :]


def inject_from_template(template: str, data_json: str) -> str:
    if '{{DATA}}' not in template:
        raise ValueError('graph_template.html 缺少 {{DATA}} 占位符')
    return template.replace('{{DATA}}', data_json)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument(
        '--wiki-root',
        type=Path,
        default=None,
        help='仓库根目录（默认：本脚本上级目录的上一级）',
    )
    ap.add_argument('--dry-run', action='store_true', help='只校验不写文件')
    ap.add_argument(
        '--from-template',
        action='store_true',
        help='用 graph_template.html + graph.json 重写整页 graph.html（与默认「仅替换 JSON」不同）',
    )
    args = ap.parse_args()

    root = args.wiki_root
    if root is None:
        root = Path(__file__).resolve().parent.parent

    graph_json = root / 'graph.json'
    graph_html = root / 'graph.html'
    template = root / 'graph_template.html'

    if not graph_json.is_file():
        print(f'ERROR: missing {graph_json}', file=sys.stderr)
        return 2
    if not graph_html.is_file():
        print(f'ERROR: missing {graph_html}', file=sys.stderr)
        return 2

    data = load_graph(graph_json)
    # 与 DESIGN §9.3 一致：紧凑单行、不 indent，避免控制字符
    data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    if args.from_template:
        if not template.is_file():
            print(f'ERROR: missing template {template}', file=sys.stderr)
            return 2
        tpl = template.read_text(encoding='utf-8')
        if '{{DATA}}' not in tpl:
            print(
                'ERROR: graph_template.html 中缺少 {{DATA}} 占位符',
                file=sys.stderr,
            )
            return 3
        new_html = tpl.replace('{{DATA}}', data_json, 1)
        if args.dry_run:
            print(
                f'OK dry-run --from-template: would write {len(new_html)} bytes to {graph_html}',
            )
            return 0
        graph_html.write_text(new_html, encoding='utf-8', newline='\n')
        print(f'OK wrote {graph_html} from template ({len(new_html)} bytes)')
        _warn_if_graph_utf8_issues(graph_html, template)
        return 0

    html = graph_html.read_text(encoding='utf-8')
    try:
        new_html = inject_into_html(html, data_json)
    except ValueError as e:
        print(f'ERROR: {e}', file=sys.stderr)
        print(
            '若需从零生成：先用 graph_template.html 生成初版 graph.html，再长期只用本脚本替换 JSON。',
            file=sys.stderr,
        )
        if template.is_file():
            try:
                tpl = template.read_text(encoding='utf-8')
                preview = inject_from_template(tpl, data_json)
                print(
                    f'提示：可将 graph_template.html + 注入结果写入 graph.html（{len(preview)} 字节）',
                    file=sys.stderr,
                )
            except ValueError:
                pass
        return 3

    if args.dry_run:
        print(f'OK dry-run: would write {len(new_html)} bytes to {graph_html}')
        return 0

    graph_html.write_text(new_html, encoding='utf-8', newline='\n')
    print(f'OK wrote {graph_html} ({len(new_html)} bytes)')
    _warn_if_graph_utf8_issues(graph_html, template)
    return 0


def _warn_if_graph_utf8_issues(graph_html: Path, template: Path) -> None:
    targets = [p for p in (graph_html, template) if p.is_file()]
    issues = _check_graph_utf8_files(targets)
    if issues:
        print('WARN UTF-8 self-check:', file=sys.stderr)
        for line in issues:
            print(f'  {line}', file=sys.stderr)
    else:
        print('OK UTF-8 self-check (graph.html, graph_template.html)')


if __name__ == '__main__':
    raise SystemExit(main())
