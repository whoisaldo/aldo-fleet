#!/usr/bin/env python3
"""Build one portable HTML review gallery with embedded screenshots."""

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
import sys
from urllib.parse import urlsplit


STYLE = """
:root{color-scheme:light;--ink:#20231e;--paper:#f6f7f2;--rule:#d9ded0}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:90px;background:transparent}
body{margin:0;color:var(--ink);font:16px/1.5 'Avenir Next',Avenir,'Trebuchet MS',sans-serif;background:transparent}
a{color:inherit;text-underline-offset:4px}a:hover{color:#496800}
a:focus-visible,button:focus-visible{outline:3px solid #76b900;outline-offset:4px}
.page{max-width:1180px;margin:auto}header{padding:28px 0 24px}
.eyebrow{font:12px/1.4 'SFMono-Regular',Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:#536048}
h1{font:500 clamp(30px,5vw,48px)/1.08 Baskerville,Palatino,serif;letter-spacing:-.03em;margin:10px 0 14px}
.role{color:#536048;max-width:760px;margin:0 0 18px}
.state{border-left:3px solid #76b900;padding-left:12px;font-size:14px}
.actions{display:flex;gap:12px 24px;flex-wrap:wrap;font-size:14px;margin-top:20px}
nav{position:sticky;top:0;z-index:2;display:flex;gap:8px 20px;flex-wrap:wrap;background:var(--paper);padding:14px 0;border-block:1px solid var(--rule);font-size:14px}
nav a{text-decoration:none}section{padding:28px 0 14px;scroll-margin-top:90px}
.caption{display:flex;align-items:baseline;gap:14px;margin-bottom:12px}
.number{font:13px 'SFMono-Regular',Consolas,monospace;color:#657257}
h2{font-size:19px;font-weight:600;letter-spacing:-.02em;margin:0}
.hint{font-size:13px;color:#596151;margin:0 0 12px}
.shot{display:block;padding:0;border:1px solid var(--rule);background:white;width:100%;cursor:zoom-in;border-radius:3px;overflow:hidden}
.shot img{display:block;width:100%;height:auto}
footer{padding:28px 0;font-size:13px;color:#596151;border-top:1px solid var(--rule);margin-top:22px}
dialog{border:1px solid var(--rule);border-radius:6px;padding:0;max-width:calc(100vw - 28px);width:1320px;max-height:calc(100vh - 28px);background:white;color:var(--ink)}
dialog::backdrop{background:rgba(20,25,15,.66)}
.dialog-head{position:sticky;top:0;background:var(--paper);padding:12px 16px;display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid var(--rule);font-size:14px}
.close{border:1px solid #adb79f;padding:6px 12px;border-radius:3px;background:white;color:var(--ink);font:inherit;cursor:pointer}
.zoom-content{overflow:auto;max-height:calc(100vh - 100px);padding:14px;background:#e9ece3}
.zoom-content img{display:block;max-width:none;margin:0 auto}
@media(max-width:600px){nav{gap:6px 14px;font-size:13px}h2{font-size:17px}section{padding-top:24px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{nav,.actions,.hint,dialog{display:none}section{break-before:page}.shot{border:0}}
"""

SCRIPT = """
const modal=document.querySelector('dialog');
const image=modal.querySelector('img');
document.querySelectorAll('.shot').forEach(button=>button.addEventListener('click',()=>{
 const source=button.querySelector('img');
 image.src=source.src;image.alt=source.alt;
 document.querySelector('#zoom-title').textContent=button.dataset.title;
 modal.showModal();modal.querySelector('.zoom-content').scrollTo(0,0);
}));
modal.querySelector('.close').addEventListener('click',()=>modal.close());
modal.addEventListener('click',event=>{if(event.target===modal)modal.close()});
"""


def escape(value):
    return html.escape(str(value), quote=True)


def image_uri(path):
    mime = mimetypes.guess_type(path)[0]
    if mime not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        raise ValueError(f"Use PNG, JPEG, WebP, or GIF screenshots: {path}")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def build(manifest, directory):
    status = manifest.get("status", "draft")
    if status not in {"draft", "submitted"}:
        raise ValueError("status must be draft or submitted; use submitted only after portal confirmation")
    screenshots = manifest.get("screenshots", [])
    if not screenshots:
        raise ValueError("At least one screenshot is required")
    title = escape(manifest["title"])
    role = escape(manifest.get("role", ""))
    note = escape(manifest.get("note", ""))
    state = "Submitted. Portal confirmation saved." if status == "submitted" else "Draft saved. Not submitted."
    sections, navigation = [], []
    for number, shot in enumerate(screenshots, 1):
        path = (directory / shot["path"]).resolve()
        name = escape(shot["title"])
        alt = escape(shot.get("alt", shot["title"]))
        uri = image_uri(path)
        navigation.append(f'<a href="#shot-{number}">{number:02d} {name}</a>')
        sections.append(f'''<section id="shot-{number}" aria-labelledby="heading-{number}">
<div class="caption"><span class="number">{number:02d}</span><h2 id="heading-{number}">{name}</h2></div>
<p class="hint">Click the screenshot to view it at full size.</p>
<button class="shot" type="button" aria-label="View {name} at full size" data-title="{name}">
<img src="{uri}" alt="{alt}" loading="lazy" decoding="async"></button></section>''')
    actions = []
    for link in manifest.get("links", []):
        href = str(link["href"])
        parsed = urlsplit(href)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Download links must be absolute HTTP(S) URLs")
        download = " download" if link.get("download") else ""
        actions.append(f'<a{download} href="{escape(href)}">{escape(link["label"])}</a>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{STYLE}</style></head>
<body><div class="page"><header>
<p class="eyebrow">Application review</p><h1>{title}</h1><p class="role">{role}</p>
<p class="state"><strong>{state}</strong> {note}</p>
<div class="actions">{' '.join(actions)}</div></header>
<nav aria-label="Screenshots">{' '.join(navigation)}</nav>
<main>{''.join(sections)}</main>
<footer>{state} The screenshots are embedded in this HTML file.</footer></div>
<dialog aria-labelledby="zoom-title"><div class="dialog-head"><strong id="zoom-title"></strong>
<button type="button" class="close">Close</button></div><div class="zoom-content"><img alt=""></div></dialog>
<script>{SCRIPT}</script></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    document = build(manifest, args.manifest.resolve().parent)
    if args.output.resolve() == args.manifest.resolve():
        raise ValueError("Output must differ from the manifest")
    if any(args.output.resolve() == (args.manifest.resolve().parent / s["path"]).resolve()
           for s in manifest["screenshots"]):
        raise ValueError("Output must not replace a screenshot")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    print(json.dumps({"file": str(args.output), "screenshots": len(manifest["screenshots"]),
                      "status": manifest.get("status", "draft"), "bytes": args.output.stat().st_size}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.exit(str(error))
