#!/usr/bin/env python3
"""Vérifie content/portfolio.json avant de publier.
  python3 outils/verifier.py
Contrôle : JSON valide, identifiants uniques, champs obligatoires, images locales présentes,
statuts de livrables connus, liens 'partie' (récit, plan) vers des parties existantes,
textes « À compléter » restés dans des parties publiées."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(R, "content/portfolio.json")))
err, warn = [], []
OBL_P = ["id", "titre", "sousTitre", "periode", "resume", "parties"]
OBL_PA = ["id", "titre", "module", "date", "texte"]
def img(path, ou):
    if path and not path.startswith("http") and not os.path.exists(os.path.join(R, path)):
        err.append(f"{ou} : image introuvable {path}")
def projet(g, p, publie):
    ou = f"{g['id']}/{p.get('id')}"
    for k in OBL_P:
        if k not in p: err.append(f"{ou} : champ manquant '{k}'")
    for k in ("hero", "couverture"):
        if p.get(k): img(p[k].get("image"), ou)
    ids = set()
    for liste, pub in (("parties", publie), ("partiesAVenir", False)):
        for pa in p.get(liste, []):
            o2 = f"{ou}/{pa.get('id')}"
            if pa.get("id") in ids: err.append(f"{o2} : id de partie en double")
            ids.add(pa.get("id"))
            for k in OBL_PA:
                if k not in pa: err.append(f"{o2} : champ manquant '{k}'")
            if pa.get("banniere"): img(pa["banniere"].get("image"), o2)
            for im in pa.get("images", []): img(im.get("src"), o2)
            for l in pa.get("livrables", []):
                if l.get("statut") not in ("rendu", "en-cours", "a-venir"): err.append(f"{o2} : statut inconnu {l.get('statut')}")
            if pub and "À compléter" in json.dumps(pa, ensure_ascii=False): warn.append(f"{o2} : texte « À compléter » dans une partie publiée")
    for r in ("recit", "recitCourt"):
        for e in (p.get(r) or {}).get("etapes", []):
            if e.get("partie") and e["partie"] not in ids: warn.append(f"{ou} : {r} renvoie vers une partie absente '{e['partie']}'")
    for rp in (p.get("plan") or {}).get("reperes", []):
        if rp.get("partie") not in ids: warn.append(f"{ou} : repère {rp.get('id')} vers une partie absente")
for g in d["semestres"] + d.get("entreprises", []):
    vus = set()
    for p in g.get("projets", []):
        if p["id"] in vus: err.append(f"{g['id']} : projet en double {p['id']}")
        vus.add(p["id"]); projet(g, p, True)
    for p in g.get("aVenir", []): projet(g, p, False)
for m in warn: print("attention :", m)
for m in err: print("ERREUR :", m)
print("OK" if not err else f"{len(err)} erreur(s)")
sys.exit(1 if err else 0)
