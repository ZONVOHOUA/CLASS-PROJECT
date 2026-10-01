# -*- coding: utf-8 -*-
"""
Construit la base Excel traçable du benchmark (formules visibles, sources par observation).

Entrées : scripts/inputs.py + SOURCES/donnees_primaires/ (BCE, BRI, Banque mondiale).
Sortie  : Base_Prix_Benchmark_CI.xlsx (à recalculer ensuite avec LibreOffice).
"""
from pathlib import Path
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment
from openpyxl.worksheet.table import Table, TableStyleInfo

import inputs as I

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "SOURCES" / "donnees_primaires"
OUT = ROOT / "Base_Prix_Benchmark_CI.xlsx"

MONTHS = [str(p) for p in pd.period_range("2014-01", "2026-09", freq="M")]
ROW_OF = {m: i + 2 for i, m in enumerate(MONTHS)}  # ligne Excel de chaque mois (en-tête en ligne 1)

FONT = "Arial"
F_BASE = Font(name=FONT, size=10)
F_INPUT = Font(name=FONT, size=10, color="0000FF")
F_LINK = Font(name=FONT, size=10, color="008000")
F_HEAD = Font(name=FONT, size=10, bold=True, color="FFFFFF")
F_TITLE = Font(name=FONT, size=14, bold=True, color="1F3864")
F_BOLD = Font(name=FONT, size=10, bold=True)
FILL_HEAD = PatternFill("solid", fgColor="1F3864")
FILL_SUB = PatternFill("solid", fgColor="D9E2F3")
FILL_ASSUMP = PatternFill("solid", fgColor="FFF2CC")
FILL_WARN = PatternFill("solid", fgColor="FCE4D6")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

FMT_FCFA = '#,##0;(#,##0);"-"'
FMT_USD = '0.000'
FMT_PCT = '0.0%'
FMT_RATE = '#,##0.00'


def head(ws, row, labels, widths=None):
    for j, lab in enumerate(labels, start=1):
        c = ws.cell(row=row, column=j, value=lab)
        c.font, c.fill, c.alignment, c.border = F_HEAD, FILL_HEAD, CENTER, BORDER
    if widths:
        for j, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[row].height = 42


def put(ws, ref, value, font=F_BASE, fmt=None, fill=None, align=None, comment=None):
    c = ws[ref]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if align:
        c.alignment = align
    if comment:
        c.comment = Comment(comment, "Benchmark CI")
    c.border = BORDER
    return c


# ---------------------------------------------------------------------------
# Chargement des données primaires
# ---------------------------------------------------------------------------
def load_ecb():
    ecb = pd.read_csv(DATA / "BCE_eurofxref-hist.csv")
    cols = ["USD", "IDR", "MYR", "THB"]
    for c in cols:
        ecb[c] = pd.to_numeric(ecb[c], errors="coerce")
    ecb["Date"] = pd.to_datetime(ecb["Date"])
    ecb["m"] = ecb["Date"].dt.to_period("M").astype(str)
    return ecb.groupby("m")[cols].mean(), ecb.groupby("m")["Date"].max()


def load_bis():
    b = pd.read_csv(DATA / "BRI_WS_XRU_moyennes_mensuelles_extrait.csv")
    out = {}
    for area, cur in [("GH", "GHS"), ("UG", "UGX"), ("VN", "VND"), ("TZ", "TZS"), ("NG", "NGN")]:
        s = b[b.area == area].set_index("period")["value"]
        out[cur] = s.to_dict()
    return out


def load_wb():
    df = pd.read_excel(DATA / "BanqueMondiale_CMO-Historical-Data-Monthly_2026-02-03.xlsx",
                       sheet_name="Monthly Prices", header=None)
    hdr = [str(h).strip() if pd.notna(h) else "" for h in df.iloc[4].tolist()]
    d = df.iloc[6:].copy()
    d.columns = ["period"] + hdr[1:]
    d["m"] = d["period"].str.replace("M", "-")
    d = d.set_index("m")
    pick = {"cacao": "Cocoa", "robusta": "Coffee, Robusta", "coton": "Cotton, A Index",
            "tsr20": "Rubber, TSR20 **", "palme": "Palm oil", "riz": "Rice, Thai 5%"}
    out = {}
    for k, col in pick.items():
        s = pd.to_numeric(d[col], errors="coerce")
        out[k] = s.to_dict()
    return out


ECB, ECB_LAST = load_ecb()
BIS = load_bis()
WB = load_wb()

wb = Workbook()

# ---------------------------------------------------------------------------
# Lisez-moi
# ---------------------------------------------------------------------------
ws = wb.active
ws.title = "Lisez-moi"
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = 120
put(ws, "A1", "Base de données du benchmark des prix agricoles – Côte d'Ivoire", F_TITLE)
ws["A1"].border = Border()
rows = [
    ("Objet", "Traçabilité complète des prix utilisés dans la note « Les prix agricoles ivoiriens sont-ils compétitifs ? » (octobre 2026)."),
    ("Date d'arrêté des données", "1er octobre 2026 (dernières annonces : prix cacao/café 2026-27 du 01/09/2026 ; prix COCOBOD du 25/09/2026)."),
    ("Règle d'or", "Aucun graphique ni chiffre de la note n'est produit en dehors de cette base. Toutes les conversions sont des formules visibles."),
    ("Codes couleur", "Bleu = donnée saisie (prix d'origine, taux) ; noir = formule ; vert = renvoi vers un autre onglet ; fond jaune = paramètre ou hypothèse à valider."),
    ("Fiabilité", "A = source officielle primaire ; B = presse/agence reprenant une annonce officielle datée ; C = source secondaire, commerciale ou approximation (indicatif)."),
    ("Observations", "Une ligne par prix : produit, qualité, stade, campagne, pays, monnaie, unité, prix d'origine, taux de change de la même période, prix FCFA/kg, référence internationale, taux de transmission, source, URL, date de consultation, remarque."),
    ("Change_mensuel / Change_periodes", "Taux mensuels (BCE pour l'euro et donc le FCFA ; BRI et banques centrales pour les autres monnaies) et moyennes exactes de chaque période de comparaison."),
    ("Cours_mensuels / Cours_periodes", "Cours internationaux mensuels (Banque mondiale « Pink Sheet » jusqu'en janvier 2026, compléments FMI/OIC/SGX ensuite) et moyennes par période."),
    ("Cacao_transmission", "Série 2016/17-2026/27 par demi-campagne : prix CI, prix Ghana, cours mondial, taux de transmission."),
    ("Series_CI", "Prix officiels ivoiriens sur 10 campagnes, en nominal et en FCFA constants 2025 ; coefficients de variation."),
    ("Indicateurs", "Comparaisons deux à deux (écart absolu, écart relatif, indice, transmission) et médianes des comparateurs."),
    ("Decomposition", "Décomposition de la valeur (cacao, anacarde, caoutchouc, palmier)."),
    ("Positionnement / Volumes_Rendements", "Données du graphique de positionnement et revenu brut à l'hectare."),
    ("Matrice", "Matrice de synthèse reprise dans la note."),
    ("Audit_QC", "Contrôle de comparabilité de chaque comparaison (période, produit, qualité, stade, unité, monnaie, référence, source, politique publique, fiscalité)."),
    ("Sources", "Référentiel des sources : institution, titre, URL, type, fiabilité, date de consultation."),
    ("Limites d'accès", "L'environnement de production n'autorisait pas le téléchargement direct (FAOSTAT, Comtrade, Eurostat, API Banque mondiale). Les fichiers primaires utilisés sont archivés dans SOURCES/donnees_primaires ; les autres chiffres proviennent des pages citées (URL)."),
]
for i, (a, b) in enumerate(rows, start=3):
    put(ws, f"A{i}", a, F_BOLD, align=WRAP)
    put(ws, f"B{i}", b, align=WRAP)

# ---------------------------------------------------------------------------
# Paramètres
# ---------------------------------------------------------------------------
wp = wb.create_sheet("Parametres")
put(wp, "A1", "Paramètres techniques (modifiables)", F_TITLE)
wp["A1"].border = Border()
head(wp, 2, ["", "Paramètre", "Valeur", "Source / justification", "URL"], [3, 46, 14, 80, 60])
for ref, lab, val, srcx, url in I.PARAMS:
    r = int(ref[1:])
    put(wp, f"B{r}", lab)
    put(wp, ref, val, F_INPUT, fill=FILL_ASSUMP, fmt="0.0000")
    put(wp, f"D{r}", srcx, align=WRAP)
    put(wp, f"E{r}", url, align=WRAP)

# ---------------------------------------------------------------------------
# Change mensuel
# ---------------------------------------------------------------------------
wc = wb.create_sheet("Change_mensuel")
labels = ["Mois", "USD par EUR (BCE, moy. mens.)", "XOF par USD", "GHS par USD", "UGX par USD", "VND par USD",
          "TZS par USD", "NGN par USD", "IDR par EUR (BCE)", "IDR par USD", "THB par EUR (BCE)", "THB par USD",
          "MYR par EUR (BCE)", "MYR par USD", "USD par USD", "XAF par USD", "Notes (compléments hors BCE/BRI)"]
