#!/usr/bin/env python3
"""Simulation de « Très futé junior », variante A (5 dés avec joker).

Implémente exactement les règles de regles.md :
- 5 dés : blanc (joker), jaune, vert, orange, violet ; 4 zones (pas de zone bleue).
- Joueur actif : jusqu'à 3 lancers, garde un dé à chaque fois ; les dés strictement
  plus petits vont sur le plateau d'argent ; après le dernier choix, les dés restants
  y vont aussi. Chaque autre joueur prend ensuite un dé du plateau.
- Fin de tour : chaque joueur peut barrer au plus un « +1 » pour utiliser un des
  5 dés posés sur la table ; une case cochée grâce à un +1 ne donne pas de bonus.
- Relance : seulement le joueur actif, avant de choisir un dé, relance tous les dés
  qu'il vient de lancer.
- Manches : 2 joueurs = 6, 3 joueurs = 5, 4 joueurs = 4.

Python 3 sans dépendance externe, graine fixe. Écrit resultats-simulation.md.
"""
import os
import random
import statistics

GRAINE = 20261015
PARTIES = 1000
MANCHES = {2: 6, 3: 5, 4: 4}
COULEURS = ["blanc", "jaune", "vert", "orange", "violet"]
ZONES = ["jaune", "vert", "orange", "violet"]

# ---------------------------------------------------------------- feuillet
# Jaune : grille 3 x 3. On coche une case qui porte exactement la valeur du dé.
JAUNE_GRILLE = [
    [1, 2, 3, 4],
    [5, 6, 1, 2],
    [3, 4, 5, 6],
]
JAUNE_BONUS_LIGNE = ["relance", "plus1", "relance"]  # ligne complète -> bonus
JAUNE_POINTS_COLONNE = [10, 10, 10, 10]                # colonne complète -> points

# Vert : on coche de gauche à droite ; le dé doit être >= au nombre de la case.
VERT_SEUILS = [1, 2, 3, 4, 1, 2, 3, 5]
VERT_POINTS = [2, 4, 7, 11, 16, 22, 29, 37]  # points = nombre sous la dernière case
VERT_BONUS = {2: "relance", 5: "plus1"}               # index de case (0 = 1re case)

# Orange : on écrit la valeur du dé dans la case suivante ; points = somme.
ORANGE_CASES = 10
ORANGE_BONUS = {2: "relance", 5: "plus1", 8: "relance"}

# Violet : valeur strictement plus grande que la case précédente, sauf après un 6.
VIOLET_CASES = 10
VIOLET_BONUS = {3: "plus1", 6: "relance"}

# Valeurs utilisées par la stratégie gloutonne (pas par les règles).
VAL_BONUS = {"relance": 2.0, "plus1": 4.0}
COUT_DE_PERDU = 1.2   # pénalité par dé envoyé sur le plateau (joueur actif)
SEUIL_RELANCE = 3.0   # on relance si le meilleur choix vaut moins que ça
SEUIL_PLUS1 = 3.0     # on utilise un +1 si le meilleur choix vaut au moins ça


def nb_sources(bonus):
    n = JAUNE_BONUS_LIGNE.count(bonus)
    n += list(VERT_BONUS.values()).count(bonus)
    n += list(ORANGE_BONUS.values()).count(bonus)
    n += list(VIOLET_BONUS.values()).count(bonus)
    return n


TOTAL_CASES = {
    "jaune": sum(len(l) for l in JAUNE_GRILLE),
    "vert": len(VERT_SEUILS),
    "orange": ORANGE_CASES,
    "violet": VIOLET_CASES,
}


