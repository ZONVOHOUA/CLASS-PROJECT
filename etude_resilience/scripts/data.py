"""
Données brutes de l'étude « Résilience des filières agricoles ivoiriennes aux chocs de prix ».

Toutes les valeurs sont saisies ici UNE SEULE FOIS, puis écrites dans la base Excel
(build_excel.py). Les calculs (transmission, amortissement, recettes, stress tests)
sont faits par formules Excel ; les graphiques et la note sont produits à partir de
la base recalculée (aucune valeur n'est recopiée à la main dans la note).

Code qualité (colonne « Qualité ») :
  A = valeur confirmée par une source primaire ou de presse officielle consultée en
      septembre-octobre 2026 (URL fournie) ;
  B = valeur publiée connue (rapport, communiqué, base internationale) mais non
      re-téléchargée pendant l'étude : à revérifier sur la source citée ;
  C = estimation / reconstitution de l'équipe (ordre de grandeur) : à valider
      institutionnellement avant toute diffusion.
"""

# ---------------------------------------------------------------------------
# 1. SÉRIES ANNUELLES (campagnes)
#    prix_int : prix international moyen de la campagne, dans l'unité indiquée
#    fx       : unités de monnaie locale par USD (moyenne de campagne)
#    conv     : facteur pour passer du prix international (unité) à « monnaie
#               locale / kg » : prix_int * fx * conv
#    prix_prod: prix producteur moyen pondéré de la campagne (monnaie locale / kg)
#    prod_kt  : production commercialisée (milliers de tonnes)
# ---------------------------------------------------------------------------

SERIES_COLS = [
    "filiere", "pays", "campagne", "annee", "prix_int", "unite_int", "fx", "conv",
    "prix_prod", "monnaie", "prod_kt", "mecanisme", "qualite", "source", "url", "commentaire",
]

ICCO = "https://www.icco.org/statistics/"
WB_PINK = "https://www.worldbank.org/en/research/commodity-markets"
CCC = "https://www.conseilcafecacao.ci/"
GOUV = "https://www.gouv.ci/"
COCOBOD = "https://cocobod.gh/"
CCA = "https://www.conseilcotonanacarde.ci/"
ICAC = "https://www.icac.org/"

_cacao_ci = [
    # campagne, annee, ICCO USD/t, XOF/USD, prix pondéré, prod kt, commentaire
    ("2012/13", 2013, 2340, 500, 725, 1449, "1re campagne de la réforme (prix minimum garanti, ventes anticipées)"),
    ("2013/14", 2014, 2920, 490, 750, 1746, ""),
    ("2014/15", 2015, 3080, 560, 850, 1796, ""),
    ("2015/16", 2016, 3000, 590, 1000, 1581, ""),
    ("2016/17", 2017, 2180, 600, 1020, 2020, "Principale 1 100 ; intermédiaire 700 (avr. 2017) ; pondération 80/20"),
    ("2017/18", 2018, 2200, 555, 710, 1964, "Principale 700 ; intermédiaire 750"),
    ("2018/19", 2019, 2300, 575, 750, 2154, ""),
    ("2019/20", 2020, 2450, 590, 825, 2105, ""),
    ("2020/21", 2021, 2420, 550, 950, 2248, "Principale 1 000 ; intermédiaire 750 ; début du DRD/LID (400 USD/t)"),
    ("2021/22", 2022, 2450, 590, 825, 2121, ""),
    ("2022/23", 2023, 2750, 615, 904, 2241, "Principale 900 ; intermédiaire 920"),
    ("2023/24", 2024, 6550, 605, 1100, 1755, "Principale 1 000 ; intermédiaire 1 500 ; production -22 %"),
    ("2024/25", 2025, 8000, 580, 1880, 1850, "Principale 1 800 ; intermédiaire 2 200"),
    ("2025/26", 2026, 4700, 565, 2480, 1850, "Principale 2 800 ; intermédiaire 1 200 (4 mars 2026) ; prix int. et prod. provisoires"),
]
_cacao_gh = [
    # campagne, annee, ICCO USD/t, GHS/USD, prix GHS/kg, prod kt
    ("2012/13", 2013, 2340, 1.95, 3.392, 835, ""),
    ("2013/14", 2014, 2920, 2.50, 3.392, 897, ""),
    ("2014/15", 2015, 3080, 3.30, 5.200, 740, ""),
    ("2015/16", 2016, 3000, 3.85, 6.720, 778, ""),
    ("2016/17", 2017, 2180, 4.25, 7.600, 969, "Prix nominal maintenu malgré la chute des cours"),
    ("2017/18", 2018, 2200, 4.45, 7.600, 905, ""),
    ("2018/19", 2019, 2300, 5.00, 7.600, 812, ""),
    ("2019/20", 2020, 2450, 5.60, 8.240, 771, ""),
    ("2020/21", 2021, 2420, 5.75, 10.560, 1047, ""),
    ("2021/22", 2022, 2450, 6.80, 10.560, 683, ""),
    ("2022/23", 2023, 2750, 11.00, 12.800, 654, ""),
    ("2023/24", 2024, 6550, 12.00, 22.700, 432, "20 128 puis 33 120 GHS/t (avr. 2024) ; production 432 kt (vs 800 kt prévues)"),
    ("2024/25", 2025, 8000, 15.00, 49.900, 600, "49 600 puis 51 660 GHS/t"),
    ("2025/26", 2026, 4700, 11.50, 49.700, 650, "58 000 GHS/t (oct. 2025) puis 41 392 (12 fév. 2026)"),
]
_coton_ci = [
    # campagne, annee, Cotlook A (USD/lb), XOF/USD, prix coton-graine 1er choix, prod kt coton-graine
    ("2014/15", 2015, 0.71, 560, 250, 450, ""),
    ("2015/16", 2016, 0.70, 590, 250, 400, ""),
    ("2016/17", 2017, 0.83, 600, 265, 328, ""),
    ("2017/18", 2018, 0.88, 555, 265, 413, ""),
    ("2018/19", 2019, 0.84, 575, 265, 482, ""),
    ("2019/20", 2020, 0.72, 590, 300, 490, ""),
    ("2020/21", 2021, 0.87, 550, 300, 560, "Prix maintenu en pleine crise COVID grâce à un soutien public"),
    ("2021/22", 2022, 1.30, 590, 300, 560, "Envolée des cours (+80 %) non transmise"),
    ("2022/23", 2023, 1.00, 615, 310, 236, "Attaque de jassides : production -58 %"),
    ("2023/24", 2024, 0.92, 605, 310, 340, ""),
    ("2024/25", 2025, 0.80, 580, 310, 470, ""),
    ("2025/26", 2026, 0.77, 565, 310, 575, "Subvention exceptionnelle 25,3 Mds FCFA (44 FCFA/kg) ; production prévisionnelle"),
]
_anacarde_ci = [
    # campagne, annee, prix noix brute CIF Inde (USD/t), XOF/USD, prix plancher bord champ, prod kt
    ("2016", 2016, 1350, 593, 350, 650, ""),
    ("2017", 2017, 1800, 582, 440, 711, ""),
    ("2018", 2018, 1600, 555, 500, 761, "Plancher 500 non respecté : prix réels 250-300 en fin de campagne"),
    ("2019", 2019, 1150, 586, 375, 634, ""),
    ("2020", 2020, 1000, 575, 400, 848, ""),
    ("2021", 2021, 1100, 554, 305, 968, ""),
    ("2022", 2022, 1050, 623, 305, 1028, ""),
    ("2023", 2023, 1000, 607, 315, 1200, ""),
    ("2024", 2024, 1350, 607, 275, 1100, "Prix réels 500-700 en fin de campagne, bien au-dessus du plancher"),
    ("2025", 2025, 1450, 580, 425, 1200, ""),
    ("2026", 2026, 1300, 560, 400, 1200, "Plancher 400 bord champ / 425 magasin intérieur / 484 portuaire"),
]
_hevea_ci = [
    # annee, TSR20 SICOM (USD/kg), XOF/USD, prix bord champ moyen (FCFA/kg), prod kt
    ("2011", 2011, 4.52, 471, 950, 235, "Pic historique des cours"),
    ("2012", 2012, 3.16, 510, 650, 256, ""),
    ("2013", 2013, 2.52, 494, 500, 290, ""),
    ("2014", 2014, 1.66, 494, 330, 312, ""),
    ("2015", 2015, 1.37, 592, 280, 400, ""),
    ("2016", 2016, 1.37, 593, 260, 453, "Point bas (≈ 230 FCFA/kg début 2016)"),
    ("2017", 2017, 1.65, 582, 380, 580, ""),
    ("2018", 2018, 1.37, 555, 300, 624, ""),
    ("2019", 2019, 1.41, 586, 300, 780, ""),
    ("2020", 2020, 1.33, 575, 290, 936, ""),
    ("2021", 2021, 1.75, 554, 400, 1100, ""),
    ("2022", 2022, 1.55, 623, 370, 1280, ""),
    ("2023", 2023, 1.40, 607, 330, 1450, ""),
    ("2024", 2024, 1.70, 607, 380, 1550, ""),
    ("2025", 2025, 1.75, 580, 420, 1600, ""),
    ("2026", 2026, 1.80, 560, 450, 1600, "Nouveau mécanisme au 1er mai 2026 : part producteur 63 % -> 66 % ; 401 (avr.) -> 493 (juil.)"),
]


