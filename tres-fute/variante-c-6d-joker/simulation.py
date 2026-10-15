#!/usr/bin/env python3
"""Simulation de « Très futé — variante C : 6 dés avec joker » (version 6-7 ans).

Implémente exactement les règles de regles.md :
- 6 dés : blanc (joker), jaune, bleu, vert, orange, violet.
- Joueur actif : jusqu'à 3 lancers, garde 1 dé à chaque fois ; les dés plus petits
  (strictement) que le dé gardé vont sur le plateau d'argent ; après le 3e choix,
  tous les dés restants vont sur le plateau d'argent.
- Puis chaque autre joueur prend 1 dé du plateau d'argent (plusieurs joueurs
  peuvent prendre le même).
- Puis chaque joueur peut utiliser au plus un « +1 » : il prend n'importe lequel
  des 6 dés. Un dé pris avec un +1 ne rapporte jamais de bonus (pas de chaîne).
- Relance : seul le joueur actif, juste après un lancer, relance tous les dés
  qu'il vient de lancer.
- Manches : 6 à 2 joueurs, 5 à 3 joueurs, 4 à 4 joueurs.

Stratégie gloutonne (choix légaux uniquement) : la règle permet plusieurs relances
de suite ; la stratégie simulée en utilise au plus une par lancer.

Python 3 sans dépendance. Graine fixe. Écrit resultats-simulation.md à côté.
"""
import random
import statistics
import os

GRAINE = 20261015
PARTIES = 2000

# ------------------------------------------------------------------ règles ---
MANCHES = {2: 6, 3: 5, 4: 4}
RELANCES_DE_DEPART = 1

COULEURS = ["blanc", "jaune", "bleu", "vert", "orange", "violet"]
ZONES = ["jaune", "bleu", "vert", "orange", "violet"]

# Jaune : 3 rangées de 3 nombres ; on coche une case portant la valeur du dé.
JAUNE_GRILLE = [[1, 2, 3], [4, 5, 6], [2, 4, 6]]
JAUNE_POINTS_RANGEE = [10, 10, 10]       # rangée complète
JAUNE_BONUS = {(0, 2): "R", (2, 1): "P"}

# Bleu : somme dé bleu + dé blanc ; on coche la case de cette somme.
BLEU_CASES = [(2, 3), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11, 12)]
BLEU_POINTS = [0, 2, 4, 6, 9, 12, 16, 20, 25, 30]  # selon le nombre de cases cochées
BLEU_BONUS = {0: "P", 8: "R"}

# Vert : de gauche à droite, le dé doit être au moins égal au nombre de la case.
VERT_SEUILS = [1, 2, 3, 4, 2, 3, 4, 5]
VERT_POINTS = [0, 3, 6, 9, 12, 16, 20, 24, 28]
VERT_BONUS = {3: "R", 6: "P"}

# Orange : de gauche à droite, on écrit la valeur du dé.
ORANGE_N = 8
ORANGE_BONUS = {2: "R", 5: "P"}

# Violet : de gauche à droite, chaque nombre plus grand que le précédent ;
# après un 6, on peut écrire n'importe quel nombre.
VIOLET_N = 8
VIOLET_BONUS = {2: "P", 5: "R"}

TAILLE_ZONE = {
    "jaune": sum(len(r) for r in JAUNE_GRILLE),
    "bleu": len(BLEU_CASES),
    "vert": len(VERT_SEUILS),
    "orange": ORANGE_N,
    "violet": VIOLET_N,
}

# ------------------------------------------------------ stratégie gloutonne ---
VAL_BONUS = {"R": 2.5, "P": 3.5}
COUT_DE_PERDU = 1.0      # par dé envoyé sur le plateau (choix 1 et 2 du joueur actif)
SEUIL_RELANCE = 3.0
SEUIL_PLUS1 = 4.0