class Feuille:
    def __init__(self):
        self.jaune = [[False] * len(l) for l in JAUNE_GRILLE]
        self.vert = 0
        self.orange = []
        self.violet = []
        self.relances = 0       # disponibles (cercles coloriés non barrés)
        self.plus1 = 0
        self.stats = {"relance_gagnee": 0, "relance_utilisee": 0,
                      "plus1_gagne": 0, "plus1_utilise": 0, "bonus_perdu": 0}

    # ---- coups légaux pour un dé : liste de (zone, case)
    def coups(self, couleur, valeur):
        zones = ZONES if couleur == "blanc" else [couleur]
        res = []
        for z in zones:
            if z == "jaune":
                for r, ligne in enumerate(JAUNE_GRILLE):
                    for c, v in enumerate(ligne):
                        if v == valeur and not self.jaune[r][c]:
                            res.append(("jaune", (r, c)))
            elif z == "vert":
                if self.vert < len(VERT_SEUILS) and valeur >= VERT_SEUILS[self.vert]:
                    res.append(("vert", self.vert))
            elif z == "orange":
                if len(self.orange) < ORANGE_CASES:
                    res.append(("orange", len(self.orange)))
            elif z == "violet":
                if len(self.violet) < VIOLET_CASES:
                    prec = self.violet[-1] if self.violet else None
                    if prec is None or prec == 6 or valeur > prec:
                        res.append(("violet", len(self.violet)))
        return res

    # ---- bonus déclenché par un coup (sans l'appliquer)
    def bonus_du_coup(self, zone, case):
        if zone == "jaune":
            r, c = case
            if all(self.jaune[r][cc] or cc == c for cc in range(len(JAUNE_GRILLE[r]))):
                return JAUNE_BONUS_LIGNE[r]
            return None
        if zone == "vert":
            return VERT_BONUS.get(case)
        if zone == "orange":
            return ORANGE_BONUS.get(case)
        return VIOLET_BONUS.get(case)

    # ---- évaluation gloutonne : points immédiats + progrès + bonus
    def evaluer(self, zone, case, valeur, avec_bonus=True):
        v = 0.0
        if zone == "jaune":
            r, c = case
            col_pleine = all(self.jaune[rr][c] or rr == r for rr in range(len(JAUNE_GRILLE)))
            v += 3.0 + (JAUNE_POINTS_COLONNE[c] if col_pleine else 0)
        elif zone == "vert":
            prec = VERT_POINTS[case - 1] if case > 0 else 0
            v += VERT_POINTS[case] - prec
            v -= 0.7 * (valeur - VERT_SEUILS[case])
        elif zone == "orange":
            v += valeur - 1.5
        else:
            prec = self.violet[-1] if self.violet else 0
            if prec == 6:
                prec = 0
            v += valeur
            if valeur < 6:
                v -= 0.8 * (valeur - prec - 1)
        b = self.bonus_du_coup(zone, case)
        if b and avec_bonus:
            v += VAL_BONUS[b]
        return v

    def meilleur(self, des, avec_bonus=True):
        """des : liste de (couleur, valeur). Renvoie (eval, index_de, zone, case)."""
        best = None
        for i, (coul, val) in enumerate(des):
            for zone, case in self.coups(coul, val):
                e = self.evaluer(zone, case, val, avec_bonus)
                if best is None or e > best[0]:
                    best = (e, i, zone, case)
        return best

    def appliquer(self, zone, case, valeur, avec_bonus=True):
        b = self.bonus_du_coup(zone, case)
        if zone == "jaune":
            r, c = case
            self.jaune[r][c] = True
        elif zone == "vert":
            self.vert += 1
        elif zone == "orange":
            self.orange.append(valeur)
        else:
            self.violet.append(valeur)
        if b:
            if not avec_bonus:
                self.stats["bonus_perdu"] += 1
            elif b == "relance":
                self.relances += 1
                self.stats["relance_gagnee"] += 1
            else:
                self.plus1 += 1
                self.stats["plus1_gagne"] += 1

    # ---- décompte final (fait par l'adulte)
    def scores(self):
        nl, nc = len(JAUNE_GRILLE), len(JAUNE_GRILLE[0])
        jaune = sum(JAUNE_POINTS_COLONNE[c] for c in range(nc)
                    if all(self.jaune[r][c] for r in range(nl)))
        vert = VERT_POINTS[self.vert - 1] if self.vert else 0
        return {"jaune": jaune, "vert": vert,
                "orange": sum(self.orange), "violet": sum(self.violet)}

    def remplissage(self):
        return {
            "jaune": sum(sum(l) for l in self.jaune) / TOTAL_CASES["jaune"],
            "vert": self.vert / TOTAL_CASES["vert"],
            "orange": len(self.orange) / TOTAL_CASES["orange"],
            "violet": len(self.violet) / TOTAL_CASES["violet"],
        }


