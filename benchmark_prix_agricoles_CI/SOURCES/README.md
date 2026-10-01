# Dossier SOURCES

Ce dossier rassemble les pièces qui permettent de vérifier les chiffres de la note et de la base `Base_Prix_Benchmark_CI.xlsx`.

| Élément | Contenu |
|---|---|
| `donnees_primaires/` | Fichiers de données téléchargés et utilisés tels quels par `scripts/build_base.py` |
| `Liste_sources.csv` | Les 127 sources de la base : clé, institution, titre et contenu utilisé, URL, type, fiabilité, date de consultation, nombre d'observations qui la citent, emplacement d'utilisation (onglet de la base ou page de la note) |

`Liste_sources.csv` est au format français : séparateur `;`, UTF-8. Lecture en Python : `pd.read_csv("Liste_sources.csv", sep=";")`.

## 1. Fichiers de données primaires archivés

| Fichier | Origine | Période couverte | Usage dans la base | Empreinte SHA-256 |
|---|---|---|---|---|
| `BanqueMondiale_CMO-Historical-Data-Monthly_2026-02-03.xlsx` | Banque mondiale, *Commodity Price Data (Pink Sheet)*, fichier mensuel mis à jour le 3 février 2026. Copie identique octet pour octet obtenue via le dépôt public GitHub `unbalancedparentheses/forex-centuries` (commit `f79a85b`, 26/02/2026), le site de la Banque mondiale n'étant pas accessible depuis l'environnement d'étude. | 1960 – janvier 2026 | `Cours_mensuels` : cacao, robusta, indice A du coton, TSR20, huile de palme, riz thaï 5 % | `fa0670dd250c419c359f5ea5febdfa45bb2ef005603fd7cd427befd8a40bffb8` |
| `BCE_eurofxref-hist.csv` | Banque centrale européenne, taux de référence quotidiens (fichier `eurofxref-hist`), tel que distribué avec le paquet Python `currencyconverter` 0.18.22. | 4 janvier 1999 – 14 septembre 2026 | `Change_mensuel` : USD/EUR (donc FCFA/USD via la parité 655,957), IDR, THB, MYR | `f230f5499c2fc54552278d3a712b71e4be2dc3224e44dbf8be71ccdce330e4ea` |
| `BRI_WS_XRU_moyennes_mensuelles_extrait.csv` | Banque des règlements internationaux, série WS_XRU (taux de change contre USD, moyennes mensuelles). Extrait des pays utiles, tiré du fichier `WS_XRU_csv_flat` du même dépôt GitHub. | janvier 2013 – avril 2025 (TZS) à janvier 2026 selon les pays | `Change_mensuel` : GHS, UGX, VND, TZS, NGN | `266d2ba792b19045da045b374838c9adf597c633fa72ed5185c2970b8925914a` |
| `FMI_taux_de_change_mensuels_extrait.csv` | FMI, taux de change mensuels (extrait de `imf_exchange_rates.csv` du même dépôt). | janvier 2013 – avril 2025 (TZS) à janvier 2026 selon les monnaies | Taux GHS de novembre et décembre 2025 (moyenne des taux de fin de mois, saisie dans `scripts/inputs.py`, fiabilité C) ; recoupement des autres taux | `9a37d828314485543da4e81e2106c5a1b587cec5ed3dab7651b181ebfeaa20d8` |

Pour vérifier l'intégrité d'un fichier : `sha256sum donnees_primaires/*`.

## 2. Documents sources non archivés

L'environnement de production n'autorisait pas le téléchargement direct de pages web ni de PDF (politique réseau : FAOSTAT, UN Comtrade, Eurostat, API Banque mondiale et BCE, sites institutionnels refusés). Les documents cités ont été consultés le 1er octobre 2026 ; leur URL figure dans `Liste_sources.csv` et dans l'onglet `Sources` de la base.

Documents à archiver en priorité (PDF ou capture datée) pour compléter le dossier, car ils portent les chiffres centraux de la note :

