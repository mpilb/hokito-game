# Résultats de simulation — variante C (6 dés avec joker)

Les « tours actifs » sont comptés réellement, feuille par feuille, pendant la simulation. La fin de chaque partie est garantie par construction (nombre de manches fixe, au plus 3 choix par tour) ; le contrôle « parties terminées » vérifie que chaque joueur a bien été joueur actif exactement « manches » fois, et un garde-fou (MAX_ITER) lèverait une erreur en cas de boucle. La « durée » du critère 6 est exprimée en tours actifs (× 1 min ≤ 20) : ce n'est pas une durée mesurée ; avec des enfants de 6-7 ans, comptez plutôt 20 à 30 minutes.

# Stratégie gloutonne

Graine 20261015, 2000 parties par nombre de joueurs, stratégie gloutonne (meilleur gain immédiat ou progrès, moins le coût des dés envoyés sur le plateau d'argent ; relances et +1 utilisés quand ils servent).

## Résumé par nombre de joueurs

| Joueurs | Manches | Score moyen | Écart-type | Parties terminées | Tours actifs (moy / max) | Tours actifs (critère : × 1 min ≤ 20) |
|---|---|---|---|---|---|---|
| 2 | 6 | 88.0 | 8.7 | 100 % | 12 / 12 | 12 |
| 3 | 5 | 90.5 | 9.4 | 100 % | 15 / 15 | 15 |
| 4 | 4 | 85.9 | 9.2 | 100 % | 16 / 16 | 16 |

## Par zone (remplissage moyen / points moyens / part moyenne du score)

| Joueurs | Jaune | Bleu | Vert | Orange | Violet |
|---|---|---|---|---|---|
| 2 | 77 % / 25.1 pts / 29 % | 59 % / 13.8 pts / 16 % | 58 % / 15.0 pts / 17 % | 42 % / 14.2 pts / 16 % | 55 % / 19.8 pts / 22 % |
| 3 | 76 % / 24.5 pts / 27 % | 61 % / 14.4 pts / 16 % | 61 % / 16.1 pts / 18 % | 48 % / 15.6 pts / 17 % | 56 % / 19.9 pts / 22 % |
| 4 | 73 % / 22.6 pts / 26 % | 59 % / 13.8 pts / 16 % | 60 % / 15.6 pts / 18 % | 48 % / 15.2 pts / 17 % | 54 % / 18.8 pts / 22 % |

## Feuilles à 0 point en jaune (jaune : 1 point par case cochée + 10 par rangée pleine)

| Joueurs | 2 | 3 | 4 |
|---|---|---|---|
| Part de feuilles à 0 point en jaune | 0.00 % | 0.00 % | 0.00 % |

## Bonus (moyenne par joueur et par partie)

| Joueurs | Relances gagnées | Relances utilisées | +1 gagnés | +1 utilisés | Bonus non pris (dé du +1) | Dés pris sans rien cocher (actif) |
|---|---|---|---|---|---|---|
| 2 | 2.82 (+1 au départ) | 3.30 | 2.96 | 2.95 | 0.31 | 0.47 |
| 3 | 2.94 (+1 au départ) | 3.22 | 3.07 | 3.06 | 0.33 | 0.42 |
| 4 | 2.81 (+1 au départ) | 2.83 | 2.97 | 2.96 | 0.34 | 0.29 |

## Vérification des critères

- OK — C6 2 joueurs : ≥ 1 000 parties (2000)
- OK — C6 2 joueurs : toutes les parties se terminent (tours actifs comptés = manches × joueurs) (100 %)
- OK — C6 2 joueurs : chaque zone ≥ 30 % remplie (min 42.1 %)
- OK — C6 2 joueurs : tours actifs × 1 min ≤ 20 (12 tours actifs)
- OK — C7 2 joueurs : aucune zone > 40 % du score (max 28.5 %)
- OK — C6 3 joueurs : ≥ 1 000 parties (2000)
- OK — C6 3 joueurs : toutes les parties se terminent (tours actifs comptés = manches × joueurs) (100 %)
- OK — C6 3 joueurs : chaque zone ≥ 30 % remplie (min 48.1 %)
- OK — C6 3 joueurs : tours actifs × 1 min ≤ 20 (15 tours actifs)
- OK — C7 3 joueurs : aucune zone > 40 % du score (max 27.1 %)
- OK — C6 4 joueurs : ≥ 1 000 parties (2000)
- OK — C6 4 joueurs : toutes les parties se terminent (tours actifs comptés = manches × joueurs) (100 %)
- OK — C6 4 joueurs : chaque zone ≥ 30 % remplie (min 47.7 %)
- OK — C6 4 joueurs : tours actifs × 1 min ≤ 20 (16 tours actifs)
- OK — C7 4 joueurs : aucune zone > 40 % du score (max 26.3 %)

**Bilan glouton : OK partout**

# Stratégie « enfant »

Graine 20261015, 2000 parties par nombre de joueurs, stratégie « enfant » (aucune relance ; un dé au hasard parmi ceux qui servent, placement au hasard ; +1 utilisé sur un coup possible tiré au hasard).

## Résumé par nombre de joueurs

| Joueurs | Manches | Score moyen | Écart-type | Parties terminées | Tours actifs (moy / max) | Tours actifs (critère : × 1 min ≤ 20) |
|---|---|---|---|---|---|---|
| 2 | 6 | 59.7 | 8.9 | 100 % | 12 / 12 | 12 |
| 3 | 5 | 64.5 | 9.1 | 100 % | 15 / 15 | 15 |
| 4 | 4 | 62.4 | 8.6 | 100 % | 16 / 16 | 16 |

## Par zone (remplissage moyen / points moyens / part moyenne du score)

| Joueurs | Jaune | Bleu | Vert | Orange | Violet |
|---|---|---|---|---|---|
| 2 | 53 % / 9.0 pts / 15 % | 46 % / 9.6 pts / 16 % | 48 % / 11.9 pts / 20 % | 74 % / 17.9 pts / 30 % | 36 % / 11.2 pts / 19 % |
| 3 | 57 % / 10.8 pts / 16 % | 50 % / 10.8 pts / 17 % | 51 % / 12.8 pts / 20 % | 83 % / 18.9 pts / 29 % | 37 % / 11.2 pts / 17 % |
| 4 | 56 % / 10.6 pts / 17 % | 49 % / 10.6 pts / 17 % | 49 % / 12.3 pts / 20 % | 83 % / 18.1 pts / 29 % | 36 % / 10.7 pts / 17 % |

## Feuilles à 0 point en jaune (jaune : 1 point par case cochée + 10 par rangée pleine)

| Joueurs | 2 | 3 | 4 |
|---|---|---|---|
| Part de feuilles à 0 point en jaune | 0.03 % | 0.00 % | 0.01 % |

## Bonus (moyenne par joueur et par partie)

| Joueurs | Relances gagnées | Relances utilisées | +1 gagnés | +1 utilisés | Bonus non pris (dé du +1) | Dés pris sans rien cocher (actif) |
|---|---|---|---|---|---|---|
| 2 | 2.17 (+1 au départ) | 0.00 | 1.98 | 1.97 | 0.38 | 0.67 |
| 3 | 2.30 (+1 au départ) | 0.00 | 2.29 | 2.28 | 0.44 | 0.65 |
| 4 | 2.25 (+1 au départ) | 0.00 | 2.25 | 2.24 | 0.43 | 0.51 |

## Vérification des critères

- OK — C6 2 joueurs : ≥ 1 000 parties (2000)
- OK — C6 2 joueurs : toutes les parties se terminent (tours actifs comptés = manches × joueurs) (100 %)
- OK — C6 2 joueurs : chaque zone ≥ 30 % remplie (min 36.2 %)
- OK — C6 2 joueurs : tours actifs × 1 min ≤ 20 (12 tours actifs)
- OK — C7 2 joueurs : aucune zone > 40 % du score (max 30.0 %)
- OK — C6 3 joueurs : ≥ 1 000 parties (2000)
- OK — C6 3 joueurs : toutes les parties se terminent (tours actifs comptés = manches × joueurs) (100 %)
- OK — C6 3 joueurs : chaque zone ≥ 30 % remplie (min 37.3 %)
- OK — C6 3 joueurs : tours actifs × 1 min ≤ 20 (15 tours actifs)
- OK — C7 3 joueurs : aucune zone > 40 % du score (max 29.4 %)
- OK — C6 4 joueurs : ≥ 1 000 parties (2000)
- OK — C6 4 joueurs : toutes les parties se terminent (tours actifs comptés = manches × joueurs) (100 %)
- OK — C6 4 joueurs : chaque zone ≥ 30 % remplie (min 36.1 %)
- OK — C6 4 joueurs : tours actifs × 1 min ≤ 20 (16 tours actifs)
- OK — C7 4 joueurs : aucune zone > 40 % du score (max 29.2 %)

**Bilan enfant : OK partout**

**Bilan général : OK partout (les deux stratégies)**
