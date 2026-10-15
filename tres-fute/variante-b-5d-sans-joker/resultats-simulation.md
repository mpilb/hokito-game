# Résultats de simulation – variante B (5 dés sans joker)

Graine 20261015 (la même pour les deux stratégies), 2000 parties par nombre de joueurs et par stratégie. Généré par `simulation.py`.

- **Gloutonne** : le joueur choisit le dé et la case qui rapportent le plus (points immédiats + progrès), utilise ses relances et ses +1 à bon escient.
- **Enfant** : aucune relance n'est jamais utilisée ; à chaque lancer (joueur actif) ou sur le plateau d'argent (joueur passif), on choisit au hasard un dé qui peut remplir au moins une case, puis au hasard une case possible ; si aucun dé ne peut servir, le joueur actif prend un dé au hasard sans rien cocher. Le +1 est utilisé en fin de tour dès qu'un coup est possible (dé, puis case, tirés au hasard).

**Fin de partie.** Chaque partie se termine par construction : le nombre de manches est fixe et chaque tour de joueur actif contient au plus 3 choix. La simulation le contrôle quand même : elle compte les tours de joueur actif réellement joués dans chaque partie et vérifie qu'ils valent manches × joueurs ; un garde-fou (au plus 100 itérations dans la boucle de relances d'un lancer) lève une erreur s'il est dépassé.

**Durée.** Le critère utilise « tours de joueur actif × 1 min ≤ 20 ». Ce n'est pas une durée mesurée : avec des enfants de 6-7 ans, comptez plutôt 20 à 30 minutes (voir `regles.md`).

# Stratégie gloutonne

## gloutonne – 2 joueurs (6 manches)

- Score moyen : 61.5 (écart-type 10.7)
- Parties terminées (tours actifs comptés = manches × joueurs) : 100 %
- Tours de joueur actif par partie : 12 (critère : × 1 min = 12 ≤ 20)

| Zone | Cases | Remplissage moyen | Points moyens | Part moyenne du score |
|------|------:|------------------:|--------------:|----------------------:|
| jaune | 12 | 55 % | 14.8 | 24 % |
| bleu | 10 | 50 % | 15.0 | 24 % |
| vert | 10 | 39 % | 10.5 | 17 % |
| orange | 8 | 36 % | 10.9 | 18 % |
| violet | 7 | 37 % | 10.3 | 17 % |

Bonus par joueur et par partie : relances gagnées 1.47, utilisées 0.86 ; +1 gagnés 1.35, utilisés 1.34 ; bonus non gagnés (case remplie par un +1) 0.21.

## gloutonne – 3 joueurs (5 manches)

- Score moyen : 66.2 (écart-type 11.3)
- Parties terminées (tours actifs comptés = manches × joueurs) : 100 %
- Tours de joueur actif par partie : 15 (critère : × 1 min = 15 ≤ 20)

| Zone | Cases | Remplissage moyen | Points moyens | Part moyenne du score |
|------|------:|------------------:|--------------:|----------------------:|
| jaune | 12 | 51 % | 13.2 | 20 % |
| bleu | 10 | 57 % | 18.3 | 27 % |
| vert | 10 | 42 % | 11.4 | 18 % |
| orange | 8 | 44 % | 12.7 | 19 % |
| violet | 7 | 40 % | 10.6 | 16 % |

Bonus par joueur et par partie : relances gagnées 1.71, utilisées 0.95 ; +1 gagnés 1.63, utilisés 1.62 ; bonus non gagnés (case remplie par un +1) 0.24.

## gloutonne – 4 joueurs (4 manches)

- Score moyen : 62.9 (écart-type 10.9)
- Parties terminées (tours actifs comptés = manches × joueurs) : 100 %
- Tours de joueur actif par partie : 16 (critère : × 1 min = 16 ≤ 20)

| Zone | Cases | Remplissage moyen | Points moyens | Part moyenne du score |
|------|------:|------------------:|--------------:|----------------------:|
| jaune | 12 | 45 % | 10.3 | 16 % |
| bleu | 10 | 58 % | 18.5 | 29 % |
| vert | 10 | 40 % | 10.8 | 17 % |
| orange | 8 | 46 % | 13.1 | 21 % |
| violet | 7 | 40 % | 10.2 | 16 % |

Bonus par joueur et par partie : relances gagnées 1.72, utilisées 0.82 ; +1 gagnés 1.62, utilisés 1.61 ; bonus non gagnés (case remplie par un +1) 0.24.

# Stratégie enfant