def _rows(lst, filiere, pays, unite, conv, monnaie, meca, src, url, qual_prix, qual_int):
    out = []
    for camp, an, pi, fx, pp, q, com in lst:
        q_lbl = qual_prix if an < 2026 else "A/C"
        out.append(dict(
            filiere=filiere, pays=pays, campagne=camp, annee=an, prix_int=pi, unite_int=unite,
            fx=fx, conv=conv, prix_prod=pp, monnaie=monnaie, prod_kt=q, mecanisme=meca,
            qualite=f"prix prod. {q_lbl} ; prix int. {qual_int}", source=src, url=url, commentaire=com,
        ))
    return out


SERIES = (
    _rows(_cacao_ci, "Cacao", "Côte d'Ivoire", "USD/t", 0.001, "FCFA",
          "Prix minimum garanti (>= 60 % CAF), ventes anticipées à la moyenne, FRP",
          "CCC (prix, production) ; ICCO (prix int.)", CCC + " ; " + ICCO, "A", "B")
    + _rows(_cacao_gh, "Cacao", "Ghana", "USD/t", 0.001, "GHS",
            "Prix fixé par Cocobod (>= 70 % FOB depuis Act 1182 de 2026), ventes à terme, prêts syndiqués",
            "Cocobod ; ICCO ; Banque du Ghana (change)", COCOBOD + " ; " + ICCO, "B", "B")
    + _rows(_coton_ci, "Coton", "Côte d'Ivoire", "USD/lb", 2.20462, "FCFA",
            "Prix administré avant semis (Interprofession/État) ; subventions intrants",
            "Conseil du Coton et de l'Anacarde ; ICAC/Cotlook A", CCA + " ; " + ICAC, "B", "B")
    + _rows(_anacarde_ci, "Anacarde", "Côte d'Ivoire", "USD/t", 0.001, "FCFA",
            "Prix plancher bord champ indicatif-obligatoire ; pas de fonds de stabilisation",
            "Conseil du Coton et de l'Anacarde ; cotations noix brute CIF Inde (presse spécialisée)", CCA, "A", "C")
    + _rows(_hevea_ci, "Hévéa", "Côte d'Ivoire", "USD/kg", 1.0, "FCFA",
            "Prix bord champ mensuel = part fixe (66 % depuis mai 2026) du prix de référence net SICOM",
            "APROMAC / CHPC ; Banque mondiale Pink Sheet (TSR20)", WB_PINK, "C", "B")
)

# ---------------------------------------------------------------------------
# 2. ÉPISODES DE CHOC (T0 = avant choc, T2 = point bas / point haut)
#    int_* en unité internationale ; fx ; conv identiques aux séries ;
#    prod_* en monnaie locale / kg ; q_* en kt (campagne de T0 et campagne de T2)
# ---------------------------------------------------------------------------

EPISODE_COLS = [
    "id", "filiere", "pays", "sens", "episode", "t0", "t2", "int_t0", "int_t2", "unite_int",
    "fx_t0", "fx_t2", "conv", "prod_t0", "prod_t2", "monnaie", "q_t0", "q_t2",
    "delai_reaction_mois", "delai_recup_mois", "recup_statut", "absorbeur", "cout_mds_fcfa",
    "mecanisme", "qualite", "source", "url", "commentaire",
]

