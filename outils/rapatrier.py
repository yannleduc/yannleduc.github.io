#!/usr/bin/env python3
"""Rapatrie dans le dépôt tous les visuels générés hébergés sur le CDN Higgsfield,
pour que le site ne dépende plus de l'abonnement.

  python3 outils/rapatrier.py          # télécharge et réécrit les liens
  python3 outils/rapatrier.py --essai  # liste seulement ce qui serait fait

Chaque fichier est enregistré dans media/ia/<identifiant>.<ext> (le point « visuel IA »
reste affiché, le site reconnaît ce dossier). Les liens sont réécrits dans
content/portfolio.json et modeles/images.json. Relancer le script ne retélécharge rien.
Il faut un accès réseau à d8j0ntlcm91z4.cloudfront.net (depuis un ordinateur personnel, ça marche)."""
import json, os, re, sys, urllib.request
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "d8j0ntlcm91z4.cloudfront.net"
essai = "--essai" in sys.argv
fichiers = [os.path.join(R, "content/portfolio.json"), os.path.join(R, "modeles/images.json")]
urls = set()
for f in fichiers:
    urls |= set(re.findall(r"https://" + re.escape(HOST) + r"/[^\"\s]+", open(f, encoding="utf-8").read()))
os.makedirs(os.path.join(R, "media/ia"), exist_ok=True)
correspondance = {}
for u in sorted(urls):
    m = re.search(r"hf_\d+_\d+_([0-9a-f-]{36})", u)
    ext = os.path.splitext(u)[1] or ".webp"
    nom = (m.group(1)[:8] if m else str(abs(hash(u)))) + ext
    local = "media/ia/" + nom
    dest = os.path.join(R, local)
    correspondance[u] = local
    if os.path.exists(dest):
        continue
    print(("à télécharger " if essai else "téléchargement ") + u + " -> " + local)
    if not essai:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as o:
            o.write(r.read())
if essai:
    print(len(urls), "liens trouvés"); sys.exit(0)
for f in fichiers:
    t = open(f, encoding="utf-8").read()
    for u, l in correspondance.items():
        t = t.replace(u, l)
    open(f, "w", encoding="utf-8").write(t)
print(len(correspondance), "visuels rapatriés dans media/ia/. Vérifier puis commit et push.")