## enfant – 2 joueurs (6 manches)

- Score moyen : 52.7 (écart-type 8.7)
- Parties terminées (tours actifs comptés = manches × joueurs) : 100 %
- Tours de joueur actif par partie : 12 (critère : × 1 min = 12 ≤ 20)

| Zone | Cases | Remplissage moyen | Points moyens | Part moyenne du score |
|------|------:|------------------:|--------------:|----------------------:|
| jaune | 12 | 39 % | 6.5 | 12 % |
| bleu | 10 | 41 % | 10.9 | 21 % |
| vert | 10 | 34 % | 8.5 | 16 % |
| orange | 8 | 64 % | 16.1 | 31 % |
| violet | 7 | 40 % | 10.8 | 20 % |

Bonus par joueur et par partie : relances gagnées 1.57, utilisées 0.00 ; +1 gagnés 1.24, utilisés 1.23 ; bonus non gagnés (case remplie par un +1) 0.22.

## enfant – 3 joueurs (5 manches)

- Score moyen : 56.7 (écart-type 9.3)
- Parties terminées (tours actifs comptés = manches × joueurs) : 100 %
- Tours de joueur actif par partie : 15 (critère : × 1 min = 15 ≤ 20)

| Zone | Cases | Remplissage moyen | Points moyens | Part moyenne du score |
|------|------:|------------------:|--------------:|----------------------:|
| jaune | 12 | 43 % | 7.4 | 13 % |
| bleu | 10 | 46 % | 13.1 | 23 % |
| vert | 10 | 35 % | 8.9 | 16 % |
| orange | 8 | 70 % | 16.6 | 29 % |
| violet | 7 | 41 % | 10.7 | 19 % |

Bonus par joueur et par partie : relances gagnées 1.72, utilisées 0.00 ; +1 gagnés 1.50, utilisés 1.48 ; bonus non gagnés (case remplie par un +1) 0.27.

## enfant – 4 joueurs (4 manches)

- Score moyen : 54.3 (écart-type 9.0)
- Parties terminées (tours actifs comptés = manches × joueurs) : 100 %
- Tours de joueur actif par partie : 16 (critère : × 1 min = 16 ≤ 20)

| Zone | Cases | Remplissage moyen | Points moyens | Part moyenne du score |
|------|------:|------------------:|--------------:|----------------------:|
| jaune | 12 | 42 % | 7.1 | 13 % |
| bleu | 10 | 47 % | 13.2 | 24 % |
| vert | 10 | 34 % | 8.4 | 16 % |
| orange | 8 | 68 % | 15.6 | 29 % |
| violet | 7 | 39 % | 10.1 | 18 % |

Bonus par joueur et par partie : relances gagnées 1.71, utilisées 0.00 ; +1 gagnés 1.38, utilisés 1.37 ; bonus non gagnés (case remplie par un +1) 0.25.

# Vérification des critères 6 et 7

## Stratégie gloutonne

- OK — 2 j. – toutes les parties se terminent (100 %)
- OK — 2 j. – remplissage jaune ≥ 30 % (55.2 %)
- OK — 2 j. – remplissage bleu ≥ 30 % (49.7 %)
- OK — 2 j. – remplissage vert ≥ 30 % (39.1 %)
- OK — 2 j. – remplissage orange ≥ 30 % (36.0 %)
- OK — 2 j. – remplissage violet ≥ 30 % (36.6 %)
- OK — 2 j. – tours actifs × 1 min ≤ 20 (12)
- OK — 2 j. – part jaune ≤ 40 % (23.9 %)
- OK — 2 j. – part bleu ≤ 40 % (24.0 %)
- OK — 2 j. – part vert ≤ 40 % (17.4 %)
- OK — 2 j. – part orange ≤ 40 % (17.9 %)
- OK — 2 j. – part violet ≤ 40 % (16.8 %)
- OK — 3 j. – toutes les parties se terminent (100 %)
- OK — 3 j. – remplissage jaune ≥ 30 % (51.2 %)
- OK — 3 j. – remplissage bleu ≥ 30 % (57.4 %)
- OK — 3 j. – remplissage vert ≥ 30 % (41.5 %)
- OK — 3 j. – remplissage orange ≥ 30 % (44.0 %)
- OK — 3 j. – remplissage violet ≥ 30 % (39.7 %)
- OK — 3 j. – tours actifs × 1 min ≤ 20 (15)
- OK — 3 j. – part jaune ≤ 40 % (19.7 %)
- OK — 3 j. – part bleu ≤ 40 % (27.2 %)
- OK — 3 j. – part vert ≤ 40 % (17.6 %)
- OK — 3 j. – part orange ≤ 40 % (19.4 %)
- OK — 3 j. – part violet ≤ 40 % (16.1 %)
- OK — 4 j. – toutes les parties se terminent (100 %)
- OK — 4 j. – remplissage jaune ≥ 30 % (44.7 %)
- OK — 4 j. – remplissage bleu ≥ 30 % (58.2 %)
- OK — 4 j. – remplissage vert ≥ 30 % (40.1 %)
- OK — 4 j. – remplissage orange ≥ 30 % (46.5 %)
- OK — 4 j. – remplissage violet ≥ 30 % (39.6 %)
- OK — 4 j. – tours actifs × 1 min ≤ 20 (16)
- OK — 4 j. – part jaune ≤ 40 % (16.2 %)
- OK — 4 j. – part bleu ≤ 40 % (28.9 %)
- OK — 4 j. – part vert ≤ 40 % (17.5 %)
- OK — 4 j. – part orange ≤ 40 % (21.1 %)
- OK — 4 j. – part violet ≤ 40 % (16.3 %)