AJ = "https://www.jeuneafrique.com/1771206/economie-entreprises/crise-du-cacao-la-cote-divoire-reduit-de-pres-de-60-le-prix-dachat-aux-producteurs/"
GOUV_2627 = "https://www.gouv.ci/actualite/campagne-principale-2026-2027-le-prix-bord-champ-du-cacao-est-fixe-a-1200-fcfa-le-kg-le-prix-du-cafe-setablit-a-1300-fcfa-le-kg-8771"
GH_2026 = "https://www.isd.gov.gh/?p=8702"
GH_2627 = "https://gna.org.gh/2026/09/ghana-opens-2026-27-cocoa-season-with-producer-price-of-ghc-42400-per-tonne/"
CAFE_2526 = "https://www.fratmat.info/article/2637237/economie/cafe-cacao/agriculture-les-prix-bord-champs-du-cafe-et-du-cacao-respectivement-fixes-a-1700-fcfa-et-2800-fcfa-pour-la-campagne-2025-2026"
COTON_2526 = "https://www.koaci.com/article/2025/07/31/cote-divoire/societe/cote-divoire-campagne-2025-2026-le-prix-du-coton-de-1er-choix-est-fixe-a-310-fcfakg-et-celui-de-2e-choix-a-285-fcfakg_189056.html"
ANAC_2026 = "https://www.koaci.com/article/2026/02/17/cote-divoire/economie/cote-divoire-noix-de-cajou-brute-les-differents-prix-planchers-obligatoires-fixes-et-les-dispositions-presentees_194450.html"
HEVEA_2026 = "https://www.sikafinance.com/marches/cote-d-ivoire-fin-de-la-decote-et-meilleure-remuneration-des-planteurs-la-campagne-heveicole-2026-demarre-sous-de-bons-auspices_62460"
INVENDUS = "https://fr.allafrica.com/stories/202602280103.html"

