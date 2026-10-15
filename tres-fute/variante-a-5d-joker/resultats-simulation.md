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
| Score moyen (écart-type) | 77.7 (10.5) | 81.0 (11.2) | 76.1 (11.6) |
| Score min / max | 48 / 115 | 45 / 120 | 35 / 110 |
| Parties terminées (tours actifs = manches × joueurs) | 100 % | 100 % | 100 % |
| Tours actifs (critère : × 1 min ≤ 20) | 12 | 15 | 16 |
| Remplissage jaune | 68 % | 68 % | 64 % |
| Remplissage vert | 50 % | 57 % | 57 % |
| Remplissage orange | 69 % | 79 % | 82 % |
| Remplissage violet | 62 % | 62 % | 58 % |
| Points jaune (part du score) | 24.7 (32 %) | 24.2 (30 %) | 21.5 (28 %) |
| Points vert (part du score) | 13.8 (17 %) | 16.7 (20 %) | 16.6 (21 %) |
| Points orange (part du score) | 17.9 (23 %) | 19.3 (24 %) | 19.1 (26 %) |
| Points violet (part du score) | 21.3 (28 %) | 20.8 (26 %) | 19.0 (25 %) |
| Feuilles à 0 point en jaune | 0.0 % | 0.0 % | 0.0 % |
| Feuilles sans aucune colonne jaune complète (0 point de colonne) | 11.0 % | 13.4 % | 17.2 % |
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
- **OK** — 2 joueurs : part du score jaune 32 % <= 40 %
- **OK** — 2 joueurs : part du score vert 17 % <= 40 %
- **OK** — 2 joueurs : part du score orange 23 % <= 40 %
- **OK** — 2 joueurs : part du score violet 28 % <= 40 %
- **OK** — 3 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 3 joueurs : 100 % des parties terminées avec exactement 5 x 3 = 15 tours actifs
- **OK** — 3 joueurs : 15 tours actifs (critère : x 1 min <= 20)
- **OK** — 3 joueurs : remplissage jaune 68 % >= 30 %
- **OK** — 3 joueurs : remplissage vert 57 % >= 30 %
- **OK** — 3 joueurs : remplissage orange 79 % >= 30 %
- **OK** — 3 joueurs : remplissage violet 62 % >= 30 %
- **OK** — 3 joueurs : part du score jaune 30 % <= 40 %
- **OK** — 3 joueurs : part du score vert 20 % <= 40 %
- **OK** — 3 joueurs : part du score orange 24 % <= 40 %
- **OK** — 3 joueurs : part du score violet 26 % <= 40 %
- **OK** — 4 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 4 joueurs : 100 % des parties terminées avec exactement 4 x 4 = 16 tours actifs
- **OK** — 4 joueurs : 16 tours actifs (critère : x 1 min <= 20)
- **OK** — 4 joueurs : remplissage jaune 64 % >= 30 %
- **OK** — 4 joueurs : remplissage vert 57 % >= 30 %
- **OK** — 4 joueurs : remplissage orange 82 % >= 30 %
- **OK** — 4 joueurs : remplissage violet 58 % >= 30 %
- **OK** — 4 joueurs : part du score jaune 28 % <= 40 %
- **OK** — 4 joueurs : part du score vert 21 % <= 40 %
- **OK** — 4 joueurs : part du score orange 26 % <= 40 %
- **OK** — 4 joueurs : part du score violet 25 % <= 40 %

**Bilan gloutonne : OK partout.**

## Stratégie enfant

| | 2 joueurs | 3 joueurs | 4 joueurs |
|---|---|---|---|
| Manches | 6 | 5 | 4 |
| Score moyen (écart-type) | 56.8 (10.2) | 60.4 (10.8) | 57.2 (11.0) |
| Score min / max | 28 / 91 | 30 / 97 | 27 / 110 |
| Parties terminées (tours actifs = manches × joueurs) | 100 % | 100 % | 100 % |
| Tours actifs (critère : × 1 min ≤ 20) | 12 | 15 | 16 |
| Remplissage jaune | 54 % | 58 % | 58 % |
| Remplissage vert | 55 % | 58 % | 56 % |
| Remplissage orange | 87 % | 93 % | 93 % |
| Remplissage violet | 39 % | 41 % | 38 % |
| Points jaune (part du score) | 11.8 (20 %) | 13.7 (22 %) | 13.2 (23 %) |
| Points vert (part du score) | 14.2 (25 %) | 15.7 (25 %) | 14.7 (25 %) |
| Points orange (part du score) | 18.7 (34 %) | 18.5 (31 %) | 17.9 (32 %) |
| Points violet (part du score) | 12.1 (21 %) | 12.5 (21 %) | 11.4 (20 %) |
| Feuilles à 0 point en jaune | 0.0 % | 0.0 % | 0.0 % |
| Feuilles sans aucune colonne jaune complète (0 point de colonne) | 55.1 % | 46.8 % | 49.6 % |
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
- **OK** — 2 joueurs : part du score jaune 20 % <= 40 %
- **OK** — 2 joueurs : part du score vert 25 % <= 40 %
- **OK** — 2 joueurs : part du score orange 34 % <= 40 %
- **OK** — 2 joueurs : part du score violet 21 % <= 40 %
- **OK** — 3 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 3 joueurs : 100 % des parties terminées avec exactement 5 x 3 = 15 tours actifs
- **OK** — 3 joueurs : 15 tours actifs (critère : x 1 min <= 20)
- **OK** — 3 joueurs : remplissage jaune 58 % >= 30 %
- **OK** — 3 joueurs : remplissage vert 58 % >= 30 %
- **OK** — 3 joueurs : remplissage orange 93 % >= 30 %
- **OK** — 3 joueurs : remplissage violet 41 % >= 30 %
- **OK** — 3 joueurs : part du score jaune 22 % <= 40 %
- **OK** — 3 joueurs : part du score vert 25 % <= 40 %
- **OK** — 3 joueurs : part du score orange 31 % <= 40 %
- **OK** — 3 joueurs : part du score violet 21 % <= 40 %
- **OK** — 4 joueurs : 1000 parties jouées (>= 1000)
- **OK** — 4 joueurs : 100 % des parties terminées avec exactement 4 x 4 = 16 tours actifs
- **OK** — 4 joueurs : 16 tours actifs (critère : x 1 min <= 20)
- **OK** — 4 joueurs : remplissage jaune 58 % >= 30 %
- **OK** — 4 joueurs : remplissage vert 56 % >= 30 %
- **OK** — 4 joueurs : remplissage orange 93 % >= 30 %
- **OK** — 4 joueurs : remplissage violet 38 % >= 30 %
- **OK** — 4 joueurs : part du score jaune 23 % <= 40 %
- **OK** — 4 joueurs : part du score vert 25 % <= 40 %
- **OK** — 4 joueurs : part du score orange 32 % <= 40 %
- **OK** — 4 joueurs : part du score violet 20 % <= 40 %

**Bilan enfant : OK partout.**

## Bilan général

**OK partout, pour les deux stratégies.**
