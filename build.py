# -*- coding: utf-8 -*-
"""Download every designer image locally + generate index.html case-study site."""
import json, os, re, html, urllib.parse
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "img")
os.makedirs(IMGDIR, exist_ok=True)

with open(os.path.join(ROOT, "designers.json"), encoding="utf-8") as f:
    DESIGNERS = json.load(f)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

def is_image_url(u):
    # skip obvious non-image (html page) urls
    path = urllib.parse.urlparse(u).path.lower()
    return any(path.endswith(e) for e in (".jpg", ".jpeg", ".png", ".webp", ".gif")) or \
           ("imgix" in u) or ("imagedelivery" in u) or ("images1" in u) or \
           ("imageserve" in u) or ("resize:fill" in u) or ("miro.medium" in u)

def ext_for(u, content_type):
    path = urllib.parse.urlparse(u).path.lower()
    for e in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if path.endswith(e):
            return ".jpg" if e == ".jpeg" else e
    if content_type:
        if "png" in content_type: return ".png"
        if "webp" in content_type: return ".webp"
        if "gif" in content_type: return ".gif"
    return ".jpg"

def download(u, dest_base, referer):
    try:
        headers = {"User-Agent": UA, "Referer": referer,
                   "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"}
        r = requests.get(u, headers=headers, timeout=30, allow_redirects=True)
        ct = r.headers.get("content-type", "")
        if r.status_code == 200 and r.content and ("image" in ct or len(r.content) > 2000):
            e = ext_for(u, ct)
            fn = dest_base + e
            with open(os.path.join(IMGDIR, fn), "wb") as fh:
                fh.write(r.content)
            return fn, len(r.content)
        return None, f"status={r.status_code} ct={ct}"
    except Exception as ex:
        return None, str(ex)

report = []
for i, d in enumerate(DESIGNERS, 1):
    ref = d.get("credentials_source") or d.get("quote_source") or ""
    local_imgs = []
    for n, im in enumerate(d.get("images", []), 1):
        u = im["url"]
        if not is_image_url(u):
            report.append((d["name"], u, "SKIP(non-image url)"))
            continue
        fn, info = download(u, f"{i:02d}_{n}", ref)
        if fn:
            local_imgs.append({"file": "img/" + fn, "caption": im.get("caption", "")})
            report.append((d["name"], u, f"OK {fn} ({info}b)"))
        else:
            # fallback: keep remote url so image still (maybe) shows
            local_imgs.append({"file": u, "caption": im.get("caption", ""), "remote": True})
            report.append((d["name"], u, f"FAIL {info} -> hotlink fallback"))
    d["_local"] = local_imgs

print("\n=== IMAGE REPORT ===")
ok = fail = skip = 0
for name, u, status in report:
    tag = "OK" if status.startswith("OK") else ("SKIP" if "SKIP" in status else "FAIL")
    if tag == "OK": ok += 1
    elif tag == "SKIP": skip += 1
    else: fail += 1
    print(f"[{tag}] {name}: {status}")
print(f"\nTOTAL ok={ok} fail(hotlink)={fail} skip={skip}")

# save enriched data for HTML step
with open(os.path.join(ROOT, "_enriched.json"), "w", encoding="utf-8") as f:
    json.dump(DESIGNERS, f, ensure_ascii=False, indent=2)
print("wrote _enriched.json")
