#!/usr/bin/env python3
"""Simulation de « Très futé junior — variante C : 6 dés avec joker » (version 6-7 ans).

Implémente les règles de regles.md :
- 6 dés : blanc (joker), jaune, bleu, vert, orange, violet.
- Joueur actif : jusqu'à 3 lancers, garde 1 dé à chaque lancer (il ne peut pas s'arrêter
  avant) ; les dés plus petits (strictement) que le dé gardé vont sur le plateau d'argent ;
  après le 3e choix, tous les dés restants vont sur le plateau d'argent.
- Puis chaque autre joueur prend 1 dé du plateau d'argent (plusieurs joueurs
  peuvent prendre le même) ou aucun s'il ne peut rien en faire.
- Puis chaque joueur peut utiliser au plus un « +1 » : il prend n'importe lequel
  des 6 dés (même un dé déjà utilisé). Un dé pris avec un +1 ne rapporte jamais de
  bonus (pas de chaîne). Un +1 gagné pendant ce tour est utilisable à la fin du même tour.
- Relance : seul le joueur actif, juste après un lancer, relance tous les dés
  qu'il vient de lancer ; plusieurs relances de suite sont permises ; une relance gagnée
  pendant le tour est utilisable dès le lancer suivant.
- Zone bleue : somme du dé bleu et du dé blanc tels qu'ils sont posés au moment où
  l'on coche (une relance ultérieure ne change rien à ce qui est déjà coché).
- Manches : 6 à 2 joueurs, 5 à 3 joueurs, 4 à 4 joueurs.

Deux stratégies, toutes deux limitées aux choix légaux :
- « gloutonne » : meilleur gain immédiat ou progrès, moins le coût des dés envoyés
  sur le plateau ; relance (autant de fois qu'il faut, tant qu'il en reste) si le meilleur
  coup vaut moins que SEUIL_RELANCE ; +1 utilisé si le coup en vaut la peine.
- « enfant » : jamais de relance ; à chaque choix (joueur actif sur ses dés lancés,
  joueur passif sur le plateau d'argent), un dé est tiré au hasard parmi ceux qui
  permettent au moins un coup, puis un placement au hasard parmi ses placements possibles
  (pour le joker : toutes zones confondues) ; si aucun dé ne sert, le joueur actif prend un
  dé au hasard sans rien cocher, le joueur passif ne prend rien ; en fin de tour, un +1
  disponible est utilisé sur un coup tiré au hasard parmi tous les coups possibles
  (dé, placement) des 6 dés, s'il en existe un.

Contrôle « toutes les parties se terminent » : la fin est garantie par construction
(nombre de manches fixe, chaque tour de joueur actif a au plus 3 choix) ; on la contrôle
en comptant réellement les tours de joueur actif joués par chaque feuille (il doit y en avoir
exactement « manches » par joueur) et grâce à un garde-fou (MAX_ITER) qui lève une erreur.

Python 3 sans dépendance. Graine fixe. Écrit resultats-simulation.md à côté.
"""
import random
import statistics
import os

GRAINE = 20261015
PARTIES = 2000
MAX_ITER = 200          # garde-fou : nombre maximal d'itérations dans un tour

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
        self.tours_actifs = 0     # tours de joueur actif réellement joués par cette feuille

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


def choix_enfant(rng, f, des, valeurs):
    """Stratégie enfant : un dé au hasard parmi ceux qui servent, puis un placement
    au hasard. Renvoie (couleur, coup) ou None si aucun dé ne peut servir."""
    utiles = []
    for coul in des:
        cps = f.coups(coul, valeurs[coul], valeurs)
        if cps:
            utiles.append((coul, cps))
    if not utiles:
        return None
    coul, cps = rng.choice(utiles)
    return coul, rng.choice(cps)