class Feuille:
    def __init__(self):
        self.jaune = [[False] * len(r) for r in JAUNE_GRILLE]
        self.bleu = [False] * len(BLEU_CASES)
        self.vert = 0
        self.orange = []
        self.violet = []
        self.relances = RELANCES_DE_DEPART
        self.plus1 = 0
        self.stats = {"R_gagnes": 0, "P_gagnes": 0, "R_utilises": 0,
                      "P_utilises": 0, "bonus_perdus_chaine": 0, "des_inutiles": 0}

    # -------- coups possibles pour un dé (couleur, valeur) --------
    def coups(self, couleur, valeur, valeurs):
        """Liste de (zone, case, valeur_ecrite) jouables avec ce dé."""
        zones = ZONES if couleur == "blanc" else [couleur]
        res = []
        for z in zones:
            if z == "jaune":
                for r, rang in enumerate(JAUNE_GRILLE):
                    for c, n in enumerate(rang):
                        if n == valeur and not self.jaune[r][c]:
                            res.append(("jaune", (r, c), valeur))
            elif z == "bleu":
                s = valeurs["bleu"] + valeurs["blanc"]
                for i, cas in enumerate(BLEU_CASES):
                    if s in cas and not self.bleu[i]:
                        res.append(("bleu", i, s))
            elif z == "vert":
                if self.vert < len(VERT_SEUILS) and valeur >= VERT_SEUILS[self.vert]:
                    res.append(("vert", self.vert, valeur))
            elif z == "orange":
                if len(self.orange) < ORANGE_N:
                    res.append(("orange", len(self.orange), valeur))
            elif z == "violet":
                if len(self.violet) < VIOLET_N:
                    der = self.violet[-1] if self.violet else None
                    if der is None or der == 6 or valeur > der:
                        res.append(("violet", len(self.violet), valeur))
        return res

    def bonus_de(self, coup):
        z, case, _ = coup
        table = {"jaune": JAUNE_BONUS, "bleu": BLEU_BONUS, "vert": VERT_BONUS,
                 "orange": ORANGE_BONUS, "violet": VIOLET_BONUS}[z]
        return table.get(case)

    def evaluer(self, coup, par_plus1=False):
        z, case, v = coup
        val = 0.0
        if z == "jaune":
            r, c = case
            deja = sum(self.jaune[r])
            pts = JAUNE_POINTS_RANGEE[r]
            val = pts / 3 * (1 + 0.5 * deja)
        elif z == "bleu":
            n = sum(self.bleu)
            val = BLEU_POINTS[n + 1] - BLEU_POINTS[n] + 1.0
        elif z == "vert":
            n = self.vert
            val = VERT_POINTS[n + 1] - VERT_POINTS[n] - 0.3 * (v - VERT_SEUILS[n]) + 0.5
        elif z == "orange":
            val = v - 1.5
        elif z == "violet":
            der = self.violet[-1] if self.violet else 0
            if der == 6:
                der = 0
            val = v if v == 6 else v - 0.8 * (v - der - 1)
        b = self.bonus_de(coup)
        if b and not par_plus1:
            val += VAL_BONUS[b]
        return val

    def jouer(self, coup, par_plus1=False):
        z, case, v = coup
        if z == "jaune":
            r, c = case
            self.jaune[r][c] = True
        elif z == "bleu":
            self.bleu[case] = True
        elif z == "vert":
            self.vert += 1
        elif z == "orange":
            self.orange.append(v)
        elif z == "violet":
            self.violet.append(v)
        b = self.bonus_de(coup)
        if b:
            if par_plus1:
                self.stats["bonus_perdus_chaine"] += 1
            elif b == "R":
                self.relances += 1
                self.stats["R_gagnes"] += 1
            else:
                self.plus1 += 1
                self.stats["P_gagnes"] += 1

    def meilleur_coup(self, des, valeurs, par_plus1=False):
        """des : liste de couleurs. Renvoie (valeur, couleur, coup) ou None."""
        best = None
        for coul in des:
            for cp in self.coups(coul, valeurs[coul], valeurs):
                e = self.evaluer(cp, par_plus1)
                if best is None or e > best[0]:
                    best = (e, coul, cp)
        return best

    # -------- décompte --------
    def scores(self):
        j = sum(JAUNE_POINTS_RANGEE[r] for r in range(len(JAUNE_GRILLE)) if all(self.jaune[r]))
        return {
            "jaune": j,
            "bleu": BLEU_POINTS[sum(self.bleu)],
            "vert": VERT_POINTS[self.vert],
            "orange": sum(self.orange),
            "violet": sum(self.violet),
        }

    def remplissage(self):
        return {
            "jaune": sum(sum(r) for r in self.jaune) / TAILLE_ZONE["jaune"],
            "bleu": sum(self.bleu) / TAILLE_ZONE["bleu"],
            "vert": self.vert / TAILLE_ZONE["vert"],
            "orange": len(self.orange) / TAILLE_ZONE["orange"],
            "violet": len(self.violet) / TAILLE_ZONE["violet"],
        }