head(wc, 1, labels, [9, 13, 11, 11, 11, 11, 11, 11, 12, 11, 11, 10, 11, 10, 8, 10, 70])
CUR_COL = {"GHS": "D", "UGX": "E", "VND": "F", "TZS": "G", "NGN": "H"}
for m in MONTHS:
    r = ROW_OF[m]
    put(wc, f"A{r}", m)
    if m in ECB.index and pd.notna(ECB.loc[m, "USD"]):
        put(wc, f"B{r}", round(float(ECB.loc[m, "USD"]), 6), F_INPUT, "0.0000")
        put(wc, f"C{r}", f"=Parametres!$C$3/B{r}", fmt=FMT_RATE)
        for c_eur, c_usd, cur in (("I", "J", "IDR"), ("K", "L", "THB"), ("M", "N", "MYR")):
            put(wc, f"{c_eur}{r}", round(float(ECB.loc[m, cur]), 4), F_INPUT, FMT_RATE)
            put(wc, f"{c_usd}{r}", f"={c_eur}{r}/B{r}", fmt=FMT_RATE)
    put(wc, f"O{r}", 1, fmt="0")
    put(wc, f"P{r}", f"=C{r}", fmt=FMT_RATE)
    notes = []
    if m == ECB.index.max() and ECB_LAST[m].day < 25:  # dernier mois du fichier BCE incomplet
        notes.append(f"BCE : moyenne partielle du 1er au {ECB_LAST[m]:%d/%m/%Y} (dernier taux du fichier) [A]")
    for cur, col in CUR_COL.items():
        sup = I.SUPP_CHANGE.get(cur, {}).get(m)
        if sup:
            put(wc, f"{col}{r}", sup[0], F_INPUT, FMT_RATE, fill=FILL_WARN if sup[2] == "C" else None,
                comment=f"{sup[1]} (fiabilité {sup[2]}) – {I.SUPP_CHANGE_URL[cur]}")
            notes.append(f"{cur} : {sup[1]} [{sup[2]}]")
        else:
            v = BIS[cur].get(m)
            if v is not None and not pd.isna(v):
                put(wc, f"{col}{r}", round(float(v), 4), F_INPUT, FMT_RATE)
    if notes:
        put(wc, f"Q{r}", " | ".join(notes), align=WRAP)
wc.freeze_panes = "B2"
put(wc, f"A{len(MONTHS)+3}", "Sources : BCE (taux de référence quotidiens, moyenne mensuelle calculée) ; BRI WS_XRU (moyennes mensuelles) ; compléments documentés en colonne Q.", F_BOLD)

# ---------------------------------------------------------------------------
# Change périodes
# ---------------------------------------------------------------------------
wcp = wb.create_sheet("Change_periodes")
cur_list = ["XOF", "GHS", "UGX", "VND", "TZS", "NGN", "IDR", "THB", "MYR", "USD", "XAF"]
src_col = {"XOF": "C", "GHS": "D", "UGX": "E", "VND": "F", "TZS": "G", "NGN": "H", "IDR": "J", "THB": "L",
           "MYR": "N", "USD": "O", "XAF": "P"}
head(wcp, 1, ["Code période", "Début", "Fin"] + cur_list + ["Nb mois GHS"], [18, 9, 9] + [10] * 11 + [10])
fx_codes = sorted({o["fx"] for o in I.OBS if not str(o["fx"]).startswith("=")})
FX_ROW = {}
for k, code in enumerate(fx_codes, start=2):
    d, f = code.split(":")
    FX_ROW[code] = k
    put(wcp, f"A{k}", code)
    put(wcp, f"B{k}", d)
    put(wcp, f"C{k}", f)
    r1, r2 = ROW_OF[d], ROW_OF[f]
    for j, cur in enumerate(cur_list):
        col = get_column_letter(4 + j)
        sc = src_col[cur]
        put(wcp, f"{col}{k}", f'=IFERROR(AVERAGE(Change_mensuel!{sc}{r1}:{sc}{r2}),"")', F_LINK, FMT_RATE)
    put(wcp, f"O{k}", f"=COUNT(Change_mensuel!D{r1}:D{r2})", F_LINK, "0")
wcp.freeze_panes = "D2"

# ---------------------------------------------------------------------------
# Cours mensuels
# ---------------------------------------------------------------------------
wm = wb.create_sheet("Cours_mensuels")
SERIES = [("cacao", "Cacao ICCO (USD/kg)"), ("robusta", "Café robusta (USD/kg)"), ("coton", "Coton indice A (USD/kg)"),
          ("tsr20", "Caoutchouc TSR20 (USD/kg)"), ("palme", "Huile de palme (USD/t)"), ("riz", "Riz Thaï 5 % (USD/t)")]
labels = ["Mois"]
for _, lab in SERIES:
    labels += [lab, "Source"]
head(wm, 1, labels, [9] + [12, 9] * len(SERIES))
SER_COL = {}
for j, (key, _) in enumerate(SERIES):
    SER_COL[key] = get_column_letter(2 + 2 * j)
for m in MONTHS:
    r = ROW_OF[m]
    put(wm, f"A{r}", m)
    for key, _ in SERIES:
        col = SER_COL[key]
        scol = get_column_letter(openpyxl_col := (ord(col) - 64) + 1) if len(col) == 1 else None
        sup = I.SUPP_COURS.get(key, {}).get(m)
        fmt = "#,##0.00" if key in ("palme", "riz") else FMT_USD
        if sup:
            put(wm, f"{col}{r}", sup[0], F_INPUT, fmt, comment=f"{sup[1]} – {sup[2]} (fiabilité {sup[3]})")
            put(wm, f"{scol}{r}", "FMI/OIC/SGX" if sup[3] == "A" else "Autre (B)")
        else:
            v = WB[key].get(m)
            if v is not None and not pd.isna(v):
                put(wm, f"{col}{r}", round(float(v), 6), F_INPUT, fmt)
                put(wm, f"{scol}{r}", "BM")
wm.freeze_panes = "B2"
put(wm, f"A{len(MONTHS)+3}", "BM = Banque mondiale, CMO Historical Data Monthly (mise à jour 03/02/2026). Compléments 2026 : FMI PCPS, OIC (Coffee Market Report), SGX (rapport mensuel SICOM) – voir commentaires de cellule.", F_BOLD)

# ---------------------------------------------------------------------------
# Cours périodes
# ---------------------------------------------------------------------------
wmp = wb.create_sheet("Cours_periodes")
head(wmp, 1, ["Code", "Série", "Début", "Fin", "Moyenne (USD/kg ou USD/t)", "Nb mois disponibles", "Nb mois de la période"],
     [26, 10, 9, 9, 16, 12, 12])
per_codes = sorted({o["prix"][1] for o in I.OBS if isinstance(o["prix"], tuple)})
PER_ROW = {}
for k, code in enumerate(per_codes, start=2):
    serie, d, f = code.split(":")
    PER_ROW[code] = k
    col = SER_COL[serie]
    r1, r2 = ROW_OF[d], ROW_OF[f]
    put(wmp, f"A{k}", code)
    put(wmp, f"B{k}", serie)
    put(wmp, f"C{k}", d)
    put(wmp, f"D{k}", f)
    put(wmp, f"E{k}", f'=IFERROR(AVERAGE(Cours_mensuels!{col}{r1}:{col}{r2}),"")', F_LINK, "#,##0.000")
    put(wmp, f"F{k}", f"=COUNT(Cours_mensuels!{col}{r1}:{col}{r2})", F_LINK, "0")
    put(wmp, f"G{k}", r2 - r1 + 1, fmt="0")
wmp.freeze_panes = "B2"

# ---------------------------------------------------------------------------
# Observations
# ---------------------------------------------------------------------------
wo = wb.create_sheet("Observations")
OBS_HEAD = ["ID", "Filière", "Produit exact", "Pays", "Année / campagne", "Période couverte", "Type de prix",
            "Stade de commercialisation", "Qualité / spécification", "Prix original", "Monnaie", "Unité d'origine",
            "kg par unité", "Code période (change)", "Taux de change (monnaie / USD)", "Source du taux de change",
            "Taux FCFA / USD (même période)", "Prix USD/kg", "Prix FCFA/kg", "Facteur d'équivalence",
            "Base de comparaison", "Prix FCFA/kg (base de comparaison)", "ID référence internationale",
            "Prix international de référence (FCFA/kg)", "Taux de transmission", "ID valeur FOB/CAF nationale",
            "Valeur FOB/CAF (FCFA/kg)", "Part producteur dans FOB/CAF", "Source", "URL", "Date de consultation",
            "Fiabilité", "Remarque méthodologique"]
head(wo, 1, OBS_HEAD, [20, 11, 24, 13, 11, 20, 22, 20, 20, 12, 8, 11, 8, 15, 12, 24, 11, 10, 11, 9, 18, 12, 18, 12,
                       10, 16, 11, 10, 34, 40, 11, 8, 50])
OBS_ROW = {}
for k, o in enumerate(I.OBS, start=2):
    OBS_ROW[o["id"]] = k
