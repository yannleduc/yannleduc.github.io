#!/usr/bin/env python3
"""Prépare une photo pour le site : recadrage optionnel, redimensionnement, conversion en WebP.

Exemples :
  python3 outils/photo.py photo.jpg img/s1/essai.webp
  python3 outils/photo.py scan.png img/s2/plan.webp --marge 0.03 --largeur 1600
  python3 outils/photo.py photo.jpg img/s2/banniere.webp --ratio 21:9
Options :
  --marge  fraction rognée sur chaque bord (ex. 0.115 pour les images des rapports aux coins noirs décoratifs)
  --ratio  recadre au centre à ce format (16:9, 21:9, 4:3, 1:1)
  --largeur largeur maximale en pixels (défaut 1600)
  --qualite qualité WebP (défaut 84)
"""
import argparse
from PIL import Image, ImageOps

a = argparse.ArgumentParser()
a.add_argument("entree"); a.add_argument("sortie")
a.add_argument("--marge", type=float, default=0)
a.add_argument("--ratio", default="")
a.add_argument("--largeur", type=int, default=1600)
a.add_argument("--qualite", type=int, default=84)
o = a.parse_args()
im = ImageOps.exif_transpose(Image.open(o.entree)).convert("RGB")
w, h = im.size
if o.marge:
    im = im.crop((int(w * o.marge), int(h * o.marge), int(w * (1 - o.marge)), int(h * (1 - o.marge))))
if o.ratio:
    rw, rh = (float(x) for x in o.ratio.split(":"))
    w, h = im.size
    if w / h > rw / rh:
        nw = int(h * rw / rh); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w * rh / rw); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
im.thumbnail((o.largeur, o.largeur * 4))
im.save(o.sortie, "WEBP", quality=o.qualite)
print(o.sortie, im.size)
