#!/usr/bin/env python3
"""Render an insights markdown file to a self-contained HTML sibling.

Used by performance-reviewer after writing docs/strategy/insights/YYYY-MM-DD.md.
Output: same path with .html extension. Self-contained styling — no external CSS.

Usage:
    python3 scripts/insights_to_html.py docs/strategy/insights/2026-05-07.md
"""
import html
import pathlib
import re
import sys


CSS = """
body {
    font: 16px/1.55 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
    color: #1a1a1a;
    max-width: 760px;
    margin: 40px auto;
    padding: 0 24px 60px;
    background: #fafaf7;
}
h1 { font-size: 28px; font-weight: 600; margin: 0 0 8px; letter-spacing: -0.01em; }
h1 + p { color: #666; margin-top: 0; }
h2 { font-size: 18px; font-weight: 600; margin: 32px 0 8px; padding-top: 18px; border-top: 1px solid #e5e3da; letter-spacing: -0.005em; }
h2:first-of-type { border-top: none; padding-top: 0; }
p { margin: 8px 0; }
strong { color: #0d0d0d; }
ul, ol { margin: 8px 0 14px; padding-left: 22px; }
li { margin: 4px 0; }
li > strong:first-child { color: #0d0d0d; }
code { background: #efece2; padding: 1px 6px; border-radius: 3px; font-size: 0.92em; font-family: "SF Mono", Menlo, monospace; }
table { border-collapse: collapse; margin: 12px 0; font-size: 14px; }
th, td { border: 1px solid #d4d2c7; padding: 6px 12px; text-align: left; }
th { background: #efece2; font-weight: 600; }
.meta { background: #f3f1e8; border-left: 3px solid #c9c5b3; padding: 12px 16px; margin: 12px 0 24px; font-size: 14px; color: #444; }
.meta strong { color: #1a1a1a; }
.headline { font-size: 17px; padding: 14px 18px; background: #fff8e1; border: 1px solid #f1d97a; border-radius: 6px; margin: 16px 0 20px; }
.no-change { padding: 24px; text-align: center; color: #666; background: #f3f1e8; border-radius: 6px; }
hr { border: none; border-top: 1px solid #e5e3da; margin: 24px 0; }
"""


def render_inline(text: str) -> str:
    """Inline markdown: **bold**, `code`, escape HTML."""
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(md: str) -> str:
    """Render the insights-file structure to HTML.
    Handles: # H1, ## H2, blank lines as paragraph breaks, - bullets, N. numbered,
    bold-prefix lines (rendered as paragraphs), --- as <hr>.
    """
    lines = md.splitlines()
    out = []
    in_list = None  # None | "ul" | "ol"

    def close_list():
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    # Track first H2 to wrap in special class
    para_buffer = []

    def flush_para():
        if para_buffer:
            joined = " ".join(para_buffer).strip()
            if joined:
                out.append(f"<p>{render_inline(joined)}</p>")
            para_buffer.clear()

    for raw in lines:
        line = raw.rstrip()

        if not line.strip():
            close_list()
            flush_para()
            continue

        if line.startswith("# "):
            close_list()
            flush_para()
            out.append(f"<h1>{render_inline(line[2:].strip())}</h1>")
            continue

        if line.startswith("## "):
            close_list()
            flush_para()
            out.append(f"<h2>{render_inline(line[3:].strip())}</h2>")
            continue

        if line.strip() == "---":
            close_list()
            flush_para()
            out.append("<hr>")
            continue

        # Bullet list item
        m = re.match(r"^(\s*)-\s+(.*)$", line)
        if m:
            flush_para()
            if in_list != "ul":
                close_list()
                out.append("<ul>")
                in_list = "ul"
            out.append(f"<li>{render_inline(m.group(2))}</li>")
            continue

        # Numbered list item
        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if m:
            flush_para()
            if in_list != "ol":
                close_list()
                out.append("<ol>")
                in_list = "ol"
            out.append(f"<li>{render_inline(m.group(3))}</li>")
            continue

        # Regular paragraph line — accumulate
        close_list()
        para_buffer.append(line.strip())

    close_list()
    flush_para()

    body_html = "\n".join(out)

    # Highlight headline section: the first <p> after the meta block.
    # Heuristic: find the H2 "Headline" and wrap the next <p> in .headline.
    body_html = re.sub(
        r"(<h2>Headline</h2>\s*)<p>(.+?)</p>",
        r'\1<div class="headline"><p>\2</p></div>',
        body_html,
        flags=re.DOTALL,
        count=1,
    )

    # Wrap the metadata block (Phase / Data freshness / Slots executed) in .meta
    # These are the consecutive <p> tags between H1 and the first H2.
    body_html = re.sub(
        r"(</h1>\s*)((?:<p>(?:<strong>(?:Phase|Data freshness|Slots executed today):.*?</p>\s*)+))",
        lambda m: m.group(1) + f'<div class="meta">{m.group(2)}</div>',
        body_html,
        flags=re.DOTALL,
        count=1,
    )

    return body_html


def render_page(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        f"  <meta charset=\"utf-8\">\n"
        f"  <title>{html.escape(title)}</title>\n"
        f"  <style>{CSS}</style>\n"
        "</head>\n"
        f"<body>\n{body}\n</body>\n"
        "</html>\n"
    )


def main():
    if len(sys.argv) != 2:
        print("usage: insights_to_html.py <path-to-insights.md>", file=sys.stderr)
        return 2
    md_path = pathlib.Path(sys.argv[1]).resolve()
    if not md_path.exists():
        print(f"not found: {md_path}", file=sys.stderr)
        return 1
    md = md_path.read_text()

    # Title = first # heading or filename stem
    m = re.search(r"^#\s+(.+)$", md, flags=re.MULTILINE)
    title = m.group(1).strip() if m else md_path.stem

    body = md_to_html(md)
    page = render_page(title, body)

    html_path = md_path.with_suffix(".html")
    html_path.write_text(page)
    print(html_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
