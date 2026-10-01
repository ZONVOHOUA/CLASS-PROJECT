# -*- coding: utf-8 -*-
"""
Rédige la note de benchmark (5 pages) à partir des valeurs calculées de la base Excel.
Produit : note_content.json (contenu structuré, repris par make_docx.js) et la note PDF (HTML -> Chromium).
Tous les chiffres cités proviennent de Base_Prix_Benchmark_CI.xlsx (lecture des valeurs recalculées).
"""
import json
import os
import re
import html
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
IDX = json.load(open(ROOT / "scripts" / "cell_index.json"))
WB = load_workbook(ROOT / "Base_Prix_Benchmark_CI.xlsx", data_only=True)
O = IDX["OBS_ROW"]
NBSP = " "
NNBSP = " "


def cell(sheet, ref):
    return WB[sheet][ref].value


def obs(oid, col):
    return cell("Observations", f"{col}{O[oid]}")


def fnum(x, dec=0):
    """Nombre au format français (espace fine insécable pour les milliers)."""
    s = f"{x:,.{dec}f}".replace(",", "§").replace(".", ",").replace("§", NNBSP)
    return s


def fpct(x, dec=0, signed=False):
    v = x * 100
    s = f"{v:+.{dec}f}" if signed else f"{v:.{dec}f}"
    s = s.replace(".", ",").replace("-", "−")
    return f"{s}{NBSP}%"


def fpct_approx(x):
    return f"≈100{NBSP}%" if 0.95 <= x <= 1.05 else fpct(x)


def fcfa(x, dec=0):
    return f"{fnum(x, dec)}{NBSP}FCFA/kg"


# ---------------------------------------------------------------------------
# Valeurs clés (toutes lues dans la base)
# ---------------------------------------------------------------------------
MED = IDX["MED_ROW"]
PAIR = {k: v for k, v in IDX["PAIR_ROW"].items()}
DEC = IDX["DEC"]
SR = IDX["SERIES_ROW"]
SUM = IDX["SUMROWS"]
YR = IDX["YR_ROW"]
SS = IDX["SER_SUM"]
RDT = IDX["RDT_ROW"]
VOL = IDX["VOL_ROW"]


def ind(fil, col):
    return cell("Indicateurs", f"{col}{MED[fil]}")


def pair(key, col):
    return cell("Indicateurs", f"{col}{PAIR[key]}")


