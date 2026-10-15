# Résultats de simulation — variante A (5 dés avec joker)

Généré par `simulation.py` (graine 20261015, 1000 parties par nombre de joueurs et par stratégie). Deux stratégies :

- **gloutonne** : le choix qui rapporte le plus de points immédiats ou de progrès, Relance si le meilleur choix est faible, +1 si le coup vaut assez.
- **enfant** : jamais de Relance ; un dé utilisable au hasard (sinon un dé au hasard sans rien cocher), une case possible au hasard ; +1 dès qu'un coup est possible, sur un coup tiré au hasard.

**Fin de partie.** La fin est garantie par construction : le nombre de manches est fixe (6, 5 ou 4) et un tour de joueur actif compte au plus 3 choix de dé (plus les Relances, limitées par les bonus gagnés). La simulation le contrôle : elle compte les tours de joueur actif réellement joués dans chaque partie et vérifie qu'ils valent manches × joueurs ; un garde-fou lève une erreur si un tour dépasse 50 itérations de boucle (jamais déclenché).

**Durée.** La ligne « tours actifs » compte les tours de joueur actif ; le critère les convertit à raison de 1 min par tour (≤ 20). Ce n'est pas une durée mesurée : les règles annoncent 20 à 30 minutes réelles avec des enfants de 6-7 ans.

## Stratégie gloutonne

| | 2 joueurs | 3 joueurs | 4 joueurs |
|---|---|---|---|
| Manches | 6 | 5 | 4 |
| Score moyen (écart-type) | 69.5 (10.4) | 72.8 (11.1) | 68.3 (11.6) |
| Score min / max | 41 / 104 | 38 / 113 | 28 / 104 |
| Parties terminées (tours actifs = manches × joueurs) | 100 % | 100 % | 100 % |
| Tours actifs (critère : × 1 min ≤ 20) | 12 | 15 | 16 |
| Remplissage jaune | 68 % | 68 % | 64 % |
| Remplissage vert | 50 % | 57 % | 57 % |
| Remplissage orange | 69 % | 79 % | 82 % |
| Remplissage violet | 62 % | 62 % | 58 % |
| Points jaune (part du score) | 16.5 (24 %) | 16.0 (22 %) | 13.8 (20 %) |
| Points vert (part du score) | 13.8 (19 %) | 16.7 (22 %) | 16.6 (23 %) |
| Points orange (part du score) | 17.9 (26 %) | 19.3 (27 %) | 19.1 (29 %) |
| Points violet (part du score) | 21.3 (31 %) | 20.8 (29 %) | 19.0 (28 %) |
| Relances gagnées (par joueur et par partie) | 2.69 | 3.02 | 2.94 |
| Relances utilisées (par joueur et par partie) | 1.64 | 1.70 | 1.42 |
| +1 gagnés (par joueur et par partie) | 1.73 | 1.95 | 1.88 |
| +1 utilisés (par joueur et par partie) | 1.69 | 1.92 | 1.87 |
| Bonus perdus (case remplie avec un +1) (par joueur et par partie) | 0.23 | 0.24 | 0.21 |

### Vérification des critères 6 et 7 — stratégie gloutonne

- **OK** — 2 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 2 joueurs : 100 % des parties terminées avec exactement 6 x 2 = 12 tours actifs
- **OK** — 2 joueurs : 12 tours actifs (critère : x 1 min <= 20)
- **OK** — 2 joueurs : remplissage jaune 68 % >= 30 %
- **OK** — 2 joueurs : remplissage vert 50 % >= 30 %
- **OK** — 2 joueurs : remplissage orange 69 % >= 30 %
- **OK** — 2 joueurs : remplissage violet 62 % >= 30 %
- **OK** — 2 joueurs : part du score jaune 24 % <= 40 %
- **OK** — 2 joueurs : part du score vert 19 % <= 40 %
- **OK** — 2 joueurs : part du score orange 26 % <= 40 %
- **OK** — 2 joueurs : part du score violet 31 % <= 40 %
- **OK** — 3 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 3 joueurs : 100 % des parties terminées avec exactement 5 x 3 = 15 tours actifs
- **OK** — 3 joueurs : 15 tours actifs (critère : x 1 min <= 20)
- **OK** — 3 joueurs : remplissage jaune 68 % >= 30 %
- **OK** — 3 joueurs : remplissage vert 57 % >= 30 %
- **OK** — 3 joueurs : remplissage orange 79 % >= 30 %
- **OK** — 3 joueurs : remplissage violet 62 % >= 30 %
- **OK** — 3 joueurs : part du score jaune 22 % <= 40 %
- **OK** — 3 joueurs : part du score vert 22 % <= 40 %
- **OK** — 3 joueurs : part du score orange 27 % <= 40 %
- **OK** — 3 joueurs : part du score violet 29 % <= 40 %
- **OK** — 4 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 4 joueurs : 100 % des parties terminées avec exactement 4 x 4 = 16 tours actifs
- **OK** — 4 joueurs : 16 tours actifs (critère : x 1 min <= 20)
- **OK** — 4 joueurs : remplissage jaune 64 % >= 30 %
- **OK** — 4 joueurs : remplissage vert 57 % >= 30 %
- **OK** — 4 joueurs : remplissage orange 82 % >= 30 %
- **OK** — 4 joueurs : remplissage violet 58 % >= 30 %
- **OK** — 4 joueurs : part du score jaune 20 % <= 40 %
- **OK** — 4 joueurs : part du score vert 23 % <= 40 %
- **OK** — 4 joueurs : part du score orange 29 % <= 40 %
- **OK** — 4 joueurs : part du score violet 28 % <= 40 %