def tour_actif(rng, f, valeurs):
    """Joue le tour du joueur actif. Renvoie la liste des couleurs sur le plateau d'argent."""
    plateau_lancer = list(COULEURS)
    argent = []
    for choix in range(3):
        if not plateau_lancer:
            break
        for c in plateau_lancer:
            valeurs[c] = rng.randint(1, 6)

        def note(couleur):
            perdus = sum(1 for d in plateau_lancer if d != couleur and valeurs[d] < valeurs[couleur])
            cps = f.coups(couleur, valeurs[couleur], valeurs)
            base = max((f.evaluer(cp) for cp in cps), default=-1.0)
            cout = COUT_DE_PERDU * perdus if choix < 2 else 0.0
            best_cp = max(cps, key=f.evaluer) if cps else None
            return base - cout, best_cp

        def meilleur():
            return max(((note(c), c) for c in plateau_lancer), key=lambda x: x[0][0])

        (score, cp), coul = meilleur()
        if score < SEUIL_RELANCE and f.relances > 0:
            f.relances -= 1
            f.stats["R_utilises"] += 1
            for c in plateau_lancer:
                valeurs[c] = rng.randint(1, 6)
            (score, cp), coul = meilleur()
        # le joueur garde le dé choisi
        plateau_lancer.remove(coul)
        petits = [d for d in plateau_lancer if valeurs[d] < valeurs[coul]]
        for d in petits:
            plateau_lancer.remove(d)
            argent.append(d)
        if cp is not None:
            f.jouer(cp)
        else:
            f.stats["des_inutiles"] += 1
    argent.extend(plateau_lancer)  # après le 3e choix, le reste va sur le plateau
    return argent


def partie(rng, nb):
    feuilles = [Feuille() for _ in range(nb)]
    valeurs = {c: 1 for c in COULEURS}
    tours = 0
    m = MANCHES[nb]
    for manche in range(m):
        for a in range(nb):
            tours += 1
            argent = tour_actif(rng, feuilles[a], valeurs)
            for p in range(nb):
                if p == a:
                    continue
                best = feuilles[p].meilleur_coup(argent, valeurs)
                if best is not None and best[0] > 0:
                    feuilles[p].jouer(best[2])
            dernier = (manche == m - 1 and a == nb - 1)
            for p in range(nb):
                f = feuilles[p]
                if f.plus1 > 0:
                    best = f.meilleur_coup(COULEURS, valeurs, par_plus1=True)
                    if best is not None and (best[0] >= SEUIL_PLUS1 or (manche == m - 1 and best[0] > 0) or dernier):
                        f.plus1 -= 1
                        f.stats["P_utilises"] += 1
                        f.jouer(best[2], par_plus1=True)
    terminee = tours == m * nb
    return feuilles, tours, terminee


def simuler(nb, rng):
    totaux, tours_l, fini = [], [], 0
    zs = {z: [] for z in ZONES}
    remp = {z: [] for z in ZONES}
    parts = {z: [] for z in ZONES}
    st = {}
    for _ in range(PARTIES):
        feuilles, tours, ok = partie(rng, nb)
        fini += ok
        tours_l.append(tours)
        for f in feuilles:
            s = f.scores()
            t = sum(s.values())
            totaux.append(t)
            r = f.remplissage()
            for z in ZONES:
                zs[z].append(s[z])
                remp[z].append(r[z])
                parts[z].append(s[z] / t if t else 0)
            for k, v in f.stats.items():
                st.setdefault(k, []).append(v)
    somme_tot = sum(totaux)
    return {
        "nb": nb,
        "moy": statistics.mean(totaux),
        "et": statistics.pstdev(totaux),
        "fini": fini / PARTIES,
        "tours": statistics.mean(tours_l),
        "tours_max": max(tours_l),
        "zone_moy": {z: statistics.mean(zs[z]) for z in ZONES},
        "remp": {z: statistics.mean(remp[z]) for z in ZONES},
        "part": {z: statistics.mean(parts[z]) for z in ZONES},
        "part_glob": {z: sum(zs[z]) / somme_tot for z in ZONES},
        "stats": {k: statistics.mean(v) for k, v in st.items()},
    }


