# Boîte à outils du portfolio

Tout ce qu'il faut pour ajouter du contenu au site sans repartir de zéro.
Le site ne se modifie qu'à un endroit : `content/portfolio.json`. La page `index.html` ne change pas pour ajouter du contenu.

## Ce qu'il y a ici

| Fichier | À quoi il sert |
|---|---|
| `modeles/partie.json` | Une étape de projet avec **tous** les champs possibles (texte, chiffres, galerie, modèle 3D, calculateur, livrables). |
| `modeles/projet.json` | Un projet complet (couverture, chiffres, blocs, récit court, plan cliquable, parties). |
| `modeles/images.json` | Les 47 visuels générés (Higgsfield), stockés dans `media/ia/` : 13 couvertures de projet (16:9), 14 bannières d'étape (21:9), plus ceux du pied et de SCORPE. Description, usage et endroit où ils servent déjà. |
| `modeles/entreprise.json` | Une nouvelle entreprise (onglet à côté de SCORPE) avec ses propres couleurs. |
| `img/modele/attente-am.svg`, `attente-entreprise.svg` | Images d'attente sobres (sans IA) quand on n'a encore aucune photo. |
| `outils/rapatrier.py` | Rapatrie dans `media/ia/` tout visuel encore hébergé chez Higgsfield (déjà fait le 17/11/2026 ; à relancer seulement si un nouveau lien Higgsfield est ajouté). |
| `outils/photo.py` | Prépare une photo : rognage, format (16:9, 21:9…), largeur 1600 px, WebP. |
| `outils/verifier.py` | Vérifie le contenu avant de publier (champs, images, liens, textes « À compléter »). |

## Effets mis de côté (non utilisés sur le site)

- `modeles/effets/nom-imprime.js` : le titre se dépose couche par couche comme une impression 3D FDM, avec une buse qui va et vient et des stries de couche. Démo : `modeles/effets/nom-imprime.html` (ouvrir yannleduc.github.io/modeles/effets/nom-imprime.html). Pour l'utiliser : voir l'en-tête du fichier .js (3 règles CSS et un appel `nomImprime(h1)`).

## Où vit chaque chose dans `portfolio.json`

- `profil` : accueil (accroche, en bref, parcours, compétences).
- `ecole` : en-tête de la page Arts et Métiers (`#ensam`).
- `semestres[i].projets` : projets **publiés** du semestre (page, carte cliquable, frise).
- `semestres[i].aVenir` : projets **préparés** : carte grisée « À venir » dans le carrousel, non cliquable, aucune page publique.
- `projet.parties` : étapes publiées. `projet.partiesAVenir` : étapes en préparation, invisibles.
- `entreprises` : SCORPE (même structure de projets).

## Aperçu des pages non publiées

Chaque projet en préparation, et chaque projet publié qui a des `partiesAVenir`, a une page d'aperçu liée nulle part :

- `#apercu-s1-pied-prothetique` : le pied avec les 4 étapes du Bloc 2 en préparation (métrologie, essai du premier pied, talon et allègement, présentation finale).
- `#apercu-s2-projet-s2` : éolienne (S2). `#apercu-s3-projet-s3` : semelle pour athlète de haut niveau (S3). `#apercu-s4-projet-s4` … `#apercu-s6-projet-s6` : projets modèles génériques.

Un bandeau jaune « Aperçu non publié » s'affiche en haut de ces pages.

## Recettes

### Ajouter un travail au Bloc 2 du pied
1. Dans `semestres[0].projets[0].partiesAVenir`, compléter la partie voulue (ou en copier une depuis `modeles/partie.json`, avec `"bloc": 2`).
2. Photos : `python3 outils/photo.py source.jpg img/s1/nom.webp`, puis les mettre dans `images` ou `banniere`.
3. Vérifier sur `#apercu-s1-pied-prothetique`.
4. Publier : déplacer l'objet de `partiesAVenir` vers `parties`, après la dernière étape du Bloc 2.
5. `python3 outils/verifier.py`, puis commit et push.