EPISODES = [
    # ---------------- CACAO ----------------
    dict(id="CAC-CI-16", filiere="Cacao", pays="Côte d'Ivoire", sens="baisse", episode="Chute des cours 2016-17",
         t0="2016-07", t2="2017-02", int_t0=3050, int_t2=1950, unite_int="USD/t", fx_t0=590, fx_t2=620, conv=0.001,
         prod_t0=1100, prod_t2=700, monnaie="FCFA", q_t0=2020, q_t2=1964,
         delai_reaction_mois=8, delai_recup_mois=42, recup_statut="partielle (1 000 FCFA en oct. 2020 = 91 % du niveau pré-choc)",
         absorbeur="Acheteurs à terme pendant la campagne, puis producteurs ; défauts d'exportateurs absorbés par le CCC",
         cout_mds_fcfa=None, mecanisme="Ventes anticipées + prix garanti", qualite="B",
         source="CCC ; ICCO ; FMI (rapports art. IV 2017)", url=CCC,
         commentaire="Prix principal maintenu 6 mois grâce aux ventes anticipées ; baisse de 36 % à la campagne intermédiaire"),
    dict(id="CAC-GH-16", filiere="Cacao", pays="Ghana", sens="baisse", episode="Chute des cours 2016-17",
         t0="2016-07", t2="2017-02", int_t0=3050, int_t2=1950, unite_int="USD/t", fx_t0=4.0, fx_t2=4.4, conv=0.001,
         prod_t0=7.6, prod_t2=7.6, monnaie="GHS", q_t0=969, q_t2=905,
         delai_reaction_mois=None, delai_recup_mois=0, recup_statut="sans objet (prix nominal maintenu)",
         absorbeur="Cocobod (endettement) ; inflation/dépréciation du cedi pour le producteur",
         cout_mds_fcfa=None, mecanisme="Prix fixé + emprunts syndiqués", qualite="B",
         source="Cocobod ; Banque mondiale", url=COCOBOD,
         commentaire="Stabilité nominale ; le prix réel producteur baisse via l'inflation (~12 %/an)"),
    dict(id="CAC-CM-16", filiere="Cacao", pays="Cameroun", sens="baisse", episode="Chute des cours 2016-17",
         t0="2016-07", t2="2017-02", int_t0=3050, int_t2=1950, unite_int="USD/t", fx_t0=590, fx_t2=620, conv=0.001,
         prod_t0=1450, prod_t2=950, monnaie="FCFA", q_t0=290, q_t2=280,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="à documenter (ONCC)",
         absorbeur="Producteurs (marché libéralisé)", cout_mds_fcfa=None, mecanisme="Marché libre, information prix ONCC",
         qualite="C", source="ONCC Cameroun (bulletins de prix)", url="https://www.oncc.cm/",
         commentaire="Ordres de grandeur ; transmission quasi immédiate"),
    dict(id="CAC-EC-16", filiere="Cacao", pays="Équateur", sens="baisse", episode="Chute des cours 2016-17",
         t0="2016-07", t2="2017-02", int_t0=3050, int_t2=1950, unite_int="USD/t", fx_t0=1, fx_t2=1, conv=0.001,
         prod_t0=2.60, prod_t2=1.70, monnaie="USD", q_t0=250, q_t2=290,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="à documenter (MAG/Anecacao)",
         absorbeur="Producteurs (marché libre)", cout_mds_fcfa=None, mecanisme="Marché libre, économie dollarisée",
         qualite="C", source="Anecacao ; MAG Équateur", url="https://anecacao.com/",
         commentaire="Production en hausse malgré la baisse des prix (productivité CCN-51)"),
    dict(id="CAC-CI-24", filiere="Cacao", pays="Côte d'Ivoire", sens="hausse", episode="Envolée 2023-25",
         t0="2022/23", t2="2024/25", int_t0=2750, int_t2=8000, unite_int="USD/t", fx_t0=615, fx_t2=580, conv=0.001,
         prod_t0=900, prod_t2=1800, monnaie="FCFA", q_t0=2241, q_t2=1850,
         delai_reaction_mois=7, delai_recup_mois=None, recup_statut="",
         absorbeur="Hausse captée par les acheteurs à terme (ventes 2023-24 conclues avant l'envolée) puis CCC/État",
         cout_mds_fcfa=None, mecanisme="Ventes anticipées", qualite="B", source="CCC ; ICCO", url=CCC,
         commentaire="Prix principal à prix principal ; part producteur tombée à ~40 % du prix mondial"),
    dict(id="CAC-GH-24", filiere="Cacao", pays="Ghana", sens="hausse", episode="Envolée 2023-25",
         t0="2022/23", t2="2024/25", int_t0=2750, int_t2=8000, unite_int="USD/t", fx_t0=11.0, fx_t2=15.0, conv=0.001,
         prod_t0=12.8, prod_t2=49.6, monnaie="GHS", q_t0=654, q_t2=600,
         delai_reaction_mois=6, delai_recup_mois=None, recup_statut="",
         absorbeur="Cocobod (contrats reportés de 2023/24, pertes > 1 Md USD)", cout_mds_fcfa=None,
         mecanisme="Ventes à terme", qualite="B", source="Cocobod ; Ministère des Finances du Ghana", url=GH_2026,
         commentaire="Production 2023/24 de 432 kt vs 800 kt prévues : contrats non honorés"),
    dict(id="CAC-CM-24", filiere="Cacao", pays="Cameroun", sens="hausse", episode="Envolée 2023-25",
         t0="2022/23", t2="2024/25", int_t0=2750, int_t2=8000, unite_int="USD/t", fx_t0=615, fx_t2=580, conv=0.001,
         prod_t0=1350, prod_t2=4500, monnaie="FCFA", q_t0=295, q_t2=300,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="",
         absorbeur="Producteurs bénéficiaires (marché libre)", cout_mds_fcfa=None, mecanisme="Marché libre",
         qualite="C", source="ONCC Cameroun", url="https://www.oncc.cm/",
         commentaire="Prix bord champ ayant dépassé 5 000 FCFA/kg au pic"),
    dict(id="CAC-CI-26", filiere="Cacao", pays="Côte d'Ivoire", sens="baisse", episode="Retournement 2025-26",
         t0="2024/25", t2="2026-03", int_t0=8000, int_t2=2860, unite_int="USD/t", fx_t0=580, fx_t2=565, conv=0.001,
         prod_t0=2800, prod_t2=1200, monnaie="FCFA", q_t0=1850, q_t2=1800,
         delai_reaction_mois=15, delai_recup_mois=None, recup_statut="en cours (1 200 FCFA reconduit pour 2026/27)",
         absorbeur="CCC/État (rachat d'invendus ~200 kt au prix garanti), puis producteurs (-57 %)",
         cout_mds_fcfa=240, mecanisme="Ventes anticipées + prix garanti + rachat public",
         qualite="A (prix) / C (coût)", source="Gouvernement CI ; Jeune Afrique ; AllAfrica (invendus)", url=AJ + " ; " + GOUV_2627 + " ; " + INVENDUS,
         commentaire="Coût = estimation : 200 kt x (2 800 - ~1 600 FCFA/kg de valeur de revente). Prix relevé à contre-courant en oct. 2025"),
    dict(id="CAC-GH-26", filiere="Cacao", pays="Ghana", sens="baisse", episode="Retournement 2025-26",
         t0="2025-10", t2="2026-02", int_t0=6000, int_t2=4100, unite_int="USD/t", fx_t0=11.5, fx_t2=11.0, conv=0.001,
         prod_t0=58.0, prod_t2=41.392, monnaie="GHS", q_t0=600, q_t2=650,
         delai_reaction_mois=4, delai_recup_mois=None, recup_statut="42 400 GHS/t en sept. 2026",
         absorbeur="Cocobod (défaut sur facilité relais 70 M USD ; dette héritée 5,8 Mds GHS) puis producteurs",
         cout_mds_fcfa=None, mecanisme="Prix fixé ; Act 1182 (2026) : >= 70 % FOB",
         qualite="A", source="Gouvernement du Ghana (ISD) ; GNA", url=GH_2026 + " ; " + GH_2627,
         commentaire="Nouveau prix = 90 % du FOB brut à 4 200 USD/t"),
    # ---------------- CAFÉ ----------------
    dict(id="CAF-CI-24", filiere="Café", pays="Côte d'Ivoire", sens="hausse", episode="Envolée robusta 2023-25",
         t0="2022/23", t2="2024/25", int_t0=2.25, int_t2=4.80, unite_int="USD/kg", fx_t0=615, fx_t2=580, conv=1.0,
         prod_t0=900, prod_t2=1500, monnaie="FCFA", q_t0=80, q_t2=60,
         delai_reaction_mois=12, delai_recup_mois=None, recup_statut="", absorbeur="CCC / acheteurs à terme",
         cout_mds_fcfa=None, mecanisme="Prix minimum garanti (campagne unique)", qualite="B/C",
         source="CCC ; Banque mondiale (robusta)", url=CAFE_2526, commentaire="Volumes ivoiriens marginaux et en déclin structurel"),
    dict(id="CAF-CI-26", filiere="Café", pays="Côte d'Ivoire", sens="baisse", episode="Repli robusta 2025-26",
         t0="2025/26", t2="2026-07", int_t0=4.60, int_t2=3.70, unite_int="USD/kg", fx_t0=570, fx_t2=560, conv=1.0,
         prod_t0=1700, prod_t2=1300, monnaie="FCFA", q_t0=60, q_t2=60,
         delai_reaction_mois=10, delai_recup_mois=None, recup_statut="en cours", absorbeur="Producteurs (à la campagne suivante)",
         cout_mds_fcfa=None, mecanisme="Prix minimum garanti", qualite="A (prix prod.) / C (prix int.)",
         source="Gouvernement CI", url=GOUV_2627, commentaire=""),
    dict(id="CAF-VN-24", filiere="Café", pays="Vietnam", sens="hausse", episode="Envolée robusta 2023-25",
         t0="2022/23", t2="2024/25", int_t0=2.25, int_t2=4.80, unite_int="USD/kg", fx_t0=23500, fx_t2=25300, conv=1.0,
         prod_t0=41000, prod_t2=120000, monnaie="VND", q_t0=1800, q_t2=1700,
         delai_reaction_mois=0, delai_recup_mois=None, recup_statut="", absorbeur="Producteurs bénéficiaires",
         cout_mds_fcfa=None, mecanisme="Marché libre ; diversification (durian, poivre)", qualite="B/C",
         source="USDA FAS (GAIN Vietnam Coffee Annual)", url="https://fas.usda.gov/data", commentaire=""),
    # ---------------- COTON ----------------
    dict(id="COT-CI-20", filiere="Coton", pays="Côte d'Ivoire", sens="baisse", episode="Choc COVID 2020",
         t0="2020-01", t2="2020-04", int_t0=0.79, int_t2=0.66, unite_int="USD/lb", fx_t0=590, fx_t2=605, conv=2.20462,
         prod_t0=300, prod_t2=300, monnaie="FCFA", q_t0=490, q_t2=560,
         delai_reaction_mois=None, delai_recup_mois=0, recup_statut="sans objet (prix maintenu)",
         absorbeur="État (soutien budgétaire) et sociétés cotonnières", cout_mds_fcfa=None,
         mecanisme="Prix administré + soutien public", qualite="B", source="CCA ; ICAC", url=CCA,
         commentaire="Montant du soutien 2020/21 à confirmer auprès du Ministère du Budget"),
    dict(id="COT-ML-20", filiere="Coton", pays="Mali", sens="baisse", episode="Choc COVID 2020",
         t0="2020-01", t2="2020-04", int_t0=0.79, int_t2=0.66, unite_int="USD/lb", fx_t0=590, fx_t2=605, conv=2.20462,
         prod_t0=275, prod_t2=200, monnaie="FCFA", q_t0=717, q_t2=147,
         delai_reaction_mois=3, delai_recup_mois=12, recup_statut="280 FCFA et ~760 kt en 2021/22",
         absorbeur="Producteurs (boycott des semis)", cout_mds_fcfa=None, mecanisme="Prix administré CMDT",
         qualite="B", source="CMDT ; ICAC ; USDA", url=ICAC,
         commentaire="Baisse annoncée avant semis : réaction d'offre extrême (-80 %)"),
    dict(id="COT-BF-20", filiere="Coton", pays="Burkina Faso", sens="baisse", episode="Choc COVID 2020",
         t0="2020-01", t2="2020-04", int_t0=0.79, int_t2=0.66, unite_int="USD/lb", fx_t0=590, fx_t2=605, conv=2.20462,
         prod_t0=265, prod_t2=250, monnaie="FCFA", q_t0=637, q_t2=470,
         delai_reaction_mois=3, delai_recup_mois=None, recup_statut="à documenter (AICB)",
         absorbeur="Fonds de lissage AICB + État", cout_mds_fcfa=None, mecanisme="Fonds de lissage (prix plancher + moyenne mobile)",
         qualite="C", source="AICB ; Kaminski et al. (IFPRI)", url="https://www.ifpri.org/", commentaire=""),
    dict(id="COT-CI-22", filiere="Coton", pays="Côte d'Ivoire", sens="hausse", episode="Envolée 2021-22",
         t0="2019/20", t2="2021/22", int_t0=0.72, int_t2=1.30, unite_int="USD/lb", fx_t0=590, fx_t2=590, conv=2.20462,
         prod_t0=300, prod_t2=300, monnaie="FCFA", q_t0=490, q_t2=560,
         delai_reaction_mois=None, delai_recup_mois=None, recup_statut="",
         absorbeur="Sociétés cotonnières (marge) ; pas de réserve constituée", cout_mds_fcfa=None,
         mecanisme="Prix administré", qualite="B", source="CCA ; ICAC", url=CCA,
         commentaire="Hausse quasi non transmise et non mise en réserve"),
    # ---------------- ANACARDE ----------------
    dict(id="ANA-CI-19", filiere="Anacarde", pays="Côte d'Ivoire", sens="baisse", episode="Effondrement 2018-19",
         t0="2018-S1", t2="2019", int_t0=1700, int_t2=1150, unite_int="USD/t", fx_t0=555, fx_t2=586, conv=0.001,
         prod_t0=550, prod_t2=330, monnaie="FCFA", q_t0=761, q_t2=634,
         delai_reaction_mois=2, delai_recup_mois=72, recup_statut="prix de marché > 550 FCFA seulement fin 2024",
         absorbeur="Producteurs (plancher non respecté)", cout_mds_fcfa=None, mecanisme="Prix plancher sans fonds",
         qualite="C", source="CCA ; RONGEAD/N'kalô", url=CCA,
         commentaire="Prix effectivement payés ; plancher officiel 500 -> 375"),
    dict(id="ANA-TZ-19", filiere="Anacarde", pays="Tanzanie", sens="baisse", episode="Effondrement 2018-19",
         t0="2017/18", t2="2019/20", int_t0=1700, int_t2=1150, unite_int="USD/t", fx_t0=2250, fx_t2=2300, conv=0.001,
         prod_t0=3.50, prod_t2=2.60, monnaie="TZS (milliers)", q_t0=313, q_t2=225,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="à documenter (CBT)",
         absorbeur="Producteurs ; intervention publique coûteuse en 2018 (achat par l'État)", cout_mds_fcfa=None,
         mecanisme="Récépissés d'entrepôt + enchères", qualite="C", source="Cashewnut Board of Tanzania", url="https://www.cashewnut.go.tz/",
         commentaire="Enchères : transmission rapide mais transparente"),
    dict(id="ANA-CI-24", filiere="Anacarde", pays="Côte d'Ivoire", sens="hausse", episode="Rebond 2024",
         t0="2024-T1", t2="2024-T4", int_t0=1050, int_t2=1650, unite_int="USD/t", fx_t0=605, fx_t2=605, conv=0.001,
         prod_t0=300, prod_t2=600, monnaie="FCFA", q_t0=1100, q_t2=1100,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="", absorbeur="Producteurs bénéficiaires",
         cout_mds_fcfa=None, mecanisme="Marché (plancher non contraignant à la hausse)", qualite="C",
         source="CCA ; presse spécialisée", url=CCA, commentaire="Plancher 275 ; prix de marché 500-700"),
    # ---------------- HÉVÉA ----------------
    dict(id="HEV-CI-16", filiere="Hévéa", pays="Côte d'Ivoire", sens="baisse", episode="Super-cycle baissier 2011-16",
         t0="2011", t2="2016", int_t0=4.52, int_t2=1.37, unite_int="USD/kg", fx_t0=471, fx_t2=593, conv=1.0,
         prod_t0=950, prod_t2=260, monnaie="FCFA", q_t0=235, q_t2=453,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="non récupéré (493 FCFA en juil. 2026)",
         absorbeur="Producteurs ; amortisseur de change (dépréciation EUR/USD)", cout_mds_fcfa=None,
         mecanisme="Prix mensuel indexé SICOM", qualite="C (prix prod.) / B (int.)", source="APROMAC ; Banque mondiale", url=WB_PINK,
         commentaire="Volumes en forte hausse (jeunes plantations) : recette moins touchée que le prix"),
    dict(id="HEV-TH-16", filiere="Hévéa", pays="Thaïlande", sens="baisse", episode="Super-cycle baissier 2011-16",
         t0="2011", t2="2016", int_t0=4.52, int_t2=1.37, unite_int="USD/kg", fx_t0=30.5, fx_t2=35.3, conv=1.0,
         prod_t0=140, prod_t2=45, monnaie="THB", q_t0=3570, q_t2=4470,
         delai_reaction_mois=0, delai_recup_mois=None, recup_statut="non récupéré",
         absorbeur="Producteurs puis État (achats publics 2012-13, aides à la surface, garantie de revenu 2019-22)",
         cout_mds_fcfa=None, mecanisme="Rubber Authority of Thailand ; cess à l'export", qualite="B/C",
         source="Rubber Authority of Thailand ; IRSG", url="https://www.raot.co.th/", commentaire=""),
    dict(id="HEV-CI-26", filiere="Hévéa", pays="Côte d'Ivoire", sens="hausse", episode="Remontée 2026",
         t0="2026-04", t2="2026-07", int_t0=1.65, int_t2=1.85, unite_int="USD/kg", fx_t0=560, fx_t2=560, conv=1.0,
         prod_t0=401, prod_t2=493, monnaie="FCFA", q_t0=1600, q_t2=1600,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="", absorbeur="Producteurs bénéficiaires",
         cout_mds_fcfa=None, mecanisme="Nouveau mécanisme (66 % du prix net)", qualite="A (prix prod.) / C (int.)",
         source="Sika Finance ; AIP", url=HEVEA_2026, commentaire="Effet combiné hausse des cours + hausse de la part producteur"),
    # ---------------- PALMIER ----------------
    dict(id="PAL-CI-22", filiere="Palmier à huile", pays="Côte d'Ivoire", sens="baisse", episode="Retournement 2022",
         t0="2022-03", t2="2022-10", int_t0=1780, int_t2=890, unite_int="USD/t", fx_t0=595, fx_t2=655, conv=0.001,
         prod_t0=120, prod_t2=80, monnaie="FCFA", q_t0=2500, q_t2=2500,
         delai_reaction_mois=1, delai_recup_mois=None, recup_statut="à documenter (AIPH/CHPC)",
         absorbeur="Producteurs de régimes et huileries ; marché régional partiellement protégé (TEC UEMOA)",
         cout_mds_fcfa=None, mecanisme="Prix mensuel des régimes indexé sur l'huile brute", qualite="C",
         source="AIPH ; Banque mondiale", url=WB_PINK, commentaire="Prix régimes (FCFA/kg) à valider auprès de l'AIPH/CHPC"),
    dict(id="PAL-ID-22", filiere="Palmier à huile", pays="Indonésie", sens="baisse", episode="Retournement 2022",
         t0="2022-03", t2="2022-07", int_t0=1780, int_t2=1050, unite_int="USD/t", fx_t0=14350, fx_t2=14950, conv=0.001,
         prod_t0=3800, prod_t2=1600, monnaie="IDR", q_t0=46000, q_t2=46000,
         delai_reaction_mois=1, delai_recup_mois=4, recup_statut="partielle après levée de l'interdiction et du prélèvement",
         absorbeur="Petits planteurs (interdiction d'exporter avr.-mai 2022)", cout_mds_fcfa=None,
         mecanisme="Fonds BPDPKS (prélèvement export progressif)", qualite="C", source="BPDPKS ; USDA", url="https://www.bpdp.or.id/",
         commentaire="Choc amplifié par une mesure commerciale nationale"),
    # ---------------- RIZ (consommateur) ----------------
    dict(id="RIZ-CI-23", filiere="Riz (importé)", pays="Côte d'Ivoire", sens="hausse", episode="Restrictions indiennes 2023",
         t0="2023-06", t2="2024-01", int_t0=515, int_t2=660, unite_int="USD/t", fx_t0=605, fx_t2=605, conv=0.001,
         prod_t0=425, prod_t2=475, monnaie="FCFA", q_t0=1500, q_t2=1500,
         delai_reaction_mois=2, delai_recup_mois=None, recup_statut="", absorbeur="Importateurs et État (plafonnement, mesures fiscales)",
         cout_mds_fcfa=None, mecanisme="Prix plafonnés ; régime fiscal à l'importation", qualite="C",
         source="FAO GIEWS FPMA ; Conseil national de lutte contre la vie chère", url="https://fpma.fao.org/",
         commentaire="Prix consommateur (riz brisé importé) ; Q = importations"),
]

