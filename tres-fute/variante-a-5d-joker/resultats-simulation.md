# Résultats de simulation — variante A (5 dés avec joker)

Généré par `simulation.py` (graine 20261015, 1000 parties par nombre de joueurs, stratégie gloutonne : le choix qui rapporte le plus de points immédiats ou de progrès).

## Synthèse

| | 2 joueurs | 3 joueurs | 4 joueurs |
|---|---|---|---|
| Manches | 6 | 5 | 4 |
| Score moyen (écart-type) | 69.3 (10.3) | 72.7 (10.8) | 68.8 (10.9) |
| Score min / max | 37 / 106 | 39 / 116 | 27 / 107 |
| Parties terminées | 100 % | 100 % | 100 % |
| Tours de joueur actif (= minutes estimées) | 12 | 15 | 16 |
| Remplissage jaune | 68 % | 68 % | 64 % |
| Remplissage vert | 50 % | 58 % | 58 % |
| Remplissage orange | 47 % | 56 % | 59 % |
| Remplissage violet | 50 % | 49 % | 45 % |
| Points jaune (part du score) | 16.5 (24 %) | 15.7 (22 %) | 13.5 (20 %) |
| Points vert (part du score) | 14.0 (19 %) | 17.0 (23 %) | 17.0 (24 %) |
| Points orange (part du score) | 17.7 (26 %) | 19.5 (27 %) | 19.6 (29 %) |
| Points violet (part du score) | 21.1 (31 %) | 20.5 (29 %) | 18.7 (27 %) |
| Relances gagnées (par joueur et par partie) | 2.50 | 2.69 | 2.63 |
| Relances utilisées (par joueur et par partie) | 1.55 | 1.48 | 1.23 |
| +1 gagnés (par joueur et par partie) | 1.52 | 1.73 | 1.69 |
| +1 utilisés (par joueur et par partie) | 1.48 | 1.70 | 1.67 |
| Bonus perdus (case cochée avec un +1) (par joueur et par partie) | 0.15 | 0.18 | 0.15 |

## Vérification des critères 6 et 7

- **OK** — 2 joueurs : >= 1000 parties jouées
- **OK** — 2 joueurs : 100 % des parties terminées
- **OK** — 2 joueurs : durée 12 tours actifs x 1 min <= 20 min
- **OK** — 2 joueurs : remplissage jaune 68 % >= 30 %
- **OK** — 2 joueurs : remplissage vert 50 % >= 30 %
- **OK** — 2 joueurs : remplissage orange 47 % >= 30 %
- **OK** — 2 joueurs : remplissage violet 50 % >= 30 %
- **OK** — 2 joueurs : part du score jaune 24 % <= 40 %
- **OK** — 2 joueurs : part du score vert 19 % <= 40 %
- **OK** — 2 joueurs : part du score orange 26 % <= 40 %
- **OK** — 2 joueurs : part du score violet 31 % <= 40 %
- **OK** — 3 joueurs : >= 1000 parties jouées
- **OK** — 3 joueurs : 100 % des parties terminées
- **OK** — 3 joueurs : durée 15 tours actifs x 1 min <= 20 min
- **OK** — 3 joueurs : remplissage jaune 68 % >= 30 %
- **OK** — 3 joueurs : remplissage vert 58 % >= 30 %
- **OK** — 3 joueurs : remplissage orange 56 % >= 30 %
- **OK** — 3 joueurs : remplissage violet 49 % >= 30 %
- **OK** — 3 joueurs : part du score jaune 22 % <= 40 %
- **OK** — 3 joueurs : part du score vert 23 % <= 40 %
- **OK** — 3 joueurs : part du score orange 27 % <= 40 %
- **OK** — 3 joueurs : part du score violet 29 % <= 40 %
- **OK** — 4 joueurs : >= 1000 parties jouées
- **OK** — 4 joueurs : 100 % des parties terminées
- **OK** — 4 joueurs : durée 16 tours actifs x 1 min <= 20 min
- **OK** — 4 joueurs : remplissage jaune 64 % >= 30 %
- **OK** — 4 joueurs : remplissage vert 58 % >= 30 %
- **OK** — 4 joueurs : remplissage orange 59 % >= 30 %
- **OK** — 4 joueurs : remplissage violet 45 % >= 30 %
- **OK** — 4 joueurs : part du score jaune 20 % <= 40 %
- **OK** — 4 joueurs : part du score vert 24 % <= 40 %
- **OK** — 4 joueurs : part du score orange 29 % <= 40 %
- **OK** — 4 joueurs : part du score violet 27 % <= 40 %

**Bilan : OK partout.**
