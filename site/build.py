"""Builds the website tools' JavaScript files from their HTML sources.

  site/savings-tool.html -> site/savings-tool.js  (mounts into <div id="nr-root">)
  site/funds-tool.html   -> site/funds-tool.js    (mounts into <div id="nf-root">)

Kajabi only holds a tiny loader, for example:
  <div id="nr-root"></div>
  <script src="https://cdn.jsdelivr.net/gh/nisbacode/nisba-rates@<commit>/site/savings-tool.js"></script>

Usage: python site/build.py            (builds both)
       python site/build.py funds-tool (builds one)
"""
import json
import re
import sys
from pathlib import Path

here = Path(__file__).parent
ROOTS = {"savings-tool": "nr-root", "funds-tool": "nf-root"}


def build(name: str) -> None:
    src = (here / f"{name}.html").read_text()
    markup = re.sub(r"<!--.*?-->", "", src.split("<style>")[0], flags=re.S).strip()
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1).strip()
    js = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
    out = (
        f"/* Built from site/{name}.html by site/build.py. Do not edit by hand. */\n"
        "(function(){\n"
        f"var root=document.getElementById('{ROOTS[name]}');if(!root)return;\n"
        f"var st=document.createElement('style');st.textContent={json.dumps(css)};document.head.appendChild(st);\n"
        f"root.innerHTML={json.dumps(markup)};\n"
        "})();\n" + js + "\n"
    )
    (here / f"{name}.js").write_text(out)
    print("built", name, len(out), "bytes")


for n in sys.argv[1:] or list(ROOTS):
    build(n)
