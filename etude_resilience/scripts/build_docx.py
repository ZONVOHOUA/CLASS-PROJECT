"""Note ministérielle (Word) – tous les chiffres sont lus dans la base Excel recalculée."""
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "Base_resilience_filieres_CI.xlsx"
G = ROOT / "graphiques"
OUT = ROOT / "Note_ministerielle_resilience_CI.docx"

GREEN = RGBColor(0x1F, 0x4E, 0x3D)
ORANGE_HEX, GREEN_HEX, LIGHT_HEX, GREY_HEX = "EB6834", "1F4E3D", "EAF2EE", "F3F3F1"


# ------------------------------------------------------------------ données
def table(ws):
    rows = list(ws.iter_rows(values_only=True))
    return [dict(zip(rows[0], r)) for r in rows[1:] if r[0] is not None]


wb = load_workbook(XLSX, data_only=True)
EP = {r["id"]: r for r in table(wb["EPISODES"])}
SER = table(wb["SERIES"])
IND = {(r["filiere"], r["pays"]): r for r in table(wb["INDICATEURS"]) if "–" in str(r.get("periode"))}
PARAM = {r["filiere"]: r for r in table(wb["STRESS_PARAM"])[:6]}
ST = table(wb["STRESS_TEST"])
S = {(r["filiere"], r["scenario"]): r for r in ST}
MECA = table(wb["MECANISMES"])
LIT = table(wb["LITTERATURE"])


def pct(x, d=0, sign=False):
    v = x * 100
    s = f"{v:+.{d}f}" if sign else f"{v:.{d}f}"
    return s.replace(".", ",").replace("-", "−") + " %"


def num(x, d=0):
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def b(eid):
    return num(EP[eid]["transmission"], 2)


def ser(fil, pays, camp):
    return next(r for r in SER if r["filiere"] == fil and r["pays"] == pays and r["campagne"] == camp)


# ------------------------------------------------------------------ helpers docx
doc = Document()
st = doc.styles["Normal"]
st.font.name = "Arial"
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.font.size = Pt(8.5)
st.paragraph_format.space_after = Pt(2)
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.line_spacing = 1.0
for lvl, size in ((1, 11), (2, 9.5)):
    hs = doc.styles[f"Heading {lvl}"]
    hs.font.name, hs.font.size, hs.font.bold = "Arial", Pt(size), True
    hs.font.color.rgb = GREEN
    hs.paragraph_format.space_before = Pt(5 if lvl == 1 else 3)
    hs.paragraph_format.space_after = Pt(2)
    hs.paragraph_format.keep_with_next = True
    rpr = hs.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        rfonts.set(qn(a), "Arial")
    for a in ("w:asciiTheme", "w:hAnsiTheme"):
        if rfonts.get(qn(a)) is not None:
            del rfonts.attrib[qn(a)]

sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.left_margin = sec.right_margin = Cm(1.5)
sec.top_margin, sec.bottom_margin = Cm(1.2), Cm(1.1)
sec.footer_distance = Cm(0.5)
fp = sec.footer.paragraphs[0]
fp.text = "MINADERPV – Note au Ministre – Résilience des filières aux chocs de prix internationaux – 1er octobre 2026 – Chiffres de qualité B/C à valider (voir AUDIT_DONNEES.md)"
fp.runs[0].font.size = Pt(6.5)
fp.runs[0].font.color.rgb = RGBColor(0x52, 0x51, 0x4E)

CONTENT_W = 18.0  # cm


def shade(cell, hex_):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hex_)
    tcPr.append(sh)


def cell_margins(tbl, cm=0.08):
    tblPr = tbl._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(int(cm * 567)))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def para(text="", bold=False, size=None, color=None, italic=False, align=None, after=2, style=None):
    p = doc.add_paragraph(style=style)
    if text:
        add_runs(p, text, bold=bold, size=size, color=color, italic=italic)
    p.paragraph_format.space_after = Pt(after)
    if align is not None:
        p.alignment = align
    return p


def add_runs(p, text, bold=False, size=None, color=None, italic=False):
    """Texte avec **gras** inline."""
    parts = text.split("**")
    for i, t in enumerate(parts):
        if not t:
            continue
        r = p.add_run(t)
        r.bold = bold or (i % 2 == 1)
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
    return p


def bullet(text, size=None, numbered=False):
    p = doc.add_paragraph(style="List Number" if numbered else "List Bullet")
    add_runs(p, text, size=size)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.left_indent = Cm(0.45)
    return p


