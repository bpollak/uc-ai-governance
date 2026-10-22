"""Build index.html from content.md. Run: python3 build.py"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
TITLE = "Governance and Oversight of the UC–CSU–CCC AI Computing Program"
DATE = "October 2026"

FIGURE = re.compile(r"<p>\[\[figure:([^|\]]+)\|([^\]]+)\]\]</p>")


def figure(match):
    src, alt = match.group(1), html.escape(match.group(2), quote=True)
    return (f'<figure><img src="images/{src}" alt="{alt}" loading="lazy">'
            f'</figure>')


body = markdown.markdown((ROOT / "content.md").read_text(), extensions=["tables"])
body = FIGURE.sub(figure, body)
body = re.sub(r"<table>", '<div class="table"><table>', body)
body = re.sub(r"</table>", "</table></div>", body)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{TITLE}</title>
<style>
:root {{
  --bg: #ffffff; --text: #1b1f24; --muted: #57606a; --rule: #d8dee4;
  --accent: #182b49; --gold: #ffcd00; --tint: #f4f6f9;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #0f1419; --text: #e6e9ed; --muted: #9aa4af; --rule: #2d333b;
    --accent: #9ec5ff; --gold: #ffcd00; --tint: #161c23;
  }}
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--bg); color: var(--text);
  font: 17px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}}
header {{ border-top: 6px solid var(--gold); background: var(--tint); }}
.wrap {{ max-width: 760px; margin: 0 auto; padding: 0 16px; }}
header .wrap {{ padding-top: 40px; padding-bottom: 28px; }}
h1 {{ font-size: 2rem; line-height: 1.2; margin: 0 0 8px; color: var(--accent); }}
.byline {{ color: var(--muted); margin: 0; font-size: 0.95rem; }}
main {{ padding-top: 24px; padding-bottom: 64px; }}
h2 {{ font-size: 1.35rem; margin: 2.4em 0 0.6em; color: var(--accent);
      padding-top: 0.6em; border-top: 1px solid var(--rule); }}
p, ul, ol {{ margin: 0 0 1em; }}
li {{ margin-bottom: 0.35em; }}
.table {{ overflow-x: auto; margin: 0 0 1.2em; }}
table {{ border-collapse: collapse; width: 100%; font-size: 0.92rem; }}
th, td {{ text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--rule); }}
th {{ background: var(--tint); font-weight: 600; }}
figure {{ margin: 1.4em 0; }}
figure img {{ display: block; width: 100%; height: auto; background: #fff;
             border: 1px solid var(--rule); border-radius: 8px; padding: 8px; }}
footer {{ border-top: 1px solid var(--rule); color: var(--muted); font-size: 0.85rem; }}
footer .wrap {{ padding-top: 16px; padding-bottom: 32px; }}
</style>
</head>
<body>
<header><div class="wrap">
<h1>{TITLE}</h1>
<p class="byline">UC San Diego IT Services · {DATE} · Draft for discussion</p>
</div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">Draft for discussion.</div></footer>
</body>
</html>
"""

(ROOT / "index.html").write_text(page)
print("wrote index.html")
