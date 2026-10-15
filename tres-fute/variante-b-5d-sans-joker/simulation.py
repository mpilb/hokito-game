#!/usr/bin/env python3
"""Simulation de « Très futé – Petits futés », variante B (5 dés de couleur, sans joker).

Implémente exactement les règles de regles.md :
- 5 dés : jaune, bleu, vert, orange, violet. Chaque dé ne sert que dans la zone de sa couleur.
- Joueur actif : jusqu'à 3 choix. Après chaque choix, les dés strictement plus petits
  vont sur le plateau d'argent ; après le 3e choix, les dés restants y vont aussi.
- Joueurs passifs : chacun prend un dé du plateau d'argent (ou passe).
- Bonus : relance (joueur actif, après un lancer) et +1 (fin de tour, n'importe quel dé,
  un seul +1 par joueur et par tour). Une case remplie grâce à un +1 ne donne pas de bonus.
- Manches : 2 joueurs -> 6, 3 joueurs -> 5, 4 joueurs -> 4.

Python 3 sans dépendance externe, graine fixe. Usage : python3 simulation.py
"""
import os
import random
import statistics

GRAINE = 20261015
PARTIES = 2000
COULEURS = ["jaune", "bleu", "vert", "orange", "violet"]
MANCHES = {2: 6, 3: 5, 4: 4}

# ---------------------------------------------------------------- feuillet
# Zone jaune : grille 3 lignes x 4 colonnes. Chaque nombre de 1 à 6 y figure deux fois.
JAUNE_GRILLE = [
    [1, 2, 3, 4],
    [5, 6, 1, 2],
    [3, 4, 5, 6],
]
JAUNE_BONUS_LIGNE = ["relance", "+1", "relance"]  # ligne complète -> bonus
JAUNE_POINTS_COLONNE = [10, 10, 10, 10]          # colonne complète -> points
JAUNE_POINTS_CASE = 1                              # chaque case cochée -> 1 point

# Zone verte « la montée » : cases dans l'ordre, valeur >= seuil.
VERT_SEUILS = [1, 2, 3, 4, 5, 2, 3, 4, 5, 6]
# Zone bleue « la descente » : cases dans l'ordre, valeur <= seuil.
BLEU_SEUILS = [6, 5, 4, 3, 2, 5, 4, 3, 2, 1]
# Points selon le nombre de cases cochées (on lit le nombre sous la dernière case cochée).
ESCALIER_POINTS = [2, 4, 7, 10, 14, 18, 23, 28, 34, 40]
VERT_BONUS = {3: "+1", 6: "relance"}    # index de case (0 = première) -> bonus
BLEU_BONUS = {3: "relance", 6: "+1"}

# Zone orange : on écrit la valeur du dé, cases dans l'ordre. Score = somme.
ORANGE_CASES = 8
ORANGE_BONUS = {2: "relance", 5: "+1"}
# Zone violette : valeur strictement plus grande que la précédente, sauf après un 6.
VIOLET_CASES = 7
VIOLET_BONUS = {2: "+1", 5: "relance"}

NB_CASES = {
    "jaune": sum(len(r) for r in JAUNE_GRILLE),
    "bleu": len(BLEU_SEUILS),
    "vert": len(VERT_SEUILS),
    "orange": ORANGE_CASES,
    "violet": VIOLET_CASES,
}