nrow_last = len(I.OBS) + 1
for o in I.OBS:
    k = OBS_ROW[o["id"]]
    s = I.S[o["source"]]
    put(wo, f"A{k}", o["id"], F_BOLD)
    for col, key in zip("BCDEFGHI", ["filiere", "produit", "pays", "campagne", "periode", "type_prix", "stade", "qualite"]):
        put(wo, f"{col}{k}", o[key], align=WRAP)
    # prix original
    if isinstance(o["prix"], tuple):
        code = o["prix"][1]
        put(wo, f"J{k}", f'=INDEX(Cours_periodes!$E$1:$E$400,MATCH("{code}",Cours_periodes!$A$1:$A$400,0))', F_LINK, "#,##0.000")
    else:
        put(wo, f"J{k}", o["prix"], F_INPUT, "#,##0.00")
    put(wo, f"K{k}", o["monnaie"])
    put(wo, f"L{k}", o["unite"])
    put(wo, f"M{k}", o["kg"], F_INPUT, "#,##0.0000")
    fx = str(o["fx"])
    put(wo, f"N{k}", fx)
    put(wo, f"O{k}", f'=IF(K{k}="USD",1,INDEX(Change_periodes!$D$1:$N$400,MATCH($N{k},Change_periodes!$A$1:$A$400,0),MATCH($K{k},Change_periodes!$D$1:$N$1,0)))',
        F_LINK, "#,##0.000")
    fxsrc = {"XOF": "BCE (parité fixe 655,957 FCFA/EUR)", "XAF": "BCE (parité fixe 655,957 FCFA/EUR)", "USD": "—",
             "GHS": "BRI / Banque du Ghana (moyenne de période)", "UGX": "BRI ; juil. 2026 : source secondaire (C)",
             "VND": "BRI ; sept. 2026 : Vietcombank", "TZS": "UBA Tanzania (approximation, C)", "NGN": "Implicite source (C)",
             "IDR": "BCE (taux croisé)", "THB": "BCE (taux croisé)", "MYR": "BCE (taux croisé)"}[o["monnaie"]]
    put(wo, f"P{k}", fxsrc, align=WRAP)
    put(wo, f"Q{k}", f'=INDEX(Change_periodes!$D$1:$D$400,MATCH($N{k},Change_periodes!$A$1:$A$400,0))', F_LINK, FMT_RATE)
    put(wo, f"R{k}", f'=IFERROR(J{k}/M{k}/O{k},"")', fmt="0.0000")
    put(wo, f"S{k}", f'=IFERROR(R{k}*Q{k},"")', fmt=FMT_FCFA)
    eq = o.get("equiv", 1)
    put(wo, f"T{k}", eq, F_INPUT if not str(eq).startswith("=") else F_LINK, "0.000")
    put(wo, f"U{k}", o.get("equiv_label") or "FCFA/kg de produit tel que vendu", align=WRAP)
    put(wo, f"V{k}", f'=IFERROR(S{k}/T{k},"")', fmt=FMT_FCFA)
    put(wo, f"W{k}", o["ref"])
    put(wo, f"X{k}", f'=IF(W{k}="","",IFERROR(INDEX($V$1:$V${nrow_last},MATCH(W{k},$A$1:$A${nrow_last},0)),""))', fmt=FMT_FCFA)
    put(wo, f"Y{k}", f'=IF(OR(X{k}="",V{k}=""),"",V{k}/X{k})', fmt=FMT_PCT)
    put(wo, f"Z{k}", o["fob"])
    put(wo, f"AA{k}", f'=IF(Z{k}="","",IFERROR(INDEX($V$1:$V${nrow_last},MATCH(Z{k},$A$1:$A${nrow_last},0)),""))', fmt=FMT_FCFA)
    put(wo, f"AB{k}", f'=IF(OR(AA{k}="",V{k}=""),"",V{k}/AA{k})', fmt=FMT_PCT)
    put(wo, f"AC{k}", f"{s['institution']} – {s['titre']}", align=WRAP)
    put(wo, f"AD{k}", s["url"], align=WRAP)
    put(wo, f"AE{k}", I.DATE_CONSULT)
    put(wo, f"AF{k}", s["fiabilite"], fill=FILL_WARN if s["fiabilite"] == "C" else None, align=CENTER)
    put(wo, f"AG{k}", o.get("remarque", ""), align=WRAP)
wo.freeze_panes = "B2"
wo.auto_filter.ref = f"A1:AG{nrow_last}"


def OBSREF(oid, col):
    """Référence Excel vers une colonne de l'onglet Observations pour un ID donné."""
    return f"Observations!${col}${OBS_ROW[oid]}"


# ---------------------------------------------------------------------------
# Cacao : transmission par demi-campagne
# ---------------------------------------------------------------------------
wt = wb.create_sheet("Cacao_transmission")
put(wt, "A1", "Cacao – prix producteur Côte d'Ivoire vs Ghana vs cours mondial (FCFA/kg, même demi-campagne)", F_TITLE)
wt["A1"].border = Border()
head(wt, 3, ["Campagne", "Demi-campagne", "Prix CI (FCFA/kg)", "Prix Ghana (FCFA/kg)", "Cours mondial ICCO (FCFA/kg)",
             "Transmission CI", "Transmission Ghana", "Indice CI (Ghana = 100)", "FCFA/USD", "GHS/USD"],
     [11, 22, 13, 13, 15, 12, 12, 13, 10, 10])
r = 4
TRANS_ROWS = []
for camp, *_ in I.CACAO_CI:
    for h, lab in (("P", "Principale (oct.-mars)"), ("I", "Intermédiaire (avr.-sept.)")):
        ci, gh = f"CAC-CI-{camp}-{h}", f"CAC-GH-{camp}-{h}"
        put(wt, f"A{r}", camp)
        put(wt, f"B{r}", lab)
        put(wt, f"C{r}", f"={OBSREF(ci, 'S')}", F_LINK, FMT_FCFA)
        put(wt, f"D{r}", f"={OBSREF(gh, 'S')}", F_LINK, FMT_FCFA)
        put(wt, f"E{r}", f"={OBSREF(ci, 'X')}", F_LINK, FMT_FCFA)
        put(wt, f"F{r}", f"=C{r}/E{r}", fmt=FMT_PCT)
        put(wt, f"G{r}", f"=D{r}/E{r}", fmt=FMT_PCT)
        put(wt, f"H{r}", f"=C{r}/D{r}*100", fmt="0")
        put(wt, f"I{r}", f"={OBSREF(ci, 'Q')}", F_LINK, FMT_RATE)
        put(wt, f"J{r}", f"={OBSREF(gh, 'O')}", F_LINK, FMT_RATE)
        TRANS_ROWS.append(r)
        r += 1
# 2026/27
put(wt, f"A{r}", "2026/27")
put(wt, f"B{r}", "Ouverture (cours d'août 2026)")
put(wt, f"C{r}", f"={OBSREF('CAC-CI-2026/27-P', 'S')}", F_LINK, FMT_FCFA)
put(wt, f"D{r}", f"={OBSREF('CAC-GH-2026/27-P', 'S')}", F_LINK, FMT_FCFA)
put(wt, f"E{r}", f"={OBSREF('CAC-CI-2026/27-P', 'X')}", F_LINK, FMT_FCFA)
put(wt, f"F{r}", f"=C{r}/E{r}", fmt=FMT_PCT)
put(wt, f"G{r}", f"=D{r}/E{r}", fmt=FMT_PCT)
put(wt, f"H{r}", f"=C{r}/D{r}*100", fmt="0")
put(wt, f"I{r}", f"={OBSREF('CAC-CI-2026/27-P', 'Q')}", F_LINK, FMT_RATE)
put(wt, f"J{r}", f"={OBSREF('CAC-GH-2026/27-P', 'O')}", F_LINK, FMT_RATE)
ROW_2627 = r
r += 2
first, last = TRANS_ROWS[0], TRANS_ROWS[-1]
last3_first = TRANS_ROWS[-6]
SUMROWS = {}
for lab, a, b in (("Moyenne 10 campagnes (2016/17-2025/26)", first, last),
                  ("Moyenne 3 dernières campagnes (2023/24-2025/26)", last3_first, last)):
    put(wt, f"A{r}", lab, F_BOLD)
    for col, fmt in (("C", FMT_FCFA), ("D", FMT_FCFA), ("E", FMT_FCFA), ("F", FMT_PCT), ("G", FMT_PCT), ("H", "0")):
        put(wt, f"{col}{r}", f"=AVERAGE({col}{a}:{col}{b})", F_BOLD, fmt)
    SUMROWS[lab] = r
    r += 1
put(wt, f"A{r}", "Coefficient de variation 10 campagnes", F_BOLD)
for col in "CDE":
    put(wt, f"{col}{r}", f"=STDEV({col}{first}:{col}{last})/AVERAGE({col}{first}:{col}{last})", F_BOLD, FMT_PCT)
ROW_CV_CAC = r
r += 2
put(wt, f"A{r}", "Lecture : la transmission rapporte le prix bord champ au cours mondial moyen de la même demi-campagne (méthode identique pour les deux pays). "
               "Les prix ivoiriens reposent sur des ventes anticipées conclues plusieurs mois avant la campagne (mars-juin 2026 pour 2026/27, source CI_CAC_VENTES) : un décalage est structurel. "
               "Demi-campagne intermédiaire 2025/26 : cours moyen avr.-août 2026 (septembre non encore publié).", align=WRAP)
wt.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
wt.row_dimensions[r].height = 45
wt.freeze_panes = "C4"

# ---------------------------------------------------------------------------
# Séries CI (nominal, réel, volatilité)
# ---------------------------------------------------------------------------
wsr = wb.create_sheet("Series_CI")
put(wsr, "A1", "Prix officiels ivoiriens : 10 campagnes, nominal et réel (FCFA constants 2025)", F_TITLE)
wsr["A1"].border = Border()
head(wsr, 3, ["Année d'ouverture", "Inflation CI (%)", "Indice des prix (2015 = 100)", "Source inflation",
              "Cacao principale", "Cacao intermédiaire", "Café", "Anacarde", "Coton graine",
              "Cacao princ. (FCFA 2025)", "Café (FCFA 2025)", "Anacarde (FCFA 2025)", "Coton (FCFA 2025)",
              "Cours cacao (FCFA/kg, princ.)", "Cours robusta (FCFA/kg, camp.)"],
     [10, 10, 12, 32, 11, 11, 10, 10, 10, 12, 11, 11, 11, 13, 13])
