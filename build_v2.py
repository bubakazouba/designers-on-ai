# -*- coding: utf-8 -*-
"""Download AI-WORK images for site #1 v2 into img2/. Writes _enriched_v2.json."""
import json, os, urllib.parse
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "img2")
os.makedirs(IMGDIR, exist_ok=True)

with open(os.path.join(ROOT, "designers_v2.json"), encoding="utf-8") as f:
    D = json.load(f)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

def ext_from_bytes(b, url):
    if b[:3] == b"\xff\xd8\xff": return ".jpg"
    if b[:8] == b"\x89PNG\r\n\x1a\n": return ".png"
    if b[:4] == b"RIFF" and b"WEBP" in b[:16]: return ".webp"
    if b[4:12] == b"ftypavif": return ".avif"
    if b[:6] in (b"GIF87a", b"GIF89a"): return ".gif"
    path = urllib.parse.urlparse(url).path.lower()
    for e in (".jpg",".jpeg",".png",".webp",".gif",".avif"):
        if path.endswith(e): return ".jpg" if e==".jpeg" else e
    return ".jpg"

report = []
for i, d in enumerate(D, 1):
    ref = d.get("credentials_source") or d.get("quote_source") or ""
    local = []
    for n, im in enumerate(d.get("ai_work_images", []), 1):
        u = im["url"]
        try:
            r = requests.get(u, headers={"User-Agent": UA, "Referer": ref,
                             "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"},
                             timeout=40, allow_redirects=True)
            ct = r.headers.get("content-type", "")
            if r.status_code == 200 and r.content and ("image" in ct or len(r.content) > 3000):
                e = ext_from_bytes(r.content[:20], u)
                fn = f"{i:02d}_{n}{e}"
                with open(os.path.join(IMGDIR, fn), "wb") as fh:
                    fh.write(r.content)
                local.append({"file": "img2/"+fn, "caption": im.get("caption","")})
                report.append((d["name"], "OK "+fn, len(r.content)))
            else:
                local.append({"file": u, "caption": im.get("caption",""), "remote": True})
                report.append((d["name"], f"FAIL {r.status_code} {ct}", 0))
        except Exception as ex:
            local.append({"file": u, "caption": im.get("caption",""), "remote": True})
            report.append((d["name"], f"ERR {ex}", 0))
    d["_local"] = local

ok = sum(1 for _,s,_ in report if s.startswith("OK"))
bad = sum(1 for _,s,_ in report if not s.startswith("OK"))
print("=== IMAGE REPORT ===")
for name, s, sz in report:
    print(f"[{'OK' if s.startswith('OK') else 'BAD'}] {name}: {s} {sz if sz else ''}")
print(f"\nTOTAL ok={ok} bad={bad}")
# flag artists with ZERO working images
zero = [d["name"] for d in D if not [x for x in d.get("_local",[]) if not x.get("remote")]]
print("ARTISTS WITH ZERO WORKING IMAGES:", zero if zero else "none")

with open(os.path.join(ROOT, "_enriched_v2.json"), "w", encoding="utf-8") as f:
    json.dump(D, f, ensure_ascii=False, indent=2)
print("wrote _enriched_v2.json ;", len(D), "artists")