def lancer(rng, couleurs):
    return [(c, rng.randint(1, 6)) for c in couleurs]


def tour(rng, feuilles, actif):
    joueur = feuilles[actif]
    a_lancer = list(COULEURS)
    choisis = []      # dés gardés par le joueur actif
    plateau = []      # plateau d'argent
    while len(choisis) < 3 and a_lancer:
        des = lancer(rng, a_lancer)
        # relance éventuelle (joueur actif seulement), autant qu'il veut
        while joueur.relances > 0:
            best = joueur.meilleur(des)
            if best is not None and best[0] >= SEUIL_RELANCE:
                break
            joueur.relances -= 1
            joueur.stats["relance_utilisee"] += 1
            des = lancer(rng, a_lancer)
        # choix glouton d'un dé, en tenant compte des dés perdus vers le plateau
        best = None
        for i, (coul, val) in enumerate(des):
            perdus = sum(1 for (_, v2) in des if v2 < val)
            cout = COUT_DE_PERDU * perdus if len(choisis) < 2 else 0.0
            options = joueur.coups(coul, val)
            e_de = max((joueur.evaluer(z, c, val) for z, c in options), default=-5.0)
            if best is None or e_de - cout > best[0]:
                best = (e_de - cout, i)
        i = best[1]
        coul, val = des[i]
        options = joueur.coups(coul, val)
        if options:
            z, c = max(options, key=lambda zc: joueur.evaluer(zc[0], zc[1], val))
            joueur.appliquer(z, c, val)
        choisis.append(des[i])
        restants = []
        for j, (c2, v2) in enumerate(des):
            if j == i:
                continue
            if v2 < val:
                plateau.append((c2, v2))
            else:
                restants.append((c2, v2))
        a_lancer = [c2 for (c2, _) in restants]
        if len(choisis) == 3:
            plateau.extend(restants)
    # joueurs passifs : un dé du plateau
    for k, f in enumerate(feuilles):
        if k == actif:
            continue
        best = f.meilleur(plateau)
        if best is not None:
            _, i, z, c = best
            f.appliquer(z, c, plateau[i][1])
    # fin du tour : au plus un +1 par joueur, sur n'importe lequel des 5 dés
    table = choisis + plateau
    for f in feuilles:
        if f.plus1 > 0:
            best = f.meilleur(table, avec_bonus=False)
            if best is not None and best[0] >= SEUIL_PLUS1:
                f.plus1 -= 1
                f.stats["plus1_utilise"] += 1
                _, i, z, c = best
                f.appliquer(z, c, table[i][1], avec_bonus=False)


def partie(rng, n):
    feuilles = [Feuille() for _ in range(n)]
    tours = 0
    garde = 0
    for _ in range(MANCHES[n]):
        for actif in range(n):
            tour(rng, feuilles, actif)
            tours += 1
            garde += 1
            if garde > 1000:      # garde-fou : ne doit jamais arriver
                return feuilles, tours, False
    return feuilles, tours, True


def moyenne(xs):
    return sum(xs) / len(xs) if xs else 0.0


def simuler():
    rng = random.Random(GRAINE)
    resultats = {}
    for n in (2, 3, 4):
        scores, finies, tours = [], 0, []
        remp = {z: [] for z in ZONES}
        part = {z: [] for z in ZONES}
        pts = {z: [] for z in ZONES}
        bstats = {k: [] for k in ["relance_gagnee", "relance_utilisee",
                                  "plus1_gagne", "plus1_utilise", "bonus_perdu"]}
        for _ in range(PARTIES):
            feuilles, t, ok = partie(rng, n)
            finies += ok
            tours.append(t)
            for f in feuilles:
                s = f.scores()
                total = sum(s.values())
                scores.append(total)
                r = f.remplissage()
                for z in ZONES:
                    remp[z].append(r[z])
                    pts[z].append(s[z])
                    part[z].append(s[z] / total if total else 0.0)
                for k in bstats:
                    bstats[k].append(f.stats[k])
        resultats[n] = {
            "score_moy": moyenne(scores),
            "score_et": statistics.pstdev(scores),
            "score_min": min(scores), "score_max": max(scores),
            "pct_finies": 100.0 * finies / PARTIES,
            "tours": moyenne(tours), "tours_max": max(tours),
            "remp": {z: moyenne(remp[z]) for z in ZONES},
            "pts": {z: moyenne(pts[z]) for z in ZONES},
            "part": {z: moyenne(part[z]) for z in ZONES},
            "bonus": {k: moyenne(v) for k, v in bstats.items()},
        }
    return resultats