def tour_actif(rng, f, valeurs, strat):
    """Joue le tour du joueur actif. Renvoie la liste des couleurs sur le plateau d'argent."""
    f.tours_actifs += 1
    a_lancer = list(COULEURS)
    gardes = []
    argent = []
    for choix in range(3):
        if not a_lancer:
            break
        for c in a_lancer:
            valeurs[c] = rng.randint(1, 6)

        if strat == "enfant":
            res = choix_enfant(rng, f, a_lancer, valeurs)
            if res is None:
                coul, cp = rng.choice(a_lancer), None
            else:
                coul, cp = res
        else:
            def note(couleur):
                perdus = sum(1 for d in a_lancer if d != couleur and valeurs[d] < valeurs[couleur])
                cps = f.coups(couleur, valeurs[couleur], valeurs)
                base = max((f.evaluer(cp) for cp in cps), default=-1.0)
                cout = COUT_DE_PERDU * perdus if choix < 2 else 0.0
                best_cp = max(cps, key=f.evaluer) if cps else None
                return base - cout, best_cp

            def meilleur():
                return max(((note(c), c) for c in a_lancer), key=lambda x: x[0][0])

            (score, cp), coul = meilleur()
            iterations = 0
            # plusieurs relances de suite possibles, tant qu'il en reste et que le coup est mauvais
            while score < SEUIL_RELANCE and f.relances > 0:
                iterations += 1
                if iterations > MAX_ITER:
                    raise RuntimeError("garde-fou : trop de relances dans un lancer")
                f.relances -= 1
                f.stats["R_utilises"] += 1
                for c in a_lancer:
                    valeurs[c] = rng.randint(1, 6)
                (score, cp), coul = meilleur()
        # le joueur garde le dé choisi (obligatoire : il ne peut pas s'arrêter)
        a_lancer.remove(coul)
        gardes.append(coul)
        petits = [d for d in a_lancer if valeurs[d] < valeurs[coul]]
        for d in petits:
            a_lancer.remove(d)
            argent.append(d)
        if cp is not None:
            f.jouer(cp)
        else:
            f.stats["des_inutiles"] += 1
    argent.extend(a_lancer)  # après le 3e choix, le reste va sur le plateau
    # contrôles de cohérence du tour
    if sorted(gardes + argent) != sorted(COULEURS):
        raise RuntimeError("tour incohérent : les 6 dés ne sont pas tous répartis")
    if not (len(gardes) == 3 or (len(gardes) < 3 and not a_lancer)):
        raise RuntimeError("tour incohérent : moins de 3 choix alors qu'il restait des dés")
    return argent


def tour_passif(rng, f, argent, valeurs, strat):
    """Un joueur autre que l'actif prend (ou non) un dé du plateau d'argent."""
    if strat == "enfant":
        res = choix_enfant(rng, f, argent, valeurs)
        if res is not None:
            f.jouer(res[1])
    else:
        best = f.meilleur_coup(argent, valeurs)
        if best is not None and best[0] > 0:
            f.jouer(best[2])


def fin_de_tour_plus1(rng, f, valeurs, strat, manche, m, dernier):
    """Utilisation éventuelle d'un +1 (un seul par tour) : n'importe lequel des 6 dés."""
    if f.plus1 <= 0:
        return
    if strat == "enfant":
        tous = [(c, cp) for c in COULEURS for cp in f.coups(c, valeurs[c], valeurs)]
        if not tous:
            return
        choix = rng.choice(tous)[1]
    else:
        best = f.meilleur_coup(COULEURS, valeurs, par_plus1=True)
        if best is None or not (best[0] >= SEUIL_PLUS1 or (manche == m - 1 and best[0] > 0) or dernier):
            return
        choix = best[2]
    f.plus1 -= 1
    f.stats["P_utilises"] += 1
    f.jouer(choix, par_plus1=True)


def partie(rng, nb, strat):
    feuilles = [Feuille() for _ in range(nb)]
    valeurs = {c: 1 for c in COULEURS}
    tours = 0
    m = MANCHES[nb]
    for manche in range(m):
        for a in range(nb):
            tours += 1
            if tours > m * nb:
                raise RuntimeError("garde-fou : plus de tours que prévu")
            argent = tour_actif(rng, feuilles[a], valeurs, strat)
            for p in range(nb):
                if p != a:
                    tour_passif(rng, feuilles[p], argent, valeurs, strat)
            dernier = (manche == m - 1 and a == nb - 1)
            for p in range(nb):
                fin_de_tour_plus1(rng, feuilles[p], valeurs, strat, manche, m, dernier)
    # comptage réel : chaque feuille doit avoir été joueur actif exactement « m » fois
    tours_comptes = sum(f.tours_actifs for f in feuilles)
    terminee = tours_comptes == m * nb and all(f.tours_actifs == m for f in feuilles)
    return feuilles, tours_comptes, terminee