### Publier le projet d'un nouveau semestre
1. Dans `semestres[i].aVenir[0]`, remplacer les textes, les chiffres, les compétences, les outils et les livrables. Les 4 parties modèles se gardent, se suppriment ou se complètent avec `modeles/partie.json`.
2. Mettre les vraies photos dans `img/sN/` et remplacer les URL de `hero`, `couverture` et des bannières. Les visuels génériques de `modeles/images.json` peuvent rester en attendant.
3. Vérifier sur `#apercu-sN-projet-sN`.
4. Publier : déplacer l'objet de `aVenir` vers `projets`, supprimer `_aide`, `titreCarte` et `sousTitreCarte`. Si le semestre a un deuxième projet, en créer un nouveau depuis `modeles/projet.json`.
5. Mettre `"statut": "en-cours"` sur le semestre en cours (valeurs : `en-cours`, `a-venir`, `termine`). La progression de la frise se calcule seule avec `debut` et `fin`.
6. `python3 outils/verifier.py`, puis commit et push.

### Ajouter une photo réelle des rapports PDF
Les images extraites des rapports ont des coins noirs décoratifs : `python3 outils/photo.py image.png media/scorpe/nom.webp --marge 0.115`. Pour un plan avec un cadre fin : `--marge 0.025`.

## Choisir un visuel générique

Couvertures (16:9) : engrenages, pièce usinée, treillis, échangeur, vérin, pièce imprimée lattice, tôle pliée, carte électronique, ossature de bâtiment, béton armé, module à vis à billes, pompe en coupe, échantillons de matériaux.
Bannières d'étape (21:9) : croquis (contexte), post-it (analyse du besoin), écran CAO (conception), simulation MEF, programmation, fraiseuse CN (fabrication), assemblage sur établi (prototype), machine de traction (essais), métrologie, planning (gestion de projet), table de plans (bilan), mains autour d'une pièce (travail en équipe), rapport et carnet (rédaction), salle de soutenance (oral).
Règle : une même image n'est utilisée qu'une fois par projet ; dès qu'une vraie photo existe, elle remplace le visuel générique.

## Photos personnelles : pour rester cohérent

Fond clair et uni (mur, table blanche), lumière du jour, pièce bien nette au centre ou sur la droite, pas de visages reconnaissables sans accord. Puis `outils/photo.py` (16:9 pour une couverture, 21:9 pour une bannière). Ranger dans `img/sN/` (Arts et Métiers) ou `media/<entreprise>/`.

## Charte

- Arts et Métiers : violet `#80276C`, jaune `#FFA300`, fond blanc.
- SCORPE : RAL 6018 vert jaune `#57A639` et noir, fond blanc, texte vert foncé `#3D7A26` (lisible sur blanc). Ces couleurs sont dans le champ `couleurs` de l'entreprise ; une autre entreprise peut avoir les siennes.
- Polices : Zilla Slab (titres), Source Sans 3 (texte).
- Titre du site « Yann Leduc. » à garder.
- Visuels IA : pas de mention en bas de page. Un petit point de 7 px (violet Arts et Métiers, couleur de l'entreprise sinon) s'affiche automatiquement dans le coin bas droit de toute image ou vidéo rangée dans `media/ia/`. **Ne jamais mettre une vraie photo dans `media/ia/`**, ni un visuel IA ailleurs.

## Style des visuels générés (si on en refait un jour, avec n'importe quel générateur)

Couvertures : « Clean studio photo of [objet] with purple parts and small yellow details, white background, soft light, object on the right side, empty white space on the left, photorealistic, no text », en 16:9.
Bannières : même palette, 21:9, vue de dessus ou plan rapproché d'un poste de travail.
Pour garder un même cadrage sur une série, donner l'image précédente en référence avec « Keep EXACTLY the same camera angle, framing, object position and scale ».
