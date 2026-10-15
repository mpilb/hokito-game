# Très futé junior

Versions simplifiées du jeu de dés **Très futé** (*Ganz schön clever*, Wolfgang Warsch) pour des enfants de **6-7 ans**, de 2 à 4 joueurs, avec un adulte qui explique les règles et compte les points à la fin.

Trois variantes ont été construites pour comparer :

| Dossier | Dés | Zones |
|---|---|---|
| [`variante-a-5d-joker/`](variante-a-5d-joker/) | 5 : blanc (joker) + jaune, vert, orange, violet | 4 |
| [`variante-b-5d-sans-joker/`](variante-b-5d-sans-joker/) | 5 : jaune, bleu, vert, orange, violet | 5 |
| [`variante-c-6d-joker/`](variante-c-6d-joker/) | 6 : blanc (joker) + jaune, bleu, vert, orange, violet | 5 |

Chaque dossier contient :

- `regles.md` : les règles, à lire par l'adulte, avec un exemple par zone ;
- `feuillet.pdf` : la feuille de score, une page A4 par joueur, à imprimer (en couleur de préférence ; elle reste utilisable en noir et blanc) ;
- `feuillet.html` : la source du feuillet ;
- `simulation.py` et `resultats-simulation.md` : des milliers de parties simulées pour vérifier la durée, le remplissage des zones et l'équilibre des points.

Ce qui ne change pas d'une variante à l'autre : le joueur actif lance jusqu'à 3 fois et garde un dé à chaque fois, les dés plus petits partent sur le plateau d'argent, les autres joueurs se servent sur le plateau. Seuls bonus gardés : la **relance** et le **+1** ; une case remplie grâce à un +1 ne donne pas de bonus, pour éviter les enchaînements. Pas de renards ni de cases ×2/×3. Manches : 6 à 2 joueurs, 5 à 3 joueurs, 4 à 4 joueurs (12 à 16 tours, environ un quart d'heure).

## Comparatif

Chiffres issus des simulations (stratégie « meilleur coup immédiat », donc un peu meilleure qu'un enfant) :

| | A · 5 dés + joker | B · 5 dés sans joker | C · 6 dés + joker |
|---|---|---|---|
| Ce que fait l'enfant pendant la partie | trouver, comparer, écrire | trouver, comparer (« ou plus » et « ou moins »), écrire | trouver, comparer, écrire, **additionner bleu + blanc** |
| Décisions par lancer | choisir un dé ; où mettre le joker | choisir un dé (chaque dé n'a qu'une zone) | choisir parmi 6 dés ; où mettre le joker |
| Score moyen | ≈ 70 | ≈ 63 | ≈ 81 |
| Zone la moins remplie | 45 % | 36 % | 42 % |
| Part maximale d'une zone dans le score | 31 % | 29 % | 24,5 % |
| Densité du feuillet | aérée | moyenne | la plus dense |
| Le plus proche du jeu original | — | — | ✔ |

**Points forts et points faibles**

- **A — 5 dés avec joker.** Le plus simple : 4 zones seulement, aucune addition pendant le jeu. Le joker garde le petit plaisir du « je le mets où je veux ». La zone bleue disparaît.
- **B — 5 dés sans joker.** Chaque dé ne va que dans sa couleur : aucune hésitation, idéal pour une toute première partie. Mais 5 zones à suivre, et les « ou moins » du bleu se confondent facilement avec les « ou plus » du vert. Zones un peu moins remplies.
- **C — 6 dés avec joker.** Tout le matériel de la boîte, toutes les couleurs. Plus riche et mieux équilibré, mais plus de comparaisons à chaque lancer (6 dés) et une règle abstraite : en bleu, on additionne le dé bleu et le dé blanc, même si le blanc est ailleurs sur la table.

**Recommandation :** commencer par **A**. C'est la variante qui demande le moins de règles à retenir tout en gardant le joker. Passer à **C** quand les enfants sont à l'aise : elle prépare au vrai jeu. **B** est une bonne alternative si le joker crée des disputes ou de l'hésitation.

## Outils

- `outils/html-vers-pdf.mjs` : régénère un PDF à partir d'un feuillet HTML (`node tres-fute/outils/html-vers-pdf.mjs feuillet.html feuillet.pdf`, Playwright et Chromium requis).
- Relancer une simulation : `python3 simulation.py` dans le dossier de la variante.