# ---------------------------------------------------------------------------
# 3. PARAMÈTRES DU TEST DE STRESS (base 2026/27)
# ---------------------------------------------------------------------------
STRESS_COLS = ["filiere", "p0", "unite", "q0_kt", "beta1", "beta2", "part_publique",
               "capacite_mds", "protection", "justification"]
STRESS = [
    dict(filiere="Cacao", p0=1200, unite="FCFA/kg", q0_kt=1800, beta1=0.2, beta2=0.95, part_publique=0.30, capacite_mds=0,
         protection="Prix garanti + ventes anticipées (~70 % de la récolte vendue à terme)",
         justification="beta1 observé 2016/17 et 2025/26 (~0,2 sur le prix moyen de campagne) ; beta2 = moyenne 2017/18 (1,09) et 2026/27 (0,86) ; part publique = récolte non vendue à terme ; FRP non publié -> capacité 0 par prudence"),
    dict(filiere="Café", p0=1300, unite="FCFA/kg", q0_kt=60, beta1=0.0, beta2=1.0, part_publique=0.30, capacite_mds=0,
         protection="Prix garanti, une seule campagne/an", justification="Même architecture que le cacao, sans campagne intermédiaire"),
    dict(filiere="Coton", p0=310, unite="FCFA/kg", q0_kt=575, beta1=0.0, beta2=0.5, part_publique=0.5, capacite_mds=0,
         protection="Prix fixé avant semis + subventions intrants (25,3 Mds en 2025/26)",
         justification="Prix intangible en cours de campagne ; beta2 = ajustement partiel (pas de fonds de lissage) ; enveloppe 2025/26 déjà affectée aux intrants ; part publique 0,5 = partage supposé État / sociétés cotonnières (C)"),
    dict(filiere="Anacarde", p0=400, unite="FCFA/kg", q0_kt=1200, beta1=1.0, beta2=1.0, part_publique=0.0, capacite_mds=0,
         protection="Prix plancher sans fonds ni obligation d'achat", justification="2018-19 : transmission ~1 sur les prix réellement payés"),
    dict(filiere="Hévéa", p0=493, unite="FCFA/kg humide", q0_kt=2700, beta1=1.0, beta2=1.0, part_publique=0.0, capacite_mds=0,
         protection="Indexation mensuelle (66 % du prix net de référence)", justification="Formule : le pourcentage de baisse est transmis en un mois ; Q0 = ~1 600 kt sec / teneur en caoutchouc sec ~0,6 = ~2 700 kt humide (C)"),
    dict(filiere="Palmier à huile", p0=100, unite="FCFA/kg régime", q0_kt=2500, beta1=0.7, beta2=0.9, part_publique=0.0, capacite_mds=0,
         protection="Prix des régimes indexé ; marché régional protégé", justification="2022 : transmission ~0,7 (estimation C)"),
]