def simuler(nb, rng, strat):
    totaux, tours_l, fini = [], [], 0
    zs = {z: [] for z in ZONES}
    remp = {z: [] for z in ZONES}
    parts = {z: [] for z in ZONES}
    st = {}
    for _ in range(PARTIES):
        feuilles, tours, ok = partie(rng, nb, strat)
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


NOM_STRAT = {
    "glouton": "stratégie gloutonne (meilleur gain immédiat ou progrès, moins le coût des dés "
               "envoyés sur le plateau d'argent ; relances et +1 utilisés quand ils servent)",
    "enfant": "stratégie « enfant » (aucune relance ; un dé au hasard parmi ceux qui servent, "
              "placement au hasard ; +1 utilisé sur un coup possible tiré au hasard)",
}


def section(strat, resultats, L):
    """Ajoute à L la présentation d'une stratégie. Renvoie True si tous les seuils sont OK."""
    titre = "Stratégie gloutonne" if strat == "glouton" else "Stratégie « enfant »"
    L.append(f"# {titre}\n")
    L.append(f"Graine {GRAINE}, {PARTIES} parties par nombre de joueurs, {NOM_STRAT[strat]}.\n")
    L.append("## Résumé par nombre de joueurs\n")
    L.append("| Joueurs | Manches | Score moyen | Écart-type | Parties terminées | Tours actifs (moy / max) | Tours actifs (critère : × 1 min ≤ 20) |")
    L.append("|---|---|---|---|---|---|---|")
    for r in resultats:
        L.append(f"| {r['nb']} | {MANCHES[r['nb']]} | {r['moy']:.1f} | {r['et']:.1f} | {100*r['fini']:.0f} % "
                 f"| {r['tours']:.0f} / {r['tours_max']} | {r['tours_max']} |")
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
        pmax = max(max(r["part"].values()), max(r["part_glob"].values()))
        checks = [
            (f"C6 {nb} joueurs : ≥ 1 000 parties", PARTIES >= 1000, f"{PARTIES}"),
            (f"C6 {nb} joueurs : toutes les parties se terminent (tours actifs comptés = manches × joueurs)",
             r["fini"] == 1.0, f"{100*r['fini']:.0f} %"),
            (f"C6 {nb} joueurs : chaque zone ≥ 30 % remplie",
             min(r["remp"].values()) >= 0.30, f"min {100*min(r['remp'].values()):.1f} %"),
            (f"C6 {nb} joueurs : tours actifs × 1 min ≤ 20", r["tours_max"] <= 20, f"{r['tours_max']} tours actifs"),
            (f"C7 {nb} joueurs : aucune zone > 40 % du score", pmax <= 0.40, f"max {100*pmax:.1f} %"),
        ]
        for nom, ok, det in checks:
            tout_ok &= ok
            L.append(f"- {'OK' if ok else 'ÉCHEC'} — {nom} ({det})")
    L.append(f"\n**Bilan {strat} : {'OK partout' if tout_ok else 'au moins un ÉCHEC'}**\n")
    return tout_ok


def main():
    L = ["# Résultats de simulation — variante C (6 dés avec joker)\n"]
    L.append("Les « tours actifs » sont comptés réellement, feuille par feuille, pendant la simulation. "
             "La fin de chaque partie est garantie par construction (nombre de manches fixe, au plus "
             "3 choix par tour) ; le contrôle « parties terminées » vérifie que chaque joueur a bien été "
             "joueur actif exactement « manches » fois, et un garde-fou (MAX_ITER) lèverait une erreur "
             "en cas de boucle. La « durée » du critère 6 est exprimée en tours actifs (× 1 min ≤ 20) : "
             "ce n'est pas une durée mesurée ; avec des enfants de 6-7 ans, comptez plutôt 20 à 30 minutes.\n")
    bilans = {}
    for strat in ("glouton", "enfant"):
        rng = random.Random(GRAINE)
        resultats = [simuler(nb, rng, strat) for nb in (2, 3, 4)]
        bilans[strat] = section(strat, resultats, L)
    L.append(f"**Bilan général : {'OK partout (les deux stratégies)' if all(bilans.values()) else 'au moins un ÉCHEC'}**\n")
    texte = "\n".join(L)
    print(texte)
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats-simulation.md")
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(texte)


if __name__ == "__main__":
    main()
