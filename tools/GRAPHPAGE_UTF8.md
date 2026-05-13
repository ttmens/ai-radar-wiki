# Graph page — UTF-8 workflow (short)

**Do:** Edit `graph_template.html` in an editor that keeps **UTF-8**. For bulk writes use **Python** (`encoding="utf-8"`, `newline="\n"`). After template/JS tweaks run `python tools/ensure_graph_js_regexes.py --verify`, then `python tools/check_graph_utf8.py`. Regenerate `graph.html` with `python tools/inject_graph_data.py --from-template`.

**Don’t:** PowerShell `Out-File`, `Set-Content`, or `>` on these HTML files **without** explicit UTF-8 (no BOM). Don’t use Python `open()` / `Path.read_text()` without `encoding="utf-8"`.

**Recover:** `python tools/restore_html_utf8_from_head.py` → `python tools/ensure_graph_js_regexes.py` → `python tools/inject_graph_data.py --from-template` → `python tools/check_graph_utf8.py`.

**Why it breaks on Windows:** Many shells and APIs default to **system ANSI (e.g. cp936)** or **UTF-16**; saving CJK as if it were single-byte text turns multibyte sequences into **`??`** or breaks regex literals.

More detail: `tools/README_GRAPH_UTF8.md`.
