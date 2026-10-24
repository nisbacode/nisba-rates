"""Builds site/savings-tool.js from site/savings-tool.html.

Kajabi only holds a tiny loader:
  <div id="nr-root"></div>
  <script src="https://cdn.jsdelivr.net/gh/nisbacode/nisba-rates@main/site/savings-tool.js"></script>
"""
import json, re
from pathlib import Path

here = Path(__file__).parent
src = (here / "savings-tool.html").read_text()
markup = re.sub(r"<!--.*?-->", "", src.split("<style>")[0], flags=re.S).strip()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1).strip()
js = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
out = (
    "/* Built from site/savings-tool.html by site/build.py. Do not edit by hand. */\n"
    "(function(){\n"
    "var root=document.getElementById('nr-root');if(!root)return;\n"
    f"var st=document.createElement('style');st.textContent={json.dumps(css)};document.head.appendChild(st);\n"
    f"root.innerHTML={json.dumps(markup)};\n"
    "})();\n" + js + "\n"
)
(here / "savings-tool.js").write_text(out)
print("built", len(out), "bytes")
