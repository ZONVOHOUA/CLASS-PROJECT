# -*- coding: utf-8 -*-
"""
Données d'entrée collectées pour le benchmark des prix agricoles ivoiriens.

Chaque observation conserve : produit, qualité, stade, campagne/période, pays,
monnaie, unité, prix d'origine, source, URL, date de consultation et fiabilité.

Fiabilité :
  A = source officielle primaire (ministère, régulateur, banque centrale, institution internationale)
  B = presse ou agence reprenant une annonce officielle datée et chiffrée
  C = source secondaire / commerciale / approximation documentée (à utiliser avec prudence)

Toutes les URL ont été consultées le 2026-10-01 (accès par moteur de recherche ; voir
METHODOLOGIE_ET_SOURCES.md pour les contraintes d'accès réseau).
"""

DATE_CONSULT = "2026-10-01"

# ---------------------------------------------------------------------------
# 1. Compléments mensuels aux cours internationaux (le fichier Banque mondiale
#    s'arrête en janvier 2026). Valeur = expression Excel (conversion visible).
# ---------------------------------------------------------------------------
# série -> {mois: (formule_excel_en_usd_par_kg_ou_t, source_courte, url, fiabilité)}
SUPP_COURS = {
    "cacao": {
        "2026-02": ("=3587.19/1000", "FMI PCPS (PCOCOUSDM, 3 587,19 USD/t)", "https://fred.stlouisfed.org/series/PCOCOUSDM", "A"),
        "2026-03": ("=3241.49/1000", "FMI PCPS (3 241,49 USD/t)", "https://fred.stlouisfed.org/series/PCOCOUSDM", "A"),
        "2026-04": ("=3392.14/1000", "FMI PCPS (3 392,14 USD/t)", "https://fred.stlouisfed.org/series/PCOCOUSDM", "A"),
        "2026-05": ("=4142.97/1000", "FMI PCPS (4 142,97 USD/t)", "https://fred.stlouisfed.org/series/PCOCOUSDM", "A"),
        "2026-06": ("=4395.46/1000", "FMI PCPS (4 395,46 USD/t)", "https://fred.stlouisfed.org/series/PCOCOUSDM", "A"),
        "2026-07": ("=5619.19/1000", "FMI PCPS (5 619,19 USD/t)", "https://fred.stlouisfed.org/series/PCOCOUSDM", "A"),
        "2026-08": ("=5987/1000", "FocusEconomics (série FMI) 5 987 USD/t ; Pink Sheet sept. 2026 : 5,95 USD/kg", "https://www.focus-economics.com/commodities/agricultural/cocoa/", "B"),
    },
    "robusta": {
        "2026-02": ("=179.73*0.0220462", "OIC, indicateur groupe Robustas 179,73 c/lb (CMR fév. 2026)", "https://ico.org/documents/cy2025-26/cmr-0226-e.pdf", "A"),
        "2026-03": ("=176.76*0.0220462", "FMI PCPS (PCOFFROBUSDM) 176,76 c/lb", "https://fred.stlouisfed.org/series/PCOFFROBUSDM", "A"),
        "2026-04": ("=164.65*0.0220462", "FMI PCPS 164,65 c/lb", "https://fred.stlouisfed.org/series/PCOFFROBUSDM", "A"),
        "2026-05": ("=166.51*0.0220462", "FMI PCPS 166,51 c/lb", "https://fred.stlouisfed.org/series/PCOFFROBUSDM", "A"),
        "2026-06": ("=169.39*0.0220462", "FMI PCPS 169,39 c/lb", "https://fred.stlouisfed.org/series/PCOFFROBUSDM", "A"),
        "2026-07": ("=185.23*0.0220462", "FMI PCPS 185,23 c/lb (OIC : 184,78)", "https://fred.stlouisfed.org/series/PCOFFROBUSDM", "A"),
        "2026-08": ("=180.63*0.0220462", "OIC, indicateur groupe Robustas 180,63 c/lb (CMR août 2026)", "https://www.ico.org/documents/cy2025-26/cmr-0826-e.pdf", "A"),
    },
    "tsr20": {
        "2026-03": ("=1.965", "SGX SICOM Rubber Monthly Report, mars 2026 (moyenne TSR20 1,965 USD/kg)",
                    "https://api2.sgx.com/sites/default/files/2026-04/SICOM%20SGX%20March%202026%20.pdf", "A"),
    },
}