put(wsr, "A4", 2015)
put(wsr, "C4", 100, F_INPUT, "0.0")
YR_ROW = {2015: 4}
infl = {y: (v, s_, u) for y, v, s_, u in I.INFLATION_CI}
for y in range(2016, 2027):
    rr = 4 + (y - 2015)
    YR_ROW[y] = rr
    put(wsr, f"A{rr}", y)
    if y in infl:
        put(wsr, f"B{rr}", infl[y][0], F_INPUT, "0.00")
        put(wsr, f"C{rr}", f"=C{rr-1}*(1+B{rr}/100)", fmt="0.0")
        put(wsr, f"D{rr}", infl[y][1], align=WRAP, comment=infl[y][2])
    else:
        put(wsr, f"B{rr}", "n.d.", fill=FILL_WARN)
        put(wsr, f"C{rr}", f"=C{rr-1}", fmt="0.0", fill=FILL_WARN,
            comment="IPC 2026 non disponible : niveau 2025 conservé (aucune extrapolation)")
        put(wsr, f"D{rr}", "IPC 2026 non publié : niveau 2025 conservé", align=WRAP)
    camp = f"{y}/{str(y+1)[2:]}"
    def cell_or_nd(oid, col_letter, target):
        if oid in OBS_ROW:
            put(wsr, f"{target}{rr}", f"={OBSREF(oid, col_letter)}", F_LINK, FMT_FCFA)
        else:
            put(wsr, f"{target}{rr}", "n.d.", fill=FILL_WARN)
    cell_or_nd(f"CAC-CI-{camp}-P" if y < 2026 else "CAC-CI-2026/27-P", "S", "E")
    cell_or_nd(f"CAC-CI-{camp}-I", "S", "F")
    cell_or_nd(f"CAF-CI-{camp}" if y < 2026 else "CAF-CI-2026/27", "S", "G")
    cell_or_nd(f"ANA-CI-{y}", "S", "H")
    cell_or_nd(f"COT-CI-{camp}", "S", "I")
    for src_c, dst_c in (("E", "J"), ("G", "K"), ("H", "L"), ("I", "M")):
        put(wsr, f"{dst_c}{rr}", f'=IF(ISNUMBER({src_c}{rr}),{src_c}{rr}*$C${4+10}/C{rr},"n.d.")', fmt=FMT_FCFA)
    cell_or_nd(f"CAC-CI-{camp}-P" if y < 2026 else "CAC-CI-2026/27-P", "X", "N")
    cell_or_nd(f"CAF-CI-{camp}" if y < 2026 else "CAF-CI-2026/27", "X", "O")
rr = YR_ROW[2026] + 2
SER_SUM = {}
put(wsr, f"A{rr}", "Variation 2016→2025 (nominal)", F_BOLD)
for c in "EGHI":
    put(wsr, f"{c}{rr}", f'=IFERROR({c}{YR_ROW[2025]}/{c}{YR_ROW[2016] if c != "I" else YR_ROW[2017]}-1,"")', F_BOLD, FMT_PCT)
SER_SUM["var_nom"] = rr
rr += 1
put(wsr, f"A{rr}", "Variation 2016→2025 (réel)", F_BOLD)
for c in "JKLM":
    put(wsr, f"{c}{rr}", f'=IFERROR({c}{YR_ROW[2025]}/{c}{YR_ROW[2016] if c != "M" else YR_ROW[2017]}-1,"")', F_BOLD, FMT_PCT)
SER_SUM["var_reel"] = rr
rr += 1
put(wsr, f"A{rr}", "Variation 2016→2026 (dernier prix connu, nominal)", F_BOLD)
for c in "EGH":
    put(wsr, f"{c}{rr}", f'=IFERROR({c}{YR_ROW[2026]}/{c}{YR_ROW[2016]}-1,"")', F_BOLD, FMT_PCT)
SER_SUM["var_nom26"] = rr
rr += 1
put(wsr, f"A{rr}", "Variation 2016→2026 (dernier prix connu, réel)", F_BOLD)
for c in "JKL":
    put(wsr, f"{c}{rr}", f'=IFERROR({c}{YR_ROW[2026]}/{c}{YR_ROW[2016]}-1,"")', F_BOLD, FMT_PCT)
SER_SUM["var_reel26"] = rr
rr += 1
put(wsr, f"A{rr}", "Coefficient de variation 2016-2025", F_BOLD)
for c in "EGHINO":
    a = YR_ROW[2016] if c != "I" else YR_ROW[2017]
    put(wsr, f"{c}{rr}", f"=STDEV({c}{a}:{c}{YR_ROW[2025]})/AVERAGE({c}{a}:{c}{YR_ROW[2025]})", F_BOLD, FMT_PCT)
SER_SUM["cv"] = rr
rr += 2
put(wsr, f"A{rr}", "Notes : prix d'ouverture de campagne (le prix intermédiaire du cacao est en colonne F). Déflateur : IPC Côte d'Ivoire de l'année d'ouverture. "
                 "Coton : série disponible à partir de 2017/18. Café 2016/17 déduit du maintien à 750 FCFA en 2017/18.", align=WRAP)
wsr.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=15)
wsr.row_dimensions[rr].height = 40
wsr.freeze_panes = "B4"

# ---------------------------------------------------------------------------
# Indicateurs (comparaisons deux à deux)
# ---------------------------------------------------------------------------
wi = wb.create_sheet("Indicateurs")
put(wi, "A1", "Indicateurs de compétitivité-prix : comparaisons deux à deux (même produit, même stade, même période)", F_TITLE)
wi["A1"].border = Border()
head(wi, 3, ["Filière", "Comparaison", "ID Côte d'Ivoire", "ID comparateur", "Prix CI (FCFA/kg)", "Prix comparateur (FCFA/kg)",
             "I. Écart absolu (FCFA/kg)", "II. Écart relatif", "Indice CI (comparateur = 100)", "IV. Transmission CI",
             "IV. Transmission comparateur", "Comparabilité", "Commentaire"],
     [11, 40, 18, 18, 12, 13, 12, 10, 12, 11, 12, 12, 60])
PAIRS = [
    # filière, libellé, ci, comp, comparabilité, commentaire
    ("Cacao", "Ghana – ouverture 2026/27", "CAC-CI-2026/27-P", "CAC-GH-2026/27-P", "Directe", "Deux prix administrés, même grade, même date ; Ghana = 71 % du FOB réalisé (Act 1182)"),
    ("Cacao", "Ghana – campagne principale 2025/26", "CAC-CI-2025/26-P", "CAC-GH-2025/26-P", "Directe", "Prix d'ouverture ; Ghana ramené à 41 392 GH¢/t au 12/02/2026"),
    ("Cacao", "Ghana – campagne intermédiaire 2025/26", "CAC-CI-2025/26-I", "CAC-GH-2025/26-I", "Directe", ""),
    ("Cacao", "Cameroun – mars-avril 2026 (marché libéralisé)", "CAC-CI-2025/26-I", "CAC-CM-2026-04", "Indicative", "Prix de marché relevé (fourchette) vs prix garanti"),
    ("Cacao", "Cameroun – fin juin 2026", "CAC-CI-2025/26-I", "CAC-CM-2026-06", "Indicative", "Le marché libéralisé suit le cours mondial avec peu de retard"),
    ("Cacao", "Nigeria – sept. 2026 (source secondaire)", "CAC-CI-2026/27-P", "CAC-NG-2026-09", "Indicative", "Source C : à confirmer"),
    ("Cacao", "Équateur – février 2026", "CAC-CI-2025/26-P", "CAC-EC-2026-02", "Indicative", "Qualités différentes (CCN-51/Nacional)"),
    ("Café", "Vietnam – fin sept. 2026", "CAF-CI-2026/27", "CAF-VN-2026-09", "Directe", "Café vert robusta, prix bord champ/collecteur"),
    ("Café", "Ouganda – juillet 2026", "CAF-CI-2025/26", "CAF-UG-2026-07", "Directe", "FAQ ≈ café vert non classé ; taux de change de source C"),
    ("Anacarde", "Burkina Faso – 2026", "ANA-CI-2026", "ANA-BF-2026", "Directe", "Deux prix planchers, même devise"),
    ("Anacarde", "Guinée-Bissau – 2026", "ANA-CI-2026", "ANA-GW-2026", "Directe", "Prix de référence producteur"),
    ("Anacarde", "Ghana – 2026", "ANA-CI-2026", "ANA-GH-2026", "Directe", "Prix minimum ; respect effectif non documenté"),
    ("Anacarde", "Tanzanie – 2025/26 (enchères)", "ANA-CI-2026", "ANA-TZ-2025/26", "Indicative", "Saison et qualité (KOR) différentes ; prix d'enchère en magasin primaire"),
    ("Anacarde", "Mali – 2025", "ANA-CI-2025", "ANA-ML-2025", "Directe", "Même année (2025)"),
    ("Coton", "Burkina Faso – 2025/26", "COT-CI-2025/26", "COT-BF-2025/26", "Directe", "Prix administrés, même qualité (1er choix)"),
    ("Coton", "Mali – 2025/26", "COT-CI-2025/26", "COT-ML-2025/26", "Directe", ""),
    ("Coton", "Bénin – 2025/26", "COT-CI-2025/26", "COT-BJ-2025/26", "Directe", "Coton conventionnel"),
    ("Coton", "Togo – 2025/26", "COT-CI-2025/26", "COT-TG-2025/26", "Directe", "Source C"),
    ("Coton", "Sénégal – 2025/26", "COT-CI-2025/26", "COT-SN-2025/26", "Indicative", "« Jusqu'à 350 FCFA » : source C"),
    ("Caoutchouc", "Thaïlande – mai 2025 (base sèche)", "CAO-CI-2025-04", "CAO-TH-2025-05", "Indicative", "CI converti en kg sec (DRC 60 %) ; un mois d'écart"),
    ("Caoutchouc", "Indonésie – août/sept. 2026 (base sèche)", "CAO-CI-2026-09", "CAO-ID-2026-08", "Indicative", "Prix de référence provincial ; un mois d'écart"),
    ("Palmier à huile", "Indonésie (Riau) – janvier 2026", "PAL-CI-FFB-2026-01", "PAL-ID-FFB-2026-01", "Indicative", "Bord champ (CI) vs livraison usine (Riau)"),
    ("Palmier à huile", "Malaisie – 2025 vs CI janv. 2026", "PAL-CI-FFB-2026-01", "PAL-MY-FFB-2025", "Indicative", "Périodes proches mais différentes"),
    ("Riz", "Sénégal – 2025", "RIZ-CI-2025", "RIZ-SN-2025", "Directe", "Prix producteur fixé (130) ; usiniers 160 avec subvention"),
    ("Riz", "Vietnam – fin 2025 (paddy frais)", "RIZ-CI-2025", "RIZ-VN-2025", "Indicative", "Paddy frais (humide) vs paddy sec"),
]
r = 4
PAIR_ROW = {}
for fil, lab, ci, comp, compar, com in PAIRS:
    put(wi, f"A{r}", fil)
    put(wi, f"B{r}", lab, align=WRAP)
    put(wi, f"C{r}", ci)
    put(wi, f"D{r}", comp)
    pc = "V" if fil == "Caoutchouc" else "S"  # caoutchouc : base kg sec ; autres : produit tel que vendu
    put(wi, f"E{r}", f"={OBSREF(ci, pc)}", F_LINK, FMT_FCFA)
    put(wi, f"F{r}", f"={OBSREF(comp, pc)}", F_LINK, FMT_FCFA)
    put(wi, f"G{r}", f"=E{r}-F{r}", fmt=FMT_FCFA)
    put(wi, f"H{r}", f"=E{r}/F{r}-1", fmt=FMT_PCT)
    put(wi, f"I{r}", f"=E{r}/F{r}*100", fmt="0")
    put(wi, f"J{r}", f"={OBSREF(ci, 'Y')}", F_LINK, FMT_PCT)
    put(wi, f"K{r}", f"={OBSREF(comp, 'Y')}", F_LINK, FMT_PCT)
    put(wi, f"L{r}", compar, fill=FILL_WARN if compar != "Directe" else None)
    put(wi, f"M{r}", com, align=WRAP)
    PAIR_ROW[(fil, lab)] = r
    r += 1
