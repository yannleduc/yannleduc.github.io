# Boîte à outils du portfolio

Tout ce qu'il faut pour ajouter du contenu au site sans repartir de zéro.
Le site ne se modifie qu'à un endroit : `content/portfolio.json`. La page `index.html` ne change pas pour ajouter du contenu.

## Ce qu'il y a ici

| Fichier | À quoi il sert |
|---|---|
| `modeles/partie.json` | Une étape de projet avec **tous** les champs possibles (texte, chiffres, galerie, modèle 3D, calculateur, livrables). |
| `modeles/projet.json` | Un projet complet (couverture, chiffres, blocs, récit court, plan cliquable, parties). |
| `modeles/images.json` | Les 29 visuels déjà générés (Higgsfield), avec description et endroit où ils servent. Réutilisables tels quels. |
| `outils/photo.py` | Prépare une photo : rognage, format (16:9, 21:9…), largeur 1600 px, WebP. |
| `outils/verifier.py` | Vérifie le contenu avant de publier (champs, images, liens, textes « À compléter »). |

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
- `#apercu-s2-projet-s2` … `#apercu-s6-projet-s6` : les projets modèles des semestres 2 à 6.

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

## Charte

- Arts et Métiers : violet `#80276C`, jaune `#FFA300`, fond blanc.
- SCORPE : vert citron `#9ED05F` et noir, fond blanc, texte vert foncé `#3F7413`.
- Polices : Zilla Slab (titres), Source Sans 3 (texte).
- Titre du site « Yann Leduc. » à garder.
- Mention IA : une seule phrase générique en bas de page.

## Style des visuels générés (si on en refait)

Couvertures : « Clean studio photo of [objet] with purple parts and small yellow details, white background, soft light, object on the right side, empty white space on the left, photorealistic, no text », en 16:9.
Bannières : même palette, 21:9, vue de dessus ou plan rapproché d'un poste de travail.
Pour garder un même cadrage sur une série, donner l'image précédente en référence avec « Keep EXACTLY the same camera angle, framing, object position and scale ».