# ---------------------------------------------------------------------------
# 2. Compléments mensuels de taux de change (monnaie locale par USD)
# ---------------------------------------------------------------------------
SUPP_CHANGE = {
    "GHS": {
        "2025-11": ("=(10.9+11.27)/2", "FMI (fin oct. 10,90 ; fin nov. 11,27) : moyenne des fins de mois (approximation)", "C"),
        "2025-12": ("=(11.27+10.45)/2", "FMI (fin nov. 11,27 ; fin déc. 10,45) : moyenne des fins de mois (approximation)", "C"),
        "2026-01": ("=10.7921", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-02": ("=10.9188", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-03": ("=10.8721", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-04": ("=11.0664", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-05": ("=11.4498", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-06": ("=11.4068", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-07": ("=11.5423", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-08": ("=11.3349", "Banque du Ghana, taux interbancaire moyen mensuel", "A"),
        "2026-09": ("=(11.55+11.43)/2", "Banque du Ghana, interbancaire 18/09 (11,55) et 28/09/2026 (11,43)", "B"),
    },
    "UGX": {
        "2026-07": ("=3678.495", "Moyenne USD/UGX juillet 2026 (poundsterlinglive.com)", "C"),
    },
    "VND": {
        "2026-09": ("=(25780+26160)/2", "Vietcombank, achat/vente 9 sept. 2026 (daibieunhandan.vn)", "B"),
    },
    "TZS": {
        "2025-11": ("=(2452.5+2422.5+2427.5)/3", "UBA Tanzania, cours d'ouverture 5, 18 et 20 nov. 2025 (milieu de fourchette)", "C"),
    },
    "NGN": {
        "2026-09": ("=5728.5/4.311", "Taux implicite de la source (5 728,5 NGN/kg = 4 311 USD/t), mansamarkets.com", "C"),
    },
}

SUPP_CHANGE_URL = {
    "GHS": "https://www.bog.gov.gh/economic-data/exchange-rate/",
    "UGX": "https://www.poundsterlinglive.com/history/USD-UGX-2026",
    "VND": "https://en.daibieunhandan.vn/print/10429994.html",
    "TZS": "https://www.ubatanzania.co.tz/wp-content/uploads/sites/21/2025/11/OPENING-FX-RATES-UBA-TANZANIA-20_November_2025.pdf",
    "NGN": "https://www.mansamarkets.com/blog/cocoa-farmgate-price-vs-world-price",
}

# ---------------------------------------------------------------------------
# 3. Inflation (indice des prix à la consommation, Côte d'Ivoire), % annuel moyen
# ---------------------------------------------------------------------------
INFLATION_CI = [
    # année, taux %, source, url
    (2016, 0.72, "Banque mondiale (WDI, d'après INS)", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=CI"),
    (2017, 0.69, "Banque mondiale (WDI, d'après INS)", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=CI"),
    (2018, 0.40, "Banque mondiale (WDI, d'après INS)", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=CI"),
    (2019, 0.79, "Banque mondiale (WDI, d'après INS)", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=CI"),
    (2020, 2.41, "Banque mondiale (WDI, d'après INS)", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=CI"),
    (2021, 4.16, "Banque mondiale (WDI) ; BCEAO 4,2 %", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=CI"),
    (2022, 5.23, "Banque mondiale (WDI) ; BCEAO 5,2 %", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=CI"),
    (2023, 4.37, "Banque mondiale (WDI) ; BCEAO 4,4 %", "https://www.bceao.int/sites/default/files/2024-04/Rapport%20annuel%20sur%20l'%C3%A9volution%20des%20prix%20%C3%A0%20la%20consommation%20-%202023.pdf"),
    (2024, 3.50, "BCEAO, Rapport annuel sur l'inflation 2024", "https://www.bceao.int/sites/default/files/2025-07/Rapport_annuel_sur_l-inflation-2024.pdf"),
    (2025, 0.10, "DG Trésor / BCEAO (rapport annuel prix UEMOA 2025)", "https://www.bceao.int/sites/default/files/2026-06/Rapport_annuel_sur%20l%27%C3%A9volution%20des%20prix%20%C3%A0%20la%20consommation%20dans%20l%27UEMOA%20en%202025.pdf"),
]

# ---------------------------------------------------------------------------
# 4. Sources (référentiel)
# ---------------------------------------------------------------------------
S = {}
def src(key, institution, titre, url, typ, fiab):
    S[key] = dict(cle=key, institution=institution, titre=titre, url=url, type=typ, fiabilite=fiab)
    return key

# Cacao CI
src("CI_CAC_1617P", "CCC / Gouvernement (via Connectionivoirienne)", "Le kilo de cacao à 1 100 FCFA pour la campagne 2016-2017", "https://connectionivoirienne.net/2016/09/28/cote-divoire-le-kilo-de-cacao-a-1-100-fcfa-pour-la-campagne-2016-2017", "Presse (annonce officielle)", "B")
src("CI_CAC_1617I", "CCC (via Connectionivoirienne)", "Prix bord champ du cacao pour la campagne intermédiaire fixé à 700 FCFA", "https://connectionivoirienne.net/2017/03/30/cote-divoire-le-prix-bord-champ-du-cacao-pour-la-campagne-intermediaire-fixe-a-700-fcfa-1-euro/", "Presse (annonce officielle)", "B")
src("CI_CAC_1718", "CCC (via Connectionivoirienne)", "Le prix d'achat au producteur de cacao maintenu à 700 FCFA (campagne intermédiaire 2017-2018)", "https://connectionivoirienne.net/2018/03/30/le-prix-dachat-au-producteur-de-cacao-en-cote-divoire-maintenu-a-700-francs-cfa", "Presse (annonce officielle)", "B")
src("CI_CAC_1819P", "CCC (via Agence Ecofin)", "Cocoa farm-gate price set to CFA750 per kilo for 2018/2019 season", "https://www.ecofinagency.com/agriculture/0210-39023-cote-d-ivoire-cocoa-farm-gate-price-set-to-cfa750-per-kilo-for-2018/2019-season", "Presse (annonce officielle)", "B")
src("CI_CAC_1819I", "Gouvernement (via Afrique-sur7)", "Le gouvernement maintient le prix du cacao à 750 FCFA pour la campagne intermédiaire", "https://www.afrique-sur7.fr/420663-prix-cacao-750-campagne-intermediaire", "Presse (annonce officielle)", "B")
src("CI_CAC_1920P", "CCC (via Connectionivoirienne)", "Le prix du kg de cacao fixé à 825 FCFA pour la campagne 2019-2020", "https://connectionivoirienne.net/2019/10/01/le-prix-du-kg-de-cacao-fixe-a-825-fcfa-en-cote-divoire-pour-la-campagne-2019-2020/", "Presse (annonce officielle)", "B")
src("CI_CAC_1920I", "CCC (via Connectionivoirienne)", "Le prix bord champ du cacao maintenu à 825 FCFA/kg pour la petite traite (le prix de marché aurait été de 625 FCFA)", "https://connectionivoirienne.net/2020/04/01/le-prix-bord-champ-du-cacao-maintenu-a-825-fcfa-kg-pour-la-petite-traite-en-cote-divoire/", "Presse (annonce officielle)", "B")
src("CI_CAC_2021P", "CCC (via BusinessWorld/Reuters)", "Ivory Coast raises 2020/21 cocoa farmgate price by 21% (1 000 FCFA/kg)", "https://www.pressreader.com/philippines/business-world/20201005/281676847366265", "Presse (annonce officielle)", "B")
src("CI_CAC_2021I", "CCC (via KOACI)", "Cacao : le Conseil fixe le kg de la fève à 750 FCFA pour la campagne intermédiaire", "https://www.koaci.com/index.php/article/2021/03/31/cote-divoire/politique/cote-divoire-cacao-le-conseil-fixe-le-kg-de-la-feve-a-750-fcfa-pour-la-campagne-intermediaire_149966.html", "Presse (annonce officielle)", "B")
src("CI_CAC_2122P", "CCC (via Connectionivoirienne)", "Le prix bord-champ du café fixé à 700 FCFA/kg, le cacao à 825 FCFA", "https://connectionivoirienne.net/2021/10/01/le-prix-bord-champ-du-cafe-fixe-a-700-fcfa-kg/", "Presse (annonce officielle)", "B")
src("CI_CAC_2122I", "CCC (via Abidjan.net)", "Le prix du kg de cacao pour la campagne intermédiaire maintenu à 825 FCFA", "https://news.abidjan.net/articles/706140/cote-divoire-le-prix-du-kg-de-cacao-pour-la-campagne-intermediaire-maintenu-a-825-fcfa", "Presse (annonce officielle)", "B")
src("CI_CAC_2223P", "CCC (via Further Africa/Reuters)", "Ivory Coast raises cocoa farmgate price by 9% for 2022/2023 (900 FCFA/kg)", "https://furtherafrica.com/2022/10/03/ivory-coast-raises-cocoa-farmgate-price-by-9-for-2022-2023-harvest/", "Presse (annonce officielle)", "B")
src("CI_CAC_2223I", "CCC (via ConfectioneryNews)", "Mid-crop 2022/23 farmgate price unchanged at 900 XOF/kg", "https://www.confectionerynews.com/Article/2023/05/03/cocoa-futures-up-6-as-farmgate-prices-stall-due-to-sluggish-exports-in-cote-d-ivoire/", "Presse (annonce officielle)", "B")
src("CI_CAC_2324P", "CCC (via Sika Finance)", "Des prix d'achat de 1 000 FCFA/kg pour le cacao et 900 FCFA/kg pour le café", "https://www.sikafinance.com/marches/cote-divoire-des-prix-dachat-de-1-000-fcfakg-pour-le-cacao-et-900-fcfakg-pour-le-cafe_42852", "Presse (annonce officielle)", "B")
src("CI_CAC_2324I", "CCC (via FoodBev/Reuters)", "Ivory Coast raises cocoa farmgate price by 50% (1 500 FCFA/kg, avril 2024)", "https://www.foodbev.com/news/ivory-coast-raises-cocoa-farmgate-price-by-50/", "Presse (annonce officielle)", "B")
src("CI_CAC_2425P", "CCC (via Agence Ecofin)", "Côte d'Ivoire : 1 800 FCFA le kg de cacao pour la campagne principale 2024/2025", "https://www.agenceecofin.com/cacao/0110-122025-cote-d-ivoire-1800-fcfa-le-kg-de-cacao-pour-la-campagne-principale-2024/2025", "Presse (annonce officielle)", "B")
src("CI_CAC_2425I", "CCC (via allAfrica/Fraternité Matin)", "Le prix d'achat aux planteurs fixé à 2 200 FCFA, un nouveau record", "https://fr.allafrica.com/stories/202504030258.html", "Presse (annonce officielle)", "B")
src("CI_CAC_2526P", "Présidence / CCC (via AIP)", "Campagne 2025-2026 : prix bord champ du cacao 2 800 FCFA/kg et café 1 700 FCFA/kg", "https://www.aip.ci/257389/cote-divoire-aip-campagne-2025-2026-le-prix-bord-champ-du-cacao-fixe-a-2-800-fcfa-kg-et-celui-du-cafe-a-1-700-fcfa-kg-alassane-ouattara/", "Agence de presse publique", "B")
src("CI_CAC_2526I", "MINADERPV / CCC (via KOACI)", "Cacao : prix bord champ fixé à 1 200 FCFA/kg pour la campagne intermédiaire 2025-2026", "https://www.koaci.com/article/2026/03/04/cote-divoire/societe/cote-divoire-cacao-le-prix-bord-champ-fixe-a-1-200-fcfakg-pour-la-campagne-intermediaire-2025-2026_194830.html", "Presse (annonce officielle)", "B")
src("CI_CAC_2627P", "Gouvernement de Côte d'Ivoire (portail officiel)", "Campagne principale 2026-2027 : cacao 1 200 FCFA/kg, café 1 300 FCFA/kg", "https://gouv.ci/actualite/campagne-principale-2026-2027-le-prix-bord-champ-du-cacao-est-fixe-a-1200-fcfa-le-kg-le-prix-du-cafe-setablit-a-1300-fcfa-le-kg-8771", "Officielle primaire", "A")
src("CI_CAC_VENTES", "Reuters (via CNBC Africa) ; Agence Ecofin", "Prix 2026/27 fondé sur >1,1 Mt de ventes anticipées mars-juin 2026 ; règle ≥60 % CAF (≥50 % en baisse)", "https://www.cnbcafrica.com/2026/ivory-coast-sets-cocoa-farmgate-price-at-1200-cfa-francs-per-kg-for-2026-27-main-crop-official-says", "Presse", "B")
src("CI_CAC_STOCKS", "7info / allAfrica", "123 000 t invendues (janv. 2026), ~200 000 t fin février 2026 ; dispositif d'achat public", "https://www.7info.ci/123-000-tonnes-invendues-etat-ivoirien-dispositif-achat-cacao/", "Presse", "B")
src("BM_CACAO_2019", "Banque mondiale", "Situation économique en Côte d'Ivoire : au pays du cacao (2019) – part producteur ≥60 % CAF, prélèvements ≈22 % CAF", "https://documents1.worldbank.org/curated/en/277191561741906355/pdf/Cote-dIvoire-Economic-Update.pdf", "Institution internationale", "A")
src("OMC_TPR_2017", "OMC", "Examen des politiques commerciales UEMOA – Annexe Côte d'Ivoire (WT/TPR/S/362) : DUS 14,6 % CAF ; prélèvements totaux 23,2 % (2016/17)", "https://www.wto.org/french/tratop_f/tpr_f/s362-03_f.pdf", "Institution internationale", "A")
# Cacao Ghana
src("GH_CAC_1620", "COCOBOD (via The Cocoa Post)", "Producer price of cocoa up 8.42% (GH¢475 → GH¢515/bag ; 7 600 → 8 240 GH¢/t)", "https://thecocoapost.com/producer-price-of-cocoa-up-8-42/", "Presse (annonce officielle)", "B")
src("GH_CAC_2021", "COCOBOD", "Cocoa producer price goes up 28% from GH¢515 to GH¢660 per bag (10 560 GH¢/t)", "https://cocobod.gh/news/cocoa-producer-price-goes-up-28-from-gh515-to-gh660-per-bag", "Officielle primaire", "A")
src("GH_CAC_2122", "Gouvernement du Ghana (via B&FT)", "Gov't maintains cocoa price at GH¢660 per bag (87,15 % du FOB)", "https://thebftonline.com/?p=97805", "Presse (annonce officielle)", "B")
src("GH_CAC_2223", "COCOBOD", "Press release – opening of 2022/23 main crop season (GH¢800/bag ; 12 800 GH¢/t)", "https://cocobod.gh/news/press-release-opening-of-202223-main-crop-season", "Officielle primaire", "A")
src("GH_CAC_2324P", "Gouvernement du Ghana (via Graphic Online)", "Cocoa price up: bag from GH¢800 to GH¢1 308 (20 928 GH¢/t)", "https://www.graphic.com.gh/news/general-news/govt-increases-cocoa-price-bag-up-from-gh-800-to-gh-1-308-tome-now-gh-20-943-from-gh-12-800.html", "Presse (annonce officielle)", "B")
src("GH_CAC_2324I", "COCOBOD (compte officiel X)", "Producer price increased by 58.26% from GH¢20 928 to GH¢33 120 per tonne from 5 April 2024", "https://x.com/ghcocobod/status/1776312981111873684", "Officielle primaire", "A")
src("GH_CAC_2425P", "COCOBOD", "Review of the producer price of cocoa for the 2024/2025 season (48 000 GH¢/t, 11 sept. 2024)", "https://cocobod.gh/news/review-of-the-producer-price-of-cocoa-for-the-20242025-cocoa-season-wednesday-11th-september-2024", "Officielle primaire", "A")
src("GH_CAC_2425I", "Gouvernement du Ghana (via Graphic Online)", "Cocoa price shoots to GH¢49 600 a tonne", "https://www.graphic.com.gh/news/general-news/ghana-news-cocoa-price-shoots-to-ghc49-600-a-tonne-its-3rd-price-adjustment-in-9-months.html", "Presse (annonce officielle)", "B")
src("GH_CAC_2526", "COCOBOD / Citi Newsroom", "51 660 GH¢/t (70 % FOB 7 200 USD à 10,25) → 58 000 GH¢/t (11,5 GH¢/USD) → 41 392 GH¢/t au 12/02/2026 (90 % FOB 4 200 USD)", "https://citinewsroom.com/2026/02/cocoa-producer-price-cut-to-gh%C2%A241392-per-tonne-from-gh%C2%A251660/", "Presse (annonce officielle)", "B")
src("GH_CAC_REFORM", "COCOBOD", "Press release on cocoa sector reforms for financial viability and long-term sustainability", "https://cocobod.gh/news/press-release-on-cocoa-sector-reforms-for-financial-viability-and-long-term-sustainability", "Officielle primaire", "A")
src("GH_CAC_2627", "COCOBOD (via MyJoyOnline)", "Producer price GH¢42 400/t for 2026/27 (71,18 % du FOB brut réalisé ; Act 1182 : minimum 70 %)", "https://www.myjoyonline.com/cocobod-increases-cocoa-producer-price-to-gh%C2%A242400-for-2026-27-season/", "Presse (annonce officielle)", "B")
src("ECOFIN_GAP", "Agence Ecofin", "Ghana-Côte d'Ivoire cocoa price gap widens sharply for 2026/27 (3,65 vs 2,07 USD/kg)", "https://www.ecofinagency.com/news-agriculture/2809-59281-ghana-cote-d-ivoire-cocoa-price-gap-widens-sharply-for-2026/27-season", "Presse", "B")
# Cacao autres
src("CM_CAC_0426", "ONCC-SIF (via Invest-Time)", "Cacao au Cameroun : 1 200-1 450 FCFA/kg dans les bassins (mars-avril 2026)", "https://invest-time.com/2026/05/07/cacao-cameroun-prix-campagne/", "Presse (données ONCC)", "B")
src("CM_CAC_0526", "ONCC-SIF (via Investir au Cameroun)", "Le prix du kilogramme repasse au-dessus de 1 500 FCFA (1 550-1 650)", "https://www.investiraucameroun.com/agriculture/0705-23372-cacao-le-prix-du-kilogramme-repasse-au-dessus-de-1-500-fcfa-a-deux-mois-de-la-fin-de-campagne", "Presse (données ONCC)", "B")
src("CM_CAC_0626", "ONCC-SIF (via Investir au Cameroun)", "Le prix aux producteurs atteint 2 250 FCFA (2 100-2 250 au 30/06/2026)", "https://www.investiraucameroun.com/agriculture/3006-23552-cacao-le-prix-aux-producteurs-atteint-2250-fcfa-son-plus-haut-niveau-depuis-le-debut-de-la-campagne-2025-2026", "Presse (données ONCC)", "B")
src("NG_CAC_0926", "Mansa Markets", "Nigeria farmgate 5 728,5 NGN/kg (≈4 311 USD/t), 25/09/2026", "https://www.mansamarkets.com/blog/cocoa-farmgate-price-vs-world-price", "Secondaire", "C")
src("EC_CAC_0126", "El Universo", "Les producteurs reçoivent 180-190 USD/quintal (janv. 2026)", "https://www.eluniverso.com/noticias/economia/precio-cacao-ecuador-exportador-productor-nota/", "Presse", "B")
src("EC_CAC_0226", "Al Día (Équateur)", "Le cacao revient à 100 USD le quintal (80-85 USD dans les petits cantons), fév. 2026", "https://www.aldia.com.ec/el-cacao-regresa-a-niveles-de-2023-100-el-quintal-y-en-cantones-pequenos-llega-a-80/", "Presse", "B")
# Cours internationaux
src("BM_PINK", "Banque mondiale", "Commodity Price Data (Pink Sheet), CMO-Historical-Data-Monthly.xlsx, mise à jour 3 février 2026", "https://www.worldbank.org/en/research/commodity-markets", "Institution internationale", "A")
src("FMI_PCPS", "FMI", "Primary Commodity Prices (via FRED : PCOCOUSDM, PCOFFROBUSDM)", "https://fred.stlouisfed.org/series/PCOCOUSDM", "Institution internationale", "A")
src("OIC_CMR", "Organisation internationale du café", "Coffee Market Report (février et août 2026)", "https://www.ico.org/documents/cy2025-26/cmr-0826-e.pdf", "Institution internationale", "A")
src("SGX_0326", "SGX", "SICOM Rubber Monthly Report – mars 2026", "https://api2.sgx.com/sites/default/files/2026-04/SICOM%20SGX%20March%202026%20.pdf", "Bourse", "A")
src("BCE_FX", "Banque centrale européenne", "Taux de référence quotidiens (eurofxref-hist), parité fixe 655,957 FCFA/EUR", "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html", "Banque centrale", "A")
src("BRI_FX", "Banque des règlements internationaux", "US dollar exchange rates (WS_XRU), moyennes mensuelles", "https://data.bis.org/topics/XRU", "Institution internationale", "A")
src("BOG_FX", "Banque du Ghana", "Taux interbancaires moyens mensuels 2026", "https://www.bog.gov.gh/economic-data/exchange-rate/", "Banque centrale", "A")
# Café
src("CI_CAF_1718", "CCC (via Connectionivoirienne)", "Le prix du kg de café reste inchangé à 750 FCFA pour la campagne 2017-2018", "https://connectionivoirienne.net/2017/12/21/cote-divoire-le-prix-du-kg-de-cafe-reste-inchange-a-750-fcfa-pour-la-campagne-2017-2018/", "Presse (annonce officielle)", "B")
src("CI_CAF_1819", "CCC (via Abidjan.net)", "Prix du café 2018-2019 : 700 FCFA/kg (baisse de 50 FCFA)", "https://news.abidjan.net/h/649843.html", "Presse (annonce officielle)", "B")
src("CI_CAF_1920", "CCC (via Connectionivoirienne)", "Café 2019-2020 fixé à 700 FCFA ; maintien permis par une subvention de 32 Mds FCFA (prix de marché : 473 FCFA)", "https://connectionivoirienne.net/2019/12/26/le-prix-du-kg-de-cafe-fixe-a-700-fcfa-pour-la-campagne-2019-2020-en-cote-divoire/", "Presse (annonce officielle)", "B")
src("CI_CAF_2021", "CCC (via KOACI)", "Café : prix bord champ fixé à 550 FCFA/kg (campagne 2020-2021, 28/12/2020)", "https://www.koaci.com/article/2020/12/23/cote-divoire/economie/cote-divoire-cafe-debut-de-la-campagne-commerciale-le-28-decembre-le-prix-bord-champ-du-kilo-fixe-a-550-fcfa-soit-une-baisse-de-155-fcfa_147642.html", "Presse (annonce officielle)", "B")
src("CI_CAF_2223", "CCC (via Abidjan.net)", "Campagne 2022-2023 : cacao 900 FCFA, café 750 FCFA", "https://news.abidjan.net/articles/712879/campagne-2022-2023-le-prix-bord-champ-du-kilogramme-de-cacao-fixe-a-900-fcfa-et-celui-du-cafe-a-750-fcfa", "Presse (annonce officielle)", "B")
src("CI_CAF_2324", "CCC (via Abidjan.net)", "Campagne 2023-2024 : cacao 1 000 FCFA, café 900 FCFA", "https://news.abidjan.net/articles/724364/campagne-principale-de-commercialisation-2023-2024-cafe-cacao-le-prix-du-kg-de-cacao-fixe-a-1000-fcfa-et-celui-du-cafe-a-900-fcfa", "Presse (annonce officielle)", "B")
src("CI_CAF_2425", "CCC (via Agence Ecofin)", "Hausse de plus de 66 % du prix bord champ du café en 2024/2025 (1 500 FCFA)", "https://www.agenceecofin.com/breves-agro/0110-122027-cote-d-ivoire-hausse-de-plus-de-66-du-prix-bord-champ-du-cafe-en-2024/2025", "Presse (annonce officielle)", "B")
src("UG_CAF_0726", "Uganda Coffee Development Authority (UCDA)", "Monthly report July 2026 : prix bord champ Robusta FAQ moyen 11 500 UGX/kg", "https://ugandacoffee.go.ug/sites/default/files/2026-09/10%20July%202026%20Report%20draft(2)(1)(1).pdf", "Officielle primaire", "A")
src("VN_CAF_0926", "Vietnam.vn (prix Dak Lak)", "Prix intérieur du café robusta, Dak Lak : 93 600 VND/kg (28/09/2026)", "https://www.vietnam.vn/en/gia-nong-san-hom-nay-28-9-2026-gia-ca-phe-trong-nuoc-di-nguoc-the-gioi-hang-vu-moi-sap-bat-dau-my-trung-giam-thue-doi-voi-60-ty-usd-hang-hoa", "Presse", "B")
# Anacarde
src("CI_ANA_2016", "Gouvernement (via Abidjan.net)", "Anacarde : le prix du kilogramme fixé à 350 FCFA (2016)", "https://news.abidjan.net/articles/582020/anacarde-le-prix-du-kilogramme-fixe-a-350-fcfa-par-le-gouvernement-ivoirien", "Presse (annonce officielle)", "B")
src("CI_ANA_2017", "CCA (via allAfrica)", "Campagne cajou 2017 : mesures arrêtées par le Conseil du coton et de l'anacarde (440 FCFA)", "https://fr.allafrica.com/stories/201702210313.html", "Presse (annonce officielle)", "B")
src("CI_ANA_2018", "CCA (via Financial Afrik)", "La campagne de commercialisation des noix de cajou s'annonce sous de bons auspices en 2018 (500 FCFA)", "https://www.financialafrik.com/2018/02/17/cote-divoire-la-campagne-de-commercialisation-des-noix-de-cajou-sannonce-sous-de-bons-auspices-en-2018", "Presse (annonce officielle)", "B")
src("CI_ANA_2019", "Gouvernement (via Fraternité Matin)", "Noix de cajou : le prix fixé à 375 FCFA/kg pour la campagne 2019", "https://www.fratmat.info/article/87617/62/noix-de-cajou-le-prix-fixe-a-375-f-cfa-kg-pour-la-campagne-2019", "Presse (annonce officielle)", "B")
src("CI_ANA_2020", "Gouvernement (via Fraternité Matin)", "Anacarde : le prix bord champ fixé à 400 FCFA le kg (2020)", "https://www.fratmat.info/article/201657/economie/anacarde-le-prix-bord-champ-fixe-a-400-fcfa-le-kg", "Presse (annonce officielle)", "B")
src("CI_ANA_2122", "CCA (via Abidjan.net)", "Démarrage de la campagne 2022 de commercialisation de la noix de cajou (prix plancher 305 FCFA, inchangé depuis 2021)", "https://news.abidjan.net/articles/703951/demarrage-ce-vendredi-de-la-campagne-2022-de-la-commercialisation-de-la-noix-de-cajou-communique", "Presse (annonce officielle)", "B")
src("CI_ANA_2023", "Gouvernement (via Abidjan.net)", "Le prix de la noix de cajou fixé à 315 FCFA/kg (2023)", "https://news.abidjan.net/articles/717534/cote-divoire-le-prix-de-la-noix-de-cajou-fixe-a-315-f-cfa-kg-officiel", "Presse (annonce officielle)", "B")
src("CI_ANA_2024", "MINADERPV (via AIP)", "Le prix bord champ du kg de l'anacarde fixé à 275 FCFA (campagne 2024)", "https://www.aip.ci/33996/cote-divoire-aip-le-prix-bord-champ-du-kg-de-lanacarde-fixe-a-275-fcfa-pour-la-campagne-2023-2024/", "Agence de presse publique", "B")
src("CI_ANA_2025", "MINADERPV (via KOACI)", "Anacarde : prix bord-champ fixé à 425 FCFA (+54 %), campagne 2025", "https://www.koaci.com/article/2025/01/17/cote-divoire/societe/cote-divoire-anacarde-le-prix-bord-champ-du-kg-fixe-a-425-fcfa-soit-une-hausse-de-54-par-rapport-a-la-campagne-precedente_183836.html", "Presse (annonce officielle)", "B")
src("CI_ANA_2026", "MINADERPV (via Agence Ecofin)", "Baisse de 6 % du prix minimum bord champ de la noix de cajou en 2026 (400 FCFA)", "https://www.agenceecofin.com/actualites-agro/0902-135589-cote-d-ivoire-baisse-de-6-du-prix-minimum-bord-champ-de-la-noix-de-cajou-en-2026", "Presse (annonce officielle)", "B")
src("CI_ANA_BAREME", "Gouvernement / CCAK (via Abidjan.net)", "Prix planchers 2026 : bord champ 400, magasin intérieur 425, magasin usine 454, magasin portuaire 484 FCFA/kg", "https://news.abidjan.net/articles/747086/commercialisation-de-lanacarde-le-gouvernement-fixe-les-prix-planchers-pour-la-campagne-2026", "Presse (annonce officielle)", "B")
src("CI_ANA_REAL", "AIP", "Campagne anacarde 2026 : près de 15 Mds FCFA de revenus à Niakara (prix moyen 416 FCFA/kg)", "https://www.aip.ci/cote-divoire-aip-campagne-anacarde-2026-pres-de-15-milliards-fcfa-de-revenus-engranges-par-les-producteurs-du-departement-de-niakara/", "Agence de presse publique", "B")
src("CI_ANA_DUS", "AIP", "Le droit unique de sortie de la noix de cajou brute désormais fixé à 5 % (20/11/2024)", "https://www.aip.ci/127213/cote-divoire-aip-le-droit-unique-de-sortie-de-la-noix-de-cajou-brute-desormais-fixe-a-5/", "Agence de presse publique", "B")
src("CI_ANA_PROD", "MINADERPV (via AIP)", "Production historique de 1 549 221 t de noix de cajou en 2025", "https://www.aip.ci/316955/aip-la-cote-divoire-atteint-une-production-historique-de-1-549-221-tonnes-de-noix-de-cajou-au-titre-de-la-campagne-2025/", "Agence de presse publique", "B")
src("BF_ANA_2026", "Gouvernement du Burkina Faso (via Sika Finance)", "Prix bord champ de la noix de cajou maintenu à 385 FCFA/kg (2026)", "https://www.sikafinance.com/marches/burkina-le-prix-bord-champ-de-la-noix-de-cajou-maintenu-a-385-fcfakg-pour-soutenir-la-transformation-locale_60008", "Presse (annonce officielle)", "B")
src("GW_ANA_2026", "Gouvernement de transition de Guinée-Bissau (via Xinhua)", "Campagne 2026 : 410 FCFA/kg au producteur, 478 FCFA/kg à Bissau", "https://english.news.cn/20260311/508ae13acd8c44109ea651276bd01b86/c.html", "Presse (annonce officielle)", "B")
src("ML_ANA_2025", "Gouvernement du Mali (via Agence Ecofin)", "Mali : la filière anacarde face au défi du respect du prix plancher (390 FCFA ; achats à 350-375)", "https://www.agenceecofin.com/actualites/0104-127164-mali-la-filiere-anacarde-face-au-defi-du-respect-du-prix-plancher", "Presse (annonce officielle)", "B")
src("GH_ANA_2026", "Tree Crops Development Authority (TCDA, Ghana)", "Government sets GHS 12.00/kg as minimum producer price for RCN (2025/2026) – benchmark FOB 1 400 USD/t, 11,0241 GH¢/USD", "https://tcda.gov.gh/government-sets-ghs-12-00-per-kilogram-as-minimum-producer-price-for-raw-cashew-nuts-2025-2026-season/", "Officielle primaire", "A")
src("TZ_ANA_2526", "The Citizen (données TMX/CBT)", "Cashew farmers earn Sh1.3tr : 430 961 t vendues pour 1 279 Mds TZS (2025/26)", "https://www.thecitizen.co.tz/tanzania/business/cashew-farmers-earn-sh1-3tr-as-production-heads-toward-record-5311708", "Presse (données officielles d'enchères)", "B")
src("INT_ANA_CI", "Cardassilaris (négociant)", "Cashew market report May 2026 : RCN Côte d'Ivoire 1 560 USD/t (avr.-mai 2026)", "https://www.cardassilaris.com/news/cashew-market-report-may-2026-rcn-quality-vietnam", "Secondaire (commerce)", "C")
src("INT_ANA_VN", "Douanes vietnamiennes (via Viet Nam News)", "Raw cashew nut imports Jan-Apr 2026 : ~1,3 Mt pour ~2,2 Mds USD (≈1 704 USD/t)", "https://vietnamnews.vn/economy/945883/raw-cashew-nut-imports-rocket-in-first-four-months.html", "Presse (données douanières)", "B")
# Coton
src("CI_COT_1718", "Gouvernement (via KOACI)", "Coton graine : 300 FCFA/kg (+35 FCFA par rapport à 265 FCFA en 2017-2018)", "https://www.koaci.com/index.php/article/2019/05/22/cote-divoire/economie/cote-divoire-le-prix-du-kilogramme-de-coton-graine-pour-la-campagne-2018-2019-fixe-a-300-fcfa-soit-une-hausse-de-35-fcfa_131167.html", "Presse (annonce officielle)", "B")
src("CI_COT_1819", "Gouvernement (via Abidjan.net)", "Le prix du coton graine de premier choix maintenu à 265 FCFA/kg (2018-2019)", "https://news.abidjan.net/h/638493.html", "Presse (annonce officielle)", "B")
src("CI_COT_1920", "Gouvernement (via KOACI)", "Le prix du coton graine reste inchangé pour la campagne 2019-2020 : 300 FCFA/kg", "https://www.koaci.com/article/2019/10/29/cote-divoire/economie/cote-divoire-le-prix-du-coton-de-graine-reste-inchange-pour-la-campagne-2019-2020-300-fcfakg_136257.html", "Presse (annonce officielle)", "B")
src("CI_COT_2122", "Gouvernement (via allAfrica)", "Campagne 2021-2022 du coton : le prix du kilo demeure à 300 F (inchangé depuis 2020-2021)", "https://fr.allafrica.com/stories/202110080394.html", "Presse (annonce officielle)", "B")
src("CI_COT_2223", "Gouvernement (via Connectionivoirienne)", "Coton campagne 2022/2023 : le prix du kilogramme fixé à 310 FCFA", "https://connectionivoirienne.net/2022/07/14/coton-camapagne-2022-2023-le-prix-du-kilogramme-fixe-a-310-fcfa/", "Presse (annonce officielle)", "B")
src("CI_COT_2324", "Gouvernement (via Abidjan.net)", "Coton graine 1er choix 310 FCFA, 2e choix 285 FCFA (2023-2024)", "https://news.abidjan.net/articles/720825/cote-divoire-le-prix-du-coton-graines-1er-choix-fixe-a-310-fcfa-et-a-285-f-cfa-le-kilo-du-2e-choix", "Presse (annonce officielle)", "B")
src("CI_COT_2526", "MINADERPV (via KOACI)", "Campagne 2025-2026 : coton 1er choix 310 FCFA/kg, 2e choix 285 FCFA/kg (31/07/2025)", "https://www.koaci.com/article/2025/07/31/cote-divoire/societe/cote-divoire-campagne-2025-2026-le-prix-du-coton-de-1er-choix-est-fixe-a-310-fcfakg-et-celui-de-2e-choix-a-285-fcfakg_189056.html", "Presse (annonce officielle)", "B")
src("CI_COT_SUB", "Agence Ecofin", "La subvention à la filière coton a plus que doublé en 2025/2026 (25,3 Mds FCFA contre 11,9 Mds)", "https://www.agenceecofin.com/actualites-agro/0108-130586-cote-d-ivoire-la-subvention-a-la-filiere-coton-a-plus-que-double-en-2025/2026", "Presse", "B")
src("CI_COT_PROD", "Agence Ecofin", "Croissance modeste de la production cotonnière 2024/2025 : 351 764 t, 984 kg/ha, 357 267 ha", "https://www.agenceecofin.com/actualites-agro/1501-124919-cote-d-ivoire-croissance-modeste-de-la-production-cotonniere-en-2024/2025", "Presse (données officielles)", "B")
src("USDA_COT", "USDA FAS", "Côte d'Ivoire Cotton and Products Annual 2026 : fibre MY2024/25 730 000 balles (480 lb)", "https://www.fas.usda.gov/data/cote-divoire-cotton-and-products-annual-5", "Institution publique étrangère", "A")
src("BF_COT_2526", "SOFITEX (Burkina Faso)", "Campagne 2025-2026 : engrais 17 500 FCFA, kg de coton 325 FCFA", "https://www.sofitex.bf/2025/04/10/campagne-cotonniere-2025-2026-les-engrais-a-17-500-f-cfa-les-insecticides-a-5-200-f-cfa-et-le-kg-de-coton-a-325-f-cfa/", "Officielle (société cotonnière)", "A")
src("BF_COT_PROD", "Agence Ecofin", "Burkina Faso : production 2024/2025 (300 000 t ; 865 kg/ha)", "https://www.agenceecofin.com/actualites-agro/2002-126013-au-burkina-faso-la-production-cotonniere-2024/2025-s-annonce-plus-faible-que-prevu", "Presse", "B")
src("ML_COT_2526", "Gouvernement du Mali (via Mali 24)", "Prix du kilo du coton graine maintenu à 300 FCFA", "https://mali24.info/mali-433-700-tonnes-de-coton-produites-le-prix-du-kilo-du-coton-graine-maintenu-a-300-f-cfa/", "Presse (annonce officielle)", "B")
src("BJ_COT_2526", "Gouvernement du Bénin (via La Nation)", "Campagne cotonnière 2025-2026 : prix des insecticides et du coton graine homologués (300 FCFA)", "https://lanation.bj/actualites/campagne-cotonniere-2025-2026-les-prix-des-insecticides-et-du-coton-graine-homologues", "Presse publique (annonce officielle)", "B")
src("BJ_COT_2627", "Gouvernement du Bénin (via Le Matinal)", "Campagne 2026-2027 : coton conventionnel 300 FCFA (1er choix), biologique 360 FCFA (CM du 13/05/2026)", "https://lematinal.bj/campagne-cotonniere-2026-2027-le-prix-de-cession-des-intrants-et-dachat-de-coton-graine-homologue/", "Presse (annonce officielle)", "B")
src("REG_COT_2526", "Africa Radio", "Coton africain : ~300 FCFA au Bénin et au Mali, 310 en Côte d'Ivoire, 325 au Burkina, jusqu'à 350 au Sénégal", "https://www.africaradio.com/actualite-115836-coton-africain-pourquoi-les-producteurs-ouest-africains-perdent-ils-du-terrain", "Presse", "C")
src("REG_COT_RDT", "La Marina (Bénin)", "Campagne 2024-2025 : rendements Bénin 1 248 kg/ha, Mali 914 kg/ha", "https://lamarinabj.com/index.php/2025/02/05/campagne-cotonniere-2024-2025-en-afrique-le-benin-peut-il-reprendre-sa-place-de-leader/", "Presse", "C")
# Caoutchouc
src("CI_CAO_MECA", "Agence Ecofin", "Ce qui change pour les producteurs de caoutchouc naturel en 2026 : 66 % du prix de référence (63 % auparavant)", "https://www.agenceecofin.com/actualites-agro/2606-139636-cote-d-ivoire-ce-qui-change-pour-les-producteurs-de-caoutchouc-naturel-en-2026", "Presse", "B")
src("CI_CAO_DRC", "Business & Actuality", "Le prix du caoutchouc : bras de fer planteurs-usiniers ; DRC officiel 60 % contre 65-68 % mesuré", "https://businessactuality.com/le-prix-du-caoutchouc-en-cote-divoire-un-bras-de-fer-entre-planteurs-usiniers-et-regulateurs/", "Presse", "C")
src("CI_CAO_0125", "APROMAC (via Yessouan)", "Prix caoutchouc Côte d'Ivoire : 442 FCFA/kg en janvier 2025", "https://www.yessouan.ci/Prix-caoutchouc-Cote-d-Ivoire-442-FCFA-kg-en-janvier-2025_a1537.html", "Presse (prix officiel)", "B")
src("CI_CAO_0425", "APROMAC (via 7info)", "Caoutchouc naturel : prix du kg pour le mois d'avril (438 FCFA)", "https://www.7info.ci/caoutchouc-naturel-voici-le-prix-du-kg-pour-le-mois-davril/", "Presse (prix officiel)", "B")
src("CI_CAO_2026", "APROMAC (via 7info)", "Caoutchouc : nouveaux prix du kg (janv. 352, fév. 368, avr. 401, mai 439, juil. 493 FCFA)", "https://www.7info.ci/caoutchouc-voici-le-nouveau-prix-du-kg/", "Presse (prix officiel)", "B")
src("CI_CAO_0926", "APROMAC (via Business & Actuality)", "Prix du caoutchouc : 484 FCFA/kg en septembre 2026", "https://businessactuality.com/cote-divoire-prix-du-caoutchouc-484-fcfa-kg-en-septembre-2026/", "Presse (prix officiel)", "B")
src("TH_CAO", "Thai Rubber Association", "Prix intérieurs (cup lump 100 %) : 58 THB/kg (2 mai 2025)", "https://www.thainr.com/en/?detail=pr-local", "Association professionnelle", "B")
src("ID_CAO", "Disperindag/Gapkindo Sumatra-Sud (via IDN Times)", "Prix de référence KKK 100 % : 38 835 à 42 238 Rp/kg (août 2026)", "https://sumsel.idntimes.com/news/sumatra-selatan/harga-karet-sumsel-kembali-menguat-akhir-agustus-tembus-rp41-ribu-00-pbgds-3n14cx", "Presse (prix officiel provincial)", "B")
src("CI_CAO_PROD", "Financial Afrik", "Numéro trois mondial du caoutchouc (≈1,6 Mt en 2023)", "https://www.financialafrik.com/2026/01/15/numero-trois-mondial-du-caoutchouc-la-cote-divoire-veut-capter-davantage-de-valeur/", "Presse", "C")
# Palmier
src("CI_PAL_Q424", "CHP-HC (via Abidjan Économie)", "Huile de palme brute 600 000 FCFA/t ; régimes bord champ 75 000 FCFA/t (oct.-déc. 2024)", "https://www.abidjaneconomie.net/2024/10/19/cote-divoire-nouvelles-tarifications-pour-lhuile-de-palme-brut-et-regimes-de-palme-pour-octobre-a-decembre-2024/", "Presse (prix officiel)", "B")
src("CI_PAL_0126", "Conseil Hévéa-Palmier à huile-Coco (via Afrik Soir)", "Prix de janvier 2026 : huile de palme brute 620 000 FCFA/t ; régimes bord champ 80 000 FCFA/t", "https://afriksoir.net/cote-divoire-le-conseil-hevea-palmier-a-huile-coco-fixe-les-prix-du-palmier-a-huile-pour-janvier-2026/", "Presse (prix officiel)", "B")
src("ID_PAL_0126", "Disbun Riau (via HaiSawit / Media Center Riau)", "Prix TBS (régimes) Riau, palmiers 10-20 ans : 3 496,91 / 3 430,63 / 3 449,84 Rp/kg (janv. 2026)", "https://haisawit.co.id/news/detail/resmi-naik-cek-daftar-harga-sawit-riau-periode-1420-januari-2026", "Officielle provinciale (via presse)", "B")
src("MY_PAL_2025", "Malaysian Palm Oil Board (MPOB)", "Overview of the Malaysian Oil Palm Industry 2025 : prix des régimes à 1 % OER 47,39 RM ; OER 19,74 %", "https://bepi.mpob.gov.my/images/overview/Overview2025.pdf", "Officielle primaire", "A")
src("USDA_PAL", "USDA FAS", "Côte d'Ivoire Oilseeds and Products Annual 2025 (huile de palme 575 000 t MY2024/25)", "https://www.fas.usda.gov/data/gain/2026/01/cote-divoire-oilseeds-and-products-report-annual-2025", "Institution publique étrangère", "A")
# Riz
src("USDA_RIZ_CI", "USDA FAS", "Côte d'Ivoire Grain and Feed Annual 2026 : paddy bord champ 233 FCFA/kg en moyenne 2025 (+8,5 %)", "https://apps.fas.usda.gov/newgainapi/api/Report/DownloadReportByFileName?fileName=Grain+and+Feed+Annual_Accra_Cote+d%27Ivoire_IV2026-0003", "Institution publique étrangère", "A")
src("USDA_RIZ_SN", "USDA FAS", "Senegal Grain and Feed Annual 2025 : paddy 130 FCFA/kg + subvention 30 FCFA (prix usinier 160)", "https://apps.fas.usda.gov/newgainapi/api/Report/DownloadReportByFileName?fileName=Grain+and+Feed+Annual_Dakar_Senegal_SG2025-0008.pdf", "Institution publique étrangère", "A")
src("VN_RIZ", "SGGP News", "Paddy frais du delta du Mékong : IR 50404 5 400-5 500 ; OM 5451 5 600-5 700 VND/kg (2025)", "https://en.sggp.org.vn/rice-farmers-in-mekong-delta-struggle-as-prices-plunge-yields-decline-post120063.html", "Presse", "B")
# Fruits
src("EC_BAN_2026", "MAGP Équateur, Acuerdo Ministerial 107 (via Agraria.pe)", "Prix minimum de soutien 2026 : 7,50 USD la caisse 22XU de 43 lb", "https://agraria.pe/noticias/ecuador-fija-en-us-7-50-el-precio-minimo-de-la-caja-de-banan-40795", "Presse (acte officiel)", "B")
src("CI_BAN_EXP", "Agence Ecofin", "Exportations ivoiriennes de bananes : 271 000 t en 2025 (+7 %)", "https://www.ecofinagency.com/news-agriculture/0402-52550-african-banana-exports-rise-5-as-ghana-takes-lead", "Presse", "B")
src("CI_MAN_2026", "Inter-Mangue (via AIP)", "Mangue 2026 : prix bord champ maintenu à 2 450 FCFA la caisse ; 220 FCFA/kg en station", "https://www.aip.ci/332817/cote-divoire-aip-filiere-mangue-le-prix-bord-champ-maintenu-a-2-450-fcfa-la-caisse-pour-la-campagne-2026/", "Agence de presse publique", "B")
src("BF_MAN_2026", "Gouvernement du Burkina Faso (via leFaso.net)", "Campagne fruitière 2026 : anacarde 385 FCFA, mangue 95 FCFA le kg", "https://lefaso.net/spip.php?article144610", "Presse (annonce officielle)", "B")
src("OCPV", "OCPV (Ministère du Commerce)", "Prix à la consommation des produits vivriers (bulletins hebdomadaires 2025-2026)", "https://www.ocpv-ci.com/", "Officielle primaire (prix consommateur)", "A")
src("CI_CAC_PROD", "CCC (via CNBC Africa/Reuters)", "La Côte d'Ivoire anticipe 2,0-2,1 Mt de cacao en 2025/26 (+10,5 %)", "https://www.cnbcafrica.com/2026/ivory-coast-expects-cocoa-output-to-rise-10-5-in-2025-26-season-regulator-says", "Presse", "B")
src("CI_CAF_PROD", "AIP", "Filière café-cacao : production de café 24 832 t d'octobre 2024 à juin 2025 (-69,7 %)", "https://www.aip.ci/257515/cote-divoire-aip-la-filiere-cafe-cacao-moteur-de-croissance-economique-face-aux-defis-sociaux-et-environnementaux-feature/", "Agence de presse publique", "B")
src("RDT_CACAO", "Wessel & Quist-Wessel (2015), NJAS – Cocoa production in West Africa, a review ; KIT (2018)", "Rendements moyens : Côte d'Ivoire ≈500-600 kg/ha ; Ghana ≈400 kg/ha", "https://www.sciencedirect.com/science/article/pii/S1573521415000160", "Littérature scientifique", "A")


src("GH_CAC_GAP", "CNBC Africa", "Will Ghana's domestic market plug COCOBOD's $1.4bn funding gap? (2026)", "https://www.cnbcafrica.com/media/7790596098459/will-ghanas-domestic-market-plug-cocobods-14bn-funding-gap", "Presse", "B")
src("USDA_RIZ_IMP", "USDA FAS", "Côte d'Ivoire Grain and Feed Annual 2026 : production 2026/27 1,75 Mt de riz blanchi ; importations ≈1,75 Mt", "https://www.fas.usda.gov/data/gain/2026/04/cote-divoire-grain-and-feed-annual", "Institution publique étrangère", "A")
src("CI_ANA_PROD26", "Cardassilaris (négociant)", "Récolte RCN Côte d'Ivoire 2026 ≈1,46 Mt", "https://www.cardassilaris.com/news/cashew-market-report-may-2026-rcn-quality-vietnam", "Secondaire (commerce)", "C")
src("CI_ANA_TRANSFO", "Agence Ecofin", "Côte d'Ivoire : achat de noix réservé aux transformateurs locaux du 9 février au 16 mars 2026 (Le Patriote)", "https://lepatriote.ci/filiere-anacarde-lachat-des-noix-de-cajou-exclusivement-reserve-aux-transformateurs-locaux-du-9-fevrier-au-16-mars-2026-au-titre-de-la-campagne-2026", "Presse", "B")
src("CI_ANA_EXP", "Fraternité Matin (via allAfrica)", "Filière cajou : >860 000 t de noix brutes exportées en 2025 ; exportations d'amandes ≈350 Mds FCFA", "https://fr.allafrica.com/stories/202601200594.html", "Presse", "B")
src("CI_ANN_EXP", "Xinhua", "Exportations d'ananas : 23 557 t en 2023 (-27 %)", "https://english.news.cn/africa/20240128/f58bff004ef74e1da7107042c6132b2c/c.html", "Presse", "B")

# ---------------------------------------------------------------------------
# 5. Observations
#    fx : code période "AAAA-MM:AAAA-MM" (moyenne mensuelle) ou valeur littérale (ex. "=11.5")
#    ref : ID de la référence internationale ; fob : ID d'une valeur FOB/CAF nationale
# ---------------------------------------------------------------------------
OBS = []
def obs(**kw):
    base = dict(equiv=1, equiv_label="", ref="", fob="", fx_note="", remarque="", qualite="", periode="")
    base.update(kw)
    OBS.append(base)

def half(camp, h):
    """Retourne (début, fin) des demi-campagnes cacao/café : P = oct.-mars, I = avr.-sept."""
    y1 = int(camp[:4])
    if h == "P":
        return f"{y1}-10", f"{y1+1}-03"
    return f"{y1+1}-04", f"{y1+1}-09"

CACAO_CI = [  # campagne, principale, intermédiaire, sourceP, sourceI
    ("2016/17", 1100, 700, "CI_CAC_1617P", "CI_CAC_1617I"),
    ("2017/18", 700, 700, "CI_CAC_1718", "CI_CAC_1718"),
    ("2018/19", 750, 750, "CI_CAC_1819P", "CI_CAC_1819I"),
    ("2019/20", 825, 825, "CI_CAC_1920P", "CI_CAC_1920I"),
    ("2020/21", 1000, 750, "CI_CAC_2021P", "CI_CAC_2021I"),
    ("2021/22", 825, 825, "CI_CAC_2122P", "CI_CAC_2122I"),
    ("2022/23", 900, 900, "CI_CAC_2223P", "CI_CAC_2223I"),
    ("2023/24", 1000, 1500, "CI_CAC_2324P", "CI_CAC_2324I"),
    ("2024/25", 1800, 2200, "CI_CAC_2425P", "CI_CAC_2425I"),
    ("2025/26", 2800, 1200, "CI_CAC_2526P", "CI_CAC_2526I"),
]
CACAO_GH = [  # campagne, principale (GH¢/t), intermédiaire (GH¢/t), sourceP, sourceI, remarque
    ("2016/17", 7600, 7600, "GH_CAC_1620", "GH_CAC_1620", "GH¢475/sac de 64 kg brut"),
    ("2017/18", 7600, 7600, "GH_CAC_1620", "GH_CAC_1620", "Prix inchangé"),
    ("2018/19", 7600, 7600, "GH_CAC_1620", "GH_CAC_1620", "Prix inchangé"),
    ("2019/20", 8240, 8240, "GH_CAC_1620", "GH_CAC_1620", "GH¢515/sac"),
    ("2020/21", 10560, 10560, "GH_CAC_2021", "GH_CAC_2021", "GH¢660/sac ; intègre le différentiel de revenu décent (LID, 400 USD/t)"),
    ("2021/22", 10560, 10560, "GH_CAC_2122", "GH_CAC_2122", "Prix maintenu ; 87,15 % du FOB selon le gouvernement"),
    ("2022/23", 12800, 12800, "GH_CAC_2223", "GH_CAC_2223", "GH¢800/sac"),
    ("2023/24", 20928, 33120, "GH_CAC_2324P", "GH_CAC_2324I", "1 308 GH¢/sac (Graphic : 20 943 GH¢/t) puis 33 120 GH¢/t à compter du 05/04/2024"),
    ("2024/25", 48000, 49600, "GH_CAC_2425P", "GH_CAC_2425I", "48 000 GH¢/t (11/09/2024), relevé à 49 600 GH¢/t en cours de campagne"),
    ("2025/26", 58000, 41392, "GH_CAC_2526", "GH_CAC_2526", "51 660 (août 2025) → 58 000 GH¢/t ; abaissé à 41 392 GH¢/t le 12/02/2026"),
]

for camp, p, i, sp, si in CACAO_CI:
    for h, val, s in (("P", p, sp), ("I", i, si)):
        d, f = half(camp, h)
        lib = "principale (oct.-mars)" if h == "P" else "intermédiaire (avr.-sept.)"
        obs(id=f"CAC-CI-{camp}-{h}", filiere="Cacao", produit="Fèves de cacao marchandes", pays="Côte d'Ivoire",
            campagne=camp, periode=f"Campagne {lib}", type_prix="Prix minimum garanti (administré)", stade="Bord champ",
            qualite="Bien fermenté, séché, trié (grade marchand)", prix=val, monnaie="XOF", unite="kg", kg=1,
            fx=f"{d}:{f}", ref=f"INT-CAC-{camp}-{h}", source=s,
            remarque="Prix administré par le CCC ; ventes anticipées ; règle ≥60 % du prix CAF de référence")
for camp, p, i, sp, si, rem in CACAO_GH:
    for h, val, s in (("P", p, sp), ("I", i, si)):
        d, f = half(camp, h)
        lib = "principale (oct.-mars)" if h == "P" else "intermédiaire (avr.-sept.)"
        obs(id=f"CAC-GH-{camp}-{h}", filiere="Cacao", produit="Fèves de cacao marchandes", pays="Ghana",
            campagne=camp, periode=f"Campagne {lib}", type_prix="Prix producteur fixé (COCOBOD)", stade="Bord champ (centres d'achat LBC)",
            qualite="Grade I/II (contrôle QCC)", prix=val, monnaie="GHS", unite="tonne", kg=1000,
            fx=f"{d}:{f}", ref=f"INT-CAC-{camp}-{h}", source=s, remarque=rem)
# Cacao 2026/27 (ouverture de campagne ; dernier cours disponible = août 2026)
obs(id="CAC-CI-2026/27-P", filiere="Cacao", produit="Fèves de cacao marchandes", pays="Côte d'Ivoire", campagne="2026/27",
    periode="Ouverture campagne principale (annonce 01/09/2026)", type_prix="Prix minimum garanti (administré)", stade="Bord champ",
    qualite="Bien fermenté, séché, trié", prix=1200, monnaie="XOF", unite="kg", kg=1, fx="2026-09:2026-09",
    ref="INT-CAC-2026-08", source="CI_CAC_2627P",
    remarque="Fondé sur >1,1 Mt de ventes anticipées conclues mars-juin 2026, au creux du marché")
obs(id="CAC-GH-2026/27-P", filiere="Cacao", produit="Fèves de cacao marchandes", pays="Ghana", campagne="2026/27",
    periode="Ouverture campagne (effet 25/09/2026)", type_prix="Prix producteur fixé (COCOBOD)", stade="Bord champ (centres d'achat LBC)",
    qualite="Grade I/II", prix=42400, monnaie="GHS", unite="tonne", kg=1000, fx="2026-09:2026-09",
    ref="INT-CAC-2026-08", fob="FOB-GH-CAC-2026/27", source="GH_CAC_2627",
    remarque="71,18 % du FOB brut réalisé (Act 1182 : minimum 70 %) ; GH¢2 650/sac de 64 kg")
obs(id="FOB-GH-CAC-2026/27", filiere="Cacao", produit="Fèves de cacao (valeur FOB brute réalisée)", pays="Ghana", campagne="2026/27",
    periode="Ventes de la campagne 2026/27", type_prix="Valeur FOB brute réalisée (dérivée)", stade="FOB Tema/Takoradi",
    qualite="Grade I/II", prix="=42400/0.7118", monnaie="GHS", unite="tonne", kg=1000, fx="2026-09:2026-09",
    source="GH_CAC_2627", remarque="Dérivé : prix producteur ÷ 71,18 % (part déclarée par le COCOBOD)")
# Cameroun (libéralisé) - points ONCC 2025/26 (petite traite)
for oid, per, lo, hi, fx, s in [
    ("CAC-CM-2026-04", "Mars-avril 2026", 1200, 1450, "2026-03:2026-04", "CM_CAC_0426"),
    ("CAC-CM-2026-05", "Début mai 2026", 1550, 1650, "2026-05:2026-05", "CM_CAC_0526"),
    ("CAC-CM-2026-06", "30 juin 2026", 2100, 2250, "2026-06:2026-06", "CM_CAC_0626"),
]:
    obs(id=oid, filiere="Cacao", produit="Fèves de cacao marchandes", pays="Cameroun", campagne="2025/26", periode=per,
        type_prix="Prix de marché (libéralisé, relevé ONCC-SIF)", stade="Bord champ (bassins de production)",
        qualite="Fèves marchandes (qualité variable)", prix=f"=({lo}+{hi})/2", monnaie="XAF", unite="kg", kg=1,
        fx=fx, ref=f"INT-CAC-{oid[-7:]}", source=s,
        remarque=f"Milieu de la fourchette {lo}-{hi} FCFA/kg ; XAF = XOF (même parité avec l'euro)")
obs(id="CAC-NG-2026-09", filiere="Cacao", produit="Fèves de cacao", pays="Nigeria", campagne="2026/27", periode="25/09/2026",
    type_prix="Prix de marché (libéralisé)", stade="Bord champ (indicatif)", qualite="Non précisée",
    prix=5728.5, monnaie="NGN", unite="kg", kg=1, fx="2026-09:2026-09", ref="INT-CAC-2026-08", source="NG_CAC_0926",
    remarque="Source secondaire ; taux de change implicite de la source ; à titre indicatif uniquement")
obs(id="CAC-EC-2026-01", filiere="Cacao", produit="Fèves de cacao sèches (CCN-51 / Nacional)", pays="Équateur", campagne="2025/26",
    periode="Janvier 2026", type_prix="Prix de marché (libéralisé)", stade="Bord champ",
    qualite="Après décotes usuelles (qualité variable)", prix="=(180+190)/2", monnaie="USD", unite="quintal (100 lb)", kg=45.3592,
    fx="2026-01:2026-01", ref="INT-CAC-2026-01", source="EC_CAC_0126", remarque="Milieu de fourchette 180-190 USD/qq")
obs(id="CAC-EC-2026-02", filiere="Cacao", produit="Fèves de cacao sèches", pays="Équateur", campagne="2025/26",
    periode="Février 2026", type_prix="Prix de marché (libéralisé)", stade="Centres de collecte principaux",
    qualite="Qualité variable", prix=100, monnaie="USD", unite="quintal (100 lb)", kg=45.3592,
    fx="2026-02:2026-02", ref="INT-CAC-2026-02", source="EC_CAC_0226", remarque="80-85 USD/qq dans les petits cantons")

# Café robusta
CAFE_CI = [("2016/17", 750, "CI_CAF_1718", "Prix 2016/17 déduit du maintien à 750 FCFA en 2017/18 (« inchangé »)"),
           ("2017/18", 750, "CI_CAF_1718", ""), ("2018/19", 700, "CI_CAF_1819", ""),
           ("2019/20", 700, "CI_CAF_1920", "Maintien financé par une subvention de 32 Mds FCFA (prix de marché estimé : 473 FCFA)"),
           ("2020/21", 550, "CI_CAF_2021", "Campagne ouverte le 28/12/2020"),
           ("2021/22", 700, "CI_CAC_2122P", ""), ("2022/23", 750, "CI_CAF_2223", ""), ("2023/24", 900, "CI_CAF_2324", ""),
           ("2024/25", 1500, "CI_CAF_2425", ""), ("2025/26", 1700, "CI_CAC_2526P", "")]
for camp, val, s, rem in CAFE_CI:
    y1 = int(camp[:4])
    obs(id=f"CAF-CI-{camp}", filiere="Café", produit="Café vert robusta (décortiqué)", pays="Côte d'Ivoire", campagne=camp,
        periode="Campagne (oct.-sept.)", type_prix="Prix minimum garanti (administré)", stade="Bord champ",
        qualite="Bien séché, décortiqué, trié", prix=val, monnaie="XOF", unite="kg", kg=1,
        fx=f"{y1}-10:{y1+1}-09", ref=f"INT-ROB-{camp}", source=s,
        remarque=(rem + " ; " if rem else "") + "Avant 2021/22 la campagne café s'ouvrait en décembre : moyenne oct.-sept. utilisée par homogénéité")
obs(id="CAF-CI-2026/27", filiere="Café", produit="Café vert robusta (décortiqué)", pays="Côte d'Ivoire", campagne="2026/27",
    periode="Ouverture (annonce 01/09/2026)", type_prix="Prix minimum garanti (administré)", stade="Bord champ",
    qualite="Bien séché, décortiqué, trié", prix=1300, monnaie="XOF", unite="kg", kg=1, fx="2026-09:2026-09",
    ref="INT-ROB-2026-08", source="CI_CAC_2627P")
obs(id="CAF-UG-2026-07", filiere="Café", produit="Café robusta FAQ (vert, non classé)", pays="Ouganda", campagne="2025/26",
    periode="Juillet 2026", type_prix="Prix de marché (libéralisé, relevé UCDA)", stade="Bord champ",
    qualite="FAQ (Fair Average Quality)", prix=11500, monnaie="UGX", unite="kg", kg=1, fx="2026-07:2026-07",
    ref="INT-ROB-2026-07", source="UG_CAF_0726", remarque="Moyenne UCDA (fourchette 11 000-12 000) ; taux de change de source secondaire (C)")
obs(id="CAF-VN-2026-09", filiere="Café", produit="Café vert robusta (nhân xô)", pays="Vietnam", campagne="2025/26",
    periode="28/09/2026", type_prix="Prix de marché intérieur", stade="Départ exploitation / collecteur (Dak Lak)",
    qualite="Robusta courant (FAQ)", prix=93600, monnaie="VND", unite="kg", kg=1, fx="2026-09:2026-09",
    ref="INT-ROB-2026-08", source="VN_CAF_0926", remarque="Prix Dak Lak ; marché très concurrentiel, rendements très élevés")

# Anacarde
ANA_CI = [(2016, 350, "CI_ANA_2016"), (2017, 440, "CI_ANA_2017"), (2018, 500, "CI_ANA_2018"), (2019, 375, "CI_ANA_2019"),
          (2020, 400, "CI_ANA_2020"), (2021, 305, "CI_ANA_2122"), (2022, 305, "CI_ANA_2122"), (2023, 315, "CI_ANA_2023"),
          (2024, 275, "CI_ANA_2024"), (2025, 425, "CI_ANA_2025"), (2026, 400, "CI_ANA_2026")]
for y, val, s in ANA_CI:
    obs(id=f"ANA-CI-{y}", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Côte d'Ivoire", campagne=str(y),
        periode="Campagne (févr.-juil.)", type_prix="Prix plancher obligatoire (administré)", stade="Bord champ",
        qualite="Bien séchée, bien triée", prix=val, monnaie="XOF", unite="kg", kg=1, fx=f"{y}-02:{y}-07",
        ref=("INT-ANA-CI-2026" if y == 2026 else ""), source=s,
        remarque="Prix plancher ; le prix réellement payé peut s'en écarter (ex. 2015 : 410 FCFA obtenus pour un plancher de 275)")
obs(id="ANA-CI-2026-REAL", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Côte d'Ivoire", campagne="2026",
    periode="Campagne 2026 (bilan août 2026)", type_prix="Prix moyen réellement payé", stade="Bord champ (département de Niakara)",
    qualite="Bien séchée, bien triée", prix=416, monnaie="XOF", unite="kg", kg=1, fx="2026-02:2026-07",
    ref="INT-ANA-CI-2026", source="CI_ANA_REAL", remarque="Moyenne locale (450 en mars, 375 en mai, ventes groupées à 400)")
obs(id="ANA-CI-2026-PORT", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Côte d'Ivoire", campagne="2026",
    periode="Campagne 2026", type_prix="Prix plancher obligatoire", stade="Magasin portuaire (Abidjan/San-Pedro)",
    qualite="Bien séchée, bien triée", prix=484, monnaie="XOF", unite="kg", kg=1, fx="2026-02:2026-07",
    ref="INT-ANA-CI-2026", source="CI_ANA_BAREME", remarque="Barème 2026 : 400 bord champ → 425 magasin intérieur → 454 usine → 484 port")
obs(id="ANA-BF-2026", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Burkina Faso", campagne="2026",
    periode="Campagne 2026", type_prix="Prix plancher (administré)", stade="Bord champ", qualite="Noix brute",
    prix=385, monnaie="XOF", unite="kg", kg=1, fx="2026-02:2026-07", ref="INT-ANA-CI-2026", source="BF_ANA_2026")
obs(id="ANA-GW-2026", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Guinée-Bissau", campagne="2026",
    periode="Campagne 2026 (ouverte le 11/03/2026)", type_prix="Prix de référence producteur (administré)", stade="Bord champ",
    qualite="Noix brute", prix=410, monnaie="XOF", unite="kg", kg=1, fx="2026-03:2026-07", ref="INT-ANA-CI-2026",
    source="GW_ANA_2026", remarque="Prix d'achat à Bissau par les intermédiaires : 478 FCFA/kg")
obs(id="ANA-ML-2025", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Mali", campagne="2025",
    periode="Campagne 2025", type_prix="Prix plancher (administré)", stade="Bord champ", qualite="Noix brute",
    prix=390, monnaie="XOF", unite="kg", kg=1, fx="2025-03:2025-07", source="ML_ANA_2025",
    remarque="Campagne 2025 (2026 non trouvée) ; achats effectifs 350-375 FCFA/kg selon la source")
obs(id="ANA-GH-2026", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Ghana", campagne="2025/26 (récolte 2026)",
    periode="Saison 2026", type_prix="Prix minimum producteur (administré, TCDA)", stade="Bord champ",
    qualite="KOR 46, 190 noix/kg, humidité ≤10 %", prix=12, monnaie="GHS", unite="kg", kg=1, fx="2026-02:2026-05",
    ref="INT-ANA-CI-2026", fob="FOB-GH-ANA-2026", source="GH_ANA_2026",
    remarque="Prix arrondi à la hausse ; respect effectif non documenté")
obs(id="FOB-GH-ANA-2026", filiere="Anacarde", produit="Noix de cajou brute (référence FOB)", pays="Ghana", campagne="2025/26 (récolte 2026)",
    periode="Référence de calcul TCDA", type_prix="FOB de référence (modèle de prix)", stade="FOB Tema",
    qualite="KOR 48, 180 noix/kg", prix=1400, monnaie="USD", unite="tonne", kg=1000, fx="2026-02:2026-05",
    source="GH_ANA_2026", remarque="Référence FOB utilisée par la TCDA pour fixer le prix producteur")
obs(id="ANA-TZ-2025/26", filiere="Anacarde", produit="Noix de cajou brute (RCN)", pays="Tanzanie", campagne="2025/26",
    periode="Enchères oct. 2025-janv. 2026", type_prix="Prix moyen d'enchères (système de récépissés d'entrepôt)",
    stade="Magasin primaire (coopératives)", qualite="Grade standard, KOR élevé (≈50 lb)",
    prix="=1279000000000/430961420", monnaie="TZS", unite="kg", kg=1, fx="2025-11:2025-11", ref="INT-ANA-CI-2026",
    source="TZ_ANA_2526", remarque="Prix moyen = recettes / volumes ; saison décalée (oct.-janv.) ; taux de change approché (C)")
obs(id="INT-ANA-CI-2026", filiere="Anacarde", produit="Noix de cajou brute d'origine ivoirienne", pays="International (Asie)",
    campagne="2026", periode="Avril-mai 2026", type_prix="Prix de marché CFR (cotation négoce)", stade="CFR Vietnam/Inde",
    qualite="RCN Côte d'Ivoire (KOR 46-48)", prix=1560, monnaie="USD", unite="tonne", kg=1000, fx="2026-04:2026-05",
    source="INT_ANA_CI", remarque="Pas de bourse pour la noix brute : cotation de négoce, à recouper")
obs(id="INT-ANA-VN-2026", filiere="Anacarde", produit="Noix de cajou brute (toutes origines)", pays="Vietnam (importations)",
    campagne="2026", periode="Janvier-avril 2026", type_prix="Valeur unitaire à l'importation", stade="CIF/CFR Vietnam",
    qualite="Toutes origines (Cambodge, Côte d'Ivoire, Nigeria…)", prix="=2200000000/1300000", monnaie="USD", unite="tonne",
    kg=1000, fx="2026-01:2026-04", source="INT_ANA_VN",
    remarque="Valeur unitaire = valeur ÷ volume ; mélange de qualités (limite de l'indicateur)")

# Coton
COT_CI = [("2017/18", 265, "CI_COT_1718"), ("2018/19", 265, "CI_COT_1819"), ("2019/20", 300, "CI_COT_1920"),
          ("2020/21", 300, "CI_COT_2122"), ("2021/22", 300, "CI_COT_2122"), ("2022/23", 310, "CI_COT_2223"),
          ("2023/24", 310, "CI_COT_2324"), ("2024/25", 310, "CI_COT_SUB"), ("2025/26", 310, "CI_COT_2526")]
for camp, val, s in COT_CI:
    y1 = int(camp[:4])
    obs(id=f"COT-CI-{camp}", filiere="Coton", produit="Coton graine 1er choix", pays="Côte d'Ivoire", campagne=camp,
        periode="Achats nov.-mars ; fibre commercialisée août-juillet", type_prix="Prix d'achat fixé (administré)",
        stade="Bord champ (marchés coton)", qualite="1er choix", prix=val, monnaie="XOF", unite="kg", kg=1,
        fx=f"{y1}-08:{y1+1}-07", equiv="=Parametres!$C$5", equiv_label="équivalent fibre (÷ rendement égrenage)",
        ref=f"INT-COT-{camp}", source=s,
        remarque="Équivalent fibre = prix coton graine ÷ rendement à l'égrenage (graine de coton non valorisée)")
for oid, pays, camp, val, s, fiab_rem in [
    ("COT-BF-2025/26", "Burkina Faso", "2025/26", 325, "BF_COT_2526", "2e choix 300 FCFA"),
    ("COT-ML-2025/26", "Mali", "2025/26", 300, "ML_COT_2526", "Décision du Conseil supérieur de l'agriculture du 06/05/2025"),
    ("COT-BJ-2025/26", "Bénin", "2025/26", 300, "BJ_COT_2526", "Conventionnel ; biologique 360 FCFA"),
    ("COT-TG-2025/26", "Togo", "2025/26", 300, "REG_COT_2526", "Source régionale secondaire (C)"),
    ("COT-SN-2025/26", "Sénégal", "2025/26", 350, "REG_COT_2526", "« jusqu'à 350 FCFA » : source secondaire (C)"),
    ("COT-BF-2026/27", "Burkina Faso", "2026/27", 310, "REG_COT_2526", "Prix plancher 2026/27 (310/285) ; source de presse non primaire"),
    ("COT-BJ-2026/27", "Bénin", "2026/27", 300, "BJ_COT_2627", "Conventionnel 1er choix ; biologique 360"),
]:
    y1 = int(camp[:4])
    obs(id=oid, filiere="Coton", produit="Coton graine 1er choix", pays=pays, campagne=camp,
        periode="Campagne", type_prix="Prix d'achat fixé (administré)", stade="Bord champ", qualite="1er choix (conventionnel)",
        prix=val, monnaie="XOF", unite="kg", kg=1, fx=f"{y1}-08:{y1+1}-07" if camp == "2025/26" else "2026-04:2026-07",
        source=s, remarque=fiab_rem)

# Caoutchouc (CI : FCFA/kg de fonds de tasse, DRC de référence 60 %)
CAO_CI = [("2025-01", 442, "2024-12", "CI_CAO_0125"), ("2025-04", 438, "2025-03", "CI_CAO_0425"),
          ("2026-01", 352, "2025-12", "CI_CAO_2026"), ("2026-02", 368, "2026-01", "CI_CAO_2026"),
          ("2026-04", 401, "2026-03", "CI_CAO_2026"), ("2026-05", 439, "", "CI_CAO_2026"),
          ("2026-07", 493, "", "CI_CAO_2026"), ("2026-09", 484, "", "CI_CAO_0926")]
for mois, val, mref, s in CAO_CI:
    obs(id=f"CAO-CI-{mois}", filiere="Caoutchouc", produit="Caoutchouc naturel (fonds de tasse)", pays="Côte d'Ivoire",
        campagne=mois[:4], periode=f"Mois {mois}", type_prix="Prix bord champ fixé (APROMAC, loi 2017-540)",
        stade="Bord champ", qualite="Coagulum humide, DRC de référence 60 %", prix=val, monnaie="XOF", unite="kg", kg=1,
        fx=f"{mref or mois}:{mref or mois}", equiv="=Parametres!$C$6", equiv_label="kg de caoutchouc sec (÷ DRC 60 %)",
        ref=(f"INT-TSR-{mref}" if mref else ""), source=s,
        remarque="Prix du mois M calculé sur les cours SICOM du mois M-1 ; producteur = 63 % (66 % en 2026) du prix de référence")
obs(id="CAO-TH-2025-05", filiere="Caoutchouc", produit="Caoutchouc (cup lump) base 100 % DRC", pays="Thaïlande", campagne="2025",
    periode="02/05/2025", type_prix="Prix de marché intérieur", stade="Marché central / bord champ",
    qualite="Cup lump 100 % DRC (sec)", prix=58, monnaie="THB", unite="kg", kg=1, fx="2025-04:2025-04",
    ref="INT-TSR-2025-04", source="TH_CAO", remarque="Comparé au TSR20 du mois précédent, comme pour la Côte d'Ivoire")
obs(id="CAO-ID-2026-08", filiere="Caoutchouc", produit="Bokar base KKK 100 % (sec)", pays="Indonésie", campagne="2026",
    periode="Août 2026 (4 relevés)", type_prix="Prix de référence provincial (Sumatra-Sud)", stade="Bord champ (prix de référence)",
    qualite="KKK 100 % (sec)", prix="=(38835+39076+41446+42238)/4", monnaie="IDR", unite="kg", kg=1, fx="2026-08:2026-08",
    source="ID_CAO", remarque="Prix de référence non reçu uniformément (dépend du KKK) ; TSR20 juil.-août 2026 non vérifié : pas de taux de transmission calculé")

# Palmier à huile
obs(id="PAL-CI-FFB-2026-01", filiere="Palmier à huile", produit="Régimes de palme (FFB)", pays="Côte d'Ivoire", campagne="2026",
    periode="Janvier 2026", type_prix="Prix fixé (Conseil Hévéa-Palmier à huile-Coco)", stade="Bord champ",
    qualite="Régimes frais (planteurs villageois)", prix=80000, monnaie="XOF", unite="tonne", kg=1000, fx="2026-01:2026-01",
    ref="INT-CPO-2026-01", source="CI_PAL_0126", remarque="Ratio = prix régime / prix mondial de l'huile brute (pas une transmission au sens strict)")
obs(id="PAL-CI-CPO-2026-01", filiere="Palmier à huile", produit="Huile de palme brute (CPO)", pays="Côte d'Ivoire", campagne="2026",
    periode="Janvier 2026", type_prix="Prix fixé (marché intérieur)", stade="Départ huilerie",
    qualite="CPO", prix=620000, monnaie="XOF", unite="tonne", kg=1000, fx="2026-01:2026-01",
    ref="INT-CPO-2026-01", source="CI_PAL_0126", remarque="Prix intérieur de l'huile brute comparé au prix mondial (CIF Rotterdam)")
obs(id="PAL-CI-FFB-2024-Q4", filiere="Palmier à huile", produit="Régimes de palme (FFB)", pays="Côte d'Ivoire", campagne="2024",
    periode="Octobre-décembre 2024", type_prix="Prix fixé (CHP-HC)", stade="Bord champ", qualite="Régimes frais",
    prix=75000, monnaie="XOF", unite="tonne", kg=1000, fx="2024-10:2024-12", ref="INT-CPO-2024-Q4", source="CI_PAL_Q424")
obs(id="PAL-ID-FFB-2026-01", filiere="Palmier à huile", produit="Régimes de palme (TBS)", pays="Indonésie", campagne="2026",
    periode="Janvier 2026 (3 semaines)", type_prix="Prix de référence provincial (Disbun Riau)", stade="Livraison usine (planteurs partenaires)",
    qualite="Palmiers de 10-20 ans", prix="=(3496.91+3430.63+3449.84)/3", monnaie="IDR", unite="kg", kg=1,
    fx="2026-01:2026-01", ref="INT-CPO-2026-01", source="ID_PAL_0126",
    remarque="Prix départ planteur partenaire ; les planteurs indépendants vendent souvent en dessous")
obs(id="PAL-MY-FFB-2025", filiere="Palmier à huile", produit="Régimes de palme (FFB)", pays="Malaisie", campagne="2025",
    periode="Moyenne 2025", type_prix="Prix de référence MPOB (1 % OER × OER national)", stade="Départ plantation (référence)",
    qualite="FFB, OER national 19,74 %", prix="=47.39*19.74", monnaie="MYR", unite="tonne", kg=1000, fx="2025-01:2025-12",
    ref="INT-CPO-2025", source="MY_PAL_2025", remarque="Prix à 1 % OER (47,39 RM) × taux d'extraction national (19,74 %)")

# Riz
obs(id="RIZ-CI-2025", filiere="Riz", produit="Riz paddy", pays="Côte d'Ivoire", campagne="2025", periode="Moyenne janv.-déc. 2025",
    type_prix="Prix moyen observé", stade="Bord champ", qualite="Paddy sec (non précisé)", prix=233, monnaie="XOF", unite="kg", kg=1,
    fx="2025-01:2025-12", ref="INT-RIZ-2025", source="USDA_RIZ_CI", remarque="+8,5 % par rapport à 2024")
obs(id="RIZ-SN-2025", filiere="Riz", produit="Riz paddy", pays="Sénégal", campagne="2025", periode="Campagne",
    type_prix="Prix producteur fixé (interprofession)", stade="Bord champ", qualite="Paddy", prix=130, monnaie="XOF", unite="kg",
    kg=1, fx="2025-01:2025-12", ref="INT-RIZ-2025", source="USDA_RIZ_SN",
    remarque="Subvention de 30 FCFA/kg depuis 2022 : prix payé par les usiniers 160 FCFA/kg")
obs(id="RIZ-VN-2025", filiere="Riz", produit="Riz paddy frais (IR 50404 / OM 5451)", pays="Vietnam", campagne="2025",
    periode="Fin 2025", type_prix="Prix de marché", stade="Bord champ (delta du Mékong)", qualite="Paddy frais (humide)",
    prix="=(5450+5650)/2", monnaie="VND", unite="kg", kg=1, fx="2025-09:2025-10", ref="INT-RIZ-2025", source="VN_RIZ",
    remarque="Paddy frais (humidité élevée) : sous-estime le prix du paddy sec ; comparaison indicative")

# Fruits
obs(id="BAN-EC-2026", filiere="Banane dessert", produit="Banane d'exportation (caisse 22XU, 43 lb)", pays="Équateur", campagne="2026",
    periode="Année 2026", type_prix="Prix minimum de soutien (administré)", stade="Pied du navire (producteur → exportateur)",
    qualite="Banane export", prix=7.5, monnaie="USD", unite="caisse 43 lb", kg=19.5045, fx="2026-01:2026-08",
    source="EC_BAN_2026", remarque="Pas de prix producteur public comparable en Côte d'Ivoire (filière intégrée)")
obs(id="MAN-CI-2026", filiere="Mangue", produit="Mangue export (Kent)", pays="Côte d'Ivoire", campagne="2026", periode="Campagne 2026",
    type_prix="Prix interprofessionnel (Inter-Mangue)", stade="Station de conditionnement", qualite="Mangue export",
    prix=220, monnaie="XOF", unite="kg", kg=1, fx="2026-03:2026-06", source="CI_MAN_2026",
    remarque="Bord champ : 2 450 FCFA la caisse (poids non publié) : non convertible en FCFA/kg")
obs(id="MAN-BF-2026", filiere="Mangue", produit="Mangue", pays="Burkina Faso", campagne="2026", periode="Campagne 2026",
    type_prix="Prix plancher (administré)", stade="Bord champ", qualite="Mangue", prix=95, monnaie="XOF", unite="kg", kg=1,
    fx="2026-03:2026-06", source="BF_MAN_2026", remarque="Stade différent du prix ivoirien (station) : pas de comparaison directe")

# Références internationales (prix = formule vers Cours_periodes)
def intl(oid, serie, d, f, filiere, produit, type_prix, stade, qualite, source, unite="kg", kg=1, rem=""):
    obs(id=oid, filiere=filiere, produit=produit, pays="International", campagne=f"{d} → {f}", periode=f"Moyenne {d} à {f}",
        type_prix=type_prix, stade=stade, qualite=qualite, prix=("PERIODE", f"{serie}:{d}:{f}"), monnaie="USD",
        unite=unite, kg=kg, fx=f"{d}:{f}", source=source, remarque=rem)

for camp, *_ in CACAO_CI:
    for h in ("P", "I"):
        d, f = half(camp, h)
        if camp == "2025/26" and h == "I":
            f = "2026-08"
        intl(f"INT-CAC-{camp}-{h}", "cacao", d, f, "Cacao", "Fèves de cacao", "Cours international (moyenne mensuelle)",
             "Bourses Londres/New York (prix ICCO)", "Standard", "BM_PINK",
             rem="Banque mondiale (ICCO) jusqu'en janv. 2026, FMI ensuite" + (" ; septembre 2026 non disponible" if camp == "2025/26" and h == "I" else ""))
for m in ("2026-01", "2026-02", "2026-08"):
    intl(f"INT-CAC-{m}", "cacao", m, m, "Cacao", "Fèves de cacao", "Cours international (mensuel)", "Prix ICCO", "Standard",
         "FMI_PCPS" if m != "2026-01" else "BM_PINK")
intl("INT-CAC-2026-04", "cacao", "2026-03", "2026-04", "Cacao", "Fèves de cacao", "Cours international", "Prix ICCO", "Standard", "FMI_PCPS")
intl("INT-CAC-2026-05", "cacao", "2026-05", "2026-05", "Cacao", "Fèves de cacao", "Cours international", "Prix ICCO", "Standard", "FMI_PCPS")
intl("INT-CAC-2026-06", "cacao", "2026-06", "2026-06", "Cacao", "Fèves de cacao", "Cours international", "Prix ICCO", "Standard", "FMI_PCPS")
for camp, *_ in CAFE_CI:
    y1 = int(camp[:4])
    f = f"{y1+1}-09" if camp != "2025/26" else "2026-08"
    intl(f"INT-ROB-{camp}", "robusta", f"{y1}-10", f, "Café", "Café robusta", "Cours international (indicateur OIC)",
         "Ex-dock New York/Le Havre-Marseille", "Robusta (indicateur OIC)", "BM_PINK",
         rem="Banque mondiale jusqu'en janv. 2026 ; OIC/FMI ensuite" if camp == "2025/26" else "")
for m in ("2026-07", "2026-08"):
    intl(f"INT-ROB-{m}", "robusta", m, m, "Café", "Café robusta", "Cours international (mensuel)", "Ex-dock", "Robusta",
         "OIC_CMR" if m == "2026-08" else "FMI_PCPS")
for camp, *_ in COT_CI:
    y1 = int(camp[:4])
    f = f"{y1+1}-07" if camp != "2025/26" else "2026-01"
    intl(f"INT-COT-{camp}", "coton", f"{y1}-08", f, "Coton", "Coton fibre", "Indice Cotlook A", "CFR Extrême-Orient",
         "Middling 1-1/8\"", "BM_PINK", rem="Campagne de commercialisation de la fibre (août-juillet)" + (" ; 2025/26 : août 2025-janv. 2026 seulement" if camp == "2025/26" else ""))
for m in ("2024-12", "2025-03", "2025-04", "2025-12", "2026-01", "2026-03"):
    intl(f"INT-TSR-{m}", "tsr20", m, m, "Caoutchouc", "Caoutchouc naturel TSR20", "Cours SGX-SICOM TSR20 (mensuel)", "FOB (contrat SICOM)",
         "TSR20 (sec)", "SGX_0326" if m == "2026-03" else "BM_PINK")
intl("INT-CPO-2026-01", "palme", "2026-01", "2026-01", "Palmier à huile", "Huile de palme brute", "Prix mondial (Malaisie/Indonésie)", "CIF Rotterdam",
     "CPO", "BM_PINK", unite="tonne", kg=1000)
intl("INT-CPO-2024-Q4", "palme", "2024-10", "2024-12", "Palmier à huile", "Huile de palme brute", "Prix mondial", "CIF Rotterdam", "CPO", "BM_PINK", unite="tonne", kg=1000)
intl("INT-CPO-2025", "palme", "2025-01", "2025-12", "Palmier à huile", "Huile de palme brute", "Prix mondial", "CIF Rotterdam", "CPO", "BM_PINK", unite="tonne", kg=1000)
intl("INT-RIZ-2025", "riz", "2025-01", "2025-12", "Riz", "Riz blanchi Thaï 5 % brisures (équivalent paddy)", "Prix FOB Bangkok × taux d'usinage",
     "FOB Bangkok (équivalent paddy)", "Thaï 5 % ; taux d'usinage 65 %", "BM_PINK", unite="tonne", kg=1000,
     rem="Équivalent paddy = prix du riz blanchi × 65 % (paramètre) ; hors fret, assurance et droits")
OBS[-1]["equiv"] = "=1/Parametres!$C$4"
OBS[-1]["equiv_label"] = "équivalent paddy (× taux d'usinage)"

# Paramètres techniques (modifiables, documentés)
PARAMS = [
    ("C3", "Parité fixe FCFA/EUR", "=655.957", "BCEAO / Traité (parité fixe depuis 1999)", "https://www.bceao.int/"),
    ("C4", "Taux d'usinage riz (paddy → blanchi)", "=0.65", "Hypothèse technique usuelle (à ajuster selon ADERIZ)", ""),
    ("C5", "Rendement à l'égrenage coton (Côte d'Ivoire)", "=(730000*480*0.45359237/1000)/351764",
     "Calculé : fibre USDA MY2024/25 (730 000 balles de 480 lb) ÷ coton graine 2024/25 (351 764 t, Ecofin)", "https://www.fas.usda.gov/data/cote-divoire-cotton-and-products-annual-5"),
    ("C6", "DRC de référence caoutchouc (Côte d'Ivoire)", "=0.6", "Convention officielle ; DRC mesuré 65-68 % selon des analyses indépendantes", "https://businessactuality.com/le-prix-du-caoutchouc-en-cote-divoire-un-bras-de-fer-entre-planteurs-usiniers-et-regulateurs/"),
    ("C7", "Conversion c/lb → USD/kg", "=0.0220462", "1 lb = 0,453592 kg", ""),
]

# Volumes et rendements (importance économique, revenu à l'hectare)
VOLUMES = [
    # filière, volume (t), libellé, prix de référence (ID obs), source, remarque
    ("Cacao", 2000000, "Production 2025/26 (prévision CCC 2,0-2,1 Mt)", "CAC-CI-2026/27-P", "CI_CAC_PROD", "Borne basse de la prévision"),
    ("Anacarde", 1549221, "Production commercialisée 2025", "ANA-CI-2026", "CI_ANA_PROD", ""),
    ("Caoutchouc", 1600000, "Production ≈1,6 Mt (2023)", "CAO-CI-2026-09", "CI_CAO_PROD", "Base humide supposée (non précisée par la source)"),
    ("Coton", 351764, "Coton graine 2024/25", "COT-CI-2025/26", "CI_COT_PROD", ""),
    ("Café", 24832, "Achats oct. 2024-juin 2025 (effondrement de la production)", "CAF-CI-2026/27", "CI_CAF_PROD", ""),
]
RENDEMENTS = [
    # filière, pays, rendement kg/ha, prix ID, source
    ("Cacao", "Côte d'Ivoire", 500, "CAC-CI-2026/27-P", "RDT_CACAO"),
    ("Cacao", "Ghana", 400, "CAC-GH-2026/27-P", "RDT_CACAO"),
    ("Coton", "Côte d'Ivoire", 984, "COT-CI-2025/26", "CI_COT_PROD"),
    ("Coton", "Burkina Faso", 865, "COT-BF-2025/26", "BF_COT_PROD"),
    ("Coton", "Mali", 914, "COT-ML-2025/26", "REG_COT_RDT"),
    ("Coton", "Bénin", 1248, "COT-BJ-2025/26", "REG_COT_RDT"),
]