class Feuille:
    def __init__(self):
        self.jaune = set()          # (ligne, colonne) cochées
        self.vert = 0               # nombre de cases cochées
        self.bleu = 0
        self.orange = []            # valeurs écrites
        self.violet = []
        self.relances = 0           # bonus disponibles
        self.plus1 = 0
        self.stats = {"relance_gagnee": 0, "plus1_gagne": 0, "relance_utilisee": 0,
                      "plus1_utilise": 0, "bonus_perdu_plus1": 0}

    # --- placements possibles pour un dé (couleur, valeur) -> liste de "coups"
    def coups(self, couleur, v):
        if couleur == "jaune":
            return [("jaune", (r, c)) for r in range(3) for c in range(4)
                    if JAUNE_GRILLE[r][c] == v and (r, c) not in self.jaune]
        if couleur == "vert":
            if self.vert < len(VERT_SEUILS) and v >= VERT_SEUILS[self.vert]:
                return [("vert", None)]
            return []
        if couleur == "bleu":
            if self.bleu < len(BLEU_SEUILS) and v <= BLEU_SEUILS[self.bleu]:
                return [("bleu", None)]
            return []
        if couleur == "orange":
            return [("orange", None)] if len(self.orange) < ORANGE_CASES else []
        if couleur == "violet":
            if len(self.violet) >= VIOLET_CASES:
                return []
            if not self.violet or self.violet[-1] == 6 or v > self.violet[-1]:
                return [("violet", None)]
            return []
        raise ValueError(couleur)

    # --- applique un coup, renvoie la liste des bonus déclenchés
    def jouer(self, coup, v, par_plus1=False):
        zone, pos = coup
        bonus = []
        if zone == "jaune":
            self.jaune.add(pos)
            r = pos[0]
            if all((r, c) in self.jaune for c in range(4)):
                bonus.append(JAUNE_BONUS_LIGNE[r])
        elif zone == "vert":
            i = self.vert
            self.vert += 1
            if i in VERT_BONUS:
                bonus.append(VERT_BONUS[i])
        elif zone == "bleu":
            i = self.bleu
            self.bleu += 1
            if i in BLEU_BONUS:
                bonus.append(BLEU_BONUS[i])
        elif zone == "orange":
            i = len(self.orange)
            self.orange.append(v)
            if i in ORANGE_BONUS:
                bonus.append(ORANGE_BONUS[i])
        elif zone == "violet":
            i = len(self.violet)
            self.violet.append(v)
            if i in VIOLET_BONUS:
                bonus.append(VIOLET_BONUS[i])
        if par_plus1:
            # Règle : une case remplie grâce à un +1 ne donne pas de bonus.
            self.stats["bonus_perdu_plus1"] += len(bonus)
            return []
        for b in bonus:
            if b == "relance":
                self.relances += 1
                self.stats["relance_gagnee"] += 1
            else:
                self.plus1 += 1
                self.stats["plus1_gagne"] += 1
        return bonus

    # --- décompte
    def score_zones(self):
        j = len(self.jaune) * JAUNE_POINTS_CASE
        for c in range(4):
            if all((r, c) in self.jaune for r in range(3)):
                j += JAUNE_POINTS_COLONNE[c]
        return {
            "jaune": j,
            "bleu": ESCALIER_POINTS[self.bleu - 1] if self.bleu else 0,
            "vert": ESCALIER_POINTS[self.vert - 1] if self.vert else 0,
            "orange": sum(self.orange),
            "violet": sum(self.violet),
        }

    def remplissage(self):
        return {
            "jaune": len(self.jaune), "bleu": self.bleu, "vert": self.vert,
            "orange": len(self.orange), "violet": len(self.violet),
        }

    # --- évaluation gloutonne d'un coup : points immédiats + progrès
    def valeur(self, coup, v):
        zone, pos = coup
        if zone == "jaune":
            r, c = pos
            g = JAUNE_POINTS_CASE
            col = sum(1 for rr in range(3) if (rr, c) in self.jaune)
            g += JAUNE_POINTS_COLONNE[c] * (col + 1) / 3.0
            lig = sum(1 for cc in range(4) if (r, cc) in self.jaune)
            g += 3.0 * (lig + 1) / 4.0
            return g
        if zone in ("vert", "bleu"):
            n = self.vert if zone == "vert" else self.bleu
            seuils = VERT_SEUILS if zone == "vert" else BLEU_SEUILS
            avant = ESCALIER_POINTS[n - 1] if n else 0
            g = ESCALIER_POINTS[n] - avant
            gaspi = (v - seuils[n]) if zone == "vert" else (seuils[n] - v)
            g -= 0.4 * gaspi
            bon = VERT_BONUS if zone == "vert" else BLEU_BONUS
            if n in bon:
                g += 3
            return g + 1.5
        if zone == "orange":
            g = v - 2.5
            if len(self.orange) in ORANGE_BONUS:
                g += 3
            return g
        if zone == "violet":
            dernier = self.violet[-1] if self.violet else 0
            base = 0 if dernier == 6 else dernier
            ecart = 0 if v == 6 else v - base - 1   # nombres « sautés » qui bloquent la suite
            g = v - 1.0 * ecart - 1.0
            if len(self.violet) in VIOLET_BONUS:
                g += 3
            return g
        raise ValueError(zone)

    def meilleur_coup(self, couleur, v):
        meilleur = None
        for coup in self.coups(couleur, v):
            g = self.valeur(coup, v)
            if meilleur is None or g > meilleur[0]:
                meilleur = (g, coup)
        return meilleur


