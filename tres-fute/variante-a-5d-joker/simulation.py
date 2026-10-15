#!/usr/bin/env python3
"""Simulation de « Très futé junior », variante A (5 dés avec joker).

Implémente exactement les règles de regles.md :
- 5 dés : blanc (joker), jaune, vert, orange, violet ; 4 zones (pas de zone bleue).
- Joueur actif : jusqu'à 3 lancers, garde un dé à chaque fois ; les dés strictement
  plus petits vont sur le plateau d'argent ; après le dernier choix, les dés restants
  y vont aussi. Chaque autre joueur prend ensuite un dé du plateau.
- Fin de tour : chaque joueur peut barrer au plus un « +1 » pour utiliser un des
  5 dés posés sur la table ; une case cochée grâce à un +1 ne donne pas de bonus.
  Les 5 dés sont autorisés, y compris celui qu'on a déjà utilisé soi-même ce tour ;
  la règle de couleur s'applique (le blanc reste un joker).
- Relance : seulement le joueur actif, avant de choisir un dé, relance tous les dés
  qu'il vient de lancer ; plusieurs Relances de suite sont permises.
- Un bonus gagné pendant un tour sert dès ce tour ; une zone pleine n'accepte plus de dé.
- Manches : 2 joueurs = 6, 3 joueurs = 5, 4 joueurs = 4.
- Points jaunes : 1 point par case cochée + 10 points par colonne complète.

Deux stratégies sont simulées :
- « gloutonne » : le choix qui rapporte le plus de points immédiats ou de progrès ;
- « enfant » : jamais de Relance ; à chaque choix, un dé utilisable tiré au hasard
  (sinon un dé au hasard sans rien cocher), une case possible au hasard ; un +1 utilisé
  dès qu'un coup est possible, sur un coup tiré au hasard.

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
# Jaune : grille 3 x 4 (3 lignes, 4 colonnes). On coche une case qui porte exactement la valeur du dé.
JAUNE_GRILLE = [
    [1, 2, 3, 4],
    [5, 6, 1, 2],
    [3, 4, 5, 6],
]
JAUNE_BONUS_LIGNE = ["relance", "plus1", "relance"]  # ligne complète -> bonus
JAUNE_POINTS_COLONNE = [10, 10, 10, 10]                # colonne complète -> points
JAUNE_POINTS_CASE = 1                                  # chaque case cochée -> 1 point

# Vert : on coche de gauche à droite ; le dé doit être >= au nombre de la case.
VERT_SEUILS = [1, 2, 3, 4, 1, 2, 3, 5]
VERT_POINTS = [2, 4, 7, 11, 16, 22, 29, 37]  # points = nombre sous la dernière case
VERT_BONUS = {2: "relance", 5: "plus1"}               # index de case (0 = 1re case)

# Orange : on écrit la valeur du dé dans la case suivante ; points = somme.
ORANGE_CASES = 7
ORANGE_BONUS = {2: "relance", 4: "plus1", 6: "relance"}

# Violet : valeur strictement plus grande que la case précédente, sauf après un 6.
VIOLET_CASES = 8
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
        jaune = JAUNE_POINTS_CASE * sum(sum(l) for l in self.jaune)
        jaune += sum(JAUNE_POINTS_COLONNE[c] for c in range(nc)
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


ITERATIONS_MAX = 50   # garde-fou : nombre maximal d'itérations de boucle dans un tour


class TourTropLong(RuntimeError):
    pass


# ---------------------------------------------------------------- stratégies
class Gloutonne:
    nom = "gloutonne"
    description = ("le choix qui rapporte le plus de points immédiats ou de progrès, "
                   "Relance si le meilleur choix est faible, +1 si le coup vaut assez")

    def relancer(self, rng, joueur, des):
        best = joueur.meilleur(des)
        return best is None or best[0] < SEUIL_RELANCE

    def choix_actif(self, rng, joueur, des, nb_choisis):
        best = None
        for i, (coul, val) in enumerate(des):
            perdus = sum(1 for (_, v2) in des if v2 < val)
            cout = COUT_DE_PERDU * perdus if nb_choisis < 2 else 0.0
            options = joueur.coups(coul, val)
            e_de = max((joueur.evaluer(z, c, val) for z, c in options), default=-5.0)
            if best is None or e_de - cout > best[0]:
                best = (e_de - cout, i)
        i = best[1]
        coul, val = des[i]
        options = joueur.coups(coul, val)
        coup = max(options, key=lambda zc: joueur.evaluer(zc[0], zc[1], val)) if options else None
        return i, coup

    def choix_passif(self, rng, joueur, plateau):
        best = joueur.meilleur(plateau)
        if best is None:
            return None
        _, i, z, c = best
        return i, (z, c)

    def plus1(self, rng, joueur, table):
        best = joueur.meilleur(table, avec_bonus=False)
        if best is None or best[0] < SEUIL_PLUS1:
            return None
        _, i, z, c = best
        return i, (z, c)


class Enfant:
    nom = "enfant"
    description = ("jamais de Relance ; un dé utilisable au hasard (sinon un dé au hasard sans "
                   "rien cocher), une case possible au hasard ; +1 dès qu'un coup est possible, "
                   "sur un coup tiré au hasard")

    def relancer(self, rng, joueur, des):
        return False

    def _choix(self, rng, joueur, des):
        utiles = [i for i, (c, v) in enumerate(des) if joueur.coups(c, v)]
        if not utiles:
            return rng.randrange(len(des)), None
        i = rng.choice(utiles)
        return i, rng.choice(joueur.coups(*des[i]))

    def choix_actif(self, rng, joueur, des, nb_choisis):
        return self._choix(rng, joueur, des)

    def choix_passif(self, rng, joueur, plateau):
        i, coup = self._choix(rng, joueur, plateau)
        return (i, coup) if coup else None

    def plus1(self, rng, joueur, table):
        coups = [(i, zc) for i, (c, v) in enumerate(table) for zc in joueur.coups(c, v)]
        return rng.choice(coups) if coups else None


STRATEGIES = [Gloutonne(), Enfant()]


def tour(rng, feuilles, actif, strat):
    joueur = feuilles[actif]
    a_lancer = list(COULEURS)
    choisis = []      # dés gardés par le joueur actif
    plateau = []      # plateau d'argent
    iterations = 0
    # le joueur actif doit choisir un dé à chaque lancer, jusqu'à 3 choix
    # tant qu'il reste des dés à lancer
    while len(choisis) < 3 and a_lancer:
        iterations += 1
        if iterations > ITERATIONS_MAX:
            raise TourTropLong("trop d'itérations dans un tour")
        des = lancer(rng, a_lancer)
        # Relances éventuelles (joueur actif seulement), plusieurs de suite possibles
        while joueur.relances > 0 and strat.relancer(rng, joueur, des):
            iterations += 1
            if iterations > ITERATIONS_MAX:
                raise TourTropLong("trop d'itérations dans un tour")
            joueur.relances -= 1
            joueur.stats["relance_utilisee"] += 1
            des = lancer(rng, a_lancer)
        i, coup = strat.choix_actif(rng, joueur, des, len(choisis))
        coul, val = des[i]
        if coup:
            joueur.appliquer(coup[0], coup[1], val)
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
    # le plateau contient toujours au moins 2 dés (5 dés, au plus 3 choisis)
    assert len(plateau) >= 2 and len(choisis) + len(plateau) == len(COULEURS)
    # joueurs passifs : un dé du plateau
    for k, f in enumerate(feuilles):
        if k == actif:
            continue
        choix = strat.choix_passif(rng, f, plateau)
        if choix:
            i, (z, c) = choix
            f.appliquer(z, c, plateau[i][1])
    # fin du tour : au plus un +1 par joueur, sur n'importe lequel des 5 dés
    # (y compris un dé déjà utilisé soi-même pendant ce tour)
    table = choisis + plateau
    for f in feuilles:
        if f.plus1 > 0:
            choix = strat.plus1(rng, f, table)
            if choix:
                f.plus1 -= 1
                f.stats["plus1_utilise"] += 1
                i, (z, c) = choix
                f.appliquer(z, c, table[i][1], avec_bonus=False)


def partie(rng, n, strat):
    """Joue une partie ; renvoie les feuilles et le nombre de tours de joueur actif joués."""
    feuilles = [Feuille() for _ in range(n)]
    tours = 0
    for _ in range(MANCHES[n]):
        for actif in range(n):
            tour(rng, feuilles, actif, strat)
            tours += 1
    return feuilles, tours


def moyenne(xs):
    return sum(xs) / len(xs) if xs else 0.0


def simuler(strat):
    rng = random.Random(GRAINE)
    resultats = {}
    for n in (2, 3, 4):
        scores, finies, tours = [], 0, []
        remp = {z: [] for z in ZONES}
        part = {z: [] for z in ZONES}
        pts = {z: [] for z in ZONES}
        jaune_zero = []
        jaune_sans_colonne = []
        bstats = {k: [] for k in ["relance_gagnee", "relance_utilisee",
                                  "plus1_gagne", "plus1_utilise", "bonus_perdu"]}
        for _ in range(PARTIES):
            feuilles, t = partie(rng, n, strat)
            finies += (t == MANCHES[n] * n)
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
                jaune_zero.append(s["jaune"] == 0)
                jaune_sans_colonne.append(
                    not any(all(f.jaune[r][c] for r in range(len(JAUNE_GRILLE)))
                            for c in range(len(JAUNE_GRILLE[0]))))
                for k in bstats:
                    bstats[k].append(f.stats[k])
        resultats[n] = {
            "score_moy": moyenne(scores),
            "score_et": statistics.pstdev(scores),
            "score_min": min(scores), "score_max": max(scores),
            "pct_finies": 100.0 * finies / PARTIES,
            "tours": moyenne(tours), "tours_min": min(tours), "tours_max": max(tours),
            "remp": {z: moyenne(remp[z]) for z in ZONES},
            "pts": {z: moyenne(pts[z]) for z in ZONES},
            "part": {z: moyenne(part[z]) for z in ZONES},
            "jaune_zero": 100.0 * moyenne(jaune_zero),
            "jaune_sans_colonne": 100.0 * moyenne(jaune_sans_colonne),
            "bonus": {k: moyenne(v) for k, v in bstats.items()},
        }
    return resultats


def verifier(res):
    lignes = []
    tout_ok = True
    for n, r in res.items():
        tests = [
            (f"{n} joueurs : {PARTIES} parties jouées (>= 1000)", PARTIES >= 1000),
            (f"{n} joueurs : {r['pct_finies']:.0f} % des parties terminées avec exactement "
             f"{MANCHES[n]} x {n} = {MANCHES[n] * n} tours actifs", r["pct_finies"] == 100.0),
            (f"{n} joueurs : {r['tours_max']} tours actifs (critère : x 1 min <= 20)",
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


def rapport(tous):
    o = []
    o.append("# Résultats de simulation — variante A (5 dés avec joker)\n")
    o.append(f"Généré par `simulation.py` (graine {GRAINE}, {PARTIES} parties par nombre de joueurs "
             "et par stratégie). Deux stratégies :\n")
    for strat, _, _, _ in tous:
        o.append(f"- **{strat.nom}** : {strat.description}.")
    o.append("\n**Fin de partie.** La fin est garantie par construction : le nombre de manches est "
             "fixe (6, 5 ou 4) et un tour de joueur actif compte au plus 3 choix de dé (plus les "
             "Relances, limitées par les bonus gagnés). La simulation le contrôle : elle compte les "
             "tours de joueur actif réellement joués dans chaque partie et vérifie qu'ils valent "
             f"manches × joueurs ; un garde-fou lève une erreur si un tour dépasse {ITERATIONS_MAX} "
             "itérations de boucle (jamais déclenché).\n")
    o.append("**Durée.** La ligne « tours actifs » compte les tours de joueur actif ; le critère "
             "les convertit à raison de 1 min par tour (≤ 20). Ce n'est pas une durée mesurée : "
             "les règles annoncent 20 à 30 minutes réelles avec des enfants de 6-7 ans.\n")
    bilan = True
    for strat, res, tout_ok, lignes in tous:
        bilan &= tout_ok
        o.append(f"## Stratégie {strat.nom}\n")
        o.append("| | 2 joueurs | 3 joueurs | 4 joueurs |")
        o.append("|---|---|---|---|")

        def ligne(nom, f):
            o.append(f"| {nom} | " + " | ".join(f(res[n], n) for n in (2, 3, 4)) + " |")
        ligne("Manches", lambda r, n: str(MANCHES[n]))
        ligne("Score moyen (écart-type)", lambda r, n: f"{r['score_moy']:.1f} ({r['score_et']:.1f})")
        ligne("Score min / max", lambda r, n: f"{r['score_min']} / {r['score_max']}")
        ligne("Parties terminées (tours actifs = manches × joueurs)",
              lambda r, n: f"{r['pct_finies']:.0f} %")
        ligne("Tours actifs (critère : × 1 min ≤ 20)", lambda r, n: f"{r['tours_max']}")
        for z in ZONES:
            ligne(f"Remplissage {z}", lambda r, n, z=z: f"{100*r['remp'][z]:.0f} %")
        for z in ZONES:
            ligne(f"Points {z} (part du score)",
                  lambda r, n, z=z: f"{r['pts'][z]:.1f} ({100*r['part'][z]:.0f} %)")
        ligne("Feuilles à 0 point en jaune", lambda r, n: f"{r['jaune_zero']:.1f} %")
        ligne("Feuilles sans aucune colonne jaune complète (0 point de colonne)",
              lambda r, n: f"{r['jaune_sans_colonne']:.1f} %")
        noms = {"relance_gagnee": "Relances gagnées", "relance_utilisee": "Relances utilisées",
                "plus1_gagne": "+1 gagnés", "plus1_utilise": "+1 utilisés",
                "bonus_perdu": "Bonus perdus (case remplie avec un +1)"}
        for k, nom in noms.items():
            ligne(f"{nom} (par joueur et par partie)", lambda r, n, k=k: f"{r['bonus'][k]:.2f}")
        o.append(f"\n### Vérification des critères 6 et 7 — stratégie {strat.nom}\n")
        for etat, nom in lignes:
            o.append(f"- **{etat}** — {nom}")
        o.append(f"\n**Bilan {strat.nom} : {'OK partout' if tout_ok else 'au moins un ÉCHEC'}.**\n")
    o.append("## Bilan général\n")
    o.append(f"**{'OK partout, pour les deux stratégies' if bilan else 'au moins un ÉCHEC'}.**\n")
    return "\n".join(o)


def main():
    tous = []
    for strat in STRATEGIES:
        res = simuler(strat)
        tout_ok, lignes = verifier(res)
        tous.append((strat, res, tout_ok, lignes))
    texte = rapport(tous)
    print(texte)
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats-simulation.md")
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(texte)


if __name__ == "__main__":
    main()