SCENARIOS = [
    dict(code="S1", nom="Prix int. -10 %", choc=-0.10, dq=0.0, deux_campagnes=False),
    dict(code="S2", nom="Prix int. -20 %", choc=-0.20, dq=0.0, deux_campagnes=False),
    dict(code="S3", nom="Prix int. -30 %", choc=-0.30, dq=0.0, deux_campagnes=False),
    dict(code="S4", nom="Prix -30 % et production -10 %", choc=-0.30, dq=-0.10, deux_campagnes=False),
    dict(code="S5", nom="Prix -30 % pendant 2 campagnes", choc=-0.30, dq=0.0, deux_campagnes=True),
]

# ---------------------------------------------------------------------------
# 4. BENCHMARK DES MÉCANISMES
# ---------------------------------------------------------------------------
MECA_COLS = ["pays", "filiere", "categorie", "mecanisme", "resultat", "cout_limite", "enseignement", "transposable", "qualite", "source"]
MECANISMES = [
    ("Ghana", "Cacao", "A+D", "Prix fixé par Cocobod, ventes à terme, prêts syndiqués ; Act 1182 (2026) : >= 70 % du FOB",
     "Prix nominal intact en 2016-18 (transmission 0)", "Dette héritée 5,8 Mds GHS ; défaut sur facilité relais 70 M USD ; contrats 2023/24 reportés ; coupe de -29 % en fév. 2026",
     "Stabiliser par la dette n'est pas soutenable ; une règle de partage explicite (% FOB) rend les ajustements prévisibles", "Partiel (règle de partage)", "A/B", "isd.gov.gh ; gna.org.gh"),
    ("Équateur", "Cacao", "E", "Marché libre, économie dollarisée, différenciation qualité (fino de aroma, CCN-51)",
     "Producteurs ~85-90 % du FOB ; production presque doublée depuis 2016", "Aucune protection contre les baisses",
     "Transmettre les hausses finance l'investissement et la productivité", "Partiel (transmission des hausses)", "C", "Anecacao"),
    ("Burkina Faso", "Coton", "C", "Fonds de lissage AICB : prix plancher + ajustement selon moyenne mobile des cours ; abondé en bonnes années",
     "Choc 2020 amorti (transmission estimée ~0,3)", "Épuisé lors de chocs longs ; recapitalisations par bailleurs",
     "Règle automatique de dotation/décaissement, plafonnée", "Oui (coton, café)", "C", "Kaminski, Headey & Bernard (IFPRI 2011)"),
    ("Mali", "Coton", "A", "Prix administré par la CMDT ; baisse brutale avant semis 2020 (275 -> 200 FCFA)",
     "Production -80 % (717 -> 147 kt) ; revenu effondré", "Rattrapage en 2021/22 seulement",
     "Un ajustement brutal annoncé avant semis détruit la recette : lisser et pré-annoncer la règle", "Contre-exemple", "B", "CMDT ; USDA"),
    ("Brésil", "Coton, café", "A+B+F", "PGPM/PEPRO (paiement de l'écart au prix minimum par enchères), FUNCAFÉ (crédit), marchés à terme B3, assurance PSR subventionnée",
     "Revenu stabilisé sans figer le prix de marché", "Coût budgétaire annuel voté ; nécessite marchés financiers et données de rendement",
     "Paiements contracycliques ciblés et budgétés ex ante", "Partiel (à moyen terme)", "B", "CONAB ; MAPA"),
    ("Malaisie", "Hévéa", "B", "Incitation à la production (IPG) : versement automatique quand le prix tombe sous un seuil",
     "Plancher de revenu pour petits planteurs", "Financé par le budget ; seuil à ajuster",
     "Déclencheur automatique et plafonné par producteur", "Oui (hévéa)", "C", "RISDA / LGM"),
    ("Thaïlande", "Hévéa", "B+D", "Achats publics (2012-13), aides à la surface, garantie de revenu (2019-22) plafonnée par exploitation ; cess export",
     "Revenu plancher pour petits planteurs", "Coût élevé, stocks publics invendables (2012-13)",
     "Plafonner la garantie ; éviter le stockage public", "Partiel", "B/C", "Rubber Authority of Thailand"),
    ("Indonésie", "Palmier à huile", "C+E", "Fonds BPDPKS financé par un prélèvement export progressif (replantation, biodiesel)",
     "Fonds de grande taille ; soutien de la demande intérieure", "Interdiction d'exporter en 2022 : prix des régimes -55 %",
     "Le prélèvement progressif constitue des réserves en haut de cycle ; éviter les mesures commerciales brutales", "Oui (prélèvement progressif)", "C", "BPDPKS ; USDA"),
    ("Tanzanie", "Anacarde", "F", "Récépissés d'entrepôt + enchères publiques",
     "Prix transparents, financement de stockage", "Intervention 2018 (achat public) coûteuse", "Outil de crédit-stockage adapté à l'anacarde", "Oui (anacarde)", "C", "Coulter & Onumah (2002) ; CBT"),
    ("Vietnam", "Café, anacarde", "E", "Transformation, irrigation, diversification des cultures (durian, poivre)",
     "Volumes stables malgré transmission totale", "Pas de protection prix", "La productivité et la diversification sont des amortisseurs de revenu", "Oui (long terme)", "B", "USDA FAS"),
]

