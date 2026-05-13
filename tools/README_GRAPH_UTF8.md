# Graph HTML and UTF-8 (Windows)

`graph.html` / `graph_template.html` are large, CJK-heavy single files. Any tool that reads or writes them with the **process default encoding** (`locale.getpreferredencoding(False)`, often **cp936** on Chinese Windows) will corrupt multibyte characters on the next save. Regenerating the graph touches these files often, so the bug shows up as **persistent mojibake** (`??`, broken regex literals, `Invalid regular expression` in the browser console).

## Avoid

- **Python**: never `open(path)` or `Path.read_text()` / `write_text()` without `encoding="utf-8"`. Prefer `newline="\n"` when rewriting whole files.
- **PowerShell**: do not paste multi‑KB HTML into `Set-Content` / `Out-File` / `>` **without** `-Encoding utf8` (UTF-8 **without BOM** matches `<meta charset="utf-8">`). Safer: run `python tools/inject_graph_data.py` or other `tools/*.py` scripts only.
- **cmd.exe**: `%PYTHONUTF8%=1` or `python -X utf8` reduces surprises for code that still uses implicit encoding; fixing call sites is still required.

## Recovery

If the worktree is already corrupted but **git objects are clean**:

```text
git checkout HEAD -- graph_template.html graph.html
python tools/inject_graph_data.py
python tools/check_graph_utf8.py
```

To merge “good UTF-8 shell from git + current inline JSON” see `tools/restore_html_utf8_from_head.py`.

## CI / local guard

```text
python tools/check_graph_utf8.py
```

Exit code `1` if replacement characters, `??`+`**` JS patterns, or obvious title mojibake are detected.