V = {}
# Cacao
V["cac_ci"] = obs("CAC-CI-2026/27-P", "S")
V["cac_gh"] = obs("CAC-GH-2026/27-P", "S")
V["cac_gap"] = V["cac_ci"] - V["cac_gh"]
V["cac_ecart"] = ind("Cacao", "H")
V["cac_idx"] = ind("Cacao", "I")
V["cac_tr_ci"] = obs("CAC-CI-2026/27-P", "Y")
V["cac_tr_gh"] = obs("CAC-GH-2026/27-P", "Y")
V["cac_icco_usd"] = obs("INT-CAC-2026-08", "R")
V["cac_icco_fcfa"] = obs("INT-CAC-2026-08", "S")
V["cac_ng"] = obs("CAC-NG-2026-09", "S")
V["cac_2526P_tr"] = obs("CAC-CI-2025/26-P", "Y")
V["cac_2526P_gh_tr"] = obs("CAC-GH-2025/26-P", "Y")
V["cac_2526I_tr"] = obs("CAC-CI-2025/26-I", "Y")
V["cac_2526I_gh"] = obs("CAC-GH-2025/26-I", "S")
V["cac_2526I_gh_tr"] = obs("CAC-GH-2025/26-I", "Y")
V["cac_cm_04"] = obs("CAC-CM-2026-04", "S")
V["cac_cm_06"] = obs("CAC-CM-2026-06", "S")
V["cac_cm_06_tr"] = obs("CAC-CM-2026-06", "Y")
V["cac_ec_02"] = obs("CAC-EC-2026-02", "S")
r10 = SUM["Moyenne 10 campagnes (2016/17-2025/26)"]
r3 = SUM["Moyenne 3 dernières campagnes (2023/24-2025/26)"]
V["cac_tr10_ci"] = cell("Cacao_transmission", f"F{r10}")
V["cac_tr10_gh"] = cell("Cacao_transmission", f"G{r10}")
V["cac_tr3_ci"] = cell("Cacao_transmission", f"F{r3}")
V["cac_tr3_gh"] = cell("Cacao_transmission", f"G{r3}")
V["cac_idx10"] = cell("Cacao_transmission", f"H{r10}")
rcv = IDX["ROW_CV_CAC"]
V["cac_cv_ci"] = cell("Cacao_transmission", f"C{rcv}")
V["cac_cv_icco"] = cell("Cacao_transmission", f"E{rcv}")
V["cac_caf_impl"] = cell("Decomposition", f"C{DEC['caf']}")
V["cac_caf_impl_usd"] = cell("Decomposition", f"D{DEC['caf']}")
V["cac_rha_ci"] = cell("Volumes_Rendements", f"F{RDT['Cacao|Côte d' + chr(39) + 'Ivoire']}")
V["cac_rha_gh"] = cell("Volumes_Rendements", f"F{RDT['Cacao|Ghana']}")
V["cac_reel26"] = cell("Series_CI", f"J{SS['var_reel26']}")
V["cac_reel25"] = cell("Series_CI", f"J{SS['var_reel']}")
# Café
V["caf_ci"] = obs("CAF-CI-2026/27", "S")
V["caf_vn"] = obs("CAF-VN-2026-09", "S")
V["caf_ug"] = obs("CAF-UG-2026-07", "S")
V["caf_ci_2526"] = obs("CAF-CI-2025/26", "S")
V["caf_idx_vn"] = pair("Café|Vietnam – fin sept. 2026", "I")
V["caf_idx_ug"] = pair("Café|Ouganda – juillet 2026", "I")
V["caf_idx"] = ind("Café", "I")
V["caf_med"] = ind("Café", "F")
V["caf_ecart"] = ind("Café", "H")
V["caf_tr_ci"] = obs("CAF-CI-2026/27", "Y")
V["caf_tr_vn"] = obs("CAF-VN-2026-09", "Y")
V["caf_tr_ug"] = obs("CAF-UG-2026-07", "Y")
V["caf_tr_med"] = ind("Café", "K")
V["caf_tr10"] = cell("Indicateurs", f"E{SR['Café']}")
V["caf_tr3"] = cell("Indicateurs", f"F{SR['Café']}")
V["caf_reel26"] = cell("Series_CI", f"K{SS['var_reel26']}")
# Anacarde
V["ana_ci"] = obs("ANA-CI-2026", "S")
V["ana_real"] = obs("ANA-CI-2026-REAL", "S")
V["ana_bf"] = obs("ANA-BF-2026", "S")
V["ana_gw"] = obs("ANA-GW-2026", "S")
V["ana_gh"] = obs("ANA-GH-2026", "S")
V["ana_tz"] = obs("ANA-TZ-2025/26", "S")
V["ana_med"] = ind("Anacarde", "F")
V["ana_idx"] = ind("Anacarde", "I")
V["ana_ecart"] = ind("Anacarde", "H")
V["ana_tr_ci"] = obs("ANA-CI-2026", "Y")
V["ana_tr_gh"] = obs("ANA-GH-2026", "Y")
V["ana_tr_tz"] = obs("ANA-TZ-2025/26", "Y")
V["ana_tr_bf"] = obs("ANA-BF-2026", "Y")
V["ana_tr_med"] = ind("Anacarde", "K")
V["ana_tr_gw"] = obs("ANA-GW-2026", "Y")
V["ana_gh_ecart"] = V["ana_ci"] / V["ana_gh"] - 1
V["ana_gh_fob"] = obs("ANA-GH-2026", "AB")
V["ana_cfr"] = obs("INT-ANA-CI-2026", "S")
a0 = DEC["ana_start"]
V["ana_log"] = sum(cell("Decomposition", f"B{a0+k}") for k in (1, 2, 3))
V["ana_dus"] = cell("Decomposition", f"B{a0+4}")
V["ana_resid"] = cell("Decomposition", f"B{a0+5}")
V["ana_resid_pct"] = cell("Decomposition", f"C{a0+5}")
V["ana_reel26"] = cell("Series_CI", f"L{SS['var_reel26']}")
# Coton
V["cot_ci"] = obs("COT-CI-2025/26", "S")
V["cot_med"] = ind("Coton", "F")
V["cot_idx"] = ind("Coton", "I")
V["cot_ecart"] = ind("Coton", "H")
V["cot_tr"] = obs("COT-CI-2025/26", "Y")
V["cot_tr10"] = cell("Indicateurs", f"E{SR['Coton']}")
V["cot_sub_kg"] = cell("Decomposition", f"B{DEC['cot_sub_kg']}")
V["cot_sub_pct"] = cell("Decomposition", f"B{DEC['cot_sub_pct']}")
V["cot_rha_ci"] = cell("Volumes_Rendements", f"F{RDT['Coton|Côte d' + chr(39) + 'Ivoire']}")
V["cot_rha_bj"] = cell("Volumes_Rendements", f"F{RDT['Coton|Bénin']}")
V["cot_rha_bf"] = cell("Volumes_Rendements", f"F{RDT['Coton|Burkina Faso']}")
V["cot_reel"] = cell("Series_CI", f"M{SS['var_reel']}")
V["cot_got"] = cell("Parametres", "C5")
V["cot_rdt_gap"] = cell("Volumes_Rendements", f"C{RDT['Coton|Côte d' + chr(39) + 'Ivoire']}") / cell("Volumes_Rendements", f"C{RDT['Coton|Bénin']}") - 1
# Caoutchouc
V["cao_ci_sep"] = obs("CAO-CI-2026-09", "S")
V["cao_ci_sep_sec"] = obs("CAO-CI-2026-09", "V")
V["cao_id"] = obs("CAO-ID-2026-08", "V")
V["cao_idx_id"] = pair("Caoutchouc|Indonésie – août/sept. 2026 (base sèche)", "I")
V["cao_idx_th"] = pair("Caoutchouc|Thaïlande – mai 2025 (base sèche)", "I")
V["cao_idx"] = ind("Caoutchouc", "I")
V["cao_share"] = cell("Decomposition", f"B{DEC['cao_share']}")
V["cao_share66"] = cell("Decomposition", f"B{DEC['cao_share66']}")
V["cao_th"] = cell("Decomposition", f"B{DEC['cao_th']}")
# Palmier
V["pal_ci"] = obs("PAL-CI-FFB-2026-01", "S")
V["pal_id"] = obs("PAL-ID-FFB-2026-01", "S")
V["pal_my"] = obs("PAL-MY-FFB-2025", "S")
V["pal_idx"] = ind("Palmier à huile", "I")
V["pal_ci_w"] = cell("Decomposition", f"B{DEC['pal_ci_w']}")
V["pal_ci_dom"] = cell("Decomposition", f"B{DEC['pal_ci_dom']}")
V["pal_id_w"] = cell("Decomposition", f"B{DEC['pal_id_w']}")
V["pal_my_w"] = cell("Decomposition", f"B{DEC['pal_my_w']}")
V["pal_cpo"] = cell("Decomposition", f"B{DEC['pal_cpo']}")
# Riz
V["riz_ci"] = obs("RIZ-CI-2025", "S")
V["riz_sn"] = obs("RIZ-SN-2025", "S")
V["riz_vn"] = obs("RIZ-VN-2025", "S")
V["riz_fob"] = obs("INT-RIZ-2025", "V")
V["riz_tr"] = obs("RIZ-CI-2025", "Y")
V["riz_idx_sn"] = pair("Riz|Sénégal – 2025", "I")
V["riz_idx"] = ind("Riz", "I")
V["riz_ecart_sn"] = pair("Riz|Sénégal – 2025", "H")
# Fruits
V["ban_ec"] = obs("BAN-EC-2026", "S")
V["man_ci"] = obs("MAN-CI-2026", "S")
V["man_bf"] = obs("MAN-BF-2026", "S")
# Volumes
V["vol_cac"] = cell("Volumes_Rendements", f"F{VOL['Cacao']}")
V["n_obs"] = len(O)
V["n_src"] = sum(1 for r in WB["Sources"].iter_rows(min_row=2, values_only=True) if r[0])
json.dump({k: (float(v) if isinstance(v, (int, float)) else v) for k, v in V.items()},
          open(ROOT / "scripts" / "note_values.json", "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------------------
# Contenu (mini-balisage : **gras**)
# ---------------------------------------------------------------------------
P = []  # pages


def pts(x):
    """Écart en points de pourcentage (x exprimé en fraction)."""
    return f"{round(x * 100):d}"


PAL_W_MED = (V["pal_id_w"] + V["pal_my_w"]) / 2  # médiane de deux comparateurs = moyenne
# écarts de rémunération des quatre filières sous leurs concurrents (cacao, café, caoutchouc, palmier)
BAS4 = [-V["cac_ecart"], 1 - V["caf_idx"] / 100, 1 - V["cao_idx"] / 100, 1 - V["pal_idx"] / 100]


def k(v, dec=0):
    return fnum(v, dec)


page1 = {
    "header": ["NOTE À L'ATTENTION DE MONSIEUR LE MINISTRE", "Benchmark international des prix agricoles · Octobre 2026"],
    "blocks": [
        {"t": "title", "text": "LES PRIX AGRICOLES IVOIRIENS SONT-ILS COMPÉTITIFS ?"},
        {"t": "subtitle", "text": "Benchmark international des principales filières végétales – données arrêtées au 1er octobre 2026"},
        {"t": "answer", "label": "Réponse courte",
         "text": f"**Pas dans la plupart des filières.** Pour le cacao, le café, le caoutchouc et le palmier, le producteur ivoirien perçoit "
                 f"{fpct(min(BAS4)).replace(NBSP + '%', '')} à {fpct(max(BAS4))} de moins que ses concurrents et une part plus faible du prix international. "
                 f"L'anacarde est au niveau de l'UEMOA mais {fpct(-V['ana_gh_ecart'])} sous le Ghana ; le coton n'est à parité que grâce au budget ; "
                 f"le riz est payé au-dessus de la parité FOB, au détriment de sa compétitivité."},
        {"t": "twocol", "left": {"label": "Objectif", "text":
            "Vérifier, filière par filière, si le prix payé au producteur ivoirien est compétitif face aux producteurs concurrents, "
            "cohérent avec la valeur internationale du produit et soutenable pour la filière, puis identifier les leviers d'action."},
         "right": {"label": "Méthode", "text":
            f"{V['n_obs']} observations de prix ({V['n_src']} sources) appariées par produit, qualité, stade (bord champ) et période ; conversion en FCFA/kg "
            "au taux de change moyen de la période exacte (BCE, BRI, banques centrales). Trois indicateurs : **indice de rémunération** "
            "(prix CI ÷ médiane des pays comparables), **taux de transmission** (prix bord champ ÷ cours international de la même période, "
            "méthode identique pour tous) et **décomposition de la valeur**. Les comparaisons imparfaites sont signalées « indicatives »."}},
        {"t": "kpis", "items": [
            {"value": f"{k(V['cac_ci'])}", "unit": "FCFA/kg", "label": f"prix du cacao 2026/27, soit {fpct(V['cac_ecart'])} par rapport au Ghana ({k(V['cac_gh'])} FCFA/kg)"},
            {"value": f"{fpct(V['cac_tr_ci'])}", "unit": "", "label": f"du cours mondial du cacao (août 2026) reçus par le planteur ivoirien, contre {fpct(V['cac_tr_gh'])} au Ghana"},
            {"value": f"{fpct(V['ana_tr_ci'])}", "unit": "", "label": f"de la valeur CFR Asie de la noix de cajou reçus bord champ (Burkina {fpct(V['ana_tr_bf'])}, G.-Bissau {fpct(V['ana_tr_gw'])}, Ghana {fpct(V['ana_tr_gh'])})"},
            {"value": f"{fpct(V['cao_share'])}", "unit": "", "label": f"du cours SICOM (kg sec) reçus par l'hévéaculteur, contre {fpct_approx(V['cao_th'])} en Thaïlande"},
        ]},
        {"t": "h2", "text": "Six constats majeurs"},
        {"t": "numbered", "items": [
            f"**Cacao : les ventes anticipées pèsent désormais sur le planteur.** {k(V['cac_ci'])} FCFA/kg en 2026/27 contre {k(V['cac_gh'])} au Ghana "
            f"({fpct(V['cac_ecart'])}) ; {fpct(V['cac_tr_ci'])} du cours mondial contre {fpct(V['cac_tr_gh'])}. Sur dix campagnes : {fpct(V['cac_tr10_ci'])} en moyenne "
            f"(Ghana {fpct(V['cac_tr10_gh'])}). Le système a protégé les planteurs pendant la chute ({fpct(V['cac_2526P_tr'])} du cours en principale 2025/26) "
            f"mais les prive de la remontée.",
            f"**Café, caoutchouc, palmier : une rémunération inférieure de {fpct(1-max(V['caf_idx'],V['cao_idx'],V['pal_idx'])/100).replace(NBSP+'%','')} à {fpct(1-min(V['caf_idx'],V['cao_idx'],V['pal_idx'])/100)} à celle des concurrents** (indices {k(V['caf_idx'])}, {k(V['cao_idx'])} et {k(V['pal_idx'])}). "
            f"Le régime de palme vaut {fpct(V['pal_ci_w'])} du prix mondial de l'huile brute, contre {fpct(V['pal_id_w'])} à {fpct(V['pal_my_w'])} en Asie.",
            f"**Anacarde : un prix plancher au niveau des voisins de l'UEMOA** ({k(V['ana_ci'])} FCFA/kg contre {k(V['ana_bf'])} à {k(V['ana_gw'])}), "
            f"mais {fpct(-V['ana_gh_ecart'])} sous le Ghana ; {fpct(V['ana_resid_pct'])} de la valeur se forme entre le port et l'acheteur asiatique.",
            f"**Coton : la parité régionale** ({k(V['cot_ci'])} contre une médiane de {k(V['cot_med'])} FCFA/kg) **repose sur une subvention de 25,3 Mds FCFA**, "
            f"soit ≈{k(V['cot_sub_kg'])} FCFA/kg ({fpct(V['cot_sub_pct'])} du prix).",
            f"**Riz : un paddy bien payé mais peu compétitif.** {k(V['riz_ci'])} FCFA/kg, {fpct(V['riz_ecart_sn'], signed=True)} par rapport au Sénégal et "
            f"{fpct(V['riz_tr']-1, signed=True)} au-dessus de l'équivalent paddy du riz thaï FOB : l'enjeu est le coût de revient, pas le prix.",
            "**Fruits et vivriers : aucun prix bord champ public comparable.** Aucune conclusion robuste n'est possible ; un dispositif d'information "
            "sur les prix au producteur est un préalable.",
        ]},
        {"t": "figure", "src": "fig1_positionnement", "width": 100,
         "caption": "Graphique 1 – Positionnement des filières : rémunération relative et part du prix international reçue par le producteur ivoirien",
         "source": "Source : base Excel jointe (onglets Positionnement, Indicateurs, Decomposition). Cacao et café : ouverture 2026/27 ; anacarde : 2026 ; "
                   "coton : 2025/26 ; caoutchouc : 2025-2026, base kg sec (DRC 60 %)."},
    ],
}

mat = []
MR = IDX["MAT_ROW"]
DIAG_ICON = {"Cacao": "▼", "Café": "▼", "Anacarde": "◆", "Coton": "●", "Caoutchouc": "▼", "Palmier à huile": "▼", "Riz": "▲"}
rows_def = [
    ("Cacao", f"{k(V['cac_ci'])}", "Ghana", f"{k(V['cac_gh'])}", fpct(V['cac_ecart']), f"{fpct(V['cac_tr_ci'])} / {fpct(V['cac_tr_gh'])}",
     fpct(V['cac_reel26'], signed=True), "Ventes anticipées conclues au creux du marché ; prélèvements ≈22 % du CAF", "Rémunération et transmission faibles"),
    ("Café", f"{k(V['caf_ci'])}", "Vietnam, Ouganda", f"{k(V['caf_med'])}", fpct(V['caf_ecart']), f"{fpct(V['caf_tr_ci'])} / {fpct(V['caf_tr_med'])}",
     fpct(V['caf_reel26'], signed=True), "Prix administré ; production effondrée (−70 % en 2024/25)", "Rémunération faible ; productivité en cause"),
    ("Anacarde", f"{k(V['ana_ci'])}", "Burkina, G.-Bissau, Ghana", f"{k(V['ana_med'])}", fpct(V['ana_ecart']), f"{fpct(V['ana_tr_ci'])} / {fpct(V['ana_tr_med'])}",
     fpct(V['ana_reel26'], signed=True), f"Valeur captée en aval ({fpct(V['ana_resid_pct'])} du CFR après le port)",
     f"Au niveau UEMOA ; {fpct(V['ana_gh_ecart'])} face au Ghana"),
    ("Coton", f"{k(V['cot_ci'])}", "Burkina, Mali, Bénin, Togo", f"{k(V['cot_med'])}", fpct(V['cot_ecart'], signed=True), f"{fpct(V['cot_tr'])} / n.d.",
     fpct(V['cot_reel'], signed=True), f"Subvention 25,3 Mds FCFA (≈{k(V['cot_sub_kg'])} FCFA/kg)", "Parité soutenue par le budget"),
    ("Caoutchouc", f"{k(V['cao_ci_sep_sec'])}*", "Thaïlande, Indonésie", f"{k(ind('Caoutchouc', 'F'))}*", fpct(ind('Caoutchouc', 'H')), f"{fpct(V['cao_share'])} / {fpct(V['cao_th'])}",
     "n.d.", "Formule 63-66 % d'un prix net de coûts ; DRC conventionnel 60 %", "Rémunération et transmission faibles"),
    ("Palmier à huile", f"{k(V['pal_ci'])}", "Indonésie, Malaisie", f"{k(ind('Palmier à huile', 'F'))}", fpct(ind('Palmier à huile', 'H')),
     f"{fpct(V['pal_ci_w'])} / {fpct((V['pal_id_w']+V['pal_my_w'])/2)}**", "n.d.", "Partage huile/régime défavorable au planteur", "Rémunération faible"),
    ("Riz", f"{k(V['riz_ci'])}", "Sénégal", f"{k(ind('Riz', 'F'))}", fpct(ind('Riz', 'H'), signed=True), f"{fpct(V['riz_tr'])} de la parité FOB",
     "n.d.", "Coût de production et d'usinage élevé", "Rémunération élevée, compétitivité faible"),
    ("Banane, mangue, ananas, vivriers", "—", "—", "—", "—", "—", "—", "Pas de prix bord champ public comparable", "Données insuffisantes"),
]
for r in rows_def:
    mat.append([f"{DIAG_ICON.get(r[0], '○')} {r[0]}"] + list(r[1:]))

page2 = {
    "header": ["CARTE GÉNÉRALE DE COMPÉTITIVITÉ", "Page 2"],
    "blocks": [
        {"t": "h1", "text": "Quatre filières sous les concurrents, l'anacarde au niveau régional, le coton à parité grâce au budget, le riz au-dessus mais coûteux"},
        {"t": "lead", "text": "Un indice inférieur à 100 signifie que le producteur ivoirien reçoit moins que son homologue, pour un même produit, au même stade et à la même période. "
                              "La « part du prix international » rapporte le prix bord champ au cours mondial de la même période, avec une méthode identique pour tous les pays."},
        {"t": "table", "style": "matrix",
         "headers": ["Filière", "Prix CI (FCFA/kg)", "Pays de référence", "Prix de référence (FCFA/kg)", "Écart CI", "Part du prix international (CI / comparateurs)",
                     "Évolution réelle du prix CI (2016→2026)", "Explication principale", "Diagnostic"],
         "widths": [12.5, 7, 12, 8, 6.5, 11, 9, 19.5, 14.5],
         "rows": mat,
         "notes": "Périodes : cacao et café 2026/27 (ouverture) ; anacarde 2026 ; coton 2025/26 (évolution réelle depuis 2017/18) ; caoutchouc sept. 2026 (* base kg sec, DRC 60 %) ; "
                  "palmier janv. 2026 (** prix du régime ÷ prix mondial de l'huile brute) ; riz 2025 (part = prix du paddy ÷ équivalent paddy du riz thaï 5 % FOB). "
                  "▼ sous les comparateurs · ● à parité · ▲ au-dessus · ◆ mitigé · ○ données insuffisantes. Source : base Excel, onglets Matrice et Indicateurs."},
        {"t": "figrow", "items": [
            {"src": "fig2_indices_prix", "width": 64,
             "caption": "Graphique 2 – Prix bord champ ivoirien en % du prix de chaque pays comparable",
             "source": "Pays : BF Burkina, BJ Bénin, GH Ghana, GW Guinée-Bissau, ID Indonésie, ML Mali, MY Malaisie, NG Nigeria, SN Sénégal, TG Togo, TH Thaïlande, "
                       "TZ Tanzanie, UG Ouganda, VN Vietnam. Points vides : comparaison indicative (stade, période ou qualité imparfaitement appariés). "
                       "* Caoutchouc et palmier : aucun comparateur direct, médiane des comparateurs indicatifs."},
            {"src": "fig3_transmission", "width": 36,
             "caption": "Graphique 3 – Part du prix international reçue par le producteur",
             "source": "Cacao : cours ICCO août 2026 ; café : robusta août 2026 (Ouganda : juil.) ; anacarde : CFR Asie avr.-mai 2026 ; coton : indice A, équivalent fibre ; "
                       "caoutchouc : TSR20 du mois précédent, base sèche."},
        ]},
        {"t": "callout", "text": f"**À retenir.** L'écart de prix avec les concurrents n'est pas d'abord un problème de change ou de qualité : c'est un problème de **transmission**. "
                                 f"La part du prix international qui atteint le planteur ivoirien est inférieure à celle des concurrents de "
                                 f"{pts(V['cao_th'] - V['cao_share'])} points pour le caoutchouc, {pts(V['cac_tr_gh'] - V['cac_tr_ci'])} pour le cacao, "
                                 f"{pts(V['caf_tr_med'] - V['caf_tr_ci'])} pour le café et {pts(PAL_W_MED - V['pal_ci_w'])} pour le palmier "
                                 f"({fpct(V['pal_ci_w'] / PAL_W_MED - 1, signed=True)} en relatif). Pour l'anacarde, elle égale celle des voisins de l'UEMOA "
                                 f"mais reste inférieure de {pts(V['ana_tr_gh'] - V['ana_tr_ci'])} points à celle du Ghana."},
    ],
}

page3 = {
    "header": ["CULTURES DE RENTE ET INDUSTRIELLES", "Page 3"],
    "blocks": [
        {"t": "h1", "text": f"Le système ivoirien stabilise les prix mais transmet moins de valeur : {fpct(V['cac_tr10_ci'])} du cours mondial du cacao en moyenne sur dix ans, contre {fpct(V['cac_tr10_gh'])} au Ghana"},
        {"t": "split", "ratio": "1.75fr 1fr", "left": [
            {"t": "figure", "src": "fig4_cacao_series", "width": 100,
             "caption": "Graphique 4 – Cacao : prix bord champ CI et Ghana et cours mondial de la même demi-campagne (FCFA/kg)",
             "source": "Source : base Excel, onglet Cacao_transmission (prix CCC et COCOBOD ; cours ICCO – Banque mondiale, FMI ; change BCE, BRI, Banque du Ghana). "
                       "Graduations : campagnes principale (oct.-mars) et intermédiaire (avr.-sept.)."}],
         "right": [{"t": "cards", "cols": 1, "items": [
            {"title": "Cacao", "icon": "▼",
             "constat": f"{fpct(V['cac_tr10_ci'])} du cours mondial transmis sur dix campagnes (Ghana {fpct(V['cac_tr10_gh'])}) ; {fpct(V['cac_tr3_ci'])} sur les trois dernières. "
                        f"Le prix 2026/27 ({k(V['cac_ci'])} FCFA/kg) implique un CAF de référence ≤{k(V['cac_caf_impl'])} FCFA/kg ({fnum(V['cac_caf_impl_usd'], 2)} $/kg) quand le marché cote "
                        f"{fnum(V['cac_icco_usd'], 2)} $/kg (août 2026). Revenu brut ≈{k(V['cac_rha_ci']/1000)} 000 FCFA/ha contre ≈{k(V['cac_rha_gh']/1000)} 000 au Ghana (rendements moyens de 500 et 400 kg/ha).",
             "explication": "Plus de 1,1 Mt vendues par anticipation de mars à juin 2026, au creux du marché ; part producteur ≥60 % du CAF ; prélèvements ≈22 % du CAF "
                            "(dont DUS 14,6 %). En 2025/26, le prix garanti (2 800) a dépassé le cours mondial : 123 000 t invendues en janvier.",
             "implication": f"Prix soutenable pour le régulateur mais peu compétitif pour le planteur ; écart de {k(-V['cac_gap'])} FCFA/kg avec le Ghana (risque de fuite). "
                            "Le Ghana garantit 70 % du FOB réalisé (Act 1182), mais avec un déficit de financement du COCOBOD ≈1,4 Md $."}]}]},
        {"t": "cards", "cols": 3, "items": [
            {"title": "Café robusta", "icon": "▼",
             "constat": f"{k(V['caf_ci'])} FCFA/kg (2026/27) contre ≈{k(V['caf_vn'])} au Vietnam (indice {k(V['caf_idx_vn'])}) ; 2025/26 : {k(V['caf_ci_2526'])} contre ≈{k(V['caf_ug'])} en Ouganda. "
                        f"Transmission moyenne {fpct(V['caf_tr10'])} sur dix ans (Vietnam {fpct(V['caf_tr_vn'])}, Ouganda {fpct(V['caf_tr_ug'])} en 2026).",
             "explication": "Prix administré calé sur les ventes anticipées ; production effondrée (24 832 t d'octobre 2024 à juin 2025, −70 %) ; maintien du prix en 2019/20 financé par 32 Mds FCFA.",
             "implication": "Le revenu du caféiculteur dépend d'abord de la productivité (régénération du verger) ; un prix plus élevé ne compense pas des volumes en chute."},
            {"title": "Anacarde", "icon": "◆",
             "constat": f"Plancher {k(V['ana_ci'])} FCFA/kg (prix moyen payé à Niakara : {k(V['ana_real'])}) ; Burkina {k(V['ana_bf'])}, G.-Bissau {k(V['ana_gw'])}, Ghana ≈{k(V['ana_gh'])}, "
                        f"Tanzanie ≈{k(V['ana_tz'])} (indicatif). Le planteur reçoit {fpct(V['ana_tr_ci'])} du CFR Asie, comme au Burkina ({fpct(V['ana_tr_bf'])}) "
                        f"et en Guinée-Bissau ({fpct(V['ana_tr_gw'])}), contre {fpct(V['ana_tr_gh'])} au Ghana.",
             "explication": f"Barème : +{k(V['ana_log'])} FCFA/kg jusqu'au magasin portuaire, DUS 5 % (≈{k(V['ana_dus'])} FCFA/kg), puis ≈{k(V['ana_resid'])} FCFA/kg ({fpct(V['ana_resid_pct'])} du CFR) "
                            "de fret, frais, financement et marges d'exportation ; pas de vente aux enchères ni de prime qualité.",
             "implication": "Prix au niveau régional mais transmission faible : la valeur se joue entre le port et l'Asie (transparence, concurrence, qualité, transformation)."},
            {"title": "Coton", "icon": "●",
             "constat": f"{k(V['cot_ci'])} FCFA/kg contre une médiane régionale de {k(V['cot_med'])} (indice {k(V['cot_idx'])}) ; équivalent fibre = {fpct(V['cot_tr'])} de l'indice A. "
                        f"Revenu brut ≈{k(V['cot_rha_ci']/1000)} 000 FCFA/ha (Bénin ≈{k(V['cot_rha_bj']/1000)} 000 ; Burkina ≈{k(V['cot_rha_bf']/1000)} 000).",
             "explication": f"Subvention exceptionnelle de 25,3 Mds FCFA en 2025/26 (11,9 en 2024/25), soit ≈{k(V['cot_sub_kg'])} FCFA/kg.",
             "implication": f"Parité obtenue par le budget, pas par la compétitivité : le levier durable est le rendement (inférieur de {fpct(-V['cot_rdt_gap'])} à celui du Bénin)."},
        ]},
        {"t": "figure", "src": "fig5_decomposition", "width": 92,
         "caption": "Graphique 5 – Sur 100 FCFA de valeur internationale, combien reviennent au producteur ?",
         "source": "Cacao : structure réglementaire du CAF (Banque mondiale 2019, OMC 2017) ; anacarde : barème 2026 (CCAK) et CFR Asie avr.-mai 2026 (cotation de négoce). Onglet Decomposition."},
        {"t": "cards", "cols": 2, "items": [
            {"title": "Caoutchouc", "icon": "▼",
             "constat": f"≈{fpct(V['cao_share'])} du cours SICOM par kg sec ({fpct(V['cao_share66'])} si le DRC réel est de 66 %) contre {fpct_approx(V['cao_th'])} en Thaïlande ; "
                        f"{k(V['cao_ci_sep'])} FCFA/kg en sept. 2026, soit ≈{k(V['cao_ci_sep_sec'])} par kg sec contre ≈{k(V['cao_id'])} en Indonésie.",
             "explication": "Formule : 63 % (66 % depuis 2026) d'un prix de référence déjà net des coûts ; DRC conventionnel de 60 % inférieur au DRC mesuré (65-68 %).",
             "implication": "Plus grand écart de transmission avec les concurrents (≈40 points) : la formule et la mesure du DRC sont les premiers leviers."},
            {"title": "Palmier à huile", "icon": "▼",
             "constat": f"Régime à {k(V['pal_ci'])} FCFA/kg (janv. 2026) contre ≈{k(V['pal_id'])} en Indonésie et ≈{k(V['pal_my'])} en Malaisie ; "
                        f"le régime vaut {fpct(V['pal_ci_w'])} du prix mondial de l'huile (Asie {fpct(V['pal_id_w'])}-{fpct(V['pal_my_w'])}).",
             "explication": f"L'huile brute est payée {fpct(V['pal_cpo'])} du prix mondial sur le marché intérieur : la valeur protégée profite à la transformation, pas au planteur.",
             "implication": "Indexer le prix du régime sur le prix de l'huile et le taux d'extraction mesuré (modèle MPOB à 1 % OER)."},
        ]},
    ],
}

RHA_ROWS = []
for (fil, pays), lecture in ((("Cacao", "Côte d'Ivoire"), "Rendement supérieur, mais prix 2026/27 inférieur de 42 % : revenu inférieur d'un quart"),
                             (("Cacao", "Ghana"), "Prix élevé (≥70 % du FOB), rendement plus faible"),
                             (("Coton", "Côte d'Ivoire"), "Prix soutenu par la subvention"),
                             (("Coton", "Bénin"), "Prix plus bas, mais rendement supérieur de 27 % : meilleur revenu"),
                             (("Coton", "Burkina Faso"), "Prix le plus élevé, rendement le plus faible"),
                             (("Coton", "Mali"), "Prix et rendement inférieurs à la Côte d'Ivoire")):
    rr = RDT[f"{fil}|{pays}"]
    RHA_ROWS.append([f"{fil} – {pays}", k(cell("Volumes_Rendements", f"C{rr}")), k(cell("Volumes_Rendements", f"E{rr}")),
                     k(cell("Volumes_Rendements", f"F{rr}"))])

page4 = {
    "header": ["FRUITS, HORTICULTURE ET VIVRIER", "Page 4"],
    "blocks": [
        {"t": "h1", "text": "Riz : rémunération élevée mais filière peu compétitive ; fruits et vivriers : des marchés différents, une information à construire"},
        {"t": "split", "left": [
            {"t": "cards", "cols": 1, "items": [
                {"title": "Riz paddy", "icon": "▲",
                 "constat": f"{k(V['riz_ci'])} FCFA/kg en moyenne 2025, contre {k(V['riz_sn'])} au Sénégal (160 payés par les usiniers avec la subvention) et ≈{k(V['riz_vn'])} au Vietnam (paddy frais). "
                            f"L'équivalent paddy du riz thaï 5 % FOB vaut {k(V['riz_fob'])} FCFA/kg : le paddy ivoirien est payé {fpct(V['riz_tr'])} de cette parité (hors fret et droits).",
                 "explication": "Riziculture majoritairement pluviale, rendements faibles, usinage coûteux ; le prix élevé reflète le coût de revient et la préférence pour le riz local, "
                                "pas une meilleure valorisation internationale. La Côte d'Ivoire importe encore ≈1,75 Mt par an.",
                 "implication": "Ici, mieux rémunérer le producteur ne passe pas par le prix mais par la baisse du coût de revient (irrigation, semences, mécanisation, qualité d'usinage)."},
            ]},
            {"t": "minititle", "text": "Prix au kilo ≠ revenu à l'hectare"},
            {"t": "table", "style": "plain compact",
             "headers": ["Filière – pays", "Rendement (kg/ha)", "Prix (FCFA/kg)", "Revenu brut (FCFA/ha)"],
             "widths": [40, 19, 18, 23], "rows": RHA_ROWS,
             "notes": f"Cacao : revenu ivoirien inférieur de {fpct(-(V['cac_rha_ci']/V['cac_rha_gh']-1))} malgré un rendement supérieur (prix 2026/27). "
                      f"Coton : le Bénin obtient le meilleur revenu avec un prix plus bas, grâce à un rendement supérieur de {fpct(1/(1+V['cot_rdt_gap'])-1)}. "
                      "Rendements : littérature (cacao), données de campagne 2024/25 (coton). Onglet Volumes_Rendements."},
        ], "right": [
            {"t": "figure", "src": "fig6_riz", "width": 100,
             "caption": "Graphique 6 – Riz paddy : prix bord champ comparés (FCFA/kg)",
             "source": "USDA (Côte d'Ivoire, Sénégal), presse vietnamienne ; riz thaï 5 % FOB (Banque mondiale) × 65 %. Onglet Observations."},
        ]},
        {"t": "h2", "text": "Des structures de marché qui conditionnent la comparaison"},
        {"t": "table", "style": "plain",
         "headers": ["Filière", "Structure de marché", "Ce qui existe", "Comparabilité", "Conclusion"],
         "widths": [13, 22, 30, 15, 20],
         "rows": [
             ["Banane dessert", "Filière intégrée (plantations exportatrices sous contrat)",
              f"Exportations 271 000 t (2025) ; Équateur : prix minimum 7,50 $ la caisse de 43 lb (≈{k(V['ban_ec'])} FCFA/kg)",
              "Aucun prix producteur public en Côte d'Ivoire", "Données insuffisantes"],
             ["Mangue", "Interprofession (Inter-Mangue), export frais",
              f"Prix en station {k(V['man_ci'])} FCFA/kg ; bord champ 2 450 FCFA la caisse (poids non publié) ; Burkina : plancher {k(V['man_bf'])} FCFA/kg bord champ",
              "Stades différents", "Non comparable en l'état"],
             ["Ananas, cola, coco, canne à sucre", "Export résiduel (ananas ≈24 000 t en 2023), niches, agro-industrie intégrée", "Pas de prix producteur publié", "—", "Données insuffisantes"],
             ["Maïs, manioc, igname, plantain, tomate, oignon", "Marchés libres domestiques",
              "OCPV : prix à la consommation hebdomadaires par marché ; pas de prix bord champ harmonisé", "Stade non comparable (consommateur)", "Données insuffisantes"],
         ]},
        {"t": "callout", "text": "**Règle de prudence appliquée.** Pour la banane, l'ananas, la mangue (au stade bord champ) et l'ensemble des vivriers, "
                                 "*les données disponibles ne permettent pas de conclure de manière robuste sur la compétitivité relative du prix de ces filières.* "
                                 "Les prix à la consommation de l'OCPV mesurent les marges de distribution, pas la rémunération du producteur."},
        {"t": "h2", "text": "Lecture transversale : quatre régimes de prix, quatre logiques de compétitivité"},
        {"t": "table", "style": "plain",
         "headers": ["Régime", "Filières", "Atout", "Faiblesse observée"],
         "widths": [20, 20, 28, 32],
         "rows": [
             ["Prix administré et ventes anticipées", "Cacao, café", f"Stabilité (coefficient de variation du prix CI {fpct(V['cac_cv_ci'])} contre {fpct(V['cac_cv_icco'])} pour le cours mondial du cacao, 2016-2026)",
              "Ventes conclues des mois à l'avance (mars-juin pour la campagne d'octobre 2026) : le planteur perd lors des remontées"],
             ["Prix plancher et barème", "Anacarde, coton, caoutchouc, palmier, mangue", "Protection minimale du producteur",
              "Formules figées, marges intermédiaires et parts producteur non revues"],
             ["Filière intégrée", "Banane, ananas", "Qualité et logistique maîtrisées", "Aucune transparence sur la rémunération des planteurs"],
             ["Marché libre domestique", "Riz, maïs, tubercules, maraîchage", "Prix qui reflète l'offre et la demande", "Aucune information publique au stade du producteur"],
         ]},
    ],
}

reco = [
    ("1", "Cacao et café – réduire le décalage des ventes anticipées",
     f"Étaler les ventes sur 12 à 18 mois par tranches plafonnées, recourir à des contrats à prix à fixer et à des couvertures, prévoir une révision en cours de campagne "
     f"quand le cours dépasse durablement le CAF de référence. Constat : CAF implicite 2026/27 ≤{fnum(V['cac_caf_impl_usd'], 1)} $/kg contre {fnum(V['cac_icco_usd'], 1)} $/kg sur le marché."),
    ("2", "Publier la formation du prix",
     "Publier à chaque campagne le barème complet (CAF ou FOB réalisé, prélèvements, marges) pour le cacao, le café, l'anacarde, le caoutchouc et le palmier, "
     f"et suivre un indicateur « part producteur ». Constat : CAF non publié ; {fpct(V['ana_resid_pct'])} de la valeur de la noix non expliquée publiquement."),
    ("3", "Réviser les formules du caoutchouc et du palmier",
     f"Caoutchouc : trajectoire au-delà de 66 % et DRC mesuré au point d'achat ; palmier : prix du régime indexé sur le prix de l'huile et le taux d'extraction mesuré. "
     f"Constat : {fpct(V['cao_share'])} contre {fpct_approx(V['cao_th'])} en Thaïlande ; régime à {fpct(V['pal_ci_w'])} du prix de l'huile contre {fpct(V['pal_id_w'])}-{fpct(V['pal_my_w'])}."),
    ("4", "Anacarde – faire jouer la concurrence et payer la qualité",
     f"Ventes groupées ou enchères en magasin (modèle tanzanien), prime au rendement en amande (KOR), publication d'un prix FOB de référence. "
     f"Constat : {fpct(V['ana_tr_ci'])} du CFR contre {fpct(V['ana_tr_gh'])} au Ghana et {fpct(V['ana_tr_tz'])} en Tanzanie (comparaison indicative)."),
    ("5", "Productivité avant prix (café, riz, coton, cacao)",
     f"Régénération du verger caféier, intensification rizicole, diffusion des itinéraires cotonniers les plus productifs ; recentrer progressivement la subvention cotonnière "
     f"(≈{k(V['cot_sub_kg'])} FCFA/kg) sur les intrants et le rendement. Constat : riz à {fpct(V['riz_tr'])} de la parité FOB ; rendement cotonnier inférieur de {fpct(-V['cot_rdt_gap'])} à celui du Bénin."),
    ("6", "Fiscalité contracyclique et observatoire des prix",
     "Moduler les prélèvements sur le cacao (≈22 % du CAF) selon le niveau des cours ; créer un observatoire des prix au producteur (Côte d'Ivoire et pays concurrents, "
     "vivriers inclus) publiant un benchmark trimestriel. Constat : aucune série bord champ publique pour les fruits et les vivriers."),
]
page5 = {
    "header": ["ENSEIGNEMENTS POUR LA CÔTE D'IVOIRE", "Page 5"],
    "blocks": [
        {"t": "h1", "text": "Six leviers pour mieux rémunérer le producteur sans fragiliser la compétitivité des filières"},
        {"t": "recos", "items": [{"n": n, "title": t, "text": tx} for n, t, tx in reco]},
        {"t": "h2", "text": "Matrice d'action"},
        {"t": "table", "style": "matrix2",
         "headers": ["Problème observé", "Filières concernées", "Action possible", "Institution pilote"],
         "widths": [27, 17, 34, 22],
         "rows": [
             ["Transmission retardée par le calendrier des ventes anticipées", "Cacao, café", "Lissage et couverture des ventes ; clause de révision en cours de campagne", "CCC, avec le MINADERPV et le ministère chargé des Finances"],
             ["Formation du prix peu transparente", "Cacao, café, anacarde, caoutchouc, palmier", "Publication des barèmes et des prix FOB/CAF réalisés ; indicateur « part producteur »", "CCC, CCAK, APROMAC, Conseil Hévéa-Palmier à huile-Coco"],
             ["Part producteur figée par formule et conventions de mesure", "Caoutchouc, palmier", "Révision des formules ; DRC et taux d'extraction mesurés", "Conseil Hévéa-Palmier à huile-Coco, APROMAC, AIPH"],
             ["Valeur captée en aval de l'exploitation", "Anacarde", "Ventes groupées, enchères, prime qualité, prix FOB publié", "CCAK, MINADERPV, ministère du Commerce"],
             ["Faible productivité, coût de revient élevé", "Café, riz, coton, cacao", "Régénération, intensification, recentrage des subventions sur le rendement", "FIRCA, ANADER, CNRA, ADERIZ, Intercoton"],
             ["Prélèvements procycliques ; information lacunaire", "Cacao ; fruits et vivriers", "Modulation des prélèvements ; observatoire des prix au producteur", "Ministère chargé des Finances, MINADERPV, OCPV, INS"],
         ]},
        {"t": "twobox", "left": {"label": "Séquencement proposé", "items": [
            "**Campagne 2026/27 (0-6 mois)** : mandat au CCC pour le lissage des ventes 2027/28 ; publication des barèmes 2026/27 ; mission technique sur la formule caoutchouc (DRC mesuré).",
            "**12-24 mois** : réforme des formules caoutchouc et palmier ; pilote d'enchères anacarde dans deux départements ; observatoire des prix opérationnel.",
            "**24-36 mois** : prélèvements cacao modulés selon les cours ; subvention cotonnière recentrée sur le rendement."]},
         "right": {"label": "Points de vigilance (soutenabilité)", "items": [
            f"Relever le prix bord champ sans réformer les ventes anticipées exposerait le CCC à des pertes : en 2025/26, un prix au-dessus du marché a laissé 123 000 t invendues.",
            f"Le modèle ghanéen (≥70 % du FOB) n'est pas un modèle en soi : il coexiste avec un déficit de financement du COCOBOD estimé à 1,4 Md $.",
            f"Pour le riz, soutenir encore le prix du paddy ({fpct(V['riz_tr'])} de la parité FOB) creuserait l'écart avec les importations."]}},
        {"t": "note", "text": "Limites : comparaisons de pays réalisées à date d'observation (et non en moyenne de campagne) lorsque les séries étrangères ne sont pas publiées ; prix étrangers "
                              "parfois issus de la presse ou de sources commerciales (cotés C dans la base) ; FAOSTAT, Comtrade et Eurostat n'étaient pas téléchargeables depuis "
                              "l'environnement d'étude. Détails : METHODOLOGIE_ET_SOURCES.md et base Excel (onglet Audit_QC)."},
    ],
}
PAGES = [page1, page2, page3, page4, page5]
json.dump({"pages": PAGES, "values": {k_: v for k_, v in V.items() if isinstance(v, (int, float, str))}},
          open(ROOT / "scripts" / "note_content.json", "w"), ensure_ascii=False, indent=1, default=float)


# ---------------------------------------------------------------------------
# Rendu HTML
# ---------------------------------------------------------------------------
def rich(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def fig_html(src, width, caption, source):
    svg = (ROOT / "figures" / f"{src}.svg").as_uri()
    return (f'<figure style="width:{width}%"><figcaption class="cap">{rich(caption)}</figcaption>'
            f'<img src="{svg}"/><div class="src">{rich(source)}</div></figure>')


def block_html(b):
    t = b["t"]
    if t == "title":
        return f'<h1 class="maintitle">{rich(b["text"])}</h1>'
    if t == "subtitle":
        return f'<div class="subtitle">{rich(b["text"])}</div>'
    if t == "answer":
        return f'<div class="answer"><span class="lbl">{rich(b["label"])}</span>{rich(b["text"])}</div>'
    if t == "twocol":
        return (f'<div class="twocol"><div><span class="lbl">{b["left"]["label"]}</span>{rich(b["left"]["text"])}</div>'
                f'<div><span class="lbl">{b["right"]["label"]}</span>{rich(b["right"]["text"])}</div></div>')
    if t == "kpis":
        items = "".join(f'<div class="kpi"><div class="v">{rich(i["value"])}<span class="u">{rich(i["unit"])}</span></div>'
                        f'<div class="l">{rich(i["label"])}</div></div>' for i in b["items"])
        return f'<div class="kpis">{items}</div>'
    if t == "h1":
        return f'<h2 class="msg">{rich(b["text"])}</h2>'
    if t == "h2":
        return f'<h3>{rich(b["text"])}</h3>'
    if t == "minititle":
        return f'<div class="cap" style="margin-top:2.4mm">{rich(b["text"])}</div>'
    if t == "lead":
        return f'<p class="lead">{rich(b["text"])}</p>'
    if t == "numbered":
        return '<ol class="constats">' + "".join(f"<li>{rich(i)}</li>" for i in b["items"]) + "</ol>"
    if t == "figure":
        return fig_html(b["src"], b["width"], b["caption"], b["source"])
    if t == "figrow":
        return '<div class="figrow">' + "".join(fig_html(i["src"], i["width"] - 1.5, i["caption"], i["source"]) for i in b["items"]) + "</div>"
    if t == "table":
        cols = "".join(f'<col style="width:{w}%">' for w in b["widths"])
        head_ = "".join(f"<th>{rich(h)}</th>" for h in b["headers"])
        body = ""
        for row in b["rows"]:
            body += "<tr>" + "".join(f"<td>{rich(str(c))}</td>" for c in row) + "</tr>"
        notes = f'<div class="src">{rich(b["notes"])}</div>' if b.get("notes") else ""
        return f'<table class="{b["style"]}"><colgroup>{cols}</colgroup><thead><tr>{head_}</tr></thead><tbody>{body}</tbody></table>{notes}'
    if t == "cards":
        out = f'<div class="cards" style="grid-template-columns: repeat({b.get("cols", 3)}, 1fr)">'
        for c in b["items"]:
            out += (f'<div class="card"><div class="ct"><span class="ic">{c["icon"]}</span>{rich(c["title"])}</div>'
                    f'<p><span class="tag">Constat</span>{rich(c["constat"])}</p>'
                    f'<p><span class="tag">Explication</span>{rich(c["explication"])}</p>'
                    f'<p><span class="tag imp">Implication</span>{rich(c["implication"])}</p></div>')
        return out + "</div>"
    if t == "split":
        l = "".join(block_html(x) for x in b["left"])
        r = "".join(block_html(x) for x in b["right"])
        return f'<div class="split" style="grid-template-columns: {b.get("ratio", "1.05fr 1fr")}"><div class="l">{l}</div><div class="r">{r}</div></div>'
    if t == "callout":
        return f'<div class="callout">{rich(b["text"])}</div>'
    if t == "recos":
        return '<div class="recos">' + "".join(f'<div class="reco"><div class="n">{i["n"]}</div><div><div class="rt">{rich(i["title"])}</div>'
                                               f'<div class="rx">{rich(i["text"])}</div></div></div>' for i in b["items"]) + "</div>"
    if t == "twobox":
        def lst(items):
            return "<ul>" + "".join(f"<li>{rich(i)}</li>" for i in items) + "</ul>"
        return (f'<div class="twobox"><div class="bx"><span class="lbl">{rich(b["left"]["label"])}</span>{lst(b["left"]["items"])}</div>'
                f'<div class="bx warn"><span class="lbl">{rich(b["right"]["label"])}</span>{lst(b["right"]["items"])}</div></div>')
    if t == "note":
        return f'<div class="src note">{rich(b["text"])}</div>'
    raise ValueError(t)


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #ffffff; }
body { font-family: 'Inter TT', 'Liberation Sans', Arial, sans-serif; color: #1b1b1a; font-size: 8.35pt; line-height: 1.32;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; font-feature-settings: "tnum" 0; }
.page { width: 210mm; height: 297mm; padding: 9mm 12mm 10mm 12mm; position: relative; overflow: hidden; page-break-after: always; }
.page:last-child { page-break-after: auto; }
.hdr { display: flex; justify-content: space-between; align-items: center; border-bottom: 2.2px solid #14325c; padding-bottom: 2.2mm; margin-bottom: 3.2mm;
       font-size: 7.2pt; letter-spacing: .06em; color: #14325c; font-weight: 700; }
.hdr span:last-child { font-weight: 500; color: #52514e; letter-spacing: .02em; }
.ftr { position: absolute; bottom: 5mm; left: 12mm; right: 12mm; display: flex; justify-content: space-between; font-size: 6.6pt; color: #898781;
       border-top: 0.6px solid #e1e0d9; padding-top: 1.4mm; }
h1.maintitle { font-size: 21pt; line-height: 1.08; margin: 1mm 0 1.2mm 0; color: #14325c; letter-spacing: -.01em; font-weight: 800; }
.subtitle { font-size: 9.6pt; color: #52514e; margin-bottom: 3mm; }
h2.msg { font-size: 12.4pt; line-height: 1.2; color: #14325c; margin: 0 0 2.4mm 0; font-weight: 750; }
h3 { font-size: 9.6pt; color: #14325c; margin: 2.8mm 0 1.6mm 0; font-weight: 700; text-transform: none; border-left: 3px solid #2a78d6; padding-left: 2mm; }
.lbl { display: inline-block; font-size: 6.8pt; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: #2a78d6; margin-right: 1.8mm; }
.answer { background: #14325c; color: #ffffff; padding: 2.8mm 3.6mm; border-radius: 2mm; font-size: 9.3pt; line-height: 1.35; margin-bottom: 3mm; }
.answer .lbl { color: #9ec5f4; display: block; margin-bottom: .6mm; }
.twocol { display: grid; grid-template-columns: 1fr 1.55fr; gap: 4mm; margin-bottom: 3mm; font-size: 8pt; color: #2b2b29; }
.twocol .lbl { display: block; margin-bottom: .5mm; }
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.6mm; margin-bottom: 2.6mm; }
.kpi { border: 0.7px solid #e1e0d9; border-top: 3px solid #2a78d6; border-radius: 1.6mm; padding: 2.2mm 2.6mm; background: #fbfbfa; }
.kpi .v { font-size: 17pt; font-weight: 750; color: #14325c; line-height: 1; margin-bottom: 1.2mm; }
.kpi .u { font-size: 8pt; font-weight: 600; margin-left: 1mm; color: #52514e; }
.kpi .l { font-size: 7.3pt; color: #3a3a38; line-height: 1.28; }
ol.constats { margin: 0 0 2.4mm 0; padding-left: 5mm; }
ol.constats li { margin-bottom: 1.25mm; padding-left: .6mm; }
ol.constats li::marker { color: #2a78d6; font-weight: 800; }
figure { margin: 0 0 2mm 0; }
figure img { width: 100%; display: block; }
.cap { font-size: 8.2pt; font-weight: 700; color: #14325c; margin-bottom: 1mm; }
.src { font-size: 6.6pt; color: #6e6d68; line-height: 1.3; margin-top: .8mm; }
.lead { font-size: 8.3pt; color: #3a3a38; margin: 0 0 2.4mm 0; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 1mm; }
th { background: #14325c; color: #fff; font-size: 6.9pt; font-weight: 650; text-align: left; padding: 1.5mm 1.4mm; vertical-align: bottom; line-height: 1.2; }
td { font-size: 7.15pt; padding: 1.35mm 1.4mm; border-bottom: 0.6px solid #e1e0d9; vertical-align: top; line-height: 1.27; }
table.matrix td:first-child, table.matrix2 td:first-child, table.plain td:first-child { font-weight: 700; color: #14325c; }
table.matrix td:nth-child(2), table.matrix td:nth-child(4), table.matrix td:nth-child(5), table.matrix td:nth-child(7) { text-align: right; font-variant-numeric: tabular-nums; }
table.matrix tbody tr:nth-child(even) td, table.plain tbody tr:nth-child(even) td, table.matrix2 tbody tr:nth-child(even) td { background: #f6f6f3; }
.figrow { display: flex; gap: 3mm; align-items: flex-start; margin-top: 2.6mm; }
.callout { border-left: 3px solid #eb6834; background: #fdf3ee; padding: 2.2mm 3mm; font-size: 8pt; margin: 2mm 0; border-radius: 0 1.6mm 1.6mm 0; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.6mm; margin: 1.6mm 0 2.2mm 0; }
.card { border: 0.7px solid #e1e0d9; border-radius: 1.8mm; padding: 2.2mm 2.6mm; background: #fcfcfb; }
.card .ct { font-size: 9.2pt; font-weight: 750; color: #14325c; margin-bottom: 1.2mm; }
.card .ic { color: #2a78d6; margin-right: 1.4mm; font-size: 8pt; }
.card p { margin: 0 0 1.15mm 0; font-size: 7.25pt; line-height: 1.3; }
.tag { display: inline-block; font-size: 6.1pt; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; color: #52514e; background: #ecebe6;
       border-radius: 1mm; padding: .2mm 1.2mm; margin-right: 1.3mm; }
.tag.imp { background: #dbe8fa; color: #14325c; }
.split { display: grid; grid-template-columns: 1.05fr 1fr; gap: 4mm; align-items: start; }
.split .cards { margin-top: 0; }
.recos { display: grid; grid-template-columns: 1fr 1fr; gap: 2.4mm 4mm; margin-bottom: 1.6mm; }
.reco { display: grid; grid-template-columns: 7mm 1fr; gap: 2mm; border: 0.7px solid #e1e0d9; border-radius: 1.8mm; padding: 2.2mm 2.6mm; background: #fcfcfb; }
.reco .n { width: 7mm; height: 7mm; border-radius: 50%; background: #2a78d6; color: #fff; font-weight: 800; font-size: 10pt; display: flex; align-items: center; justify-content: center; }
.reco .rt { font-weight: 750; color: #14325c; font-size: 8.6pt; margin-bottom: .8mm; }
.reco .rx { font-size: 7.3pt; line-height: 1.32; color: #2b2b29; }
.note { margin-top: 2mm; }
table.compact td { font-size: 6.9pt; padding: 1mm 1.2mm; } table.compact th { font-size: 6.6pt; padding: 1.2mm; }
table.compact td:nth-child(n+2), table.compact th:nth-child(n+2) { text-align: right; font-variant-numeric: tabular-nums; }
.twobox { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; margin-top: 3mm; }
.twobox .bx { border: 0.7px solid #e1e0d9; border-top: 3px solid #2a78d6; border-radius: 1.6mm; padding: 2.2mm 3mm; background: #fbfbfa; font-size: 7.4pt; }
.twobox .bx.warn { border-top-color: #eb6834; }
.twobox .lbl { display: block; margin-bottom: 1mm; }
.twobox ul { margin: 0; padding-left: 4mm; } .twobox li { margin-bottom: 1mm; line-height: 1.3; }
strong { font-weight: 700; color: #0f2747; }
.answer strong { color: #ffffff; }
"""


def page_html(i, p):
    blocks = "".join(block_html(b) for b in p["blocks"])
    return (f'<section class="page"><div class="hdr"><span>{rich(p["header"][0])}</span><span>{rich(p["header"][1])}</span></div>'
            f'{blocks}<div class="ftr"><span>Les prix agricoles ivoiriens sont-ils compétitifs ? – Note de benchmark, octobre 2026</span>'
            f'<span>Base : Base_Prix_Benchmark_CI.xlsx · page {i}/5</span></div></section>')


HTML = ("<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>Benchmark des prix agricoles – Côte d'Ivoire</title>"
        f"<style>{CSS}</style></head><body>" + "".join(page_html(i + 1, p) for i, p in enumerate(PAGES)) + "</body></html>")
(ROOT / "scripts" / "note.html").write_text(HTML, encoding="utf-8")

from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    exe = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    browser = pw.chromium.launch(executable_path=exe) if Path(exe).exists() else pw.chromium.launch()
    pg = browser.new_page()
    pg.goto((ROOT / "scripts" / "note.html").as_uri())
    pg.wait_for_timeout(800)
    # contrôle de débordement : chaque page doit tenir dans 297 mm
    overflow = pg.evaluate("""() => Array.from(document.querySelectorAll('.page')).map(p => {
        const ftr = p.querySelector('.ftr'); const kids = Array.from(p.children).filter(c => !c.classList.contains('ftr'));
        const last = kids[kids.length-1].getBoundingClientRect(); return Math.round(ftr.getBoundingClientRect().top - last.bottom); })""")
    print("Marge libre avant pied de page (px) :", overflow)
    pg.pdf(path=str(ROOT / "Note_Benchmark_Prix_Agricoles_CI.pdf"), format="A4", print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    browser.close()
print("PDF écrit")