# ---------------------------------------------------------------------------
# 5. REVUE DE LITTÉRATURE
# ---------------------------------------------------------------------------
LIT_COLS = ["reference", "instrument", "pays", "resultat", "limites", "enseignement_ci"]
LITTERATURE = [
    ("Newbery & Stiglitz (1981), The Theory of Commodity Price Stabilization, Oxford UP", "Stabilisation des prix", "Théorie",
     "Gains de bien-être de la stabilisation des prix faibles ; c'est l'instabilité du revenu qui compte", "Hypothèses de marchés complets", "Cibler la recette/le revenu plutôt que le prix"),
    ("Deaton & Laroque (1992), Review of Economic Studies 59(1)", "Stocks régulateurs", "Monde",
     "Les prix des matières premières ont de longues périodes de calme et des pics : les stocks s'épuisent", "Modèle de stockage compétitif", "Un fonds doit être dimensionné pour des chocs longs"),
    ("Cashin, Liang & McDermott (2000), IMF Staff Papers 47(2)", "Fonds de stabilisation", "Monde",
     "Les chocs de prix sont très persistants (plusieurs années) pour de nombreuses matières premières", "Échantillon 1957-98", "Une règle de décaissement doit supposer que le choc peut durer >= 2 campagnes"),
    ("Deaton (1999), Journal of Economic Perspectives 13(3)", "Offices de commercialisation", "Afrique",
     "Les offices ont souvent capté les hausses et transmis les baisses", "Analyse historique", "Règle de partage transparente des hausses"),
    ("Varangis & Larson (1996), WB Policy Research WP 1667", "Couverture (futures/options)", "Pays en développement",
     "Les instruments de marché sont moins coûteux que les fonds pour les risques de court terme", "Ne couvrent pas les chocs pluriannuels", "Options put sur une partie des ventes anticipées"),
    ("Borensztein, Jeanne & Sandri (2013), Journal of Development Economics 101", "Couverture macro", "Exportateurs de matières premières",
     "La couverture réduit fortement le besoin de réserves de précaution", "Coût des primes, risque politique en cas de perte", "Complément aux ventes anticipées"),
    ("Gilbert (1996), World Development 24(1)", "Accords internationaux de produits", "Monde",
     "Échec des accords de stabilisation (stocks, quotas)", "—", "Éviter les mécanismes de soutien des cours mondiaux (ex. ITRC hévéa)"),
    ("Baffes & Gardner (2003), Policy Reform 6(3)", "Transmission des prix", "10 pays",
     "Transmission faible et lente sous régimes administrés", "Données annuelles", "Mesurer la transmission séparément par régime"),
    ("Meyer & von Cramon-Taubadel (2004), Journal of Agricultural Economics 55(3)", "Transmission asymétrique", "Revue",
     "L'asymétrie est fréquente ; méthodes ECM/seuils", "Sensibilité aux méthodes", "Tester beta hausse vs beta baisse"),
    ("Shin, Yu & Greenwood-Nimmo (2014), in Festschrift P. Schmidt, Springer", "NARDL", "Méthode",
     "Cadre pour estimer des effets de long terme asymétriques", "Exige des séries mensuelles longues", "Méthode recommandée pour l'annexe économétrique"),
    ("Minot (2011), IFPRI Discussion Paper 1059", "Transmission prix vivriers", "Afrique subsaharienne",
     "Transmission forte pour le riz importé, faible pour le maïs", "Données 2007-08", "Riz : surveiller ; maïs : ne pas forcer l'analyse internationale"),
    ("Kaminski, Headey & Bernard (2011), IFPRI DP 1074", "Fonds de lissage coton", "Burkina Faso",
     "Le mécanisme de lissage a amorti les chocs mais s'est épuisé", "Gouvernance et capitalisation", "Fonds de lissage coton pour la CI"),
    ("Delpeuch & Leblois (2013), World Development 51", "Réformes coton", "Afrique de l'Ouest",
     "La réponse de l'offre aux réformes de prix est faible et hétérogène", "Données nationales", "Le prix seul n'explique pas la production"),
    ("Coulter & Onumah (2002), Food Policy 27(4)", "Récépissés d'entrepôt", "Afrique",
     "Les récépissés facilitent le crédit et le report des ventes", "Exige un cadre légal et des entrepôts certifiés", "Pertinent pour l'anacarde"),
    ("Karlan, Osei, Osei-Akoto & Udry (2014), Quarterly Journal of Economics 129(2)", "Assurance indicielle", "Ghana",
     "L'assurance augmente l'investissement agricole ; la contrainte de risque est déterminante", "Demande faible au prix du marché", "Assurance rendement subventionnée pour le coton"),
    ("Kireyev (2010), IMF WP 10/269", "Taxe à l'exportation cacao", "Côte d'Ivoire",
     "Pouvoir de marché limité ; la taxe pèse en partie sur les producteurs", "Données pré-réforme", "Le DUS fait partie de l'absorbeur (recettes publiques)"),
    ("Frankel (2011), NBER WP 16945", "Règles budgétaires contracycliques", "Chili",
     "Règles fondées sur un prix de référence de long terme fixé par un comité indépendant", "Contexte cuivre", "Prix de référence indépendant pour le FRP"),
    ("OCDE (2011), Managing Risk in Agriculture: Policy Assessment and Design", "Gestion des risques", "OCDE",
     "Distinguer risques normaux (exploitant), marchands (marché) et catastrophiques (État)", "Pays développés", "Répartir les couches de risque entre acteurs"),
]