r += 1
put(wi, f"A{r}", "III. Position relative : médiane des comparateurs directs de la même période (à défaut de comparateur direct : médiane des comparateurs indicatifs, résultat indicatif)", F_BOLD)
r += 1
head(wi, r, ["Filière", "Période de référence", "ID CI", "Statut du benchmark", "Prix CI (FCFA/kg)", "Médiane comparateurs (FCFA/kg)",
             "Écart absolu", "Écart relatif", "Indice CI (médiane = 100)", "Transmission CI", "Médiane transmission comparateurs",
             "Nb comparateurs", "Comparateurs retenus"])
r += 1
MED_ROW = {}
MED_DEF = [
    ("Cacao", "Ouverture 2026/27", "CAC-CI-2026/27-P", ["CAC-GH-2026/27-P"], "Directs",
     "Ghana (seul comparateur direct à la même date ; Nigeria sept. 2026 exclu : source C, comparaison indicative)"),
    ("Café", "Sept. 2026 (CI 2026/27)", "CAF-CI-2026/27", ["CAF-VN-2026-09", "CAF-UG-2026-07"], "Directs", "Vietnam (sept. 2026), Ouganda (juil. 2026)"),
    ("Anacarde", "Campagne 2026", "ANA-CI-2026", ["ANA-BF-2026", "ANA-GW-2026", "ANA-GH-2026"], "Directs",
     "Burkina, Guinée-Bissau, Ghana (Tanzanie exclue : saison, qualité et stade différents, comparaison indicative)"),
    ("Coton", "Campagne 2025/26", "COT-CI-2025/26", ["COT-BF-2025/26", "COT-ML-2025/26", "COT-BJ-2025/26", "COT-TG-2025/26"], "Directs",
     "Burkina, Mali, Bénin, Togo (Sénégal exclu : comparaison indicative)"),
    ("Caoutchouc", "2025-2026 (base sèche)", "CAO-CI-2026-09", ["CAO-TH-2025-05", "CAO-ID-2026-08"], "Indicatifs (aucun direct)",
     "Thaïlande (mai 2025), Indonésie (août 2026)"),
    ("Palmier à huile", "Janv. 2026 / 2025", "PAL-CI-FFB-2026-01", ["PAL-ID-FFB-2026-01", "PAL-MY-FFB-2025"], "Indicatifs (aucun direct)",
     "Indonésie (Riau), Malaisie"),
    ("Riz", "2025", "RIZ-CI-2025", ["RIZ-SN-2025"], "Directs", "Sénégal (Vietnam exclu : paddy frais, comparaison indicative)"),
]
for fil, per, ci, comps, statut, lab in MED_DEF:
    put(wi, f"A{r}", fil, F_BOLD)
    put(wi, f"B{r}", per)
    put(wi, f"C{r}", ci)
    put(wi, f"D{r}", statut, fill=FILL_WARN if statut != "Directs" else None)
    pc = "V" if fil == "Caoutchouc" else "S"
    put(wi, f"E{r}", f"={OBSREF(ci, pc)}", F_LINK, FMT_FCFA)
    refs = ",".join(OBSREF(c, pc) for c in comps)
    put(wi, f"F{r}", f"=MEDIAN({refs})", F_LINK, FMT_FCFA)
    put(wi, f"G{r}", f"=E{r}-F{r}", fmt=FMT_FCFA)
    put(wi, f"H{r}", f"=E{r}/F{r}-1", fmt=FMT_PCT)
    put(wi, f"I{r}", f"=E{r}/F{r}*100", fmt="0")
    put(wi, f"J{r}", f"={OBSREF(ci, 'Y')}", F_LINK, FMT_PCT)
    trefs = ",".join(OBSREF(c, "Y") for c in comps)
    put(wi, f"K{r}", f'=IFERROR(MEDIAN({trefs}),"")', F_LINK, FMT_PCT)
    put(wi, f"L{r}", len(comps), fmt="0")
    put(wi, f"M{r}", lab, align=WRAP)
    MED_ROW[fil] = r
    r += 1
r += 1
put(wi, f"A{r}", "VI. Transmission moyenne sur la durée (prix CI ÷ cours international de la même campagne)", F_BOLD)
r += 1
head(wi, r, ["Filière", "Période", "", "", "Moyenne CI", "Moyenne 3 dernières campagnes", "", "", "", "", "", "", "Note"])
r += 1
SERIES_ROW = {}
caf_ids = [o["id"] for o in I.OBS if o["id"].startswith("CAF-CI-20") and o["id"] != "CAF-CI-2026/27"]
cot_ids = [o["id"] for o in I.OBS if o["id"].startswith("COT-CI-")]
for fil, per, ids, note in (("Café", "2016/17-2025/26", caf_ids, "Robusta (indicateur OIC) ; 2025/26 : oct. 2025-août 2026"),
                            ("Coton", "2017/18-2025/26", cot_ids, "Équivalent fibre (rendement à l'égrenage) ÷ indice A ; 2025/26 partiel")):
    put(wi, f"A{r}", fil, F_BOLD)
    put(wi, f"B{r}", per)
    put(wi, f"E{r}", "=AVERAGE(" + ",".join(OBSREF(x, "Y") for x in ids) + ")", F_LINK, FMT_PCT)
    put(wi, f"F{r}", "=AVERAGE(" + ",".join(OBSREF(x, "Y") for x in ids[-3:]) + ")", F_LINK, FMT_PCT)
    put(wi, f"M{r}", note, align=WRAP)
    SERIES_ROW[fil] = r
    r += 1
put(wi, f"A{r}", "Cacao", F_BOLD)
put(wi, f"B{r}", "2016/17-2025/26 (demi-campagnes)")
put(wi, f"E{r}", f"=Cacao_transmission!F{SUMROWS['Moyenne 10 campagnes (2016/17-2025/26)']}", F_LINK, FMT_PCT)
put(wi, f"F{r}", f"=Cacao_transmission!F{SUMROWS['Moyenne 3 dernières campagnes (2023/24-2025/26)']}", F_LINK, FMT_PCT)
put(wi, f"M{r}", "Ghana sur la même période : voir onglet Cacao_transmission", align=WRAP)
SERIES_ROW["Cacao"] = r
wi.freeze_panes = "C4"

# ---------------------------------------------------------------------------
# Décomposition
# ---------------------------------------------------------------------------
wd = wb.create_sheet("Decomposition")
put(wd, "A1", "Décomposition de la valeur : du prix international au prix producteur", F_TITLE)
wd["A1"].border = Border()
wd.column_dimensions["A"].width = 58
for c, w in zip("BCDE", (16, 16, 16, 70)):
    wd.column_dimensions[c].width = w
r = 3
head(wd, r, ["Cacao – structure du prix CAF (règle de partage)", "% du CAF", "FCFA/kg (2026/27, si part = 60 %)", "USD/kg", "Source / note"])
DEC = {}
r += 1
put(wd, f"A{r}", "Prix CAF de référence implicite (prix bord champ ÷ 60 %)")
put(wd, f"B{r}", "=1", fmt=FMT_PCT)
put(wd, f"C{r}", f"={OBSREF('CAC-CI-2026/27-P', 'S')}/B{r+1}", F_LINK, FMT_FCFA)
put(wd, f"D{r}", f"=C{r}/{OBSREF('CAC-CI-2026/27-P', 'Q')}", F_LINK, FMT_USD)
put(wd, f"E{r}", "Calcul : 1 200 FCFA/kg ÷ 60 % (plancher réglementaire). Majorant du CAF si la part producteur dépasse 60 %.", align=WRAP)
DEC["caf"] = r
r += 1
for lab, pct, note in (("Producteur (prix bord champ garanti)", "=0.6", "Règle de partage ≥60 % du CAF (Banque mondiale 2019 ; Agence Ecofin 2026)"),
                       ("Droit unique de sortie (DUS)", "=0.146", "14,6 % du CAF depuis le 16/11/2012 (OMC TPR 2017 ; Banque mondiale 2019)"),
                       ("Autres prélèvements fiscaux et parafiscaux", "=0.22-0.146", "Plafond global ≈22 % du CAF (Banque mondiale 2019) ; 23,2 % observé en 2016/17 (OMC)"),
                       ("Coûts de commercialisation, transport, conditionnement, marges, fret et assurance (résidu)", f"=1-B{r}-B{r+1}-B{r+2}", "Résidu calculé (dont ≈225 FCFA/kg de marges privées selon la Banque mondiale 2019)")):
    put(wd, f"A{r}", lab, align=WRAP)
    put(wd, f"B{r}", pct, F_INPUT if not pct.startswith("=1-") else F_BASE, FMT_PCT)
    put(wd, f"C{r}", f"=$C${DEC['caf']}*B{r}", fmt=FMT_FCFA)
    put(wd, f"D{r}", f"=C{r}/{OBSREF('CAC-CI-2026/27-P', 'Q')}", F_LINK, FMT_USD)
    put(wd, f"E{r}", note, align=WRAP)
    r += 1
