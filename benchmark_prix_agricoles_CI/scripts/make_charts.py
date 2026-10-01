# -*- coding: utf-8 -*-
"""
Graphiques de la note, construits EXCLUSIVEMENT à partir de la base Excel recalculée
(Base_Prix_Benchmark_CI.xlsx, lecture des valeurs calculées). Sorties SVG (note PDF) et PNG (note Word).
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
IDX = json.load(open(ROOT / "scripts" / "cell_index.json"))
WB = load_workbook(ROOT / "Base_Prix_Benchmark_CI.xlsx", data_only=True)

# Inter converti en TrueType (« Inter TT ») pour un PDF sans polices Type 3 ; repli Liberation Sans
for f in font_manager.findSystemFonts(["/usr/local/share/fonts/intertt"]):
    font_manager.fontManager.addfont(f)
plt.rcParams.update({
    "font.family": ["Inter TT", "Liberation Sans", "DejaVu Sans"], "font.size": 8.5, "svg.fonttype": "none",
    "axes.edgecolor": "#c3c2b7", "axes.linewidth": 0.8, "axes.labelcolor": "#52514e",
    "xtick.color": "#898781", "ytick.color": "#898781", "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 100,
})
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, MUTED, GRID, BASE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SURFACE = "#ffffff"


def v(sheet, ref):
    return WB[sheet][ref].value


def save(fig, name):
    fig.savefig(FIG / f"{name}.svg", bbox_inches="tight", facecolor=SURFACE)
    fig.savefig(FIG / f"{name}.png", dpi=300, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def grid(ax, axis="x"):
    ax.grid(axis=axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


DATA = {}

# ---------------------------------------------------------------------------
# Graphique 1 – positionnement (bulles)
# ---------------------------------------------------------------------------
pos = []
for fil, r in IDX["POS_ROW"].items():
    pos.append((fil, v("Positionnement", f"B{r}"), v("Positionnement", f"C{r}"), v("Positionnement", f"D{r}")))
DATA["positionnement"] = pos
fig, ax = plt.subplots(figsize=(6.6, 3.1))
grid(ax, "both")
ax.axvline(100, color=INK2, linewidth=1)
ax.text(101.5, 0.965, "Parité avec les\ncomparateurs", color=INK2, fontsize=7.5, va="top", transform=ax.get_xaxis_transform())
smax = max(p[3] for p in pos)
# positions des étiquettes (coordonnées données) avec traits de rappel
lab_pos = {"Cacao": (47, 62, "center"), "Café": (52, 78, "center"), "Anacarde": (90, 30, "center"),
           "Coton": (115, 58, "center"), "Caoutchouc": (86, 80, "center")}
for fil, x, y, size in pos:
    s = 3200 * size / smax + 40
    ax.scatter(x, y * 100, s=s, color=BLUE, alpha=0.18, linewidths=0, zorder=2)
    ax.scatter(x, y * 100, s=s, facecolors="none", edgecolors=BLUE, linewidths=1.6, zorder=3)
    ax.scatter(x, y * 100, s=16, color=BLUE, edgecolors="white", linewidths=1, zorder=4)
    tx, ty, ha = lab_pos[fil]
    ax.annotate(f"{fil}\nindice {x:.0f} · {y*100:.0f} %", (x, y * 100), xytext=(tx, ty), textcoords="data",
                ha=ha, va="center", fontsize=7.8, color=INK, fontweight="semibold", linespacing=1.15,
                arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.7, shrinkA=2, shrinkB=3))
ax.set_xlim(40, 125)
ax.set_ylim(0, 100)
ax.set_xlabel("Rémunération du producteur ivoirien — indice (médiane des pays comparables = 100)")
ax.set_ylabel("Part du prix international reçue (%)")
for t, (xx, yy, ha) in {"Rémunération inférieure\naux concurrents": (41, 3, "left"),
                         "Au-dessus de la parité :\nrémunération ≥ concurrents": (124, 30, "right")}.items():
    ax.text(xx, yy, t, color=MUTED, fontsize=7, ha=ha, va="bottom", style="italic")
ax.text(0.0, -0.235, "Taille des bulles : valeur brute au producteur (production × prix bord champ, Mds FCFA) – cacao ≈ 2 400 ; caoutchouc ≈ 770 ; anacarde ≈ 620 ; coton ≈ 110 ; café ≈ 30.",
        transform=ax.transAxes, fontsize=6.8, color=INK2)
save(fig, "fig1_positionnement")

# ---------------------------------------------------------------------------
# Graphique 2 – indices de prix par comparateur (dot plot)
# ---------------------------------------------------------------------------
order = ["Cacao", "Café", "Anacarde", "Coton", "Caoutchouc", "Palmier à huile", "Riz"]
pairs = {}
for key, r in IDX["PAIR_ROW"].items():
    fil, lab = key.split("|")
    idx_val = v("Indicateurs", f"I{r}")
    compar = v("Indicateurs", f"L{r}")
    pays = lab.split("–")[0].strip().replace(" (Riau)", "")
    pairs.setdefault(fil, []).append((pays, idx_val, compar, lab))
med = {fil: v("Indicateurs", f"I{r}") for fil, r in IDX["MED_ROW"].items()}
DATA["indices"] = {"pairs": pairs, "medianes": med}
# on retient pour le graphique les comparaisons à la même période que la ligne médiane
keep = {"Cacao": ["Ghana – ouverture 2026/27", "Nigeria – sept. 2026 (source secondaire)"],
        "Café": None, "Anacarde": ["Burkina Faso – 2026", "Guinée-Bissau – 2026", "Ghana – 2026", "Tanzanie – 2025/26 (enchères)"],
        "Coton": None, "Caoutchouc": None, "Palmier à huile": None, "Riz": None}
short = {"Burkina Faso": "BF", "Guinée-Bissau": "GW", "Ghana": "GH", "Tanzanie": "TZ", "Mali": "ML", "Bénin": "BJ",
         "Togo": "TG", "Sénégal": "SN", "Vietnam": "VN", "Ouganda": "UG", "Thaïlande": "TH", "Indonésie": "ID",
         "Malaisie": "MY", "Cameroun": "CM", "Nigeria": "NG", "Équateur": "EC", "Indonésie (Riau)": "ID"}
fig, ax = plt.subplots(figsize=(4.8, 3.1))
grid(ax, "x")
ax.axvline(100, color=INK2, linewidth=1)
ys = list(range(len(order)))[::-1]
for y, fil in zip(ys, order):
    pts = pairs[fil]
    if keep.get(fil):
        pts = [p for p in pts if p[3] in keep[fil]]
    pts = sorted(pts, key=lambda p: p[1])
    groups = []
    for pays, iv, compar, lab in pts:
        if groups and abs(groups[-1][0] - iv) < 0.6:
            groups[-1][1].append(short.get(pays, pays[:2].upper()))
        else:
            groups.append([iv, [short.get(pays, pays[:2].upper())]])
        filled = compar == "Directe"
        ax.scatter(iv, y, s=46, color=BLUE if filled else "white", edgecolors=BLUE, linewidths=1.6, zorder=3)
    for j, (iv, codes) in enumerate(groups):
        near_med = abs(iv - med[fil]) < 3 and len(codes) > 1
        ax.annotate("·".join(codes), (iv, y), xytext=(9, 0) if near_med else (0, 7.5 if j % 2 == 0 else -9.5),
                    textcoords="offset points", ha="left" if near_med else "center", va="center", fontsize=6.6, color=INK2)
    m = med[fil]
    ax.plot([m, m], [y - 0.28, y + 0.28], color=INK, linewidth=2.2, solid_capstyle="round", zorder=4)
ax.set_yticks(ys)
ax.set_yticklabels(order, color=INK, fontsize=8.2)
ax.set_xlim(40, 240)
ax.set_xticks([50, 75, 100, 125, 150, 175, 200, 225])
ax.set_xlabel("Prix bord champ ivoirien en % du prix du pays comparable (100 = même prix)", fontsize=7.6)
ax.tick_params(axis="y", length=0)
leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE, markeredgecolor=BLUE, markersize=6.5, label="Comparaison directe"),
       Line2D([0], [0], marker="o", color="w", markerfacecolor="white", markeredgecolor=BLUE, markeredgewidth=1.6, markersize=6.5, label="Comparaison indicative"),
       Line2D([0], [0], color=INK, linewidth=2.2, label="Médiane des comparateurs directs*")]
ax.legend(handles=leg, loc="upper right", frameon=False, fontsize=7.2, handletextpad=0.4)
save(fig, "fig2_indices_prix")

# ---------------------------------------------------------------------------
# Graphique 3 – part du prix international reçue (CI vs comparateurs)
# ---------------------------------------------------------------------------
tr_rows = [("Cacao\n(2026/27)", "Cacao"), ("Café\n(2026/27)", "Café"), ("Anacarde\n(2026)", "Anacarde"),
           ("Coton\n(2025/26)", "Coton"), ("Caoutchouc\n(2025-26)", "Caoutchouc")]
tr = []
for lab, fil in tr_rows:
    r = IDX["MED_ROW"][fil]
    ci = v("Indicateurs", f"J{r}")
    comp = v("Indicateurs", f"K{r}")
    if fil == "Caoutchouc":
        ci = v("Decomposition", f"B{IDX['DEC']['cao_share']}")
    tr.append((lab, ci, comp if isinstance(comp, (int, float)) else None))
DATA["transmission"] = tr
fig, ax = plt.subplots(figsize=(2.7, 2.85))
grid(ax, "x")
h = 0.34
for i, (lab, ci, comp) in enumerate(tr[::-1]):
    ax.barh(i + h / 2 + 0.02, ci * 100, height=h, color=BLUE, zorder=3)
    ax.text(ci * 100 + 1.5, i + h / 2 + 0.02, f"{ci*100:.0f} %", va="center", fontsize=7.2, color=INK)
    if comp is not None:
        ax.barh(i - h / 2 - 0.02, comp * 100, height=h, color=ORANGE, zorder=3)
        ax.text(comp * 100 + 1.5, i - h / 2 - 0.02, f"{comp*100:.0f} %", va="center", fontsize=7.2, color=INK)
    else:
        ax.text(1.5, i - h / 2 - 0.02, "n.d.", va="center", fontsize=7, color=MUTED)
ax.set_yticks(range(len(tr)))
ax.set_yticklabels([t[0] for t in tr[::-1]], fontsize=7.6, color=INK)
ax.set_xlim(0, 118)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0", "25", "50", "75", "100 %"])
ax.tick_params(axis="y", length=0)
leg = [Line2D([0], [0], color=BLUE, linewidth=6, label="Côte d'Ivoire"),
       Line2D([0], [0], color=ORANGE, linewidth=6, label="Comparateurs (médiane)")]
ax.legend(handles=leg, loc="lower center", bbox_to_anchor=(0.45, -0.24), ncol=2, frameon=False, fontsize=7.2, handlelength=1.2)
save(fig, "fig3_transmission")

# ---------------------------------------------------------------------------
# Graphique 4 – cacao : prix CI, prix Ghana, cours mondial (FCFA/kg)
# ---------------------------------------------------------------------------
rows = IDX["TRANS_ROWS"] + [IDX["ROW_2627"]]
labels, ci, gh, wd = [], [], [], []
for r in rows:
    camp = v("Cacao_transmission", f"A{r}")
    half = v("Cacao_transmission", f"B{r}")
    tag = "P" if half.startswith("Princ") else ("I" if half.startswith("Inter") else "Ouv.")
    labels.append(f"{camp[2:]}\n{tag}")
    ci.append(v("Cacao_transmission", f"C{r}"))
    gh.append(v("Cacao_transmission", f"D{r}"))
    wd.append(v("Cacao_transmission", f"E{r}"))
DATA["cacao_series"] = {"labels": labels, "ci": ci, "gh": gh, "monde": wd}
fig, ax = plt.subplots(figsize=(5.0, 2.55))
grid(ax, "y")
x = list(range(len(labels)))
ax.plot(x, wd, color=MUTED, linewidth=2, solid_joinstyle="round", label="Cours mondial (ICCO, même période)")
ax.fill_between(x, wd, color=MUTED, alpha=0.08, linewidth=0)
ax.plot(x, gh, color=ORANGE, linewidth=2, solid_joinstyle="round", label="Ghana – prix producteur")
ax.plot(x, ci, color=BLUE, linewidth=2.2, solid_joinstyle="round", label="Côte d'Ivoire – prix bord champ")
for series, col in ((ci, BLUE), (gh, ORANGE), (wd, MUTED)):
    ax.scatter(x[-1], series[-1], s=30, color=col, edgecolors="white", linewidths=1.5, zorder=5)
ax.annotate(f"{ci[-1]:,.0f}".replace(",", " "), (x[-1], ci[-1]), xytext=(6, -2), textcoords="offset points", fontsize=7.2, color=INK, va="center")
ax.annotate(f"{gh[-1]:,.0f}".replace(",", " "), (x[-1], gh[-1]), xytext=(6, 0), textcoords="offset points", fontsize=7.2, color=INK, va="center")
ax.annotate(f"{wd[-1]:,.0f}".replace(",", " "), (x[-1], wd[-1]), xytext=(6, 0), textcoords="offset points", fontsize=7.2, color=INK, va="center")
i_peak = max(range(len(wd)), key=lambda k: wd[k])
ax.annotate(f"Pic : {wd[i_peak]:,.0f}".replace(",", " "), (x[i_peak], wd[i_peak]), xytext=(-8, 4), textcoords="offset points",
            fontsize=7, color=INK2, ha="right")
major = [k for k, l in enumerate(labels) if l.endswith("P") or l.endswith("Ouv.")]
ax.set_xticks(x, minor=True)
ax.set_xticks([k + 0.5 if k + 1 < len(x) and labels[k].endswith("P") else k for k in major])
ax.set_xticklabels([labels[k].split("\n")[0] if labels[k].endswith("P") else "\n" + labels[k].split("\n")[0] + "*" for k in major], fontsize=6.5)
ax.text(1.0, -0.2, "* ouverture de campagne", transform=ax.transAxes, ha="right", fontsize=6.3, color=MUTED)
ax.tick_params(axis="x", which="major", length=0)
ax.tick_params(axis="x", which="minor", length=3, color=BASE)
k25 = labels.index("25/26\nP")
ax.annotate("2025/26 principale :\nprix CI > cours mondial", (x[k25], ci[k25]), xytext=(x[k25] + 1.0, 5500),
            fontsize=7, color=INK2, ha="center", arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.7))
ax.set_xlim(-0.4, len(x) + 0.1)
ax.set_ylim(0, 6000)
ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000])
ax.set_yticklabels(["0", "1 000", "2 000", "3 000", "4 000", "5 000", "6 000"])
ax.set_ylabel("FCFA/kg")
ax.legend(loc="upper left", frameon=False, fontsize=7.2, ncol=1)
save(fig, "fig4_cacao_series")

# ---------------------------------------------------------------------------
# Graphique 5 – décomposition de la valeur (cacao, anacarde)
# ---------------------------------------------------------------------------
D = IDX["DEC"]
caf_r = D["caf"]
cac = {"Producteur": v("Decomposition", f"B{caf_r+1}"),
       "Logistique intérieure (barème)": 0,
       "Fiscalité et parafiscalité": v("Decomposition", f"B{caf_r+2}") + v("Decomposition", f"B{caf_r+3}"),
       "Autres coûts, fret et marges (résidu)": v("Decomposition", f"B{caf_r+4}")}
a0 = D["ana_start"]
ana = {"Producteur": v("Decomposition", f"C{a0}"),
       "Logistique intérieure (barème)": sum(v("Decomposition", f"C{a0+k}") for k in (1, 2, 3)),
       "Fiscalité et parafiscalité": v("Decomposition", f"C{a0+4}"),
       "Autres coûts, fret et marges (résidu)": v("Decomposition", f"C{a0+5}")}
DATA["decomposition"] = {"cacao": cac, "anacarde": ana}
cols = [BLUE, AQUA, ORANGE, YELLOW]
fig, ax = plt.subplots(figsize=(6.6, 1.25))
bars = [("Cacao – partage du CAF (règle)", cac), ("Anacarde 2026 – bord champ → CFR Asie", ana)]
for i, (lab, d) in enumerate(bars[::-1]):
    left = 0
    for (k, val), c in zip(d.items(), cols):
        if val <= 0:
            continue
        ax.barh(i, val * 100 - 0.4, left=left + 0.2, height=0.56, color=c, zorder=3)
        if val * 100 >= 6:
            ax.text(left + val * 50, i, f"{val*100:.0f}", ha="center", va="center", fontsize=7.6,
                    color="white" if c in (BLUE, ORANGE) else INK, fontweight="semibold")
        left += val * 100
ax.set_yticks([0, 1])
ax.set_yticklabels([b[0].replace("\n", " ") for b in bars[::-1]], fontsize=7.4, color=INK)
ax.set_xlim(0, 100)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xticklabels(["0", "20", "40", "60", "80", "100 %"])
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
leg = [Line2D([0], [0], color=c, linewidth=6, label=k) for k, c in zip(cac.keys(), cols)]
ax.legend(handles=leg, loc="lower center", bbox_to_anchor=(0.36, 1.0), ncol=4, frameon=False, fontsize=6.8, handlelength=1.1,
          columnspacing=1.0)
save(fig, "fig5_decomposition")

# ---------------------------------------------------------------------------
# Graphique 6 – riz paddy : CI vs comparateurs et parité FOB (emphasis)
# ---------------------------------------------------------------------------
O = IDX["OBS_ROW"]
riz = [("Côte d'Ivoire (paddy, 2025)", v("Observations", f"S{O['RIZ-CI-2025']}"), True),
       ("Sénégal (prix fixé, 2025)", v("Observations", f"S{O['RIZ-SN-2025']}"), False),
       ("Vietnam (paddy frais, fin 2025)", v("Observations", f"S{O['RIZ-VN-2025']}"), False),
       ("Équivalent paddy du riz thaï 5 % FOB", v("Observations", f"V{O['INT-RIZ-2025']}"), False)]
DATA["riz"] = riz
fig, ax = plt.subplots(figsize=(3.3, 1.9))
grid(ax, "x")
for i, (lab, val, emph) in enumerate(riz[::-1]):
    ax.barh(i, val, height=0.5, color=BLUE if emph else BASE, zorder=3)
    ax.text(val + 4, i, f"{val:.0f}", va="center", fontsize=7.4, color=INK)
ax.set_yticks(range(len(riz)))
ax.set_yticklabels([r[0] for r in riz[::-1]], fontsize=7.2, color=INK)
ax.set_xlim(0, 280)
ax.set_xlabel("FCFA/kg de paddy")
ax.tick_params(axis="y", length=0)
save(fig, "fig6_riz")

json.dump(DATA, open(ROOT / "scripts" / "chart_data.json", "w"), ensure_ascii=False, indent=1, default=str)
print("Graphiques écrits dans", FIG)