def partie(nb_joueurs, rng):
    feuilles = [Feuille() for _ in range(nb_joueurs)]
    tours_actifs = 0
    manches = MANCHES[nb_joueurs]
    for manche in range(manches):
        for actif in range(nb_joueurs):
            tours_actifs += 1
            dernier_tour = (manche == manches - 1)
            f = feuilles[actif]
            valeurs = {c: rng.randint(1, 6) for c in COULEURS}
            dispo = list(COULEURS)
            plateau = []
            for choix in range(3):
                if not dispo:
                    break
                for c in dispo:
                    valeurs[c] = rng.randint(1, 6)
                while True:
                    options = []
                    for c in dispo:
                        m = f.meilleur_coup(c, valeurs[c])
                        plus_petits = sum(1 for d in dispo if valeurs[d] < valeurs[c])
                        cout = 0.6 * plus_petits if choix < 2 else 0.0
                        if m:
                            options.append((m[0] - cout, c, m[1]))
                        else:
                            options.append((-5 - cout, c, None))
                    options.sort(key=lambda o: o[0], reverse=True)
                    if f.relances > 0 and options[0][0] < 2.0:
                        f.relances -= 1
                        f.stats["relance_utilisee"] += 1
                        for c in dispo:
                            valeurs[c] = rng.randint(1, 6)
                        continue
                    break
                _, c_choisi, coup = options[0]
                v = valeurs[c_choisi]
                if coup is not None:
                    f.jouer(coup, v)
                dispo.remove(c_choisi)
                petits = [d for d in dispo if valeurs[d] < v]
                for d in petits:
                    dispo.remove(d)
                    plateau.append(d)
            plateau.extend(dispo)
            # joueurs passifs
            for p in range(nb_joueurs):
                if p == actif:
                    continue
                fp = feuilles[p]
                best = None
                for c in plateau:
                    m = fp.meilleur_coup(c, valeurs[c])
                    if m and (best is None or m[0] > best[0]):
                        best = (m[0], c, m[1])
                if best and best[0] > -1.0:
                    fp.jouer(best[2], valeurs[best[1]])
            # +1 : un seul par joueur et par tour, n'importe lequel des 5 dés
            for p in range(nb_joueurs):
                fp = feuilles[p]
                if fp.plus1 <= 0:
                    continue
                best = None
                for c in COULEURS:
                    m = fp.meilleur_coup(c, valeurs[c])
                    if m and (best is None or m[0] > best[0]):
                        best = (m[0], c, m[1])
                seuil = 0.0 if dernier_tour else 3.5
                if best and best[0] >= seuil:
                    fp.plus1 -= 1
                    fp.stats["plus1_utilise"] += 1
                    fp.jouer(best[2], valeurs[best[1]], par_plus1=True)
    return feuilles, tours_actifs, True