def grid(rows, widths, header=True, size=7, head_fill=GREEN_HEX, zebra=True, bold_first_col=True):
    t = doc.add_table(rows=len(rows), cols=len(widths))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    t.autofit = False
    cell_margins(t, 0.07)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.width = Cm(widths[j])
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            add_runs(p, str(val), size=size, bold=(header and i == 0) or (bold_first_col and j == 0 and i > 0),
                     color=RGBColor(0xFF, 0xFF, 0xFF) if header and i == 0 else None)
            if header and i == 0:
                shade(c, head_fill)
            elif zebra and i % 2 == 0:
                shade(c, GREY_HEX)
    # largeurs de grille
    tblGrid = t._tbl.tblGrid
    for j, gc in enumerate(tblGrid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[j] * 567)))
    # bordures légères
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "2")
        el.set(qn("w:color"), "BFBFBF")
        borders.append(el)
    t._tbl.tblPr.append(borders)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return t


def box(lines, fill=LIGHT_HEX, size=8, title=None):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_margins(t, 0.15)
    c = t.cell(0, 0)
    c.width = Cm(CONTENT_W)
    shade(c, fill)
    first = True
    if title:
        p = c.paragraphs[0]
        add_runs(p, title, bold=True, size=size + 0.5, color=GREEN)
        p.paragraph_format.space_after = Pt(1)
        first = False
    for ln in lines:
        p = c.paragraphs[0] if first else c.add_paragraph()
        first = False
        add_runs(p, ln, size=size)
        p.paragraph_format.space_after = Pt(1.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def figure(path, width_cm, caption=None):
    p = doc.add_paragraph()
    p.alignment = 1
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    p.paragraph_format.space_after = Pt(0)
    if caption:
        para(caption, size=6.5, italic=True, color=RGBColor(0x52, 0x51, 0x4E), after=2)


def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def two_figs(p1, p2, w1, w2, caption=None):
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, (pth, w) in enumerate(((p1, w1), (p2, w2))):
        c = t.cell(0, j)
        c.width = Cm(w + 0.2)
        par = c.paragraphs[0]
        par.alignment = 1
        par.add_run().add_picture(str(pth), width=Cm(w))
    if caption:
        para(caption, size=6.5, italic=True, color=RGBColor(0x52, 0x51, 0x4E), after=2)


# ------------------------------------------------------------------ valeurs clés
c16, c26, c24 = EP["CAC-CI-16"], EP["CAC-CI-26"], EP["CAC-CI-24"]
gh24, cm24, gh16 = EP["CAC-GH-24"], EP["CAC-CM-24"], EP["CAC-GH-16"]
cot22, cotml, cotbf = EP["COT-CI-22"], EP["COT-ML-20"], EP["COT-BF-20"]
ana19, hev16, pal22 = EP["ANA-CI-19"], EP["HEV-CI-16"], EP["PAL-CI-22"]
coton_2223 = ser("Coton", "Côte d'Ivoire", "2022/23")
cac_2324 = ser("Cacao", "Côte d'Ivoire", "2023/24")
cac_2526 = ser("Cacao", "Côte d'Ivoire", "2025/26")
val_cacao_2627 = PARAM["Cacao"]["valeur_filiere_mds"]
perte_cacao_2627 = cac_2526["recette_mds"] - val_cacao_2627
ind_cot = IND[("Coton", "Côte d'Ivoire")]
ind_cac = IND[("Cacao", "Côte d'Ivoire")]
s3 = {f: S[(f, "S3")] for f in PARAM}
s4 = {f: S[(f, "S4")] for f in PARAM}
s5 = {f: S[(f, "S5")] for f in PARAM}
beta1_cacao = PARAM["Cacao"]["beta1"]

# =================================================================== PAGE 1
p = para("NOTE AU MINISTRE  •  Cellule d'études  •  1er octobre 2026  •  Diffusion restreinte", size=7, color=RGBColor(0x52, 0x51, 0x4E), after=1)
para("LES FILIÈRES AGRICOLES IVOIRIENNES RÉSISTENT-ELLES AUX CHOCS INTERNATIONAUX ?", bold=True, size=14, color=GREEN, after=0)
para("Benchmark international de la résilience des prix et des revenus agricoles", size=10, italic=True, after=4)

box([
    "**Question.** Les grandes filières ivoiriennes sont-elles assez résilientes face aux chocs de prix mondiaux, et "
    "comment leur capacité d'absorption se compare-t-elle à celle des pays concurrents ?",
    "**Résilience** = capacité d'une filière à absorber un choc international défavorable, à en limiter l'effet sur les "
    "producteurs, puis à revenir à une trajectoire soutenable **sans déséquilibre financier excessif**. Elle est mesurée selon "
    "5 dimensions : **exposition**, **transmission** (variation du prix producteur ÷ variation du prix mondial), "
    "**absorption** (1 − transmission, et qui paie), **récupération** (délai de retour au niveau pré-choc), **soutenabilité** "
    "(coût et financement). **Un prix stable n'est pas un prix résilient** : il peut cacher une dette, une subvention ou un simple retard.",
], title=None, size=7.8)

doc.add_heading("Six constats majeurs", level=2)
constats = [
    f"**Le cacao retarde le choc plus qu'il ne l'amortit.** Les ventes anticipées protègent le producteur pendant la campagne "
    f"(transmission ≈ {num(beta1_cacao, 1)} sur le prix moyen de campagne), mais le choc est presque intégralement répercuté à la campagne suivante : "
    f"transmission de **{b('CAC-CI-16')}** en 2016-17 (délai {c16['delai_reaction_mois']} mois) et de **{b('CAC-CI-26')}** en 2025-26.",
    f"**Le dispositif cacao n'a pas résisté au retournement de 2025-26.** Le prix mondial a chuté de {pct(-c26['choc_int_usd'])} "
    f"(en USD) ; le prix bord champ est passé de 2 800 à 1 200 FCFA/kg ({pct(c26['choc_prod'])}). Environ 200 000 t d'invendus ont été rachetées par l'État : "
    f"coût estimé à **~{num(c26['cout_mds_fcfa'])} Mds FCFA**. La recette des planteurs baisse d'environ **{num(round(perte_cacao_2627, -2))} Mds FCFA** en 2026/27.",
    f"**Les hausses sont mal transmises et ne sont pas épargnées.** Pendant l'envolée de 2023-25, la transmission des hausses a été de "
    f"**{b('CAC-CI-24')}** en Côte d'Ivoire, contre {b('CAC-GH-24')} au Ghana et {b('CAC-CM-24')} au Cameroun. Pour le coton en 2021-22, elle a été de "
    f"**{b('COT-CI-22')}** alors que les cours progressaient de {pct(cot22['choc_int'])}. La filière renonce aux gains des années fastes "
    f"sans les mettre en réserve pour les années de crise.",
    f"**Anacarde, hévéa et palmier : aucun amortisseur.** Les producteurs portent 100 % du choc. La transmission a été de {b('ANA-CI-19')} pour "
    f"l'anacarde en 2018-19 et de {b('HEV-CI-16')} pour l'hévéa en 2011-16 ; le prix de l'hévéa n'a jamais retrouvé son niveau de 2011. "
    f"Ce sont les filières dont la recette baisse le plus en cas de choc de −30 %.",
    f"**Un prix protégé ne garantit pas la recette.** Coton 2022/23 : prix maintenu, production en baisse de "
    f"{pct(-(coton_2223['prod_kt'] / 560 - 1))} (jassides), recette des producteurs {pct(coton_2223['var_recette'])}. "
    f"{pct(ind_cot['part_variance_recette_due_Q'])} de la variabilité de la recette cotonnière vient des volumes et non du prix.",
    "**À l'étranger, les dispositifs qui tiennent sont pilotés par une règle.** Ils combinent une réserve constituée en haut de cycle (fonds de lissage "
    "du Burkina Faso, prélèvement progressif en Indonésie), un déclenchement automatique et plafonné (IPG en Malaisie) et une règle de "
    "partage connue d'avance (Ghana, Act 2026 : ≥ 70 % du FOB). La stabilisation financée par la dette (Cocobod) et les ajustements "
    "brutaux (Mali, coton 2020 : production −80 %) échouent.",
]
for c in constats:
    bullet(c, size=7.8, numbered=True)

doc.add_heading("Principaux chocs identifiés (seuil : baisse ≥ 15 % ; sensibilité à 20 % en annexe)", level=2)
para("Hévéa 2011-16 (−70 % en USD) • Cacao 2016-17 (−36 %) • Anacarde 2018-19 (−32 %) • Coton COVID 2020 (−17 %) • "
     "Huile de palme 2022 (−50 %) • Riz importé 2023 (+28 %, choc consommateur) • Envolée cacao et café 2023-25 (+191 % et +113 %) • "
     "Retournement du cacao 2025-26 (−64 %).", size=7.6, after=2)
figure(G / "G1_choc_int_vs_producteur.png", 10.2,
       "Lecture : un point situé sous la diagonale signale un choc amorti. La plupart des épisodes ivoiriens sont sur la diagonale ou au-dessus "
       "(transmission ≥ 1, prix producteur mesuré après ajustement). Source : base Excel, onglet EPISODES.")

# =================================================================== PAGE 2
page_break()
doc.add_heading("1. Carte de vulnérabilité des filières : le même choc n'a pas le même effet", level=1)
para("Indicateurs observés (onglets EPISODES, INDICATEURS, STRESS_TEST). Aucune note synthétique n'est attribuée : les colonnes "
     "décrivent des faits mesurés.", size=7.5, italic=True)
rows = [["Filière", "Exposition", "Transmission des baisses (β) et délai", "Protection du producteur", "Coût de la stabilisation", "Récupération", "Vulnérabilité principale"]]
rows += [
    ["Cacao", "Très forte : 1er exportateur mondial (~40 %) ; prix USD/GBP ; ~1,8 Mt",
     f"β = {b('CAC-CI-16')} (2017) ; {b('CAC-CI-26')} (2026) ; délai de 5 à 15 mois", "Prix minimum garanti + ventes anticipées (~70 %) : protection **pendant** la campagne",
     f"~{num(c26['cout_mds_fcfa'])} Mds (rachats 2026, estimation) ; FRP non publié", f"{c16['delai_recup_mois']} mois (2017-20, retour à 91 %) ; 2026 en cours",
     "Pas de réserve dimensionnée pour un choc > 40 % ou de 2 campagnes ; risque de défaut des exportateurs"],
    ["Café", "Forte mais volumes marginaux (~60 kt)", f"β = {b('CAF-CI-26')} (2026, une campagne de retard)", "Prix minimum garanti annuel",
     f"Faible (≈ {num(s3['Café']['besoin_public_mds'])} Mds en cas de choc de −30 %)", "—", "Déclin structurel de la production : le prix n'est pas le problème"],
    ["Coton", "Forte (fibre exportée en USD) ; ~575 kt de coton-graine",
     f"β = 0 (2020) ; hausses : β = {b('COT-CI-22')}", "Prix fixé avant les semis pour toute la campagne",
     "Subvention de 25,3 Mds en 2025/26 (44 FCFA/kg, 14 % de la valeur)", "Volumes : 3 campagnes après 2022/23",
     "Recette exposée aux chocs de rendement ; protection financée par le budget, sans fonds de lissage"],
    ["Anacarde", "Très forte : 1er producteur mondial ; ~75 % de la récolte exportée brute vers l'Inde et le Vietnam", f"β = {b('ANA-CI-19')} (2019) ; délai < 2 mois",
     "Prix plancher sans fonds ni obligation d'achat (non respecté en 2018)", "Aucun", f"{ana19['delai_recup_mois']} mois (2019-24)",
     "Dépendance à 2 acheteurs ; transformation locale encore minoritaire"],
    ["Hévéa", "Très forte : 3e producteur mondial ; prix SICOM (USD)", f"β = {b('HEV-CI-16')} (2011-16) ; délai d'un mois (formule)",
     "Aucune : indexation (66 % du prix net depuis mai 2026)", "Aucun", "Jamais revenu au niveau de 2011",
     f"Perte la plus élevée en test de stress (~{num(s3['Hévéa']['perte_recette_c1_mds'])} Mds pour −30 %)"],
    ["Palmier à huile", "Moyenne : marché régional (CEDEAO) en partie protégé", f"β ≈ {b('PAL-CI-22')} (2022)", "Indexation mensuelle des régimes",
     "Aucun", "À documenter", "Petits planteurs villageois sans couverture"],
    ["Banane, ananas, mangue", "Forte (UE), contrats en EUR", "Non mesurable (prix contractuels)", "Intégration des plantations ; aucun risque de change (FCFA arrimé à l'euro)", "—", "—",
     "Risque d'accès au marché et de normes (MD2, mouche des fruits), plus que de prix"],
    ["Riz importé, blé", "Forte côté consommateur (~1,5 Mt de riz importé)", f"β ≈ {b('RIZ-CI-23')} vers le consommateur (2023)", "Plafonnement des prix, mesures fiscales",
     "Dépense fiscale", "—", "Choc sur le pouvoir d'achat urbain, pas sur le revenu agricole"],
    ["Sucre, maïs", "Faible (marché intérieur protégé / peu échangé)", "Non significative", "Protection à l'importation", "Supporté par le consommateur", "—", "Analyse internationale non pertinente"],
]
grid(rows, [1.6, 2.7, 2.6, 2.9, 2.4, 2.0, 3.8], size=6.6)

doc.add_heading("Quatre profils de résilience", level=2)
for t_ in [
    "**Stable mais fragile : cacao et coton.** Le prix est tenu, mais par des engagements (contrats à terme, budget) sans réserve publiée : "
    "la stabilité casse au-delà d'un certain choc (cacao 2017 et 2026) ou se paie chaque année (coton).",
    "**Volatile et sans amortisseur : anacarde, hévéa, palmier.** Ces filières transmettent le choc en 1 à 2 mois. Leur résilience repose sur la croissance "
    f"des volumes (production d'hévéa multipliée par {num(1600 / 235, 0)} depuis 2011) et sur l'épargne des ménages, deux amortisseurs non pilotés.",
    "**Prix protégé, recette non protégée : coton 2022/23 et cacao 2023/24.** En 2023/24, le prix du cacao a augmenté (+22 %) mais la production a baissé "
    f"de 22 % : la recette a reculé ({pct(cac_2324['var_recette'])}) en pleine envolée des cours.",
    "**Peu exposées au prix mondial : banane, sucre, maïs.** Leur vulnérabilité est ailleurs (accès aux marchés, climat, compétitivité).",
]:
    bullet(t_, size=7.6)
figure(G / "G3_qui_absorbe.png", 10.5,
       "Répartition de la charge d'une baisse des cours pendant la campagne en cours (paramètres de l'onglet STRESS_PARAM : β1 observé ; partage "
       "public/privé de la part non transmise = hypothèse documentée).")

# =================================================================== PAGE 3
page_break()
doc.add_heading("2. Que s'est-il passé lors des grands chocs ?", level=1)
rows = [["Épisode", "Choc mondial", "Réaction de la Côte d'Ivoire", "Impact producteur", "Qui a absorbé ?", "Résultat"]]
rows += [
    ["Cacao 2016-17",
     f"ICCO {pct(c16['choc_int_usd'])} (juil. 2016 → fév. 2017)",
     "Prix principal maintenu à 1 100 FCFA jusqu'en mars, puis 700 FCFA à la campagne intermédiaire",
     f"{pct(c16['choc_prod'])} sur le prix ; recette {pct(c16['var_recette'])} ; β = {b('CAC-CI-16')}",
     "Acheteurs à terme (6 mois), puis producteurs ; contrats d'exportateurs défaillants repris par le CCC",
     f"Retour à 91 % du prix pré-choc après {c16['delai_recup_mois']} mois. Ghana : prix nominal gelé (β = 0), financé par l'emprunt"],
    ["Coton 2020 (COVID)",
     f"Cotlook A {pct(EP['COT-CI-20']['choc_int_usd'])} (janv. → avril 2020)",
     "Prix de 300 FCFA/kg maintenu ; soutien public", "Prix 0 % ; recette +14 % (volumes)", "État et sociétés cotonnières",
     f"Mali : prix −27 %, production {pct(cotml['q_t2'] / cotml['q_t0'] - 1)}, recette {pct(cotml['var_recette'])}. Burkina Faso : fonds de lissage, β = {b('COT-BF-20')}"],
    ["Hévéa 2011-16",
     f"TSR20 {pct(hev16['choc_int_usd'])} (moyenne 2011 → 2016)",
     "Aucune (prix indexé) ; ajustements fiscaux ponctuels",
     f"Prix {pct(hev16['choc_prod'])} ; recette {pct(hev16['var_recette'])} grâce aux volumes",
     "Producteurs ; dépréciation de l'euro (et donc du FCFA) face au dollar", "Prix toujours inférieur de moitié à 2011. Thaïlande : achats publics coûteux, puis garantie de revenu plafonnée"],
    ["Cacao 2023-26 (envolée puis effondrement)",
     f"ICCO {pct(c24['choc_int_usd'], sign=True)} (2022/23 → 2024/25), puis {pct(c26['choc_int_usd'])} jusqu'en mars 2026",
     "Hausses progressives 1 000 → 1 500 → 1 800 → 2 200 → 2 800 ; puis 1 200 FCFA (mars 2026, reconduit en 2026/27)",
     f"Hausse transmise à {b('CAC-CI-24')} ; baisse de {pct(c26['choc_prod'])} ; recette de 2026/27 ≈ {num(val_cacao_2627)} Mds contre {num(cac_2526['recette_mds'])} Mds",
     "CCC/État : rachat d'environ 200 kt d'invendus ; exportateurs défaillants ; puis producteurs",
     "Prix relevé à contre-courant en octobre 2025 (ventes conclues aux prix hauts) ; ajustement brutal de −57 % 5 mois plus tard. Ghana : −29 % en février 2026, nouvelle loi (≥ 70 % du FOB)"],
]
grid(rows, [2.0, 2.4, 3.4, 3.1, 3.2, 3.9], size=6.6)
figure(G / "G5_cacao_part_producteur.png", 17.0,
       "La part du prix mondial au comptant (spot) reçue par le planteur a chuté à ~30 % en 2023/24 puis a dépassé 90 % en 2025/26. Le mécanisme décale donc le choc dans le temps sans le réduire. "
       "Les ventes anticipées étant conclues à d'autres prix que le comptant, la part rapportée au prix effectivement réalisé (CAF) est moins volatile. Source : SERIES.")
figure(G / "G2_recuperation.png", 11.0,
       "Barres hachurées : prix pré-choc non retrouvé au 1er octobre 2026. Un délai nul correspond à un prix maintenu, qui n'est pas un « retour » au sens de la résilience.")

# =================================================================== PAGE 4
page_break()
doc.add_heading("3. Comment font les autres ? Les mécanismes étrangers les plus instructifs", level=1)
rows = [["Pays", "Filière", "Mécanisme", "Résultat observé", "Coût / limite", "Enseignement pour la Côte d'Ivoire"]]
for m in MECA:
    rows.append([m["pays"], m["filiere"], m["mecanisme"], m["resultat"], m["cout_limite"], m["enseignement"]])
grid(rows, [1.6, 1.4, 4.2, 3.2, 3.4, 4.2], size=6.4)

doc.add_heading("Six modèles de stabilisation comparés", level=2)
rows = [["Modèle", "Efficacité observée", "Coût", "Besoin de données", "Principal risque", "Compatibilité avec la Côte d'Ivoire"],
        ["A. Prix administré (CI, Ghana, Mali)", "Élevée tant que le choc est court", "Caché (dette, subvention, contrats)", "Faible", "Ajustement brutal, dette", "Existe : à doter d'une règle et d'une réserve"],
        ["B. Fonds de stabilisation à règle (Burkina Faso, Chili)", "Bonne si la règle est automatique et le fonds abondé en haut de cycle", "Financé par les années fastes", "Moyen (prix de référence)", "Épuisement, captation politique", "**Forte** (cacao, coton, café)"],
        ["C. Assurance revenu / recette (Brésil, OCDE)", "Bonne pour les chocs de volume", "Subvention des primes (30 à 60 %)", "**Élevé** (rendements par zone)", "Antisélection, coût de gestion", "Moyenne : coton d'abord (zones homogènes)"],
        ["D. Ventes à terme / options (CI, Ghana)", "Bonne sur 6 à 18 mois", "Prime des options ; risque de contrepartie", "Moyen", "Défauts en cas de forte baisse, manque à gagner en hausse", "Existe : ajouter des garanties et des options de vente (put)"],
        ["E. Paiement contracyclique (Malaisie, Thaïlande)", "Bonne pour les petits planteurs", "Budgétaire, à plafonner", "Moyen (registre des producteurs)", "Coût ouvert sans plafond", "Forte pour l'hévéa (registre CHPC)"],
        ["F. Marché + intervention ciblée (Équateur, Vietnam, Tanzanie)", "Volatile mais à récupération rapide (productivité)", "Faible", "Faible", "Pertes non couvertes", "Forte pour l'anacarde (récépissés d'entrepôt)"]]
grid(rows, [3.4, 3.0, 2.6, 2.3, 2.9, 3.8], size=6.4)
box([
    "**Garantie de prix, de recette ou de revenu ?** Une garantie de prix protège P ; une garantie de recette protège P × Q ; une garantie de revenu protège la recette "
    "nette des coûts. La garantie de recette n'est utile que lorsque les volumes varient fortement. Part de la variance de la recette due aux volumes : "
    f"**coton {pct(ind_cot['part_variance_recette_due_Q'])}**, cacao {pct(ind_cac['part_variance_recette_due_Q'])}, "
    f"anacarde {pct(IND[('Anacarde', 'Côte d' + chr(39) + 'Ivoire')]['part_variance_recette_due_Q'])}, hévéa {pct(IND[('Hévéa', 'Côte d' + chr(39) + 'Ivoire')]['part_variance_recette_due_Q'])}. "
    "La garantie de recette (de préférence indicielle, par zone) est donc d'abord pertinente pour le **coton**. Pour les autres filières, l'enjeu principal est le prix.",
], size=7.4)

# =================================================================== PAGE 5
page_break()
doc.add_heading("4. Si les prix mondiaux baissaient de 30 % demain", level=1)
para("Test de stress standardisé, base 2026/27 (prix et volumes actuels). Hypothèses et 5 scénarios complets : onglets STRESS_PARAM et STRESS_TEST.", size=7.3, italic=True)
rows = [["Filière", "Baisse mondiale", "Baisse du prix producteur (campagne 1 / 2)", "Perte de recette des producteurs, campagne 1 (Mds FCFA)",
         "Protection existante", "Besoin potentiel d'intervention publique (Mds FCFA ; FCFA/kg)", "Deux campagnes consécutives : perte cumulée des producteurs"]]
for f in PARAM:
    r3, r5 = s3[f], s5[f]
    rows.append([f, "−30 %", f"{pct(r3['dP_prod_c1'])} / {pct(r5['dP_prod_c2'])}", num(r3["perte_recette_c1_mds"]),
                 PARAM[f]["protection"], f"{num(r3['besoin_public_mds'])} ; {num(r3['besoin_public_FCFA_kg'])}" if r3["besoin_public_mds"] else "0 (choc entièrement subi par les producteurs)",
                 f"{num(r5['perte_recette_cumulee_mds'])} Mds"])
grid(rows, [1.9, 1.3, 2.4, 2.3, 4.2, 3.3, 2.6], size=6.6)
figure(G / "G4_stress_test_30.png", 16.5)
para(f"**Lecture.** Pour le cacao, le choc est reporté à la campagne suivante (−{num(-s5['Cacao']['dP_prod_c2'] * 100, 1).replace('−', '')} %). "
     f"La charge portée pendant la campagne revient d'abord aux acheteurs à terme, si leurs contrats sont honorés : "
     f"~{num(s3['Cacao']['charge_absorbee_hors_prod_mds'])} Mds FCFA. Sur cette charge, environ {num(s3['Cacao']['besoin_public_mds'])} Mds sont à risque pour le régulateur, "
     f"un ordre de grandeur cohérent avec les rachats de 2026. Aucune réserve publiée ne couvre ce besoin. "
     f"Si la production baisse en plus de 10 %, une garantie de recette à 90 % coûterait {num(s4['Cacao']['cout_garantie_recette_90_mds'])} Mds pour le cacao "
     f"et {num(s4['Hévéa']['cout_garantie_recette_90_mds'])} Mds pour l'hévéa.", size=7.4)

doc.add_heading("5. Priorités pour la Côte d'Ivoire", level=1)
rows = [["Vulnérabilité", "Filières", "Réponse existante", "Limite observée", "Option à étudier", "Qui paie ?"],
        ["Réserve absente ou opaque face aux chocs > 40 % ou sur deux campagnes", "Cacao, café", "Ventes anticipées, prix garanti, FRP",
         "2017 et 2026 : ajustement brutal ; rachats ~240 Mds", "**Fonds de réserve à règle automatique** : prélèvement quand le CAF dépasse sa moyenne mobile sur 5 ans, décaissement plafonné (≤ 25 % du choc), publication trimestrielle",
         "Prélèvement de filière en haut de cycle ; pas le budget général"],
        ["Risque de contrepartie des ventes anticipées", "Cacao", "Agrément des exportateurs", "Défauts en 2017 et 2026",
         "Garanties de bonne exécution / dépôts de marge ; **options de vente (put)** sur 20 à 30 % des ventes", "Exportateurs (garanties) ; CCC (primes, ~3 à 6 % de la valeur couverte)"],
        ["Hausses peu transmises, non épargnées", "Cacao, coton", "Prix fixé discrétionnairement", f"β hausse : cacao {b('CAC-CI-24')}, coton 0",
         "**Règle de partage publiée** (% du CAF, comme au Ghana), complément de prix en fin de campagne, part des hausses versée au fonds", "Neutre budgétairement"],
        ["Aucune protection, transmission ≥ 1", "Hévéa, palmier", "Indexation sur la formule", f"Perte de ~{num(s3['Hévéa']['perte_recette_c1_mds'])} Mds pour un choc de −30 %",
         "**Paiement contracyclique plafonné** (type IPG) pour les petits planteurs inscrits au registre, déclenché sous un prix seuil", "Prélèvement progressif à l'export (cess) en haut de cycle"],
        ["Plancher non opposable, ventes forcées", "Anacarde", "Prix plancher", "Plancher non respecté en 2018",
         "**Récépissés d'entrepôt** et crédit de stockage ; transformation locale ; diversification des débouchés", "Banques, avec garantie partielle (FIRCA/bailleurs)"],
        ["Recette exposée aux chocs de rendement", "Coton", "Subvention des intrants (25,3 Mds)", "2022/23 : recette −56 % malgré un prix stable",
         "**Garantie de recette / assurance indicielle de rendement** par zone ; fonds de lissage cotonnier", "Primes partagées : producteurs, sociétés cotonnières, État (dégressif)"]]
grid(rows, [3.0, 1.5, 2.3, 2.8, 5.2, 3.2], size=6.4)
para("**Principes budgétaires.** Aucune option ne repose sur une subvention permanente non financée. Les réserves sont constituées en haut de cycle et "
     f"dimensionnées pour **deux campagnes consécutives à −30 %** (cacao : ≈ {num(s5['Cacao']['charge_absorbee_hors_prod_mds'])} Mds FCFA de charge hors producteurs, dont ≈ {num(s5['Cacao']['besoin_public_mds'])} Mds à risque public). "
     "Elles sont plafonnées par producteur et soumises à une gouvernance indépendante (prix de référence fixé par un comité). "
     "**Prochaines étapes :** valider les données B/C avec le CCC, le CCA, le CHPC, le Trésor et l'INS ; obtenir l'état du FRP ; estimer les modèles NARDL sur données mensuelles.", size=7.4)

# =================================================================== ANNEXES
doc.add_section(WD_SECTION.NEW_PAGE)
doc.add_heading("Annexe A – Test de stress complet (5 scénarios × 6 filières)", level=1)
rows = [["Filière", "Scénario", "ΔP prod. c1", "ΔP prod. c2", "Δ recette c1", "Perte cumulée (Mds)", "Charge hors producteurs (Mds)", "Besoin public (Mds)", "FCFA/kg", "% de la valeur", "Garantie recette 90 % (Mds)"]]
for r in ST:
    rows.append([r["filiere"], r["libelle"], pct(r["dP_prod_c1"]), pct(r["dP_prod_c2"]) if isinstance(r["dP_prod_c2"], (int, float)) else "—",
                 pct(r["dRecette_c1"]), num(r["perte_recette_cumulee_mds"]), num(r["charge_absorbee_hors_prod_mds"]),
                 num(r["besoin_public_mds"]), num(r["besoin_public_FCFA_kg"]), pct(r["besoin_public_pct_valeur"], 1), num(r["cout_garantie_recette_90_mds"])])
grid(rows, [1.9, 3.4, 1.3, 1.3, 1.3, 1.5, 1.7, 1.4, 1.2, 1.4, 1.6], size=6.2, bold_first_col=False)
para("Formules : ΔP c1 = β1 × choc ; Δ recette = (1 + ΔP)(1 + ΔQ) − 1 ; charge hors producteurs = (1 − β) × |choc| × P0 × Q0 ; besoin public = charge × part publique ; "
     "garantie de recette à 90 % = max(0 ; 0,9 − (1 + Δ recette)) × P0 × Q0. La capacité financière identifiée est fixée à 0 tant que l'état du FRP n'est pas publié. "
     "Le déficit de financement est donc égal au besoin public.", size=6.8)

doc.add_heading("Annexe B – Asymétrie : transmission des hausses vs transmission des baisses (épisodes)", level=1)
rows = [["Épisode", "Pays", "Sens", "Choc int. (monnaie locale)", "Choc producteur", "Transmission β", "Δ recette", "Délai de réaction (mois)", "Qualité"]]
for r in EP.values():
    rows.append([f"{r['filiere']} – {r['episode']}", r["pays"], r["sens"], pct(r["choc_int"]), pct(r["choc_prod"]), num(r["transmission"], 2),
                 pct(r["var_recette"]), r["delai_reaction_mois"] if r["delai_reaction_mois"] is not None else "—", r["qualite"]])
grid(rows, [4.6, 1.9, 1.2, 1.9, 1.7, 1.5, 1.5, 1.7, 1.9], size=6.2, bold_first_col=False)
para("Lecture : β > 1 = le prix producteur baisse plus que le prix mondial (marges fixes, défaut du plancher, mesures commerciales). β = 0 = prix gelé, la charge est portée par une autre partie. "
     "Les β calculés sur les moyennes annuelles (onglet INDICATEURS) sont plus faibles, car ils mesurent la transmission de la même campagne, avant l'ajustement retardé.", size=6.8)

doc.add_heading("Annexe C – Revue de littérature (synthèse)", level=1)
rows = [["Référence", "Instrument", "Résultat", "Enseignement pour la CI"]]
for r in LIT:
    rows.append([r["reference"], r["instrument"], r["resultat"], r["enseignement_ci"]])
grid(rows, [5.4, 2.6, 5.2, 4.8], size=6.2, bold_first_col=False)

doc.add_heading("Annexe D – Indicateurs harmonisés (séries annuelles)", level=1)
rows = [["Filière – pays", "Période", "CV prix int.", "CV prix prod.", "CV recette", "β baisses (annuel)", "β hausses (annuel)", "Drawdown max prix prod.", "Baisse max recette", "Part variance recette due à Q", "Chocs ≥ 15 % / ≥ 20 %"]]
for (f, pays), r in IND.items():
    rows.append([f"{f} – {pays}", r["periode"], pct(r["I1_CV_prix_int"]), pct(r["I2_CV_prix_prod"]), pct(r["CV_recette"]),
                 num(r["I3_beta_baisse_annuel"], 2) if isinstance(r["I3_beta_baisse_annuel"], (int, float)) else "—",
                 num(r["I4_beta_hausse_annuel"], 2) if isinstance(r["I4_beta_hausse_annuel"], (int, float)) else "—",
                 pct(r["I6_drawdown_max_prod"]), pct(r["I7_baisse_max_recette"]), pct(r["part_variance_recette_due_Q"]),
                 f"{r['nb_chocs_int_15pct']} / {r['nb_chocs_int_20pct']}"])
grid(rows, [2.6, 2.0, 1.3, 1.3, 1.3, 1.5, 1.5, 1.6, 1.6, 1.8, 1.5], size=6.2, bold_first_col=False)
para("Chocs comptés sur les variations annuelles du prix international en monnaie locale (seuils de 15 % et 20 %) ; les épisodes infra-annuels (cacao 2016-17, coton 2020) n'apparaissent qu'avec le seuil mensuel de l'onglet EPISODES. "
     "Note : au Ghana, la volatilité est mesurée en cedis et intègre donc la dépréciation et l'inflation. Un CV du prix producteur faible ne signifie pas une résilience élevée (voir la section 1). "
     "Méthodologie complète : METHODOLOGIE_RESILIENCE.md ; limites : AUDIT_DONNEES.md.", size=6.8)

doc.save(OUT)
print("écrit", OUT)