**Bilan gloutonne : OK partout**

## Stratégie enfant

- OK — 2 j. – toutes les parties se terminent (100 %)
- OK — 2 j. – remplissage jaune ≥ 30 % (39.4 %)
- OK — 2 j. – remplissage bleu ≥ 30 % (40.8 %)
- OK — 2 j. – remplissage vert ≥ 30 % (33.9 %)
- OK — 2 j. – remplissage orange ≥ 30 % (63.5 %)
- OK — 2 j. – remplissage violet ≥ 30 % (39.8 %)
- OK — 2 j. – tours actifs × 1 min ≤ 20 (12)
- OK — 2 j. – part jaune ≤ 40 % (12.3 %)
- OK — 2 j. – part bleu ≤ 40 % (20.6 %)
- OK — 2 j. – part vert ≤ 40 % (16.2 %)
- OK — 2 j. – part orange ≤ 40 % (30.6 %)
- OK — 2 j. – part violet ≤ 40 % (20.3 %)
- OK — 3 j. – toutes les parties se terminent (100 %)
- OK — 3 j. – remplissage jaune ≥ 30 % (42.8 %)
- OK — 3 j. – remplissage bleu ≥ 30 % (46.4 %)
- OK — 3 j. – remplissage vert ≥ 30 % (35.2 %)
- OK — 3 j. – remplissage orange ≥ 30 % (69.7 %)
- OK — 3 j. – remplissage violet ≥ 30 % (40.7 %)
- OK — 3 j. – tours actifs × 1 min ≤ 20 (15)
- OK — 3 j. – part jaune ≤ 40 % (13.0 %)
- OK — 3 j. – part bleu ≤ 40 % (22.9 %)
- OK — 3 j. – part vert ≤ 40 % (15.8 %)
- OK — 3 j. – part orange ≤ 40 % (29.5 %)
- OK — 3 j. – part violet ≤ 40 % (18.8 %)
- OK — 4 j. – toutes les parties se terminent (100 %)
- OK — 4 j. – remplissage jaune ≥ 30 % (42.0 %)
- OK — 4 j. – remplissage bleu ≥ 30 % (46.6 %)
- OK — 4 j. – remplissage vert ≥ 30 % (33.8 %)
- OK — 4 j. – remplissage orange ≥ 30 % (67.9 %)
- OK — 4 j. – remplissage violet ≥ 30 % (39.1 %)
- OK — 4 j. – tours actifs × 1 min ≤ 20 (16)
- OK — 4 j. – part jaune ≤ 40 % (13.1 %)
- OK — 4 j. – part bleu ≤ 40 % (24.0 %)
- OK — 4 j. – part vert ≤ 40 % (15.7 %)
- OK — 4 j. – part orange ≤ 40 % (28.8 %)
- OK — 4 j. – part violet ≤ 40 % (18.4 %)

**Bilan enfant : OK partout**

## Marges (valeurs les plus proches des seuils)

| Stratégie | Remplissage minimum (toutes zones, 2/3/4 j.) | Part maximale (toutes zones, 2/3/4 j.) |
|-----------|-----------------------------------------------|-----------------------------------------|
| gloutonne | 36.0 % (orange, 2 j.) | 28.9 % (bleu, 4 j.) |
| enfant | 33.8 % (vert, 4 j.) | 30.6 % (orange, 2 j.) |

**Bilan général : OK partout**