**Bilan gloutonne : OK partout.**

## Stratégie enfant

| | 2 joueurs | 3 joueurs | 4 joueurs |
|---|---|---|---|
| Manches | 6 | 5 | 4 |
| Score moyen (écart-type) | 50.4 (10.1) | 53.4 (10.7) | 50.3 (10.8) |
| Score min / max | 22 / 82 | 22 / 90 | 21 / 98 |
| Parties terminées (tours actifs = manches × joueurs) | 100 % | 100 % | 100 % |
| Tours actifs (critère : × 1 min ≤ 20) | 12 | 15 | 16 |
| Remplissage jaune | 54 % | 58 % | 58 % |
| Remplissage vert | 55 % | 58 % | 56 % |
| Remplissage orange | 87 % | 93 % | 93 % |
| Remplissage violet | 39 % | 41 % | 38 % |
| Points jaune (part du score) | 5.3 (10 %) | 6.6 (12 %) | 6.3 (12 %) |
| Points vert (part du score) | 14.2 (28 %) | 15.7 (29 %) | 14.7 (29 %) |
| Points orange (part du score) | 18.7 (38 %) | 18.5 (36 %) | 17.9 (37 %) |
| Points violet (part du score) | 12.1 (24 %) | 12.5 (24 %) | 11.4 (23 %) |
| Relances gagnées (par joueur et par partie) | 2.45 | 2.73 | 2.72 |
| Relances utilisées (par joueur et par partie) | 0.00 | 0.00 | 0.00 |
| +1 gagnés (par joueur et par partie) | 1.44 | 1.63 | 1.53 |
| +1 utilisés (par joueur et par partie) | 1.42 | 1.61 | 1.52 |
| Bonus perdus (case remplie avec un +1) (par joueur et par partie) | 0.27 | 0.29 | 0.27 |

### Vérification des critères 6 et 7 — stratégie enfant

- **OK** — 2 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 2 joueurs : 100 % des parties terminées avec exactement 6 x 2 = 12 tours actifs
- **OK** — 2 joueurs : 12 tours actifs (critère : x 1 min <= 20)
- **OK** — 2 joueurs : remplissage jaune 54 % >= 30 %
- **OK** — 2 joueurs : remplissage vert 55 % >= 30 %
- **OK** — 2 joueurs : remplissage orange 87 % >= 30 %
- **OK** — 2 joueurs : remplissage violet 39 % >= 30 %
- **OK** — 2 joueurs : part du score jaune 10 % <= 40 %
- **OK** — 2 joueurs : part du score vert 28 % <= 40 %
- **OK** — 2 joueurs : part du score orange 38 % <= 40 %
- **OK** — 2 joueurs : part du score violet 24 % <= 40 %
- **OK** — 3 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 3 joueurs : 100 % des parties terminées avec exactement 5 x 3 = 15 tours actifs
- **OK** — 3 joueurs : 15 tours actifs (critère : x 1 min <= 20)
- **OK** — 3 joueurs : remplissage jaune 58 % >= 30 %
- **OK** — 3 joueurs : remplissage vert 58 % >= 30 %
- **OK** — 3 joueurs : remplissage orange 93 % >= 30 %
- **OK** — 3 joueurs : remplissage violet 41 % >= 30 %
- **OK** — 3 joueurs : part du score jaune 12 % <= 40 %
- **OK** — 3 joueurs : part du score vert 29 % <= 40 %
- **OK** — 3 joueurs : part du score orange 36 % <= 40 %
- **OK** — 3 joueurs : part du score violet 24 % <= 40 %
- **OK** — 4 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 4 joueurs : 100 % des parties terminées avec exactement 4 x 4 = 16 tours actifs
- **OK** — 4 joueurs : 16 tours actifs (critère : x 1 min <= 20)
- **OK** — 4 joueurs : remplissage jaune 58 % >= 30 %
- **OK** — 4 joueurs : remplissage vert 56 % >= 30 %
- **OK** — 4 joueurs : remplissage orange 93 % >= 30 %
- **OK** — 4 joueurs : remplissage violet 38 % >= 30 %
- **OK** — 4 joueurs : part du score jaune 12 % <= 40 %
- **OK** — 4 joueurs : part du score vert 29 % <= 40 %
- **OK** — 4 joueurs : part du score orange 37 % <= 40 %
- **OK** — 4 joueurs : part du score violet 23 % <= 40 %

**Bilan enfant : OK partout.**

## Bilan général

**OK partout, pour les deux stratégies.**