| Priorité | Document | Chiffres portés | URL |
|---|---|---|---|
| 1 | Gouvernement de Côte d'Ivoire – prix bord champ 2026/27 du cacao et du café | Cacao 1 200 FCFA/kg ; café 1 300 FCFA/kg | https://gouv.ci/actualite/campagne-principale-2026-2027-le-prix-bord-champ-du-cacao-est-fixe-a-1200-fcfa-le-kg-le-prix-du-cafe-setablit-a-1300-fcfa-le-kg-8771 |
| 1 | COCOBOD (via MyJoyOnline) – prix producteur 2026/27 | 42 400 GH¢/t ; 71,18 % du FOB brut réalisé | https://www.myjoyonline.com/cocobod-increases-cocoa-producer-price-to-gh%C2%A242400-for-2026-27-season/ |
| 1 | Banque mondiale (2019) – *Situation économique en Côte d'Ivoire : au pays du cacao* | Part producteur ≥60 % du CAF ; prélèvements ≈22 % ; marges | https://documents1.worldbank.org/curated/en/277191561741906355/pdf/Cote-dIvoire-Economic-Update.pdf |
| 1 | OMC – Examen des politiques commerciales UEMOA, annexe Côte d'Ivoire (WT/TPR/S/362) | DUS 14,6 % du CAF ; prélèvements 2016/17 | https://www.wto.org/french/tratop_f/tpr_f/s362-03_f.pdf |
| 1 | FMI – *Primary Commodity Prices* (via FRED : PCOCOUSDM, PCOFFROBUSDM) | Cours du cacao et du robusta, février-juillet 2026 | https://fred.stlouisfed.org/series/PCOCOUSDM |
| 1 | OIC – *Coffee Market Report* août 2026 | Indicateur robusta 180,63 c/lb | https://www.ico.org/documents/cy2025-26/cmr-0826-e.pdf |
| 2 | UCDA (Ouganda) – rapport mensuel de juillet 2026 | Robusta FAQ 11 500 UGX/kg | https://ugandacoffee.go.ug/sites/default/files/2026-09/10%20July%202026%20Report%20draft(2)(1)(1).pdf |
| 2 | TCDA (Ghana) – prix minimum de la noix de cajou 2025/26 | 12,00 GH¢/kg ; FOB de référence 1 400 USD/t | https://tcda.gov.gh/government-sets-ghs-12-00-per-kilogram-as-minimum-producer-price-for-raw-cashew-nuts-2025-2026-season/ |
| 2 | MINADERPV (via Agence Ecofin) – prix minimum de la noix de cajou 2026 | 400 FCFA/kg | https://www.agenceecofin.com/actualites-agro/0902-135589-cote-d-ivoire-baisse-de-6-du-prix-minimum-bord-champ-de-la-noix-de-cajou-en-2026 |
| 2 | MINADERPV (via KOACI) – prix du coton graine 2025/26 | 310 FCFA/kg (1er choix) | https://www.koaci.com/article/2025/07/31/cote-divoire/societe/cote-divoire-campagne-2025-2026-le-prix-du-coton-de-1er-choix-est-fixe-a-310-fcfakg-et-celui-de-2e-choix-a-285-fcfakg_189056.html |
| 2 | SOFITEX (Burkina Faso) – campagne cotonnière 2025/26 | 325 FCFA/kg | https://www.sofitex.bf/2025/04/10/campagne-cotonniere-2025-2026-les-engrais-a-17-500-f-cfa-les-insecticides-a-5-200-f-cfa-et-le-kg-de-coton-a-325-f-cfa/ |
| 2 | USDA FAS – *Côte d'Ivoire Cotton and Products Annual 2026* | Fibre 2024/25 (rendement à l'égrenage calculé) | https://www.fas.usda.gov/data/cote-divoire-cotton-and-products-annual-5 |
| 2 | SGX – *SICOM Rubber Monthly Report*, mars 2026 | TSR20 moyen 1,965 USD/kg | https://api2.sgx.com/sites/default/files/2026-04/SICOM%20SGX%20March%202026%20.pdf |
| 2 | MPOB – *Overview of the Malaysian Oil Palm Industry 2025* | Prix des régimes à 1 % OER : 47,39 RM | https://bepi.mpob.gov.my/images/overview/Overview2025.pdf |
| 2 | USDA FAS – *Grain and Feed Annual* Côte d'Ivoire 2026 et Sénégal 2025 | Paddy 233 FCFA/kg (CI) ; 130 FCFA/kg (Sénégal) | voir `Liste_sources.csv` (clés `USDA_RIZ_CI`, `USDA_RIZ_SN`) |
| 3 | Toutes les autres sources | Voir `Liste_sources.csv` | — |

Les sources de fiabilité B (presse ou agence reprenant une annonce officielle datée) gagneraient à être remplacées par l'acte officiel correspondant (arrêté, communiqué du CCC, du Conseil Hévéa-Palmier à huile-Coco, de l'APROMAC ou de la CCAK) lorsque le ministère y a accès.