def simuler():
    rng = random.Random(GRAINE)
    resultats = {}
    for n in (2, 3, 4):
        scores, tours, finies = [], [], 0
        rempl = {z: [] for z in COULEURS}
        parts = {z: [] for z in COULEURS}
        stats_bonus = {}
        nb_feuilles = 0
        for _ in range(PARTIES):
            feuilles, t, fini = partie(n, rng)
            finies += fini
            tours.append(t)
            for f in feuilles:
                nb_feuilles += 1
                sz = f.score_zones()
                tot = sum(sz.values())
                scores.append(tot)
                r = f.remplissage()
                for z in COULEURS:
                    rempl[z].append(r[z] / NB_CASES[z])
                    parts[z].append(sz[z] / tot if tot else 0)
                for k, val in f.stats.items():
                    stats_bonus[k] = stats_bonus.get(k, 0) + val
        resultats[n] = {
            "score_moy": statistics.mean(scores),
            "score_et": statistics.pstdev(scores),
            "finies": 100.0 * finies / PARTIES,
            "tours": statistics.mean(tours),
            "rempl": {z: 100 * statistics.mean(rempl[z]) for z in COULEURS},
            "part": {z: 100 * statistics.mean(parts[z]) for z in COULEURS},
            "bonus": {k: v / nb_feuilles for k, v in stats_bonus.items()},
        }
    return resultats


def rapport(res):
    L = []
    L.append("# Résultats de simulation – variante B (5 dés sans joker)\n")
    L.append(f"Graine {GRAINE}, {PARTIES} parties par nombre de joueurs, stratégie gloutonne "
             "(points immédiats + progrès). Généré par `simulation.py`.\n")
    verifs = []
    for n, r in res.items():
        L.append(f"## {n} joueurs ({MANCHES[n]} manches)\n")
        L.append(f"- Score moyen : {r['score_moy']:.1f} (écart-type {r['score_et']:.1f})")
        L.append(f"- Parties terminées : {r['finies']:.0f} %")
        L.append(f"- Tours de joueur actif par partie : {r['tours']:.0f} "
                 f"(durée estimée {r['tours']:.0f} min)")
        L.append("")
        L.append("| Zone | Cases | Remplissage moyen | Part moyenne du score |")
        L.append("|------|------:|------------------:|----------------------:|")
        for z in COULEURS:
            L.append(f"| {z} | {NB_CASES[z]} | {r['rempl'][z]:.0f} % | {r['part'][z]:.0f} % |")
        L.append("")
        b = r["bonus"]
        L.append("Bonus par joueur et par partie : "
                 f"relances gagnées {b['relance_gagnee']:.2f}, utilisées {b['relance_utilisee']:.2f} ; "
                 f"+1 gagnés {b['plus1_gagne']:.2f}, utilisés {b['plus1_utilise']:.2f} ; "
                 f"bonus non gagnés (case remplie par un +1) {b['bonus_perdu_plus1']:.2f}.\n")
        verifs.append((f"{n} j. – toutes les parties se terminent", r["finies"] == 100.0))
        for z in COULEURS:
            verifs.append((f"{n} j. – remplissage {z} ≥ 30 % ({r['rempl'][z]:.0f} %)",
                           r["rempl"][z] >= 30.0))
        verifs.append((f"{n} j. – durée ≤ 20 min ({r['tours']:.0f} tours actifs)",
                       r["tours"] * 1 <= 20))
        for z in COULEURS:
            verifs.append((f"{n} j. – part {z} ≤ 40 % ({r['part'][z]:.0f} %)",
                           r["part"][z] <= 40.0))
    L.append("## Vérification des critères 6 et 7\n")
    for nom, ok in verifs:
        L.append(f"- {'OK' if ok else 'ÉCHEC'} — {nom}")
    tout = all(ok for _, ok in verifs)
    L.append("")
    L.append(f"**Bilan : {'OK partout' if tout else 'au moins un ÉCHEC'}**")
    return "\n".join(L) + "\n", tout


if __name__ == "__main__":
    res = simuler()
    texte, tout = rapport(res)
    print(texte)
    ici = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(ici, "resultats-simulation.md"), "w", encoding="utf-8") as fh:
        fh.write(texte)
