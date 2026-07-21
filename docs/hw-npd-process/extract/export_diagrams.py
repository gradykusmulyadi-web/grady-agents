"""Export every Mermaid diagram in the docs to a standalone SVG in ../diagrams/.

You only need this when you want image FILES - for slide decks, Word, email, or a
PDF export. Confluence does not need it: its Mermaid macro renders the fenced
blocks straight from the Markdown.

How it works: starts a tiny local server, opens the page in your browser, lets
Mermaid render each diagram, and posts the resulting SVG back to be saved. It
uses the browser you already have, so there is no headless-Chrome download.

Prerequisite (one-off, ~3 MB):
    npm install mermaid@11

Usage:
    python export_diagrams.py
"""

import http.server
import re
import threading
import urllib.parse
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent
OUT = DOCS / "diagrams"
MERMAID = HERE / "node_modules" / "mermaid" / "dist" / "mermaid.min.js"
SOURCES = ("01-swimlanes.md", "02-gantt-dependencies.md")
PORT = 8900

# Gantt sections are titled by lane only ("Full NPD"), which would collide with
# the swimlane filenames. Prefix them so the two sets stay distinguishable.
GANTT_PREFIX = "gantt-"


def slugify(text):
    text = re.sub(r"[^\w\s.-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text)


def collect():
    """(filename_stem, mermaid_code) for every block, titled by nearest heading."""
    items = []
    for name in SOURCES:
        text = (DOCS / name).read_text(encoding="utf-8").replace("\r\n", "\n")
        is_gantt_doc = "gantt" in name
        heading = name
        for chunk in re.split(r"^(##+ .+)$", text, flags=re.M):
            if chunk.startswith("#"):
                heading = chunk.lstrip("# ").strip()
                continue
            for code in re.findall(r"```mermaid\n(.*?)```", chunk, re.S):
                stem = slugify(heading)
                if is_gantt_doc:
                    stem = GANTT_PREFIX + stem
                items.append((stem, code))
    return items


def build_page(items):
    divs = "".join(
        f'<div data-name="{stem}"><h3>{stem}</h3><pre class="mermaid">{code}</pre></div>'
        for stem, code in items
    )
    return f"""<!doctype html><html><body style="background:#fff;font-family:sans-serif">
<h2 id="status">Rendering {len(items)} diagrams...</h2>
<script src="/mermaid.min.js"></script>
{divs}
<script>
mermaid.initialize({{ startOnLoad: false, securityLevel: "loose" }});
(async () => {{
  await mermaid.run();
  let n = 0;
  for (const d of document.querySelectorAll('div[data-name]')) {{
    const svg = d.querySelector('svg');
    if (!svg) continue;
    // Pin intrinsic size so the saved file is not viewport-dependent.
    const b = svg.getBBox();
    const w = Math.ceil(b.width), h = Math.ceil(b.height);
    svg.setAttribute('width', w);
    svg.setAttribute('height', h);
    svg.setAttribute('viewBox', `0 0 ${{w}} ${{h}}`);
    svg.removeAttribute('style');
    await fetch('/save?name=' + encodeURIComponent(d.dataset.name),
                {{ method: 'POST', body: svg.outerHTML }});
    n++;
  }}
  document.getElementById('status').textContent =
    'Done - saved ' + n + ' SVGs. You can close this tab.';
}})();
</script></body></html>"""


def main():
    if not MERMAID.exists():
        raise SystemExit(
            f"mermaid not found at {MERMAID}\n"
            f"Install it first:  cd {HERE} && npm install mermaid@11"
        )

    items = collect()
    OUT.mkdir(exist_ok=True)
    page = build_page(items).encode("utf-8")
    saved = []
    done = threading.Event()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/mermaid.min.js":
                body = MERMAID.read_bytes()
                ctype = "application/javascript"
            else:
                body, ctype = page, "text/html; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            name = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)["name"][0]
            data = self.rfile.read(int(self.headers["Content-Length"]))
            (OUT / f"{name}.svg").write_bytes(data)
            saved.append(name)
            print(f"  {name}.svg  ({len(data) // 1024} KB)")
            self.send_response(204)
            self.end_headers()
            if len(saved) == len(items):
                done.set()

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    url = f"http://127.0.0.1:{PORT}/"
    print(f"Opening {url} to render {len(items)} diagrams...")
    webbrowser.open(url)

    if not done.wait(timeout=120):
        print(f"\nTimed out - saved {len(saved)} of {len(items)}. Is the page still open?")
    server.shutdown()
    print(f"\n{len(saved)} SVGs written to {OUT}")


if __name__ == "__main__":
    main()