put(wd, f"A{r}", "Pour mémoire : cours mondial ICCO, août 2026 (FCFA/kg)")
put(wd, f"C{r}", f"={OBSREF('INT-CAC-2026-08', 'S')}", F_LINK, FMT_FCFA)
put(wd, f"D{r}", f"={OBSREF('INT-CAC-2026-08', 'R')}", F_LINK, FMT_USD)
put(wd, f"E{r}", "Le CAF implicite des ventes anticipées est très inférieur au cours de marché d'août 2026 : décalage dû au calendrier des ventes (mars-juin 2026).", align=WRAP)
DEC["icco"] = r
r += 2

head(wd, r, ["Anacarde 2026 – du bord champ au CFR Asie", "FCFA/kg", "% du CFR", "USD/kg", "Source / note"])
r += 1
DEC["ana_start"] = r
ana_rows = [
    ("Prix plancher bord champ", "=400", "Barème 2026 (CCAK)"),
    ("Collecte → magasin intérieur", "=425-400", "Plancher magasin intérieur 425"),
    ("Magasin intérieur → magasin usine", "=454-425", "Plancher magasin usine 454"),
    ("Magasin usine → magasin portuaire", "=484-454", "Plancher magasin portuaire 484"),
]
for lab, v, note in ana_rows:
    put(wd, f"A{r}", lab)
    put(wd, f"B{r}", v, F_INPUT, FMT_FCFA)
    put(wd, f"E{r}", note, align=WRAP)
    r += 1
put(wd, f"A{r}", "Droit unique de sortie (5 % de la valeur CAF de référence)")
cfr_ref = OBSREF("INT-ANA-CI-2026", "S")
put(wd, f"B{r}", f"=0.05*{cfr_ref}", F_LINK, FMT_FCFA)
put(wd, f"E{r}", "DUS 5 % depuis le 20/11/2024 (assiette approximée par le CFR)", align=WRAP)
r += 1
put(wd, f"A{r}", "Fret maritime, frais portuaires, conditionnement, financement, freinte et marge exportateur (résidu)")
put(wd, f"B{r}", f"={cfr_ref}-SUM(B{DEC['ana_start']}:B{r-1})", fmt=FMT_FCFA)
put(wd, f"E{r}", "Résidu calculé ; non décomposable faute de données publiques sur les coûts d'exportation", align=WRAP)
r += 1
put(wd, f"A{r}", "Prix CFR Vietnam/Inde, noix ivoirienne (avr.-mai 2026)", F_BOLD)
put(wd, f"B{r}", f"={cfr_ref}", F_LINK, FMT_FCFA)
DEC["ana_cfr"] = r
for rr_ in range(DEC["ana_start"], r + 1):
    put(wd, f"C{rr_}", f"=B{rr_}/$B${r}", fmt=FMT_PCT)
    put(wd, f"D{rr_}", f"=B{rr_}/{OBSREF('INT-ANA-CI-2026', 'Q')}", F_LINK, FMT_USD)
put(wd, f"E{r}", "Cotation de négoce (fiabilité C) ; valeur unitaire Vietnam toutes origines janv.-avr. 2026 : voir Observations", align=WRAP)
r += 2

head(wd, r, ["Caoutchouc – part du cours mondial (base kg sec)", "Valeur", "", "", "Source / note"])
r += 1
put(wd, f"A{r}", "Part du prix de référence revenant au producteur (règle 2026)")
put(wd, f"B{r}", "=0.66", F_INPUT, FMT_PCT)
put(wd, f"E{r}", "63 % jusqu'en 2025 ; 66 % à partir de 2026 (Agence Ecofin)", align=WRAP)
r += 1
put(wd, f"A{r}", "Moyenne observée : prix bord champ (sec, DRC 60 %) ÷ TSR20 du mois précédent")
cao_ids = ["CAO-CI-2025-01", "CAO-CI-2025-04", "CAO-CI-2026-01", "CAO-CI-2026-02", "CAO-CI-2026-04"]
put(wd, f"B{r}", "=AVERAGE(" + ",".join(OBSREF(x, "Y") for x in cao_ids) + ")", F_LINK, FMT_PCT)
put(wd, f"E{r}", "5 couples mois/TSR20 vérifiés (janv. et avr. 2025 ; janv., févr. et avr. 2026)", align=WRAP)
DEC["cao_share"] = r
r += 1
put(wd, f"A{r}", "Même calcul si le DRC réel est de 66 % (milieu de 65-68 %)")
put(wd, f"B{r}", f"=B{r-1}*Parametres!$C$6/0.66", F_LINK, FMT_PCT)
put(wd, f"E{r}", "Un DRC réel supérieur à la convention réduit la rémunération effective par kg sec", align=WRAP)
DEC["cao_share66"] = r
r += 1
put(wd, f"A{r}", "Thaïlande : prix cup lump 100 % DRC ÷ TSR20 (mai 2025)")
put(wd, f"B{r}", f"={OBSREF('CAO-TH-2025-05', 'Y')}", F_LINK, FMT_PCT)
DEC["cao_th"] = r
r += 2

head(wd, r, ["Palmier à huile – partage huile/régime", "Ratio", "", "", "Source / note"])
r += 1
put(wd, f"A{r}", "CI : prix du régime ÷ prix intérieur de l'huile brute (janv. 2026)")
put(wd, f"B{r}", f"={OBSREF('PAL-CI-FFB-2026-01', 'S')}/{OBSREF('PAL-CI-CPO-2026-01', 'S')}", F_LINK, FMT_PCT)
DEC["pal_ci_dom"] = r
r += 1
put(wd, f"A{r}", "CI : prix du régime ÷ prix mondial de l'huile brute (janv. 2026)")
put(wd, f"B{r}", f"={OBSREF('PAL-CI-FFB-2026-01', 'Y')}", F_LINK, FMT_PCT)
DEC["pal_ci_w"] = r
r += 1
put(wd, f"A{r}", "Indonésie (Riau) : prix du régime ÷ prix mondial de l'huile brute (janv. 2026)")
put(wd, f"B{r}", f"={OBSREF('PAL-ID-FFB-2026-01', 'Y')}", F_LINK, FMT_PCT)
DEC["pal_id_w"] = r
r += 1
put(wd, f"A{r}", "Malaisie : prix du régime (MPOB) ÷ prix mondial de l'huile brute (2025)")
put(wd, f"B{r}", f"={OBSREF('PAL-MY-FFB-2025', 'Y')}", F_LINK, FMT_PCT)
DEC["pal_my_w"] = r
r += 1
put(wd, f"A{r}", "CI : prix intérieur de l'huile brute ÷ prix mondial (janv. 2026)")
put(wd, f"B{r}", f"={OBSREF('PAL-CI-CPO-2026-01', 'Y')}", F_LINK, FMT_PCT)
put(wd, f"E{r}", "Un ratio >100 % signale un marché intérieur protégé (prix de l'huile supérieur au prix mondial)", align=WRAP)
DEC["pal_cpo"] = r
r += 2
head(wd, r, ["Coton – soutien budgétaire 2025/26", "Valeur", "", "", "Source / note"])
r += 1
put(wd, f"A{r}", "Subvention exceptionnelle 2025/26 (FCFA)")
put(wd, f"B{r}", 25300000000, F_INPUT, "#,##0")
put(wd, f"E{r}", "Agence Ecofin (0108-130586) : 25,3 Mds FCFA contre 11,9 Mds en 2024/25", align=WRAP)
DEC["cot_sub"] = r
r += 1
put(wd, f"A{r}", "Production de coton graine de référence (t, campagne 2024/25)")
put(wd, f"B{r}", "=Volumes_Rendements!B" + str(0), F_LINK, "#,##0")
DEC["cot_prod"] = r
r += 1
put(wd, f"A{r}", "Subvention rapportée au kg de coton graine (FCFA/kg)")
put(wd, f"B{r}", f"=B{DEC['cot_sub']}/(B{DEC['cot_prod']}*1000)", fmt="#,##0")
put(wd, f"E{r}", "Ordre de grandeur : la production 2025/26 n'étant pas encore publiée, la production 2024/25 sert de dénominateur", align=WRAP)
DEC["cot_sub_kg"] = r
r += 1
put(wd, f"A{r}", "En % du prix d'achat (310 FCFA/kg)")
put(wd, f"B{r}", f"=B{DEC['cot_sub_kg']}/{OBSREF('COT-CI-2025/26', 'S')}", F_LINK, FMT_PCT)
DEC["cot_sub_pct"] = r

