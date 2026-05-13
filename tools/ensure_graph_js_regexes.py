#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Idempotently restore hardened parseWeeklySummaryText() in graph HTML templates.

Weekly summary lines come from scripts/weekly_trends.py generate_weekly_summary().
Regex literals use \\u escapes for Chinese/fullwidth punctuation so a mis-encoded
save cannot turn （ into ?? and produce Invalid regular expression (nothing to repeat).

Typical pipeline (after HEAD restore / chrome patch):
  python tools/patch_graph_template_chrome.py
  python tools/ensure_graph_js_regexes.py
  python tools/apply_graph_template_fixes.py
  python tools/inject_graph_data.py --from-template

Encoding pitfalls: tools/README_GRAPH_UTF8.md. In parseWeeklySummaryText(), non-ASCII must
appear only as \\u escapes inside /.../ regex literals; a lossy re-save can replace those
code points with ASCII "?" and produce /??.../ ("Nothing to repeat" in the engine).

Verify JS parse + forbid broken patterns:
  python tools/ensure_graph_js_regexes.py --verify
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "graph_template.html"
GRAPH_HTML = ROOT / "graph.html"

PARSE_START = "    function parseWeeklySummaryText(s) {\n"
PARSE_END = "\n    function renderWeeklySummaryPanel"


# Raw string so \\u… / \\d survive for JS; emoji/CJK in string literals are UTF-8 (not Python \\u surrogates).
CANONICAL_PARSE_BLOCK = r"""    function parseWeeklySummaryText(s) {
      var chips = [];
      var lede = '';
      if (!s || typeof s !== 'string') return { chips: chips, lede: lede };
      /* Only \uNNNN in regex literals here (not raw multi-byte). Lossy saves turn e.g. U+FF08 into "?", which breaks /.../ with "Nothing to repeat". Matches scripts/weekly_trends.py generate_weekly_summary(). */
      var mDays = s.match(/\uff08(\d+)\u5929\uff09/);
      if (mDays) chips.push('📅 追踪 ' + mDays[1] + ' 天');
      var mCum = s.match(/\u7d2f\u8ba1\s*\*\*(\d+)\*\*\s*\u6761\u60c5\u62a5/);
      var mCur = s.match(/\u5f53\u524d\u6570\u636e\s*\*\*(\d+)\*\*\s*\u6761\u60c5\u62a5/);
      if (mCum) chips.push('📰 ' + mCum[1] + ' 条情报');
      else if (mCur) chips.push('📰 ' + mCur[1] + ' 条情报');
      var mFocus = s.match(/\u7126\u70b9\u9886\u57df\s*\*\*([^*]+)\*\*/);
      if (mFocus) chips.push('🎯 焦点 · ' + mFocus[1].trim());
      var mNar = s.match(/\u6838\u5fc3\u53d9\u4e8b\s*\*\*([^*]+)\*\*/);
      if (mNar) lede = '核心叙事：' + mNar[1].trim();
      return { chips: chips, lede: lede };
    }
"""


def patch_parse_weekly_summary(html: str) -> tuple[str, bool]:
    """Replace parseWeeklySummaryText with canonical implementation."""
    i = html.find(PARSE_START)
    j = html.find(PARSE_END, i + 1)
    if i == -1 or j == -1:
        raise SystemExit("ensure_graph_js_regexes: parseWeeklySummaryText anchors not found")
    cur = html[i:j]
    if cur == CANONICAL_PARSE_BLOCK:
        return html, False
    return html[:i] + CANONICAL_PARSE_BLOCK + html[j:], True


def apply_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\ufeff")
    new, changed = patch_parse_weekly_summary(raw)
    if changed:
        path.write_text(new, encoding="utf-8", newline="\n")
    return changed


def verify_no_broken_regex_literals(html_path: Path) -> None:
    text = html_path.read_text(encoding="utf-8")
    if re.search(r"\?\?\s*\*\*", text):
        raise SystemExit(f"{html_path}: found literal ?? before ** pattern (likely mojibake)")


def verify_inline_scripts_new_function(html_path: Path) -> None:
    verify_js = r"""
const fs = require('fs');
const html = fs.readFileSync(process.argv[1], 'utf8');
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m;
while ((m = re.exec(html))) {
  const attrs = m[1];
  const body = m[2];
  if (/\bsrc\s*=/.test(attrs)) continue;
  if (/id\s*=\s*["']graph-data["']/.test(attrs)) continue;
  if (/type\s*=\s*["']application\/json["']/.test(attrs)) continue;
  const code = body.trim();
  if (!code) continue;
  try {
    new Function(code);
  } catch (e) {
    console.error('Invalid inline script:', e && e.message);
    process.exit(1);
  }
}
"""
    subprocess.run(
        ["node", "-e", verify_js, str(html_path)],
        cwd=str(ROOT),
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument(
        "--also-graph-html",
        action="store_true",
        help="Also patch graph.html if present (normally inject --from-template is enough).",
    )
    ap.add_argument(
        "--verify",
        action="store_true",
        help="Run Node new Function check on graph.html inline scripts + grep-style guards.",
    )
    args = ap.parse_args()

    if args.verify:
        verify_no_broken_regex_literals(TEMPLATE)
        verify_no_broken_regex_literals(GRAPH_HTML)
        verify_inline_scripts_new_function(GRAPH_HTML)
        print("OK verify", TEMPLATE, GRAPH_HTML)
        return 0

    changed_tpl = apply_file(TEMPLATE)
    changed_graph = False
    if args.also_graph_html and GRAPH_HTML.is_file():
        changed_graph = apply_file(GRAPH_HTML)

    if changed_tpl or changed_graph:
        parts = []
        if changed_tpl:
            parts.append(str(TEMPLATE))
        if changed_graph:
            parts.append(str(GRAPH_HTML))
        print("OK patched", ", ".join(parts))
    else:
        print("OK already canonical", TEMPLATE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