def main():
    rng = random.Random(GRAINE)
    resultats = [simuler(nb, rng) for nb in (2, 3, 4)]
    L = []
    L.append("# Résultats de simulation — variante C (6 dés avec joker)\n")
    L.append(f"Graine {GRAINE}, {PARTIES} parties par nombre de joueurs, stratégie gloutonne "
             "(meilleur gain immédiat ou progrès, moins le coût des dés envoyés sur le plateau d'argent).\n")
    L.append("## Résumé par nombre de joueurs\n")
    L.append("| Joueurs | Manches | Score moyen | Écart-type | Parties terminées | Tours actifs (moy / max) | Durée estimée |")
    L.append("|---|---|---|---|---|---|---|")
    for r in resultats:
        L.append(f"| {r['nb']} | {MANCHES[r['nb']]} | {r['moy']:.1f} | {r['et']:.1f} | {100*r['fini']:.0f} % "
                 f"| {r['tours']:.0f} / {r['tours_max']} | {r['tours_max']} min |")
    L.append("\n## Par zone (remplissage moyen / points moyens / part moyenne du score)\n")
    L.append("| Joueurs | " + " | ".join(z.capitalize() for z in ZONES) + " |")
    L.append("|---|" + "---|" * len(ZONES))
    for r in resultats:
        cells = [f"{100*r['remp'][z]:.0f} % / {r['zone_moy'][z]:.1f} pts / {100*r['part'][z]:.0f} %" for z in ZONES]
        L.append(f"| {r['nb']} | " + " | ".join(cells) + " |")
    L.append("\n## Bonus (moyenne par joueur et par partie)\n")
    L.append("| Joueurs | Relances gagnées | Relances utilisées | +1 gagnés | +1 utilisés | Bonus non pris (dé du +1) | Dés pris sans rien cocher (actif) |")
    L.append("|---|---|---|---|---|---|---|")
    for r in resultats:
        s = r["stats"]
        L.append(f"| {r['nb']} | {s['R_gagnes']:.2f} (+{RELANCES_DE_DEPART} au départ) | {s['R_utilises']:.2f} | "
                 f"{s['P_gagnes']:.2f} | {s['P_utilises']:.2f} | {s['bonus_perdus_chaine']:.2f} | {s['des_inutiles']:.2f} |")

    L.append("\n## Vérification des critères\n")
    tout_ok = True
    for r in resultats:
        nb = r["nb"]
        checks = [
            (f"C6 {nb} joueurs : ≥ 1 000 parties", PARTIES >= 1000, f"{PARTIES}"),
            (f"C6 {nb} joueurs : toutes les parties se terminent", r["fini"] == 1.0, f"{100*r['fini']:.0f} %"),
            (f"C6 {nb} joueurs : chaque zone ≥ 30 % remplie",
             min(r["remp"].values()) >= 0.30, f"min {100*min(r['remp'].values()):.0f} %"),
            (f"C6 {nb} joueurs : durée ≤ 20 min", r["tours_max"] <= 20, f"{r['tours_max']} tours actifs"),
            (f"C7 {nb} joueurs : aucune zone > 40 % du score",
             max(max(r["part"].values()), max(r["part_glob"].values())) <= 0.40,
             f"max {100*max(max(r['part'].values()), max(r['part_glob'].values())):.1f} %"),
        ]
        for nom, ok, det in checks:
            tout_ok &= ok
            L.append(f"- {'OK' if ok else 'ÉCHEC'} — {nom} ({det})")
    L.append(f"\n**Bilan : {'OK partout' if tout_ok else 'au moins un ÉCHEC'}**\n")
    texte = "\n".join(L)
    print(texte)
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats-simulation.md")
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(texte)


if __name__ == "__main__":
    main()