# ---------------------------------------------------------------------------
# Volumes et rendements
# ---------------------------------------------------------------------------
wv = wb.create_sheet("Volumes_Rendements")
put(wv, "A1", "Importance économique (valeur brute au producteur) et revenu brut à l'hectare", F_TITLE)
wv["A1"].border = Border()
head(wv, 3, ["Filière", "Volume (t)", "Libellé", "ID prix", "Prix FCFA/kg", "Valeur brute producteur (Mds FCFA)", "Source", "URL", "Remarque"],
     [14, 13, 40, 18, 12, 16, 40, 50, 40])
r = 4
VOL_ROW = {}
for fil, vol, lab, pid, sk, rem in I.VOLUMES:
    s = I.S[sk]
    put(wv, f"A{r}", fil, F_BOLD)
    put(wv, f"B{r}", vol, F_INPUT, "#,##0")
    put(wv, f"C{r}", lab, align=WRAP)
    put(wv, f"D{r}", pid)
    put(wv, f"E{r}", f"={OBSREF(pid, 'S')}", F_LINK, FMT_FCFA)
    put(wv, f"F{r}", f"=B{r}*1000*E{r}/1000000000", fmt="#,##0")
    put(wv, f"G{r}", f"{s['institution']} – {s['titre']}", align=WRAP)
    put(wv, f"H{r}", s["url"], align=WRAP)
    put(wv, f"I{r}", rem, align=WRAP)
    VOL_ROW[fil] = r
    r += 1
r += 1
head(wv, r, ["Filière", "Pays", "Rendement (kg/ha)", "ID prix", "Prix FCFA/kg", "Revenu brut (FCFA/ha)", "Source", "URL", ""])
r += 1
RDT_ROW = {}
for fil, pays, rdt, pid, sk in I.RENDEMENTS:
    s = I.S[sk]
    put(wv, f"A{r}", fil, F_BOLD)
    put(wv, f"B{r}", pays)
    put(wv, f"C{r}", rdt, F_INPUT, "#,##0")
    put(wv, f"D{r}", pid)
    put(wv, f"E{r}", f"={OBSREF(pid, 'S')}", F_LINK, FMT_FCFA)
    put(wv, f"F{r}", f"=C{r}*E{r}", fmt="#,##0")
    put(wv, f"G{r}", f"{s['institution']} – {s['titre']}", align=WRAP)
    put(wv, f"H{r}", s["url"], align=WRAP)
    RDT_ROW[(fil, pays)] = r
    r += 1

wd[f"B{DEC['cot_prod']}"] = f"=Volumes_Rendements!B{VOL_ROW['Coton']}"
wd[f"B{DEC['cot_prod']}"].font = F_LINK
wd[f"B{DEC['cot_prod']}"].number_format = "#,##0"

# ---------------------------------------------------------------------------
# Positionnement (graphique à bulles)
# ---------------------------------------------------------------------------
wpz = wb.create_sheet("Positionnement")
put(wpz, "A1", "Positionnement des filières (graphique 1 de la note)", F_TITLE)
wpz["A1"].border = Border()
head(wpz, 3, ["Filière", "X : rémunération relative (indice CI, médiane comparateurs = 100)", "Y : taux de transmission (prix CI / référence internationale)",
              "Taille : valeur brute au producteur (Mds FCFA)", "Note"], [16, 22, 22, 18, 70])
r = 4
POS_ROW = {}
for fil, note in (("Cacao", "Ouverture 2026/27 ; transmission vs cours d'août 2026"),
                  ("Café", "2026/27 ; transmission vs robusta d'août 2026"),
                  ("Anacarde", "Campagne 2026 ; transmission vs CFR Asie avr.-mai 2026"),
                  ("Coton", "2025/26 ; transmission en équivalent fibre vs indice A"),
                  ("Caoutchouc", "Sept. 2026 (base sèche) ; transmission = moyenne des couples vérifiés")):
    put(wpz, f"A{r}", fil, F_BOLD)
    put(wpz, f"B{r}", f"=Indicateurs!I{MED_ROW[fil]}", F_LINK, "0")
    if fil == "Caoutchouc":
        put(wpz, f"C{r}", f"=Decomposition!B{DEC['cao_share']}", F_LINK, FMT_PCT)
    else:
        put(wpz, f"C{r}", f"=Indicateurs!J{MED_ROW[fil]}", F_LINK, FMT_PCT)
    put(wpz, f"D{r}", f"=Volumes_Rendements!F{VOL_ROW[fil]}", F_LINK, "#,##0")
    put(wpz, f"E{r}", note, align=WRAP)
    POS_ROW[fil] = r
    r += 1

# ---------------------------------------------------------------------------
# Matrice de synthèse
# ---------------------------------------------------------------------------
wx = wb.create_sheet("Matrice")
put(wx, "A1", "Matrice de synthèse – compétitivité-prix des filières ivoiriennes", F_TITLE)
wx["A1"].border = Border()
head(wx, 3, ["Filière", "Prix CI (FCFA/kg)", "Benchmark (pays)", "Prix benchmark (FCFA/kg)", "Écart CI vs benchmark",
             "Part producteur / transmission", "Tendance (10 ans, nominal)", "Facteur explicatif principal", "Diagnostic", "Fiabilité"],
     [14, 12, 26, 13, 12, 14, 14, 50, 34, 9])
MAT = [
    ("Cacao", "Ghana (ouverture 2026/27)", f"=Indicateurs!E{MED_ROW['Cacao']}", f"=Indicateurs!F{MED_ROW['Cacao']}",
     f"=Indicateurs!H{MED_ROW['Cacao']}", f"=Indicateurs!J{MED_ROW['Cacao']}", f"=Series_CI!E{SER_SUM['var_nom']}",
     "Ventes anticipées conclues au creux du marché (mars-juin 2026) ; règle ≥60 % CAF ; prélèvements ≈22 % du CAF ; Ghana : 70 % du FOB réalisé garanti par la loi",
     "Rémunération inférieure au benchmark ; transmission faible à court terme (décalage des ventes anticipées)", "A/B"),
    ("Café", "Vietnam, Ouganda (2026)", f"=Indicateurs!E{MED_ROW['Café']}", f"=Indicateurs!F{MED_ROW['Café']}",
     f"=Indicateurs!H{MED_ROW['Café']}", f"=Indicateurs!J{MED_ROW['Café']}", f"=Series_CI!G{SER_SUM['var_nom']}",
     "Prix administré aligné sur ventes anticipées ; productivité très faible (production -70 % en 2024/25)",
     "Rémunération inférieure au benchmark ; problème de productivité plus que de prix", "A/B/C"),
    ("Anacarde", "Burkina, G.-Bissau, Ghana (2026)", f"=Indicateurs!E{MED_ROW['Anacarde']}", f"=Indicateurs!F{MED_ROW['Anacarde']}",
     f"=Indicateurs!H{MED_ROW['Anacarde']}", f"=Indicateurs!J{MED_ROW['Anacarde']}", f"=Series_CI!H{SER_SUM['var_nom']}",
     "Plancher aligné sur les voisins UEMOA ; forte valeur captée entre le port et le CFR Asie ; Ghana/Tanzanie mieux transmis (enchères, qualité)",
     "Prix au niveau des voisins UEMOA, nettement inférieur au Ghana ; valeur captée en aval du port", "B/C"),
    ("Coton", "Burkina, Mali, Bénin, Togo (2025/26)", f"=Indicateurs!E{MED_ROW['Coton']}", f"=Indicateurs!F{MED_ROW['Coton']}",
     f"=Indicateurs!H{MED_ROW['Coton']}", f"=Indicateurs!J{MED_ROW['Coton']}", f"=Series_CI!I{SER_SUM['var_nom']}",
     "Prix administré soutenu par une subvention de 25,3 Mds FCFA (2025/26) ; rendements dans la moyenne régionale",
     "Prix proche de la référence, soutenu par le budget", "A/B"),
    ("Caoutchouc", "Thaïlande, Indonésie", f"=Indicateurs!E{MED_ROW['Caoutchouc']}", f"=Indicateurs!F{MED_ROW['Caoutchouc']}",
     f"=Indicateurs!H{MED_ROW['Caoutchouc']}", f"=Decomposition!B{DEC['cao_share']}", "n.d.",
     "Formule : 63-66 % d'un prix de référence net de coûts ; DRC conventionnel 60 % < DRC réel ; pouvoir de négociation des usiniers",
     "Transmission faible ; rémunération inférieure aux producteurs asiatiques", "B/C"),
    ("Palmier à huile", "Indonésie, Malaisie", f"=Indicateurs!E{MED_ROW['Palmier à huile']}", f"=Indicateurs!F{MED_ROW['Palmier à huile']}",
     f"=Indicateurs!H{MED_ROW['Palmier à huile']}", f"=Decomposition!B{DEC['pal_ci_w']}", "n.d.",
     "Prix du régime ≈14 % du prix mondial de l'huile brute contre ≈21-22 % en Asie (≈13 % du prix intérieur de l'huile), alors que l'huile brute est payée au-dessus du prix mondial sur le marché intérieur",
     "Rémunération inférieure ; partage de la valeur défavorable au planteur", "A/B"),
    ("Riz", "Sénégal (2025)", f"=Indicateurs!E{MED_ROW['Riz']}", f"=Indicateurs!F{MED_ROW['Riz']}",
     f"=Indicateurs!H{MED_ROW['Riz']}", f"={OBSREF('RIZ-CI-2025', 'Y')}", "n.d.",
     "Paddy payé au-dessus de la parité FOB du riz importé (équivalent paddy du riz thaï 5 %, hors fret et droits) : coûts de production et d'usinage élevés, rendements faibles",
     "Rémunération supérieure mais compétitivité faible face aux importations", "A/B"),
    ("Banane dessert", "Équateur (prix minimum)", "n.d.", f"={OBSREF('BAN-EC-2026', 'S')}", "n.d.", "n.d.", "n.d.",
     "Filière intégrée (plantations exportatrices) : aucun prix producteur public en Côte d'Ivoire",
     "Données insuffisantes pour conclure", "B"),
    ("Mangue", "Burkina Faso", f"={OBSREF('MAN-CI-2026', 'S')}", f"={OBSREF('MAN-BF-2026', 'S')}", "n.c.", "n.d.", "n.d.",
     "Prix CI fixé en station (220 FCFA/kg) et à la caisse bord champ (poids non publié) : stades non comparables",
     "Données insuffisantes pour conclure", "B"),
    ("Ananas, maïs, manioc, igname, plantain, tomate, oignon, cola, coco, canne", "—", "n.d.", "n.d.", "n.d.", "n.d.", "n.d.",
     "Pas de prix bord champ public harmonisé (OCPV publie des prix à la consommation) ; FAOSTAT non accessible depuis l'environnement d'étude",
     "Données insuffisantes pour conclure", "—"),
]
r = 4
MAT_ROW = {}
for fil, bench, pci, pb, ecart, part, tend, fact, diag, fiab in MAT:
    put(wx, f"A{r}", fil, F_BOLD, align=WRAP)
    put(wx, f"B{r}", pci, F_LINK if str(pci).startswith("=") else F_BASE, FMT_FCFA)
    put(wx, f"C{r}", bench, align=WRAP)
    put(wx, f"D{r}", pb, F_LINK if str(pb).startswith("=") else F_BASE, FMT_FCFA)
    put(wx, f"E{r}", ecart, F_LINK if str(ecart).startswith("=") else F_BASE, FMT_PCT)
    put(wx, f"F{r}", part, F_LINK if str(part).startswith("=") else F_BASE, FMT_PCT)
    put(wx, f"G{r}", tend, F_LINK if str(tend).startswith("=") else F_BASE, FMT_PCT)
    put(wx, f"H{r}", fact, align=WRAP)
    put(wx, f"I{r}", diag, align=WRAP)
    put(wx, f"J{r}", fiab, align=CENTER)
    wx.row_dimensions[r].height = 48
    MAT_ROW[fil] = r
    r += 1