def verifier(res):
    lignes = []
    tout_ok = True
    for n, r in res.items():
        tests = [
            (f"{n} joueurs : >= 1000 parties jouées", PARTIES >= 1000),
            (f"{n} joueurs : 100 % des parties terminées", r["pct_finies"] == 100.0),
            (f"{n} joueurs : durée {r['tours_max']} tours actifs x 1 min <= 20 min",
             r["tours_max"] <= 20),
        ]
        for z in ZONES:
            tests.append((f"{n} joueurs : remplissage {z} {100*r['remp'][z]:.0f} % >= 30 %",
                          r["remp"][z] >= 0.30))
        for z in ZONES:
            tests.append((f"{n} joueurs : part du score {z} {100*r['part'][z]:.0f} % <= 40 %",
                          r["part"][z] <= 0.40))
        for nom, ok in tests:
            tout_ok &= ok
            lignes.append(("OK" if ok else "ÉCHEC", nom))
    return tout_ok, lignes


def rapport(res, tout_ok, lignes):
    o = []
    o.append("# Résultats de simulation — variante A (5 dés avec joker)\n")
    o.append(f"Généré par `simulation.py` (graine {GRAINE}, {PARTIES} parties par nombre de joueurs, "
             "stratégie gloutonne : le choix qui rapporte le plus de points immédiats ou de progrès).\n")
    o.append("## Synthèse\n")
    o.append("| | 2 joueurs | 3 joueurs | 4 joueurs |")
    o.append("|---|---|---|---|")
    def ligne(nom, f):
        o.append(f"| {nom} | " + " | ".join(f(res[n]) for n in (2, 3, 4)) + " |")
    ligne("Manches", lambda r: "")
    o[-1] = "| Manches | " + " | ".join(str(MANCHES[n]) for n in (2, 3, 4)) + " |"
    ligne("Score moyen (écart-type)", lambda r: f"{r['score_moy']:.1f} ({r['score_et']:.1f})")
    ligne("Score min / max", lambda r: f"{r['score_min']} / {r['score_max']}")
    ligne("Parties terminées", lambda r: f"{r['pct_finies']:.0f} %")
    ligne("Tours de joueur actif (= minutes estimées)", lambda r: f"{r['tours']:.0f}")
    for z in ZONES:
        ligne(f"Remplissage {z}", lambda r, z=z: f"{100*r['remp'][z]:.0f} %")
    for z in ZONES:
        ligne(f"Points {z} (part du score)",
              lambda r, z=z: f"{r['pts'][z]:.1f} ({100*r['part'][z]:.0f} %)")
    noms = {"relance_gagnee": "Relances gagnées", "relance_utilisee": "Relances utilisées",
            "plus1_gagne": "+1 gagnés", "plus1_utilise": "+1 utilisés",
            "bonus_perdu": "Bonus perdus (case cochée avec un +1)"}
    for k, nom in noms.items():
        ligne(f"{nom} (par joueur et par partie)", lambda r, k=k: f"{r['bonus'][k]:.2f}")
    o.append("\n## Vérification des critères 6 et 7\n")
    for etat, nom in lignes:
        o.append(f"- **{etat}** — {nom}")
    o.append(f"\n**Bilan : {'OK partout' if tout_ok else 'au moins un ÉCHEC'}.**\n")
    return "\n".join(o)


def main():
    res = simuler()
    tout_ok, lignes = verifier(res)
    texte = rapport(res, tout_ok, lignes)
    print(texte)
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats-simulation.md")
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(texte)


if __name__ == "__main__":
    main()