# ---------------------------------------------------------------------------
# 6. CARTE DE VULNÉRABILITÉ (lecture qualitative des filières hors quantification)
# ---------------------------------------------------------------------------
FILIERES_QUALI = [
    ("Banane dessert", "Forte (UE), contrats en EUR", "Faible : contrats annuels intégrés ; pas de risque de change (FCFA arrimé à l'EUR)", "Producteurs intégrés (plantations industrielles)",
     "Vulnérabilité d'accès au marché (préférences UE, normes) plus que de prix"),
    ("Ananas, mangue", "Forte (UE)", "Non mesurable (prix contractuels, données de prix producteur absentes)", "Exportateurs / stations de conditionnement",
     "Choc de compétitivité structurel (ananas MD2) et sanitaire (mouche des fruits), non un choc de prix"),
    ("Sucre", "Faible (marché intérieur protégé)", "Faible : protection à l'importation", "Consommateur / budget (prix intérieur administré)", "Coût de protection pour le consommateur"),
    ("Riz importé", "Forte (importations ~1,5 Mt)", "Partielle (~0,4 au consommateur en 2023)", "Importateurs, État (fiscalité), consommateurs", "Choc de pouvoir d'achat urbain"),
    ("Maïs", "Faible", "Non significative", "—", "Analyse internationale non pertinente"),
]