put(wx, f"A{r+1}", "Lecture : écart = prix CI ÷ benchmark − 1 ; part producteur = prix CI ÷ référence internationale (caoutchouc : base sèche ; palmier : prix du régime ÷ prix mondial de l'huile ; riz : ÷ équivalent paddy du riz thaï 5 % FOB). n.d. = non disponible ; n.c. = non comparable.", align=WRAP)
wx.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=10)
wx.row_dimensions[r + 1].height = 40

# ---------------------------------------------------------------------------
# Audit qualité
# ---------------------------------------------------------------------------
wq = wb.create_sheet("Audit_QC")
put(wq, "A1", "Audit de cohérence (section 18 du cahier des charges)", F_TITLE)
wq["A1"].border = Border()
checks = ["Période", "Produit", "Qualité", "Stade", "Unité", "Monnaie", "Référence internationale", "Source primaire",
          "Politique publique (soutien)", "Fiscalité"]
head(wq, 3, ["Comparaison"] + checks + ["Verdict"], [40] + [16] * len(checks) + [22])
AUDIT = [
    ("Cacao CI vs Ghana (2016/17-2026/27)", ["OK (même demi-campagne)", "OK", "OK (grade marchand)", "OK (bord champ)", "OK (GH¢/t → kg)",
     "OK (BRI/BoG mensuel)", "OK (ICCO, même période)", "Partiel (presse relayant CCC/COCOBOD)", "Ghana : 70 % FOB légal ; CI : ventes anticipées, rachat de stocks 2026",
     "CI : DUS 14,6 % + ≈7 % ; Ghana : non documenté"], "Comparaison directe"),
    ("Cacao CI vs Cameroun / Nigeria / Équateur", ["Partiel (points de marché)", "OK", "Différente (Équateur)", "OK", "OK (quintal → kg)",
     "OK", "OK", "Non (presse/secondaire)", "Marchés libéralisés", "Non documentée"], "Indicative"),
    ("Café CI vs Vietnam / Ouganda", ["Proche (juil.-sept. 2026)", "OK (café vert)", "OK (FAQ)", "OK", "OK", "Partiel (UGX source C)",
     "OK (OIC)", "Ouganda : UCDA (A)", "CI : prix administré (subvention 2019/20)", "Non documentée"], "Directe (Vietnam) / directe-prudente (Ouganda)"),
    ("Anacarde CI vs UEMOA / Ghana", ["OK (campagne 2026)", "OK (noix brute)", "Partiel (KOR Ghana spécifié)", "OK (bord champ)", "OK", "OK",
     "Partiel (cotation de négoce)", "Ghana TCDA (A)", "Prix planchers non toujours respectés", "CI : DUS 5 %"], "Comparaison directe"),
    ("Anacarde CI vs Tanzanie", ["Décalée (oct.-janv.)", "OK", "Différente (KOR élevé)", "Différent (magasin primaire)", "OK", "Approx. (C)",
     "Partiel", "Non", "Système d'enchères", "Non documentée"], "Indicative"),
    ("Coton CI vs UEMOA", ["OK (2025/26)", "OK (coton graine 1er choix)", "OK", "OK", "OK", "OK (même devise)", "OK (indice A, éq. fibre)",
     "Partiel (Sofitex A ; autres B/C)", "CI : subvention 25,3 Mds FCFA", "Non documentée"], "Comparaison directe"),
    ("Caoutchouc CI vs Thaïlande / Indonésie", ["Décalée (mai 2025 / août 2026)", "OK", "Converti en base sèche (DRC 60 %)", "Proche", "OK (kg sec)", "OK (BCE)",
     "Partiel (TSR20 2026 incomplet)", "Non (presse)", "Thaïlande : soutiens ponctuels", "Non documentée"], "Indicative"),
    ("Palmier CI vs Indonésie / Malaisie", ["Proche (janv. 2026 / 2025)", "OK (régimes)", "Partiel (OER différents)", "Différent (bord champ / usine)", "OK", "OK (BCE)",
     "OK (CIF Rotterdam)", "Malaisie MPOB (A)", "Prix administré CI ; prélèvements export Indonésie", "Taxes export Indonésie non retraitées"], "Indicative"),
    ("Riz CI vs Sénégal / Vietnam / parité FOB (riz thaï)", ["OK (2025)", "OK (paddy)", "Partiel (paddy frais VN)", "OK", "OK", "OK",
     "Partiel (FOB Bangkok, hors fret)", "USDA (A)", "Sénégal : subvention 30 FCFA/kg", "Droits à l'importation non retraités"], "Directe (Sénégal) / indicative (Vietnam)"),
    ("Banane, mangue, ananas, vivriers", ["—"] * 10, "Données insuffisantes"),
]
r = 4
for lab, vals, verdict in AUDIT:
    put(wq, f"A{r}", lab, F_BOLD, align=WRAP)
    for j, v in enumerate(vals):
        c = put(wq, f"{get_column_letter(2+j)}{r}", v, align=WRAP)
        if v.startswith(("Partiel", "Différ", "Décal", "Approx", "Non", "—")):
            c.fill = FILL_WARN
    put(wq, f"{get_column_letter(2+len(checks))}{r}", verdict, F_BOLD, align=WRAP)
    wq.row_dimensions[r].height = 60
    r += 1

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------
wsx = wb.create_sheet("Sources")
head(wsx, 1, ["Clé", "Institution", "Titre / contenu utilisé", "URL", "Type", "Fiabilité", "Date de consultation"],
     [16, 34, 70, 70, 22, 9, 12])
for k, (key, s) in enumerate(sorted(I.S.items()), start=2):
    put(wsx, f"A{k}", key)
    put(wsx, f"B{k}", s["institution"], align=WRAP)
    put(wsx, f"C{k}", s["titre"], align=WRAP)
    put(wsx, f"D{k}", s["url"], align=WRAP)
    put(wsx, f"E{k}", s["type"])
    put(wsx, f"F{k}", s["fiabilite"], fill=FILL_WARN if s["fiabilite"] == "C" else None, align=CENTER)
    put(wsx, f"G{k}", I.DATE_CONSULT)
wsx.freeze_panes = "B2"
wsx.auto_filter.ref = f"A1:G{len(I.S)+1}"

# Ordre des onglets
order = ["Lisez-moi", "Matrice", "Indicateurs", "Observations", "Cacao_transmission", "Series_CI", "Decomposition",
         "Positionnement", "Volumes_Rendements", "Audit_QC", "Sources", "Cours_mensuels", "Cours_periodes",
         "Change_mensuel", "Change_periodes", "Parametres"]
wb._sheets = [wb[n] for n in order]
for wsh in wb.worksheets:
    wsh.sheet_view.zoomScale = 90
wb.save(OUT)

# Index des cellules clés pour les scripts aval (graphiques, note)
import json
json.dump({"OBS_ROW": OBS_ROW, "TRANS_ROWS": TRANS_ROWS, "ROW_2627": ROW_2627, "SUMROWS": SUMROWS, "ROW_CV_CAC": ROW_CV_CAC,
           "YR_ROW": YR_ROW, "SER_SUM": SER_SUM, "PAIR_ROW": {f"{a}|{b}": v for (a, b), v in PAIR_ROW.items()},
           "MED_ROW": MED_ROW, "DEC": DEC, "VOL_ROW": VOL_ROW, "RDT_ROW": {f"{a}|{b}": v for (a, b), v in RDT_ROW.items()},
           "POS_ROW": POS_ROW, "MAT_ROW": MAT_ROW, "SERIES_ROW": SERIES_ROW},
          open(ROOT / "scripts" / "cell_index.json", "w"), ensure_ascii=False, indent=1)
print("Écrit :", OUT)
