"""Graphiques de la note, lus exclusivement depuis la base Excel recalculée."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import load_workbook  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "Base_resilience_filieres_CI.xlsx"
OUT = ROOT / "graphiques"
OUT.mkdir(exist_ok=True)

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "axes.titlesize": 9, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "legend.frameon": False,
})


def table(ws):
    rows = list(ws.iter_rows(values_only=True))
    h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]


wb = load_workbook(XLSX, data_only=True)
EP = {r["id"]: r for r in table(wb["EPISODES"])}
SERIES = table(wb["SERIES"])
PARAM = table(wb["STRESS_PARAM"])[:6]
STRESS = table(wb["STRESS_TEST"])
SHORT = {"Côte d'Ivoire": "CI", "Ghana": "GH", "Cameroun": "CM", "Équateur": "EC", "Mali": "ML",
         "Burkina Faso": "BF", "Tanzanie": "TZ", "Thaïlande": "TH", "Indonésie": "ID", "Vietnam": "VN"}


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------- G1 choc int vs choc producteur
fig, ax = plt.subplots(figsize=(4.6, 3.4))
lim = 80
ax.plot([0, lim], [0, lim], color=INK2, lw=1, ls="--")
ax.text(lim * 0.56, lim * 0.50, "transmission = 1", color=INK2, fontsize=7, rotation=33)
ax.fill_between([0, lim], [0, 0], [0, lim], color=AQUA, alpha=0.07, lw=0)
ax.text(lim * 0.97, 3, "Zone d'amortissement\n(sous la diagonale)", color=INK2, fontsize=7, ha="right", va="bottom")
offsets = {"CAC-CI-16": (5, 3), "CAC-CM-16": (-58, 2), "CAC-EC-16": (6, -10), "CAC-GH-16": (5, 3), "COT-CI-20": (5, 3),
           "COT-ML-20": (5, 2), "COT-BF-20": (5, -2), "ANA-CI-19": (-56, 3), "ANA-TZ-19": (-10, -11), "HEV-CI-16": (-58, 2),
           "HEV-TH-16": (5, -9), "PAL-CI-22": (5, -9), "PAL-ID-22": (5, 2), "CAC-CI-26": (6, -4), "CAC-GH-26": (5, -8),
           "CAF-CI-26": (-56, 2)}
for eid, r in EP.items():
    if r["sens"] != "baisse":
        continue
    x, y = -r["choc_int"] * 100, -r["choc_prod"] * 100
    ci = r["pays"] == "Côte d'Ivoire"
    ax.scatter(x, y, s=34 if ci else 26, color=ORANGE if ci else BLUE, edgecolor=SURF, lw=1.5, zorder=3)
    fil = {"Anacarde": "Anac.", "Palmier à huile": "Palme"}.get(r["filiere"], r["filiere"])
    lbl = f"{fil} {SHORT[r['pays']]} {str(r['t2'])[:4]}"
    dx, dy = offsets.get(eid, (4, 2))
    ax.annotate(lbl, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=6.3, color=INK)
ax.scatter([], [], color=ORANGE, label="Côte d'Ivoire")
ax.scatter([], [], color=BLUE, label="Pays de référence")
ax.legend(loc="upper left", fontsize=7)
ax.set_xlim(0, lim)
ax.set_ylim(-3, lim)
ax.set_xlabel("Baisse du prix international, en monnaie locale (%)")
ax.set_ylabel("Baisse du prix producteur (%)")
ax.set_title("Graphique 1 – Choc international vs choc subi par le producteur")
save(fig, "G1_choc_int_vs_producteur.png")

# --------------------------------------------------------- G2 délai de récupération
def months_between(a, b):
    ya, ma = int(a[:4]), int(a[5:7]) if len(a) >= 7 and a[4] == "-" else 6
    yb, mb = int(b[:4]), int(b[5:7])
    return (yb - ya) * 12 + (mb - ma)


items = []
for eid in ["COT-CI-20", "CAC-GH-16", "PAL-ID-22", "COT-ML-20", "CAC-CI-16", "ANA-CI-19", "HEV-CI-16", "HEV-TH-16", "CAC-CI-26"]:
    r = EP[eid]
    lbl = f"{r['filiere']} – {r['pays']} ({r['episode'].split()[-1]})"
    if isinstance(r["delai_recup_mois"], (int, float)):
        items.append((lbl, r["delai_recup_mois"], "ok", r["pays"] == "Côte d'Ivoire"))
    else:
        t2 = str(r["t2"]) if "-" in str(r["t2"]) else f"{str(r['t2'])[:4]}-06"
        items.append((lbl, months_between(t2, "2026-10"), "non" if "non" in r["recup_statut"] else "cours",
                      r["pays"] == "Côte d'Ivoire"))
fig, ax = plt.subplots(figsize=(4.6, 2.9))
for i, (lbl, m, st, ci) in enumerate(items):
    col = ORANGE if ci else BLUE
    if st == "ok":
        ax.barh(i, max(m, 0.6), color=col, height=0.62)
        ax.text(max(m, 0.6) + 2, i, "0 (prix maintenu)" if m == 0 else f"{m:.0f} mois", va="center", fontsize=6.5, color=INK)
    else:
        ax.barh(i, m, color=SURF, edgecolor=col, hatch="////", height=0.62, lw=1)
        ax.text(m + 2, i, ("non récupéré" if st == "non" else "en cours") + f" ({m:.0f}+ mois)", va="center", fontsize=6.5, color=INK)
ax.set_yticks(range(len(items)), [x[0] for x in items], fontsize=6.6)
ax.invert_yaxis()
ax.set_xlim(0, 200)
ax.set_xlabel("Mois entre le point bas et le retour au prix producteur pré-choc")
ax.set_title("Graphique 2 – Temps de récupération après un choc")
ax.grid(axis="y", visible=False)
save(fig, "G2_recuperation.png")

# --------------------------------------------------------- G3 qui absorbe le choc (campagne 1)
fig, ax = plt.subplots(figsize=(4.6, 2.5))
names = [p["filiere"] for p in PARAM]
prod = [p["beta1"] for p in PARAM]
pub = [(1 - p["beta1"]) * p["part_publique"] for p in PARAM]
priv = [(1 - p["beta1"]) * (1 - p["part_publique"]) for p in PARAM]
y = range(len(names))
ax.barh(y, prod, color=ORANGE, height=0.6, label="Producteurs", edgecolor=SURF, lw=1)
ax.barh(y, priv, left=prod, color=BLUE, height=0.6, label="Acheteurs à terme / égreneurs / huileries", edgecolor=SURF, lw=1)
ax.barh(y, pub, left=[a + b for a, b in zip(prod, priv)], color=AQUA, height=0.6, label="Régulateur / État", edgecolor=SURF, lw=1)
for i in y:
    if prod[i] >= 0.15:
        ax.text(prod[i] / 2, i, f"{prod[i]:.0%}", ha="center", va="center", fontsize=6.5, color=INK)
ax.set_yticks(list(y), names)
ax.invert_yaxis()
ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
ax.set_title("Graphique 3 – Qui absorbe une baisse des cours ? (campagne en cours)")
ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.13), ncol=3, fontsize=6.5)
ax.grid(axis="y", visible=False)
save(fig, "G3_qui_absorbe.png")

# --------------------------------------------------------- G4 stress test -30 %
s3 = {r["filiere"]: r for r in STRESS if r["scenario"] == "S3"}
s4 = {r["filiere"]: r for r in STRESS if r["scenario"] == "S4"}
s5 = {r["filiere"]: r for r in STRESS if r["scenario"] == "S5"}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 2.6), gridspec_kw={"wspace": 0.6})
fig.suptitle("Graphique 4 – Test de stress : baisse de 30 % du prix international", x=0.08, ha="left", fontsize=9, fontweight="bold", y=1.04)
yy = list(range(len(names)))
h = 0.26
a1.barh([i - h for i in yy], [-s3[n]["dP_prod_c1"] * 100 for n in names], height=h, color=ORANGE, label="Prix producteur, campagne 1")
a1.barh(yy, [-(s5[n]["dP_prod_c2"] or 0) * 100 for n in names], height=h, color=YELLOW, label="Prix producteur, campagne 2")
a1.barh([i + h for i in yy], [-s4[n]["dRecette_c1"] * 100 for n in names], height=h, color=BLUE, label="Recette (si production -10 %)")
a1.set_yticks(yy, names)
a1.invert_yaxis()
a1.set_xlabel("Baisse (%)")
a1.set_title("a) Impact producteur (%)")
a1.legend(loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1, fontsize=6.5)
a1.grid(axis="y", visible=False)
a2.barh([i - h / 2 for i in yy], [s3[n]["perte_recette_c1_mds"] for n in names], height=h, color=BLUE, label="Perte de recette des producteurs")
a2.barh([i + h / 2 for i in yy], [s3[n]["besoin_public_mds"] for n in names], height=h, color=AQUA, label="Besoin potentiel public (régulateur/État)")
for i, n in enumerate(names):
    a2.text(s3[n]["perte_recette_c1_mds"] + 4, i - h / 2, f"{s3[n]['perte_recette_c1_mds']:.0f}", va="center", fontsize=6.3)
    a2.text(s3[n]["besoin_public_mds"] + 4, i + h / 2, f"{s3[n]['besoin_public_mds']:.0f}", va="center", fontsize=6.3)
a2.set_yticks(yy, names)
a2.invert_yaxis()
a2.set_xlabel("Milliards FCFA, campagne 1")
a2.set_title("b) Coût, campagne 1 (Mds FCFA)")
a2.legend(loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1, fontsize=6.5)
a2.grid(axis="y", visible=False)
a2.set_xlim(0, max(s3[n]["perte_recette_c1_mds"] for n in names) * 1.18)
save(fig, "G4_stress_test_30.png")

# --------------------------------------------------------- G5 cacao : part du prix mondial reçue
fig, (b1, b2) = plt.subplots(1, 2, figsize=(7.2, 2.4), gridspec_kw={"wspace": 0.25})
fig.suptitle("Graphique 5 – Cacao : prix mondial (spot) et prix producteur", x=0.08, ha="left", fontsize=9, fontweight="bold", y=1.04)
ci = [r for r in SERIES if r["filiere"] == "Cacao" and r["pays"] == "Côte d'Ivoire"]
gh = [r for r in SERIES if r["filiere"] == "Cacao" and r["pays"] == "Ghana"]
x = [r["campagne"][2:] for r in ci]
b1.plot(x, [r["prix_int_local_kg"] for r in ci], color=BLUE, lw=2, label="Prix mondial ICCO (FCFA/kg)")
b1.plot(x, [r["prix_prod"] for r in ci], color=ORANGE, lw=2, label="Prix producteur CI (FCFA/kg, moyenne pondérée)")
b1.scatter([x[-1]], [1200], color=ORANGE, s=20, zorder=3)
b1.annotate("2026/27 : 1 200", (x[-1], 1200), xytext=(-58, -3), textcoords="offset points", fontsize=6.3)
b1.set_title("a) Côte d'Ivoire (FCFA/kg)")
b1.tick_params(axis="x", labelrotation=60, labelsize=6.3)
b1.legend(fontsize=6.3, loc="upper left")
b2.plot(x, [r["part_producteur"] * 100 for r in ci], color=ORANGE, lw=2, label="Côte d'Ivoire")
b2.plot([r["campagne"][2:] for r in gh], [r["part_producteur"] * 100 for r in gh], color=BLUE, lw=2, label="Ghana")
b2.axhline(60, color=INK2, lw=0.8, ls="--")
b2.text(6.5, 61.5, "référence CI : 60 % du CAF", fontsize=6.3, color=INK2)
b2.set_ylim(20, 100)
b2.set_title("b) Part du prix mondial spot reçue (%)")
b2.tick_params(axis="x", labelrotation=60, labelsize=6.3)
b2.legend(fontsize=6.3, loc="upper center")
save(fig, "G5_cacao_part_producteur.png")
print("graphiques écrits dans", OUT)
