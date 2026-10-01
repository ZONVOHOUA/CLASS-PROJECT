# Méthodologie et sources

**Benchmark international des prix agricoles de la Côte d'Ivoire : les prix pratiqués sont-ils compétitifs ?**
Données arrêtées au 1er octobre 2026 (dernières annonces intégrées : prix cacao et café 2026/27 du 1er septembre 2026, prix COCOBOD du 25 septembre 2026).

Ce document complète la note de cinq pages. Il explique ce qui a été mesuré, comment, avec quelles sources et dans quelles limites. Tous les chiffres de la note et des graphiques sont calculés dans la base `Base_Prix_Benchmark_CI.xlsx`, avec des formules visibles. Aucun chiffre n'a été estimé hors de cette base.

---

## Sommaire

1. [Contenu du dossier](#1-contenu-du-dossier)
2. [Ce que « compétitif » veut dire dans cette étude](#2-ce-que--compétitif--veut-dire-dans-cette-étude)
3. [Filières couvertes](#3-filières-couvertes)
4. [Pays comparateurs](#4-pays-comparateurs)
5. [Règle de comparabilité et équivalences](#5-règle-de-comparabilité-et-équivalences)
6. [Période d'étude et appariement dans le temps](#6-période-détude-et-appariement-dans-le-temps)
7. [Conversion des monnaies](#7-conversion-des-monnaies)
8. [Prix internationaux de référence](#8-prix-internationaux-de-référence)
9. [Indicateurs I à VIII : définitions et formules](#9-indicateurs-i-à-viii--définitions-et-formules)
10. [Matrice de synthèse et graphiques](#10-matrice-de-synthèse-et-graphiques)
11. [Audit de cohérence](#11-audit-de-cohérence)
12. [Difficultés rencontrées](#12-difficultés-rencontrées)
13. [Limites des données](#13-limites-des-données)
14. [Reproduire et mettre à jour](#14-reproduire-et-mettre-à-jour)
15. [Liste des sources](#15-liste-des-sources)

---

## 1. Contenu du dossier

| Fichier | Contenu |
|---|---|
| `Note_Benchmark_Prix_Agricoles_CI.pdf` | Note ministérielle de 5 pages (message, carte générale, cultures de rente, fruits et vivriers, recommandations). |
| `Note_Benchmark_Prix_Agricoles_CI.docx` | Même note, version Word modifiable (5 pages, texte et tableaux éditables, graphiques en images). |
| `Base_Prix_Benchmark_CI.xlsx` | Base de traçabilité : 16 onglets, 177 observations de prix, 127 sources, 4 213 formules (0 erreur au recalcul). |
| `Base_Prix_Benchmark_CI_observations.csv` | Export des 177 observations (valeurs recalculées). Séparateur `;`, décimale `,`, UTF-8. |
| `METHODOLOGIE_ET_SOURCES.md` | Le présent document. |
| `SOURCES/` | Fichiers de données primaires archivés, liste des sources (`Liste_sources.csv`) et mode d'emploi (`README.md`). |
| `figures/` | Les 6 graphiques de la note (SVG vectoriel et PNG 300 dpi), produits uniquement à partir de la base. |
| `scripts/` | Chaîne de production complète (saisie des données, base, recalcul, graphiques, PDF, Word, exports). |

Onglets de la base :

| Onglet | Rôle |
|---|---|
| `Lisez-moi` | Mode d'emploi, codes couleur, codes de fiabilité. |
| `Matrice` | Matrice de synthèse reprise en page 2 de la note. |
| `Indicateurs` | Comparaisons deux à deux, position par rapport à la médiane des comparateurs, transmission moyenne sur dix ans. |
| `Observations` | Une ligne par prix : 33 colonnes, du prix d'origine au prix FCFA/kg et au taux de transmission. |
| `Cacao_transmission` | Série 2016/17-2026/27 par demi-campagne (Côte d'Ivoire, Ghana, cours mondial). |
| `Series_CI` | Prix officiels ivoiriens sur dix campagnes, en nominal et en FCFA constants 2025 ; volatilité. |
| `Decomposition` | Du prix international au prix producteur (cacao, anacarde, caoutchouc, palmier, coton). |
| `Positionnement`, `Volumes_Rendements` | Données du graphique 1 ; valeur brute au producteur ; revenu brut à l'hectare. |
| `Audit_QC` | Contrôle de comparabilité de chaque comparaison (section 11). |
| `Sources` | Référentiel des 127 sources (institution, titre, URL, type, fiabilité, date de consultation). |
| `Cours_mensuels`, `Cours_periodes` | Cours internationaux mensuels et moyennes exactes de chaque période comparée. |
| `Change_mensuel`, `Change_periodes` | Taux de change mensuels et moyennes exactes de chaque période comparée. |
| `Parametres` | Paramètres techniques modifiables (parité FCFA/EUR, taux d'usinage, rendement à l'égrenage, DRC). |

Codes couleur de la base : bleu = donnée saisie (prix d'origine, taux) ; noir = formule ; vert = renvoi vers un autre onglet ; fond jaune = paramètre ou hypothèse à valider ; fond orangé = donnée de fiabilité C ou contrôle non satisfait.

## 2. Ce que « compétitif » veut dire dans cette étude

Un prix agricole n'est pas « compétitif » dans l'absolu. L'étude retient trois dimensions, mesurées séparément et jamais agrégées en un score composite.

**A. Rémunération relative du producteur.** Le producteur ivoirien reçoit-il plus ou moins que son homologue d'un pays comparable, pour le même produit, au même stade et à la même période ?

> Indice de rémunération = prix bord champ CI ÷ prix bord champ du comparateur × 100. Un indice inférieur à 100 signifie que le producteur ivoirien reçoit moins.

**B. Transmission du prix international.** Quelle part du cours mondial atteint le producteur ? La formule est identique pour tous les pays : même référence internationale, même période, même conversion.

> Taux de transmission = prix bord champ (FCFA/kg, base de comparaison) ÷ prix international de référence de la même période (FCFA/kg).

**C. Compétitivité et soutenabilité de la filière.** Le prix est-il cohérent avec la valeur à l'exportation et finançable sans déficit ? On distingue :

| Situation | Critère observable | Exemple dans l'étude |
|---|---|---|
| Prix élevé et soutenable | Indice ≥ 100, transmission cohérente avec les concurrents, financement par le marché | Aucune filière ne remplit les trois conditions en 2026 |
| Prix élevé mais déconnecté | Prix supérieur au cours mondial ou à la parité FOB, ou maintenu par une subvention ou des stocks invendus | Cacao principal 2025/26 (103 % du cours, 123 000 t invendues) ; riz (151 % de la parité FOB) ; coton (parité régionale grâce à une subvention de ≈72 FCFA/kg, 23 % du prix) |
| Prix bas, peu compétitif pour le planteur | Indice < 100 et transmission inférieure aux concurrents | Cacao 2026/27 (indice 58, transmission 35 % contre 62 % au Ghana : soutenable pour le régulateur, pas pour le planteur) ; café ; caoutchouc ; palmier |
| Prix au niveau régional, valeur captée en aval | Indice ≈ 100 face aux voisins, mais part du prix international faible en absolu | Anacarde (indice 98 face à la médiane Burkina, Guinée-Bissau, Ghana, mais −34 % face au Ghana seul ; 46 % du CFR Asie, 40 % de la valeur formée entre le port et l'acheteur) |

La part producteur dans la valeur FOB/CAF (indicateur V) et la décomposition de la valeur (indicateur VIII) complètent la dimension C.

## 3. Filières couvertes

Critères de sélection : poids de la filière dans les exportations, les revenus agricoles ou la sécurité alimentaire ; existence d'un prix au producteur observable ; existence d'une référence internationale.

| Filière | Ordre de grandeur (source dans la base) | Prix ivoirien utilisé | Traitement |
|---|---|---|---|
| Cacao | Production 2025/26 prévue à 2,0-2,1 Mt (CCC) | Prix minimum garanti bord champ (CCC), campagne principale et intermédiaire | Analysée, comparaison directe (Ghana) |
| Anacarde | 1 549 221 t commercialisées en 2025 (MINADERPV) | Prix plancher bord champ (CCAK) et barème jusqu'au port | Analysée, comparaison directe (UEMOA, Ghana) |
| Caoutchouc naturel | ≈1,6 Mt en 2023 | Prix mensuel bord champ (APROMAC), coagulum à DRC de référence 60 % | Analysée, comparaison indicative |
| Coton | 351 764 t de coton graine en 2024/25 | Prix d'achat du coton graine 1er choix | Analysée, comparaison directe (UEMOA) |
| Café robusta | 24 832 t achetées d'octobre 2024 à juin 2025 | Prix minimum garanti du café vert | Analysée, comparaison directe (Vietnam, Ouganda) |
| Palmier à huile | Volume non repris dans les calculs | Prix du régime fixé par le Conseil Hévéa-Palmier à huile-Coco | Analysée, comparaison indicative |
| Riz | Importations ≈1,75 Mt par an (USDA) | Prix moyen du paddy 2025 (USDA) | Analysée (Sénégal direct, Vietnam indicatif, parité FOB) |
| Banane dessert | Exportations 271 000 t en 2025 | Aucun prix producteur public (filière intégrée) | Données insuffisantes |
| Mangue | Exportation de fruits frais | Prix en station 220 FCFA/kg ; prix bord champ à la caisse (poids non publié) | Non comparable en l'état |
| Ananas, cola, coco, canne à sucre | Ananas : 23 557 t exportées en 2023 | Aucun prix producteur public identifié lors de la collecte | Données insuffisantes |
| Maïs, manioc, igname, plantain, tomate, oignon | Marchés domestiques | OCPV : prix à la consommation (stade non comparable) | Données insuffisantes |

Pour les filières classées « données insuffisantes » ou « non comparable », la note applique la règle de prudence : *les données disponibles ne permettent pas de conclure de manière robuste sur la compétitivité relative du prix de ces filières.*

## 4. Pays comparateurs

Deux à cinq comparateurs par filière, choisis pour leur proximité (même zone, même devise ou même produit) et leur poids sur le marché mondial. Chaque comparaison est qualifiée de **directe** (même produit, même stade, même période, même qualité) ou d'**indicative** (un de ces éléments imparfaitement apparié, écart documenté dans l'onglet `Audit_QC`).

| Filière | Comparateurs | Justification | Type |
|---|---|---|---|
| Cacao | Ghana | Concurrent direct : même zone, même grade de fèves, prix producteur administré (COCOBOD), risque de fuite transfrontalière. Série complète par demi-campagne 2016/17-2026/27. | Directe |
| | Cameroun, Nigeria | Marchés libéralisés d'Afrique de l'Ouest et centrale : montrent un prix qui suit le marché. Relevés ponctuels (Nigeria : source C). | Indicative |
| | Équateur | Grand exportateur d'Amérique latine ; qualités différentes (CCN-51, Nacional). | Indicative |
| Café robusta | Vietnam | Premier producteur mondial de robusta ; prix bord champ publié quotidiennement (Dak Lak). | Directe |
| | Ouganda | Producteur africain de robusta ; prix bord champ publié par l'autorité caféière (FAQ). | Directe (taux de change de fiabilité C) |
| Anacarde | Burkina Faso, Guinée-Bissau, Mali | Pays UEMOA, même devise, prix plancher ou de référence bord champ. Mali : campagne 2025 comparée au prix ivoirien 2025. | Directe |
| | Ghana | Voisin, prix minimum (TCDA) fondé sur un FOB de référence. | Directe |
| | Tanzanie | Grand producteur africain, système d'enchères ; saison et qualité (KOR) différentes. | Indicative |
| Coton | Burkina Faso, Mali, Bénin, Togo | Pays UEMOA, même devise, coton graine 1er choix à prix administré, même campagne 2025/26. | Directe |
| | Sénégal | Prix « jusqu'à 350 FCFA/kg » (source C). | Indicative |
| Caoutchouc | Thaïlande, Indonésie | Deux premiers producteurs mondiaux ; prix intérieurs en base sèche (cup lump 100 % DRC, KKK 100 %). Décalage de période. | Indicative |
| Palmier à huile | Indonésie (Riau), Malaisie | Deux premiers producteurs mondiaux ; prix de référence des régimes. Stade (livraison usine) et taux d'extraction différents. | Indicative |
| Riz | Sénégal | Pays UEMOA, prix du paddy fixé par l'interprofession. | Directe |
| | Vietnam | Grand exportateur ; paddy frais (humide) contre paddy sec. | Indicative |
| | Parité FOB | Riz thaï 5 % brisures FOB Bangkok ramené en équivalent paddy. | Référence internationale |
| Banane, mangue | Équateur (prix minimum à l'exportation), Burkina Faso (plancher mangue) | Illustratif : aucun prix ivoirien comparable au même stade. | Non comparable |

Indicateur de position (III) : médiane des **comparateurs directs** de la même période. Les comparaisons indicatives sont montrées (points vides du graphique 2) mais n'entrent pas dans la médiane : Nigeria pour le cacao, Tanzanie pour l'anacarde, Sénégal pour le coton, Vietnam pour le riz. Seules exceptions, le caoutchouc et le palmier, qui n'ont aucun comparateur direct : la médiane porte alors sur les comparateurs indicatifs, et le résultat est lui-même indicatif (colonne D « Statut du benchmark » de l'onglet `Indicateurs`). La médiane a été préférée à la moyenne car elle n'est pas tirée par un comparateur atypique (l'échantillon compte 1 à 4 pays). La liste des comparateurs retenus figure en colonne M de l'onglet `Indicateurs`.

Effet de cette règle sur l'anacarde : face à ses voisins directs (Burkina, Guinée-Bissau, Ghana), le prix ivoirien est à l'indice 98 ; l'inclusion de la Tanzanie (comparaison indicative) l'aurait abaissé à 79. La note retient donc « au niveau de l'UEMOA, 34 % sous le Ghana ».

## 5. Règle de comparabilité et équivalences

Chaque prix est décrit par une fiche logique complète avant toute comparaison :

> Produit → qualité → stade de commercialisation → campagne / période → pays → monnaie → unité → source

Dans la base, ces éléments occupent les colonnes B à P de l'onglet `Observations`. Une comparaison n'est faite que lorsque produit, stade et période sont alignés ; sinon elle est qualifiée d'indicative ou écartée.

Interdits appliqués : jamais de prix bord champ comparé à un prix FOB ou à un prix de détail ; jamais de campagnes différentes mélangées ; jamais un prix de qualité premium comparé à un prix de qualité standard sans le signaler ; jamais un prix converti au taux de change d'une autre période ; jamais un prix extrapolé sans le signaler.

Équivalences techniques (paramètres modifiables dans l'onglet `Parametres`) :

| Filière | Problème | Traitement | Paramètre |
|---|---|---|---|
| Coton | Prix du coton graine contre cours de la fibre | Équivalent fibre = prix du coton graine ÷ rendement à l'égrenage | 45,2 % (calculé : 730 000 balles de 480 lb de fibre, USDA, ÷ 351 764 t de coton graine 2024/25) |
| Caoutchouc | Coagulum humide contre caoutchouc sec (TSR20) | Prix base sèche = prix bord champ ÷ DRC de référence ; sensibilité au DRC mesuré | DRC 60 % (convention officielle) ; DRC mesuré 65-68 % (test à 66 %) |
| Riz | Paddy contre riz blanchi | Équivalent paddy = prix du riz blanchi × taux d'usinage | 65 % (hypothèse technique usuelle, à valider avec l'ADERIZ) |
| Palmier | Régime contre huile brute | Pas d'équivalence (taux d'extraction différents) : ratio prix du régime ÷ prix de l'huile, calculé de la même façon pour tous les pays | — |
| Anacarde | Rendement en amande (KOR) différent selon l'origine | Pas de correction : écart signalé (Ghana KOR 46 spécifié ; Tanzanie KOR élevé, comparaison indicative) | — |
| Café | Grades différents | Café vert courant (FAQ) comparé au café vert ivoirien « bien séché, décortiqué, trié » | — |
| Toutes | Unités | Conversion en kg : sac de 64 kg, tonne, quintal de 100 lb (45,36 kg), caisse de 43 lb, livre (0,4536 kg) | Colonne M de `Observations` |

## 6. Période d'étude et appariement dans le temps

Période : dix campagnes, de 2016/17 à 2025/26, plus les prix d'ouverture 2026/27 lorsqu'ils sont connus. Pour chaque filière, la note privilégie le dernier niveau observé, puis la moyenne des trois dernières campagnes et la tendance longue (nominale et réelle).

| Filière | Période de comparaison | Référence internationale appariée |
|---|---|---|
| Cacao | Demi-campagnes : principale (octobre-mars) et intermédiaire (avril-septembre) | Moyenne ICCO des six mois de la demi-campagne ; ouverture 2026/27 : dernier mois publié (août 2026) |
| Café | Campagne octobre-septembre (avant 2021/22, ouverture en décembre : moyenne octobre-septembre retenue par homogénéité) | Moyenne robusta octobre-septembre ; 2025/26 : octobre 2025-août 2026 ; 2026/27 : août 2026 |
| Coton | Campagne de commercialisation de la fibre (août-juillet) | Moyenne de l'indice A ; 2025/26 : août 2025-janvier 2026 (dernier mois disponible) |
| Caoutchouc | Mois M (prix APROMAC) | TSR20 du mois M-1 (le prix ivoirien du mois est fixé sur le cours du mois précédent) |
| Anacarde | Campagne de commercialisation 2026 (ouverte en février) | Cotation CFR Asie avril-mai 2026 de la noix ivoirienne |
| Palmier | Janvier 2026 (Côte d'Ivoire, Indonésie) ; moyenne 2025 (Malaisie) | Huile brute CIF Rotterdam, même mois ou même année |
| Riz | Année 2025 | Moyenne 2025 du riz thaï 5 % FOB |

Les prix étrangers sans série publiée (Cameroun, Nigeria, Vietnam, Ouganda, Indonésie, Thaïlande) sont comparés **à date d'observation** au prix ivoirien en vigueur à cette date. La demi-campagne intermédiaire 2025/26 du cacao utilise la moyenne avril-août 2026 (septembre 2026 n'était pas publié au 1er octobre).

Évolution réelle (indicateur VII) : prix déflaté par l'indice des prix à la consommation de la Côte d'Ivoire (2015 = 100 ; inflation 2016-2025 : Banque mondiale d'après l'INS, BCEAO). L'indice 2026 n'étant pas publié, le niveau 2025 est conservé (signalé dans `Series_CI`).

## 7. Conversion des monnaies

Principe : chaque prix est converti au taux de change **moyen de la période exacte** qu'il couvre (une demi-campagne, une campagne, un mois), jamais au taux du jour de l'étude. Le prix d'origine, la monnaie, l'unité, le taux utilisé et la source du taux sont conservés sur chaque ligne de l'onglet `Observations` (colonnes J à Q).

| Monnaie | Source | Méthode |
|---|---|---|
| FCFA (XOF) et franc CFA d'Afrique centrale (XAF) | Parité fixe 655,957 FCFA = 1 EUR ; taux de référence quotidiens de la BCE (USD par EUR) | FCFA par USD = 655,957 ÷ (USD par EUR), moyenne mensuelle des taux quotidiens, puis moyenne des mois de la période |
| Roupie indonésienne, baht, ringgit | BCE (taux croisés via l'euro) | Monnaie par USD = (monnaie par EUR) ÷ (USD par EUR) |
| Cedi, shilling ougandais, dong, shilling tanzanien, naira | BRI, série WS_XRU (moyennes mensuelles, USD) | Moyenne des mois de la période ; compléments documentés ci-dessous |

Compléments lorsque la série BRI s'arrête avant la période étudiée (fiabilité indiquée dans `Change_mensuel`, colonne Q) :

| Monnaie | Mois | Source | Fiabilité |
|---|---|---|---|
| GHS | janvier-août 2026 | Banque du Ghana, taux interbancaire moyen mensuel | A |
| GHS | septembre 2026 | Banque du Ghana, moyenne des cotations des 18 et 28 septembre 2026 | B |
| GHS | novembre-décembre 2025 | FMI, moyenne des taux de fin de mois (approximation) | C |
| UGX | juillet 2026 | Moyenne mensuelle publiée par un site de change (poundsterlinglive.com) | C |
| VND | septembre 2026 | Vietcombank, milieu achat/vente du 9 septembre 2026 | B |
| TZS | novembre 2025 | UBA Tanzania, cours d'ouverture des 5, 18 et 20 novembre 2025 | C |
| NGN | septembre 2026 | Taux implicite de la source du prix (5 728,5 NGN/kg = 4 311 USD/t) | C |

Le fichier BCE archivé s'arrête au 14 septembre 2026 : la moyenne de septembre 2026 porte sur les jours ouvrés du 1er au 14 septembre (signalé dans `Change_mensuel`). L'effet est négligeable : la parité euro-dollar a peu varié sur le mois.

## 8. Prix internationaux de référence

| Filière | Série | Stade | Source (jusqu'en janvier 2026, puis compléments) | Conversion |
|---|---|---|---|---|
| Cacao | Prix ICCO (moyenne des bourses de Londres et New York) | Bourse | Banque mondiale, Pink Sheet ; FMI (série PCOCOUSDM) de février à juillet 2026 ; août 2026 : FocusEconomics d'après le FMI (fiabilité B) | USD/kg |
| Café | Robusta (indicateur OIC) | Ex-dock New York / Le Havre-Marseille | Banque mondiale ; FMI (PCOFFROBUSDM) et OIC (Coffee Market Report) en 2026 | c/lb × 0,0220462 = USD/kg |
| Coton | Indice A (Middling 1-1/8") | CFR Extrême-Orient | Banque mondiale (jusqu'en janvier 2026) | USD/kg, comparé à l'équivalent fibre |
| Caoutchouc | TSR20 (SICOM) | FOB | Banque mondiale ; SGX, rapport mensuel SICOM (mars 2026) | USD/kg, comparé au prix base sèche |
| Palmier | Huile de palme brute | CIF Rotterdam | Banque mondiale | USD/t |
| Riz | Thaï 5 % brisures | FOB Bangkok | Banque mondiale | USD/t × 65 % = équivalent paddy |
| Anacarde | Noix brute ivoirienne (KOR 46-48) | CFR Vietnam/Inde | Cotation de négoce (pas de bourse ; fiabilité C) ; recoupement : valeur unitaire des importations vietnamiennes janvier-avril 2026 | USD/t |

Le Pink Sheet de la Banque mondiale archivé est la version mise à jour le 3 février 2026 (données jusqu'en janvier 2026). Les mois suivants proviennent des sources indiquées en commentaire de cellule dans `Cours_mensuels`. Des valeurs de 2026 attribuées au Pink Sheet par des résumés de moteurs de recherche ont été écartées lorsqu'elles étaient incohérentes avec les séries du FMI et de l'OIC (cacao, mai 2026) ou contradictoires entre elles (TSR20, juillet-août 2026).

## 9. Indicateurs I à VIII : définitions et formules

| N° | Indicateur | Formule | Emplacement |
|---|---|---|---|
| I | Écart absolu | Prix CI − prix comparateur (FCFA/kg, même base) | `Indicateurs`, col. G |
| II | Écart relatif | (Prix CI − prix comparateur) ÷ prix comparateur | `Indicateurs`, col. H ; indice = prix CI ÷ prix comparateur × 100 (col. I) |
| III | Position relative | Prix CI ÷ médiane des comparateurs directs × 100 (caoutchouc, palmier : comparateurs indicatifs, faute de direct) | `Indicateurs`, bloc III |
| IV | Taux de transmission | Prix bord champ ÷ prix international de la même période, même méthode pour tous les pays | `Observations`, col. Y ; `Indicateurs`, col. J-K |
| V | Part du producteur dans la valeur FOB/CAF | Prix bord champ ÷ valeur FOB ou CAF nationale (Ghana : 71 % du FOB réalisé ; Côte d'Ivoire : CAF implicite = prix ÷ 60 %) | `Observations`, col. AB ; `Decomposition` |
| VI | Volatilité | Coefficient de variation = écart-type ÷ moyenne, sur 2016-2025 (campagnes) ou sur les demi-campagnes du cacao ; transmission moyenne sur dix ans | `Series_CI`, `Cacao_transmission`, `Indicateurs` bloc VI |
| VII | Évolution réelle | Prix ÷ IPC (2015 = 100) × IPC 2025, variation entre la première et la dernière campagne | `Series_CI` |
| VIII | Décomposition de la valeur | Cacao : CAF = producteur + DUS (14,6 %) + autres prélèvements + coûts et marges (résidu) ; anacarde : bord champ → magasin portuaire (barème) → DUS 5 % → CFR (résidu) ; caoutchouc et palmier : parts et ratios ; coton : subvention ÷ production | `Decomposition` |

Indicateur complémentaire : **revenu brut à l'hectare** = rendement moyen (kg/ha) × prix bord champ (`Volumes_Rendements`). Il montre qu'un prix au kilo plus bas peut donner un revenu à l'hectare plus élevé (coton béninois) et inversement (cacao ivoirien face au Ghana).

Les résidus de décomposition (coûts de commercialisation, fret, marges) ne sont pas observés directement : ils sont calculés par différence et présentés comme tels.

## 10. Matrice de synthèse et graphiques

La matrice (onglet `Matrice`, page 2 de la note) suit la structure demandée : filière, prix CI, benchmark, écart, part producteur, tendance, facteur explicatif, diagnostic. Elle ne classe pas les filières : les diagnostics sont qualitatifs et chaque chiffre renvoie par formule à l'onglet `Indicateurs`.

Les six graphiques sont produits par `scripts/make_charts.py`, qui ne lit que les valeurs recalculées de la base (fichier `scripts/chart_data.json` pour la trace) :

| Graphique | Données | Onglet source |
|---|---|---|
| 1. Positionnement (bulles) | X : indice de rémunération ; Y : taux de transmission ; taille : valeur brute au producteur (production × prix) | `Positionnement`, `Volumes_Rendements` |
| 2. Prix CI en % de chaque comparateur | Indices deux à deux ; points pleins = directs, vides = indicatifs ; trait = médiane | `Indicateurs` |
| 3. Part du prix international reçue | Transmission CI et médiane des comparateurs | `Indicateurs`, `Decomposition` |
| 4. Cacao : série par demi-campagne | Prix CI, prix Ghana, cours ICCO (FCFA/kg) | `Cacao_transmission` |
| 5. Décomposition (barres 100 %) | Partage du CAF (cacao) et du CFR (anacarde) | `Decomposition` |
| 6. Riz paddy | Prix CI, Sénégal, Vietnam, équivalent paddy du riz thaï FOB | `Observations` |

## 11. Audit de cohérence

Chaque comparaison a été contrôlée sur dix critères : période, produit, qualité, stade, unité, monnaie, référence internationale, source primaire, politique publique, fiscalité (onglet `Audit_QC`). Synthèse :

| Comparaison | Points non satisfaits ou partiels | Verdict |
|---|---|---|
| Cacao CI / Ghana (2016/17-2026/27) | Sources primaires relayées par la presse ; fiscalité ghanéenne non documentée | Directe |
| Cacao CI / Cameroun, Nigeria, Équateur | Relevés ponctuels ; qualité différente (Équateur) ; sources secondaires | Indicative |
| Café CI / Vietnam, Ouganda | Taux de change UGX de fiabilité C ; périodes proches (juillet-septembre 2026) | Directe (Vietnam), directe avec prudence (Ouganda) |
| Anacarde CI / UEMOA, Ghana | Référence internationale = cotation de négoce ; planchers pas toujours respectés | Directe |
| Anacarde CI / Tanzanie | Saison, qualité (KOR) et stade (magasin primaire) différents ; change approximatif | Indicative |
| Coton CI / UEMOA | Sources secondaires pour certains pays ; subvention ivoirienne de 25,3 Mds FCFA | Directe |
| Caoutchouc CI / Thaïlande, Indonésie | Périodes décalées ; conversion en base sèche (DRC 60 %) ; TSR20 2026 incomplet | Indicative |
| Palmier CI / Indonésie, Malaisie | Stade (bord champ / usine) et taux d'extraction différents ; taxes à l'exportation indonésiennes non retraitées | Indicative |
| Riz CI / Sénégal, Vietnam, parité FOB | Paddy frais au Vietnam ; parité FOB hors fret et droits ; subvention sénégalaise de 30 FCFA/kg | Directe (Sénégal), indicative (Vietnam) |
| Banane, mangue, ananas, vivriers | Pas de prix producteur public au même stade | Données insuffisantes |

Contrôles techniques : 4 213 formules recalculées sans erreur ; chaque chiffre de la note est lu dans la base (fichier `scripts/note_values.json`) ; chaque graphique est produit à partir des seules valeurs de la base.

## 12. Difficultés rencontrées

1. **Accès réseau restreint.** L'environnement d'étude n'autorisait pas le téléchargement direct depuis FAOSTAT, UN Comtrade, Eurostat, les API de la Banque mondiale et de la BCE, ni la consultation directe des sites institutionnels (ICCO, gouv.ci notamment). Les données ont été obtenues par d'autres voies, documentées ligne par ligne :
   - Pink Sheet de la Banque mondiale (fichier original du 3 février 2026), séries BRI et FMI : copies publiques sur GitHub (dépôt `unbalancedparentheses/forex-centuries`, commit `f79a85b` du 26 février 2026) ; le fichier de la Banque mondiale est identique octet pour octet à celui archivé dans `SOURCES/donnees_primaires/`.
   - Taux quotidiens de la BCE : fichier `eurofxref-hist` distribué avec le paquet Python `currencyconverter` 0.18.22 (données jusqu'au 14 septembre 2026).
   - Prix officiels et cours de 2026 : pages de presse et d'institutions identifiées par recherche, citées avec leur URL.
2. **Prix officiels relayés par la presse.** Beaucoup d'annonces officielles (CCC, COCOBOD, gouvernements) ne sont accessibles que par des articles de presse ou d'agence qui les reprennent (fiabilité B). Les montants ont été recoupés lorsque plusieurs sources étaient disponibles.
3. **Séries étrangères incomplètes.** Les prix bord champ de nombreux pays ne sont pas publiés en séries : comparaisons à date d'observation, qualifiées d'indicatives quand les dates diffèrent.
4. **Fin des séries de la Banque mondiale en janvier 2026.** Les cours de 2026 proviennent du FMI, de l'OIC et du SGX ; aucun TSR20 vérifié n'a été trouvé pour 2026 au-delà de mars ; l'indice A du coton n'est pas complété après janvier 2026.
5. **Données non vérifiables écartées.** Des chiffres de résumés automatiques non confirmés par une source primaire ont été rejetés (exemples : valeurs du Pink Sheet de mai 2026 incohérentes avec le FMI ; un FOB ghanéen « de 2 650 USD/t » qui confondait prix au sac et prix à la tonne). Les prix à la consommation de l'OCPV n'ont pas été repris faute de bulletin consultable.
6. **Conventions de mesure contestées.** Le DRC du caoutchouc (60 % conventionnel contre 65-68 % mesuré selon des analyses indépendantes) et le rendement à l'égrenage du coton (calculé, non publié) ont été traités comme des paramètres modifiables, avec un test de sensibilité pour le DRC.

## 13. Limites des données

- **Fiabilité.** 26 sources de niveau A, 94 de niveau B, 7 de niveau C ; 72 observations A, 100 B, 5 C. Les observations C (cacao au Nigeria, coton au Togo et au Sénégal, coton burkinabè 2026/27, cotation CFR de l'anacarde) et les taux de change C (UGX, TZS, NGN, GHS de fin 2025) sont signalés dans la base ; aucune conclusion de la note ne repose sur une seule donnée C, sauf la transmission et la décomposition de l'anacarde, fondées sur la cotation CFR de la noix ivoirienne (1 560 USD/t), seule référence internationale disponible pour la noix brute ; elle est cohérente avec la valeur unitaire des importations vietnamiennes toutes origines (≈1 690 USD/t, janvier-avril 2026).
- **Prix administrés et prix effectifs.** Les prix ivoiriens sont des prix officiels minimums ou planchers. Les prix réellement payés peuvent être inférieurs (non-respect signalé pour le caoutchouc, la noix de cajou et le cacao en 2025/26) ou supérieurs (anacarde : 416 FCFA/kg payés en moyenne à Niakara contre un plancher de 400).
- **Qualité.** Les différences de qualité ne sont jamais corrigées par un coefficient arbitraire : elles sont signalées (KOR de l'anacarde, qualités de cacao équatoriennes, paddy frais vietnamien, taux d'extraction du palmier).
- **Décomposition.** Les coûts de commercialisation, de fret et les marges sont obtenus par différence ; la fiscalité des pays comparateurs n'est pas documentée.
- **Rendements.** Les rendements du cacao proviennent de la littérature (500 kg/ha en Côte d'Ivoire, 400 au Ghana) ; ceux du coton de données de campagne 2024/25. Le revenu à l'hectare est un ordre de grandeur.
- **Volumes.** La taille des bulles du graphique 1 combine des années différentes (prévision 2025/26 pour le cacao, production 2023 pour le caoutchouc, base humide supposée) : elle situe l'ordre de grandeur, pas une valeur exacte.
- **Fruits et vivriers.** Aucune conclusion sur la compétitivité-prix n'est possible sans un dispositif de collecte de prix au producteur.

## 14. Reproduire et mettre à jour

Toutes les données saisies sont dans `scripts/inputs.py` (prix, taux de change complémentaires, cours 2026, inflation, volumes, rendements, paramètres, sources). Les fichiers primaires sont dans `SOURCES/donnees_primaires/`.

```bash
bash scripts/run_all.sh
```

| Étape | Script | Résultat |
|---|---|---|
| 1 | `scripts/build_base.py` | `Base_Prix_Benchmark_CI.xlsx` (formules, sans valeurs) |
| 2 | `scripts/recalc_lo.py` | Recalcul par LibreOffice et contrôle : arrêt si une formule renvoie une erreur |
| 3 | `scripts/make_charts.py` | `figures/` (SVG et PNG), `scripts/chart_data.json` |
| 4 | `scripts/make_note.py` | `Note_Benchmark_Prix_Agricoles_CI.pdf`, `scripts/note_content.json`, `scripts/note_values.json` |
| 5 | `scripts/make_docx.js` | `Note_Benchmark_Prix_Agricoles_CI.docx` |
| 6 | `scripts/export_csv.py` | `Base_Prix_Benchmark_CI_observations.csv`, `SOURCES/Liste_sources.csv`, tableau de la section 15 |

Prérequis : Python 3 (pandas, openpyxl, matplotlib, playwright avec Chromium), LibreOffice avec le pont Python `uno`, Node.js avec le paquet `docx`. Police : Inter convertie en TrueType (« Inter TT ») ; à défaut, Liberation Sans ou Arial (vérifier alors que la note tient en cinq pages : `make_note.py` affiche la marge libre de chaque page).

Pour mettre à jour un prix : modifier ou ajouter l'observation dans `scripts/inputs.py` (avec sa source), relancer la chaîne, relire la note. Pour changer une hypothèse (DRC, taux d'usinage, rendement à l'égrenage) : modifier l'onglet `Parametres` du classeur (tous les calculs suivent) ou la valeur correspondante dans `inputs.py`.

## 15. Liste des sources

<!-- SOURCES:DEBUT -->
127 sources (fiabilité A : 26 ; B : 94 ; C : 7), toutes consultées le 1er octobre 2026 (date indiquée pour chaque ligne de la base). Version tableur : `SOURCES/Liste_sources.csv` (avec le nombre d'observations qui citent chaque source).

| Clé | Institution | Titre / contenu utilisé | Fiab. | Utilisation | Lien |
|---|---|---|---|---|---|
| `BCE_FX` | Banque centrale européenne | Taux de référence quotidiens (eurofxref-hist), parité fixe 655,957 FCFA/EUR | A | Change_mensuel, Change_periodes (taux BCE : EUR donc FCFA ; IDR, THB, MYR) | [lien](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) |
| `BF_ANA_2026` | Gouvernement du Burkina Faso (via Sika Finance) | Prix bord champ de la noix de cajou maintenu à 385 FCFA/kg (2026) | B | 1 obs. | [lien](https://www.sikafinance.com/marches/burkina-le-prix-bord-champ-de-la-noix-de-cajou-maintenu-a-385-fcfakg-pour-soutenir-la-transformation-locale_60008) |
| `BF_COT_2526` | SOFITEX (Burkina Faso) | Campagne 2025-2026 : engrais 17 500 FCFA, kg de coton 325 FCFA | A | 1 obs. | [lien](https://www.sofitex.bf/2025/04/10/campagne-cotonniere-2025-2026-les-engrais-a-17-500-f-cfa-les-insecticides-a-5-200-f-cfa-et-le-kg-de-coton-a-325-f-cfa/) |
| `BF_COT_PROD` | Agence Ecofin | Burkina Faso : production 2024/2025 (300 000 t ; 865 kg/ha) | B | Volumes_Rendements | [lien](https://www.agenceecofin.com/actualites-agro/2002-126013-au-burkina-faso-la-production-cotonniere-2024/2025-s-annonce-plus-faible-que-prevu) |
| `BF_MAN_2026` | Gouvernement du Burkina Faso (via leFaso.net) | Campagne fruitière 2026 : anacarde 385 FCFA, mangue 95 FCFA le kg | B | 1 obs. | [lien](https://lefaso.net/spip.php?article144610) |
| `BJ_COT_2526` | Gouvernement du Bénin (via La Nation) | Campagne cotonnière 2025-2026 : prix des insecticides et du coton graine homologués (300 FCFA) | B | 1 obs. | [lien](https://lanation.bj/actualites/campagne-cotonniere-2025-2026-les-prix-des-insecticides-et-du-coton-graine-homologues) |
| `BJ_COT_2627` | Gouvernement du Bénin (via Le Matinal) | Campagne 2026-2027 : coton conventionnel 300 FCFA (1er choix), biologique 360 FCFA (CM du 13/05/2026) | B | 1 obs. | [lien](https://lematinal.bj/campagne-cotonniere-2026-2027-le-prix-de-cession-des-intrants-et-dachat-de-coton-graine-homologue/) |
| `BM_CACAO_2019` | Banque mondiale | Situation économique en Côte d'Ivoire : au pays du cacao (2019) – part producteur ≥60 % CAF, prélèvements ≈22 % CAF | A | Decomposition (règle de partage du CAF, prélèvements ≈22 %, marges privées) | [lien](https://documents1.worldbank.org/curated/en/277191561741906355/pdf/Cote-dIvoire-Economic-Update.pdf) |
| `BM_PINK` | Banque mondiale | Commodity Price Data (Pink Sheet), CMO-Historical-Data-Monthly.xlsx, mise à jour 3 février 2026 | A | 49 obs. | [lien](https://www.worldbank.org/en/research/commodity-markets) |
| `BOG_FX` | Banque du Ghana | Taux interbancaires moyens mensuels 2026 | A | Change_mensuel | [lien](https://www.bog.gov.gh/economic-data/exchange-rate/) |
| `BRI_FX` | Banque des règlements internationaux | US dollar exchange rates (WS_XRU), moyennes mensuelles | A | Change_mensuel, Change_periodes (GHS, UGX, VND, TZS, NGN) | [lien](https://data.bis.org/topics/XRU) |
| `CI_ANA_2016` | Gouvernement (via Abidjan.net) | Anacarde : le prix du kilogramme fixé à 350 FCFA (2016) | B | 1 obs. | [lien](https://news.abidjan.net/articles/582020/anacarde-le-prix-du-kilogramme-fixe-a-350-fcfa-par-le-gouvernement-ivoirien) |
| `CI_ANA_2017` | CCA (via allAfrica) | Campagne cajou 2017 : mesures arrêtées par le Conseil du coton et de l'anacarde (440 FCFA) | B | 1 obs. | [lien](https://fr.allafrica.com/stories/201702210313.html) |
| `CI_ANA_2018` | CCA (via Financial Afrik) | La campagne de commercialisation des noix de cajou s'annonce sous de bons auspices en 2018 (500 FCFA) | B | 1 obs. | [lien](https://www.financialafrik.com/2018/02/17/cote-divoire-la-campagne-de-commercialisation-des-noix-de-cajou-sannonce-sous-de-bons-auspices-en-2018) |
| `CI_ANA_2019` | Gouvernement (via Fraternité Matin) | Noix de cajou : le prix fixé à 375 FCFA/kg pour la campagne 2019 | B | 1 obs. | [lien](https://www.fratmat.info/article/87617/62/noix-de-cajou-le-prix-fixe-a-375-f-cfa-kg-pour-la-campagne-2019) |
| `CI_ANA_2020` | Gouvernement (via Fraternité Matin) | Anacarde : le prix bord champ fixé à 400 FCFA le kg (2020) | B | 1 obs. | [lien](https://www.fratmat.info/article/201657/economie/anacarde-le-prix-bord-champ-fixe-a-400-fcfa-le-kg) |
| `CI_ANA_2023` | Gouvernement (via Abidjan.net) | Le prix de la noix de cajou fixé à 315 FCFA/kg (2023) | B | 1 obs. | [lien](https://news.abidjan.net/articles/717534/cote-divoire-le-prix-de-la-noix-de-cajou-fixe-a-315-f-cfa-kg-officiel) |
| `CI_ANA_2024` | MINADERPV (via AIP) | Le prix bord champ du kg de l'anacarde fixé à 275 FCFA (campagne 2024) | B | 1 obs. | [lien](https://www.aip.ci/33996/cote-divoire-aip-le-prix-bord-champ-du-kg-de-lanacarde-fixe-a-275-fcfa-pour-la-campagne-2023-2024/) |
| `CI_ANA_2025` | MINADERPV (via KOACI) | Anacarde : prix bord-champ fixé à 425 FCFA (+54 %), campagne 2025 | B | 1 obs. | [lien](https://www.koaci.com/article/2025/01/17/cote-divoire/societe/cote-divoire-anacarde-le-prix-bord-champ-du-kg-fixe-a-425-fcfa-soit-une-hausse-de-54-par-rapport-a-la-campagne-precedente_183836.html) |
| `CI_ANA_2026` | MINADERPV (via Agence Ecofin) | Baisse de 6 % du prix minimum bord champ de la noix de cajou en 2026 (400 FCFA) | B | 1 obs. | [lien](https://www.agenceecofin.com/actualites-agro/0902-135589-cote-d-ivoire-baisse-de-6-du-prix-minimum-bord-champ-de-la-noix-de-cajou-en-2026) |
| `CI_ANA_2122` | CCA (via Abidjan.net) | Démarrage de la campagne 2022 de commercialisation de la noix de cajou (prix plancher 305 FCFA, inchangé depuis 2021) | B | 2 obs. | [lien](https://news.abidjan.net/articles/703951/demarrage-ce-vendredi-de-la-campagne-2022-de-la-commercialisation-de-la-noix-de-cajou-communique) |
| `CI_ANA_BAREME` | Gouvernement / CCAK (via Abidjan.net) | Prix planchers 2026 : bord champ 400, magasin intérieur 425, magasin usine 454, magasin portuaire 484 FCFA/kg | B | 1 obs. | [lien](https://news.abidjan.net/articles/747086/commercialisation-de-lanacarde-le-gouvernement-fixe-les-prix-planchers-pour-la-campagne-2026) |
| `CI_ANA_DUS` | AIP | Le droit unique de sortie de la noix de cajou brute désormais fixé à 5 % (20/11/2024) | B | Decomposition (DUS de la noix brute : 5 %) | [lien](https://www.aip.ci/127213/cote-divoire-aip-le-droit-unique-de-sortie-de-la-noix-de-cajou-brute-desormais-fixe-a-5/) |
| `CI_ANA_EXP` | Fraternité Matin (via allAfrica) | Filière cajou : >860 000 t de noix brutes exportées en 2025 ; exportations d'amandes ≈350 Mds FCFA | B | Contexte anacarde (exportations 2025), consulté pour l'analyse | [lien](https://fr.allafrica.com/stories/202601200594.html) |
| `CI_ANA_PROD` | MINADERPV (via AIP) | Production historique de 1 549 221 t de noix de cajou en 2025 | B | Volumes_Rendements | [lien](https://www.aip.ci/316955/aip-la-cote-divoire-atteint-une-production-historique-de-1-549-221-tonnes-de-noix-de-cajou-au-titre-de-la-campagne-2025/) |
| `CI_ANA_PROD26` | Cardassilaris (négociant) | Récolte RCN Côte d'Ivoire 2026 ≈1,46 Mt | C | Observations | [lien](https://www.cardassilaris.com/news/cashew-market-report-may-2026-rcn-quality-vietnam) |
| `CI_ANA_REAL` | AIP | Campagne anacarde 2026 : près de 15 Mds FCFA de revenus à Niakara (prix moyen 416 FCFA/kg) | B | 1 obs. | [lien](https://www.aip.ci/cote-divoire-aip-campagne-anacarde-2026-pres-de-15-milliards-fcfa-de-revenus-engranges-par-les-producteurs-du-departement-de-niakara/) |
| `CI_ANA_TRANSFO` | Agence Ecofin | Côte d'Ivoire : achat de noix réservé aux transformateurs locaux du 9 février au 16 mars 2026 (Le Patriote) | B | Contexte anacarde (achats réservés aux transformateurs locaux), consulté pour l'analyse | [lien](https://lepatriote.ci/filiere-anacarde-lachat-des-noix-de-cajou-exclusivement-reserve-aux-transformateurs-locaux-du-9-fevrier-au-16-mars-2026-au-titre-de-la-campagne-2026) |
| `CI_ANN_EXP` | Xinhua | Exportations d'ananas : 23 557 t en 2023 (-27 %) | B | Note p. 4 (exportations d'ananas 2023) | [lien](https://english.news.cn/africa/20240128/f58bff004ef74e1da7107042c6132b2c/c.html) |
| `CI_BAN_EXP` | Agence Ecofin | Exportations ivoiriennes de bananes : 271 000 t en 2025 (+7 %) | B | Note p. 4 (exportations de bananes 2025) | [lien](https://www.ecofinagency.com/news-agriculture/0402-52550-african-banana-exports-rise-5-as-ghana-takes-lead) |
| `CI_CAC_1617I` | CCC (via Connectionivoirienne) | Prix bord champ du cacao pour la campagne intermédiaire fixé à 700 FCFA | B | 1 obs. | [lien](https://connectionivoirienne.net/2017/03/30/cote-divoire-le-prix-bord-champ-du-cacao-pour-la-campagne-intermediaire-fixe-a-700-fcfa-1-euro/) |
| `CI_CAC_1617P` | CCC / Gouvernement (via Connectionivoirienne) | Le kilo de cacao à 1 100 FCFA pour la campagne 2016-2017 | B | 1 obs. | [lien](https://connectionivoirienne.net/2016/09/28/cote-divoire-le-kilo-de-cacao-a-1-100-fcfa-pour-la-campagne-2016-2017) |
| `CI_CAC_1718` | CCC (via Connectionivoirienne) | Le prix d'achat au producteur de cacao maintenu à 700 FCFA (campagne intermédiaire 2017-2018) | B | 2 obs. | [lien](https://connectionivoirienne.net/2018/03/30/le-prix-dachat-au-producteur-de-cacao-en-cote-divoire-maintenu-a-700-francs-cfa) |
| `CI_CAC_1819I` | Gouvernement (via Afrique-sur7) | Le gouvernement maintient le prix du cacao à 750 FCFA pour la campagne intermédiaire | B | 1 obs. | [lien](https://www.afrique-sur7.fr/420663-prix-cacao-750-campagne-intermediaire) |
| `CI_CAC_1819P` | CCC (via Agence Ecofin) | Cocoa farm-gate price set to CFA750 per kilo for 2018/2019 season | B | 1 obs. | [lien](https://www.ecofinagency.com/agriculture/0210-39023-cote-d-ivoire-cocoa-farm-gate-price-set-to-cfa750-per-kilo-for-2018/2019-season) |
| `CI_CAC_1920I` | CCC (via Connectionivoirienne) | Le prix bord champ du cacao maintenu à 825 FCFA/kg pour la petite traite (le prix de marché aurait été de 625 FCFA) | B | 1 obs. | [lien](https://connectionivoirienne.net/2020/04/01/le-prix-bord-champ-du-cacao-maintenu-a-825-fcfa-kg-pour-la-petite-traite-en-cote-divoire/) |
| `CI_CAC_1920P` | CCC (via Connectionivoirienne) | Le prix du kg de cacao fixé à 825 FCFA pour la campagne 2019-2020 | B | 1 obs. | [lien](https://connectionivoirienne.net/2019/10/01/le-prix-du-kg-de-cacao-fixe-a-825-fcfa-en-cote-divoire-pour-la-campagne-2019-2020/) |
| `CI_CAC_2021I` | CCC (via KOACI) | Cacao : le Conseil fixe le kg de la fève à 750 FCFA pour la campagne intermédiaire | B | 1 obs. | [lien](https://www.koaci.com/index.php/article/2021/03/31/cote-divoire/politique/cote-divoire-cacao-le-conseil-fixe-le-kg-de-la-feve-a-750-fcfa-pour-la-campagne-intermediaire_149966.html) |
| `CI_CAC_2021P` | CCC (via BusinessWorld/Reuters) | Ivory Coast raises 2020/21 cocoa farmgate price by 21% (1 000 FCFA/kg) | B | 1 obs. | [lien](https://www.pressreader.com/philippines/business-world/20201005/281676847366265) |
| `CI_CAC_2122I` | CCC (via Abidjan.net) | Le prix du kg de cacao pour la campagne intermédiaire maintenu à 825 FCFA | B | 1 obs. | [lien](https://news.abidjan.net/articles/706140/cote-divoire-le-prix-du-kg-de-cacao-pour-la-campagne-intermediaire-maintenu-a-825-fcfa) |
| `CI_CAC_2122P` | CCC (via Connectionivoirienne) | Le prix bord-champ du café fixé à 700 FCFA/kg, le cacao à 825 FCFA | B | 2 obs. | [lien](https://connectionivoirienne.net/2021/10/01/le-prix-bord-champ-du-cafe-fixe-a-700-fcfa-kg/) |
| `CI_CAC_2223I` | CCC (via ConfectioneryNews) | Mid-crop 2022/23 farmgate price unchanged at 900 XOF/kg | B | 1 obs. | [lien](https://www.confectionerynews.com/Article/2023/05/03/cocoa-futures-up-6-as-farmgate-prices-stall-due-to-sluggish-exports-in-cote-d-ivoire/) |
| `CI_CAC_2223P` | CCC (via Further Africa/Reuters) | Ivory Coast raises cocoa farmgate price by 9% for 2022/2023 (900 FCFA/kg) | B | 1 obs. | [lien](https://furtherafrica.com/2022/10/03/ivory-coast-raises-cocoa-farmgate-price-by-9-for-2022-2023-harvest/) |
| `CI_CAC_2324I` | CCC (via FoodBev/Reuters) | Ivory Coast raises cocoa farmgate price by 50% (1 500 FCFA/kg, avril 2024) | B | 1 obs. | [lien](https://www.foodbev.com/news/ivory-coast-raises-cocoa-farmgate-price-by-50/) |
| `CI_CAC_2324P` | CCC (via Sika Finance) | Des prix d'achat de 1 000 FCFA/kg pour le cacao et 900 FCFA/kg pour le café | B | 1 obs. | [lien](https://www.sikafinance.com/marches/cote-divoire-des-prix-dachat-de-1-000-fcfakg-pour-le-cacao-et-900-fcfakg-pour-le-cafe_42852) |
| `CI_CAC_2425I` | CCC (via allAfrica/Fraternité Matin) | Le prix d'achat aux planteurs fixé à 2 200 FCFA, un nouveau record | B | 1 obs. | [lien](https://fr.allafrica.com/stories/202504030258.html) |
| `CI_CAC_2425P` | CCC (via Agence Ecofin) | Côte d'Ivoire : 1 800 FCFA le kg de cacao pour la campagne principale 2024/2025 | B | 1 obs. | [lien](https://www.agenceecofin.com/cacao/0110-122025-cote-d-ivoire-1800-fcfa-le-kg-de-cacao-pour-la-campagne-principale-2024/2025) |
| `CI_CAC_2526I` | MINADERPV / CCC (via KOACI) | Cacao : prix bord champ fixé à 1 200 FCFA/kg pour la campagne intermédiaire 2025-2026 | B | 1 obs. | [lien](https://www.koaci.com/article/2026/03/04/cote-divoire/societe/cote-divoire-cacao-le-prix-bord-champ-fixe-a-1-200-fcfakg-pour-la-campagne-intermediaire-2025-2026_194830.html) |
| `CI_CAC_2526P` | Présidence / CCC (via AIP) | Campagne 2025-2026 : prix bord champ du cacao 2 800 FCFA/kg et café 1 700 FCFA/kg | B | 2 obs. | [lien](https://www.aip.ci/257389/cote-divoire-aip-campagne-2025-2026-le-prix-bord-champ-du-cacao-fixe-a-2-800-fcfa-kg-et-celui-du-cafe-a-1-700-fcfa-kg-alassane-ouattara/) |
| `CI_CAC_2627P` | Gouvernement de Côte d'Ivoire (portail officiel) | Campagne principale 2026-2027 : cacao 1 200 FCFA/kg, café 1 300 FCFA/kg | A | 2 obs. | [lien](https://gouv.ci/actualite/campagne-principale-2026-2027-le-prix-bord-champ-du-cacao-est-fixe-a-1200-fcfa-le-kg-le-prix-du-cafe-setablit-a-1300-fcfa-le-kg-8771) |
| `CI_CAC_PROD` | CCC (via CNBC Africa/Reuters) | La Côte d'Ivoire anticipe 2,0-2,1 Mt de cacao en 2025/26 (+10,5 %) | B | Volumes_Rendements | [lien](https://www.cnbcafrica.com/2026/ivory-coast-expects-cocoa-output-to-rise-10-5-in-2025-26-season-regulator-says) |
| `CI_CAC_STOCKS` | 7info / allAfrica | 123 000 t invendues (janv. 2026), ~200 000 t fin février 2026 ; dispositif d'achat public | B | Note p. 3 et 5 (123 000 t invendues en 2025/26) | [lien](https://www.7info.ci/123-000-tonnes-invendues-etat-ivoirien-dispositif-achat-cacao/) |
| `CI_CAC_VENTES` | Reuters (via CNBC Africa) ; Agence Ecofin | Prix 2026/27 fondé sur >1,1 Mt de ventes anticipées mars-juin 2026 ; règle ≥60 % CAF (≥50 % en baisse) | B | Note p. 3 et 4 ; Matrice ; Cacao_transmission (ventes anticipées mars-juin 2026) | [lien](https://www.cnbcafrica.com/2026/ivory-coast-sets-cocoa-farmgate-price-at-1200-cfa-francs-per-kg-for-2026-27-main-crop-official-says) |
| `CI_CAF_1718` | CCC (via Connectionivoirienne) | Le prix du kg de café reste inchangé à 750 FCFA pour la campagne 2017-2018 | B | 2 obs. | [lien](https://connectionivoirienne.net/2017/12/21/cote-divoire-le-prix-du-kg-de-cafe-reste-inchange-a-750-fcfa-pour-la-campagne-2017-2018/) |
| `CI_CAF_1819` | CCC (via Abidjan.net) | Prix du café 2018-2019 : 700 FCFA/kg (baisse de 50 FCFA) | B | 1 obs. | [lien](https://news.abidjan.net/h/649843.html) |
| `CI_CAF_1920` | CCC (via Connectionivoirienne) | Café 2019-2020 fixé à 700 FCFA ; maintien permis par une subvention de 32 Mds FCFA (prix de marché : 473 FCFA) | B | 1 obs. | [lien](https://connectionivoirienne.net/2019/12/26/le-prix-du-kg-de-cafe-fixe-a-700-fcfa-pour-la-campagne-2019-2020-en-cote-divoire/) |
| `CI_CAF_2021` | CCC (via KOACI) | Café : prix bord champ fixé à 550 FCFA/kg (campagne 2020-2021, 28/12/2020) | B | 1 obs. | [lien](https://www.koaci.com/article/2020/12/23/cote-divoire/economie/cote-divoire-cafe-debut-de-la-campagne-commerciale-le-28-decembre-le-prix-bord-champ-du-kilo-fixe-a-550-fcfa-soit-une-baisse-de-155-fcfa_147642.html) |
| `CI_CAF_2223` | CCC (via Abidjan.net) | Campagne 2022-2023 : cacao 900 FCFA, café 750 FCFA | B | 1 obs. | [lien](https://news.abidjan.net/articles/712879/campagne-2022-2023-le-prix-bord-champ-du-kilogramme-de-cacao-fixe-a-900-fcfa-et-celui-du-cafe-a-750-fcfa) |
| `CI_CAF_2324` | CCC (via Abidjan.net) | Campagne 2023-2024 : cacao 1 000 FCFA, café 900 FCFA | B | 1 obs. | [lien](https://news.abidjan.net/articles/724364/campagne-principale-de-commercialisation-2023-2024-cafe-cacao-le-prix-du-kg-de-cacao-fixe-a-1000-fcfa-et-celui-du-cafe-a-900-fcfa) |
| `CI_CAF_2425` | CCC (via Agence Ecofin) | Hausse de plus de 66 % du prix bord champ du café en 2024/2025 (1 500 FCFA) | B | 1 obs. | [lien](https://www.agenceecofin.com/breves-agro/0110-122027-cote-d-ivoire-hausse-de-plus-de-66-du-prix-bord-champ-du-cafe-en-2024/2025) |
| `CI_CAF_PROD` | AIP | Filière café-cacao : production de café 24 832 t d'octobre 2024 à juin 2025 (-69,7 %) | B | Volumes_Rendements | [lien](https://www.aip.ci/257515/cote-divoire-aip-la-filiere-cafe-cacao-moteur-de-croissance-economique-face-aux-defis-sociaux-et-environnementaux-feature/) |
| `CI_CAO_0125` | APROMAC (via Yessouan) | Prix caoutchouc Côte d'Ivoire : 442 FCFA/kg en janvier 2025 | B | 1 obs. | [lien](https://www.yessouan.ci/Prix-caoutchouc-Cote-d-Ivoire-442-FCFA-kg-en-janvier-2025_a1537.html) |
| `CI_CAO_0425` | APROMAC (via 7info) | Caoutchouc naturel : prix du kg pour le mois d'avril (438 FCFA) | B | 1 obs. | [lien](https://www.7info.ci/caoutchouc-naturel-voici-le-prix-du-kg-pour-le-mois-davril/) |
| `CI_CAO_0926` | APROMAC (via Business & Actuality) | Prix du caoutchouc : 484 FCFA/kg en septembre 2026 | B | 1 obs. | [lien](https://businessactuality.com/cote-divoire-prix-du-caoutchouc-484-fcfa-kg-en-septembre-2026/) |
| `CI_CAO_2026` | APROMAC (via 7info) | Caoutchouc : nouveaux prix du kg (janv. 352, fév. 368, avr. 401, mai 439, juil. 493 FCFA) | B | 5 obs. | [lien](https://www.7info.ci/caoutchouc-voici-le-nouveau-prix-du-kg/) |
| `CI_CAO_DRC` | Business & Actuality | Le prix du caoutchouc : bras de fer planteurs-usiniers ; DRC officiel 60 % contre 65-68 % mesuré | C | Parametres | [lien](https://businessactuality.com/le-prix-du-caoutchouc-en-cote-divoire-un-bras-de-fer-entre-planteurs-usiniers-et-regulateurs/) |
| `CI_CAO_MECA` | Agence Ecofin | Ce qui change pour les producteurs de caoutchouc naturel en 2026 : 66 % du prix de référence (63 % auparavant) | B | Decomposition (part producteur caoutchouc : 63 % puis 66 %) | [lien](https://www.agenceecofin.com/actualites-agro/2606-139636-cote-d-ivoire-ce-qui-change-pour-les-producteurs-de-caoutchouc-naturel-en-2026) |
| `CI_CAO_PROD` | Financial Afrik | Numéro trois mondial du caoutchouc (≈1,6 Mt en 2023) | C | Volumes_Rendements | [lien](https://www.financialafrik.com/2026/01/15/numero-trois-mondial-du-caoutchouc-la-cote-divoire-veut-capter-davantage-de-valeur/) |
| `CI_COT_1718` | Gouvernement (via KOACI) | Coton graine : 300 FCFA/kg (+35 FCFA par rapport à 265 FCFA en 2017-2018) | B | 1 obs. | [lien](https://www.koaci.com/index.php/article/2019/05/22/cote-divoire/economie/cote-divoire-le-prix-du-kilogramme-de-coton-graine-pour-la-campagne-2018-2019-fixe-a-300-fcfa-soit-une-hausse-de-35-fcfa_131167.html) |
| `CI_COT_1819` | Gouvernement (via Abidjan.net) | Le prix du coton graine de premier choix maintenu à 265 FCFA/kg (2018-2019) | B | 1 obs. | [lien](https://news.abidjan.net/h/638493.html) |
| `CI_COT_1920` | Gouvernement (via KOACI) | Le prix du coton graine reste inchangé pour la campagne 2019-2020 : 300 FCFA/kg | B | 1 obs. | [lien](https://www.koaci.com/article/2019/10/29/cote-divoire/economie/cote-divoire-le-prix-du-coton-de-graine-reste-inchange-pour-la-campagne-2019-2020-300-fcfakg_136257.html) |
| `CI_COT_2122` | Gouvernement (via allAfrica) | Campagne 2021-2022 du coton : le prix du kilo demeure à 300 F (inchangé depuis 2020-2021) | B | 2 obs. | [lien](https://fr.allafrica.com/stories/202110080394.html) |
| `CI_COT_2223` | Gouvernement (via Connectionivoirienne) | Coton campagne 2022/2023 : le prix du kilogramme fixé à 310 FCFA | B | 1 obs. | [lien](https://connectionivoirienne.net/2022/07/14/coton-camapagne-2022-2023-le-prix-du-kilogramme-fixe-a-310-fcfa/) |
| `CI_COT_2324` | Gouvernement (via Abidjan.net) | Coton graine 1er choix 310 FCFA, 2e choix 285 FCFA (2023-2024) | B | 1 obs. | [lien](https://news.abidjan.net/articles/720825/cote-divoire-le-prix-du-coton-graines-1er-choix-fixe-a-310-fcfa-et-a-285-f-cfa-le-kilo-du-2e-choix) |
| `CI_COT_2526` | MINADERPV (via KOACI) | Campagne 2025-2026 : coton 1er choix 310 FCFA/kg, 2e choix 285 FCFA/kg (31/07/2025) | B | 1 obs. | [lien](https://www.koaci.com/article/2025/07/31/cote-divoire/societe/cote-divoire-campagne-2025-2026-le-prix-du-coton-de-1er-choix-est-fixe-a-310-fcfakg-et-celui-de-2e-choix-a-285-fcfakg_189056.html) |
| `CI_COT_PROD` | Agence Ecofin | Croissance modeste de la production cotonnière 2024/2025 : 351 764 t, 984 kg/ha, 357 267 ha | B | Volumes_Rendements | [lien](https://www.agenceecofin.com/actualites-agro/1501-124919-cote-d-ivoire-croissance-modeste-de-la-production-cotonniere-en-2024/2025) |
| `CI_COT_SUB` | Agence Ecofin | La subvention à la filière coton a plus que doublé en 2025/2026 (25,3 Mds FCFA contre 11,9 Mds) | B | 1 obs. | [lien](https://www.agenceecofin.com/actualites-agro/0108-130586-cote-d-ivoire-la-subvention-a-la-filiere-coton-a-plus-que-double-en-2025/2026) |
| `CI_MAN_2026` | Inter-Mangue (via AIP) | Mangue 2026 : prix bord champ maintenu à 2 450 FCFA la caisse ; 220 FCFA/kg en station | B | 1 obs. | [lien](https://www.aip.ci/332817/cote-divoire-aip-filiere-mangue-le-prix-bord-champ-maintenu-a-2-450-fcfa-la-caisse-pour-la-campagne-2026/) |
| `CI_PAL_0126` | Conseil Hévéa-Palmier à huile-Coco (via Afrik Soir) | Prix de janvier 2026 : huile de palme brute 620 000 FCFA/t ; régimes bord champ 80 000 FCFA/t | B | 2 obs. | [lien](https://afriksoir.net/cote-divoire-le-conseil-hevea-palmier-a-huile-coco-fixe-les-prix-du-palmier-a-huile-pour-janvier-2026/) |
| `CI_PAL_Q424` | CHP-HC (via Abidjan Économie) | Huile de palme brute 600 000 FCFA/t ; régimes bord champ 75 000 FCFA/t (oct.-déc. 2024) | B | 1 obs. | [lien](https://www.abidjaneconomie.net/2024/10/19/cote-divoire-nouvelles-tarifications-pour-lhuile-de-palme-brut-et-regimes-de-palme-pour-octobre-a-decembre-2024/) |
| `CM_CAC_0426` | ONCC-SIF (via Invest-Time) | Cacao au Cameroun : 1 200-1 450 FCFA/kg dans les bassins (mars-avril 2026) | B | 1 obs. | [lien](https://invest-time.com/2026/05/07/cacao-cameroun-prix-campagne/) |
| `CM_CAC_0526` | ONCC-SIF (via Investir au Cameroun) | Le prix du kilogramme repasse au-dessus de 1 500 FCFA (1 550-1 650) | B | 1 obs. | [lien](https://www.investiraucameroun.com/agriculture/0705-23372-cacao-le-prix-du-kilogramme-repasse-au-dessus-de-1-500-fcfa-a-deux-mois-de-la-fin-de-campagne) |
| `CM_CAC_0626` | ONCC-SIF (via Investir au Cameroun) | Le prix aux producteurs atteint 2 250 FCFA (2 100-2 250 au 30/06/2026) | B | 1 obs. | [lien](https://www.investiraucameroun.com/agriculture/3006-23552-cacao-le-prix-aux-producteurs-atteint-2250-fcfa-son-plus-haut-niveau-depuis-le-debut-de-la-campagne-2025-2026) |
| `ECOFIN_GAP` | Agence Ecofin | Ghana-Côte d'Ivoire cocoa price gap widens sharply for 2026/27 (3,65 vs 2,07 USD/kg) | B | Recoupement de l'écart de prix Ghana / Côte d'Ivoire 2026/27 | [lien](https://www.ecofinagency.com/news-agriculture/2809-59281-ghana-cote-d-ivoire-cocoa-price-gap-widens-sharply-for-2026/27-season) |
| `EC_BAN_2026` | MAGP Équateur, Acuerdo Ministerial 107 (via Agraria.pe) | Prix minimum de soutien 2026 : 7,50 USD la caisse 22XU de 43 lb | B | 1 obs. | [lien](https://agraria.pe/noticias/ecuador-fija-en-us-7-50-el-precio-minimo-de-la-caja-de-banan-40795) |
| `EC_CAC_0126` | El Universo | Les producteurs reçoivent 180-190 USD/quintal (janv. 2026) | B | 1 obs. | [lien](https://www.eluniverso.com/noticias/economia/precio-cacao-ecuador-exportador-productor-nota/) |
| `EC_CAC_0226` | Al Día (Équateur) | Le cacao revient à 100 USD le quintal (80-85 USD dans les petits cantons), fév. 2026 | B | 1 obs. | [lien](https://www.aldia.com.ec/el-cacao-regresa-a-niveles-de-2023-100-el-quintal-y-en-cantones-pequenos-llega-a-80/) |
| `FMI_PCPS` | FMI | Primary Commodity Prices (via FRED : PCOCOUSDM, PCOFFROBUSDM) | A | 6 obs. ; Observations, Cours_mensuels | [lien](https://fred.stlouisfed.org/series/PCOCOUSDM) |
| `GH_ANA_2026` | Tree Crops Development Authority (TCDA, Ghana) | Government sets GHS 12.00/kg as minimum producer price for RCN (2025/2026) – benchmark FOB 1 400 USD/t, 11,0241 GH¢/USD | A | 2 obs. | [lien](https://tcda.gov.gh/government-sets-ghs-12-00-per-kilogram-as-minimum-producer-price-for-raw-cashew-nuts-2025-2026-season/) |
| `GH_CAC_1620` | COCOBOD (via The Cocoa Post) | Producer price of cocoa up 8.42% (GH¢475 → GH¢515/bag ; 7 600 → 8 240 GH¢/t) | B | 8 obs. | [lien](https://thecocoapost.com/producer-price-of-cocoa-up-8-42/) |
| `GH_CAC_2021` | COCOBOD | Cocoa producer price goes up 28% from GH¢515 to GH¢660 per bag (10 560 GH¢/t) | A | 2 obs. | [lien](https://cocobod.gh/news/cocoa-producer-price-goes-up-28-from-gh515-to-gh660-per-bag) |
| `GH_CAC_2122` | Gouvernement du Ghana (via B&FT) | Gov't maintains cocoa price at GH¢660 per bag (87,15 % du FOB) | B | 2 obs. | [lien](https://thebftonline.com/?p=97805) |
| `GH_CAC_2223` | COCOBOD | Press release – opening of 2022/23 main crop season (GH¢800/bag ; 12 800 GH¢/t) | A | 2 obs. | [lien](https://cocobod.gh/news/press-release-opening-of-202223-main-crop-season) |
| `GH_CAC_2324I` | COCOBOD (compte officiel X) | Producer price increased by 58.26% from GH¢20 928 to GH¢33 120 per tonne from 5 April 2024 | A | 1 obs. | [lien](https://x.com/ghcocobod/status/1776312981111873684) |
| `GH_CAC_2324P` | Gouvernement du Ghana (via Graphic Online) | Cocoa price up: bag from GH¢800 to GH¢1 308 (20 928 GH¢/t) | B | 1 obs. | [lien](https://www.graphic.com.gh/news/general-news/govt-increases-cocoa-price-bag-up-from-gh-800-to-gh-1-308-tome-now-gh-20-943-from-gh-12-800.html) |
| `GH_CAC_2425I` | Gouvernement du Ghana (via Graphic Online) | Cocoa price shoots to GH¢49 600 a tonne | B | 1 obs. | [lien](https://www.graphic.com.gh/news/general-news/ghana-news-cocoa-price-shoots-to-ghc49-600-a-tonne-its-3rd-price-adjustment-in-9-months.html) |
| `GH_CAC_2425P` | COCOBOD | Review of the producer price of cocoa for the 2024/2025 season (48 000 GH¢/t, 11 sept. 2024) | A | 1 obs. | [lien](https://cocobod.gh/news/review-of-the-producer-price-of-cocoa-for-the-20242025-cocoa-season-wednesday-11th-september-2024) |
| `GH_CAC_2526` | COCOBOD / Citi Newsroom | 51 660 GH¢/t (70 % FOB 7 200 USD à 10,25) → 58 000 GH¢/t (11,5 GH¢/USD) → 41 392 GH¢/t au 12/02/2026 (90 % FOB 4 200 USD) | B | 2 obs. | [lien](https://citinewsroom.com/2026/02/cocoa-producer-price-cut-to-gh%C2%A241392-per-tonne-from-gh%C2%A251660/) |
| `GH_CAC_2627` | COCOBOD (via MyJoyOnline) | Producer price GH¢42 400/t for 2026/27 (71,18 % du FOB brut réalisé ; Act 1182 : minimum 70 %) | B | 2 obs. | [lien](https://www.myjoyonline.com/cocobod-increases-cocoa-producer-price-to-gh%C2%A242400-for-2026-27-season/) |
| `GH_CAC_GAP` | CNBC Africa | Will Ghana's domestic market plug COCOBOD's $1.4bn funding gap? (2026) | B | Note p. 3 et 5 (déficit de financement du COCOBOD ≈1,4 Md $) | [lien](https://www.cnbcafrica.com/media/7790596098459/will-ghanas-domestic-market-plug-cocobods-14bn-funding-gap) |
| `GH_CAC_REFORM` | COCOBOD | Press release on cocoa sector reforms for financial viability and long-term sustainability | A | Contexte Ghana (réformes du COCOBOD), consulté pour l'analyse | [lien](https://cocobod.gh/news/press-release-on-cocoa-sector-reforms-for-financial-viability-and-long-term-sustainability) |
| `GW_ANA_2026` | Gouvernement de transition de Guinée-Bissau (via Xinhua) | Campagne 2026 : 410 FCFA/kg au producteur, 478 FCFA/kg à Bissau | B | 1 obs. | [lien](https://english.news.cn/20260311/508ae13acd8c44109ea651276bd01b86/c.html) |
| `ID_CAO` | Disperindag/Gapkindo Sumatra-Sud (via IDN Times) | Prix de référence KKK 100 % : 38 835 à 42 238 Rp/kg (août 2026) | B | 1 obs. | [lien](https://sumsel.idntimes.com/news/sumatra-selatan/harga-karet-sumsel-kembali-menguat-akhir-agustus-tembus-rp41-ribu-00-pbgds-3n14cx) |
| `ID_PAL_0126` | Disbun Riau (via HaiSawit / Media Center Riau) | Prix TBS (régimes) Riau, palmiers 10-20 ans : 3 496,91 / 3 430,63 / 3 449,84 Rp/kg (janv. 2026) | B | 1 obs. | [lien](https://haisawit.co.id/news/detail/resmi-naik-cek-daftar-harga-sawit-riau-periode-1420-januari-2026) |
| `INT_ANA_CI` | Cardassilaris (négociant) | Cashew market report May 2026 : RCN Côte d'Ivoire 1 560 USD/t (avr.-mai 2026) | C | 1 obs. | [lien](https://www.cardassilaris.com/news/cashew-market-report-may-2026-rcn-quality-vietnam) |
| `INT_ANA_VN` | Douanes vietnamiennes (via Viet Nam News) | Raw cashew nut imports Jan-Apr 2026 : ~1,3 Mt pour ~2,2 Mds USD (≈1 704 USD/t) | B | 1 obs. | [lien](https://vietnamnews.vn/economy/945883/raw-cashew-nut-imports-rocket-in-first-four-months.html) |
| `ML_ANA_2025` | Gouvernement du Mali (via Agence Ecofin) | Mali : la filière anacarde face au défi du respect du prix plancher (390 FCFA ; achats à 350-375) | B | 1 obs. | [lien](https://www.agenceecofin.com/actualites/0104-127164-mali-la-filiere-anacarde-face-au-defi-du-respect-du-prix-plancher) |
| `ML_COT_2526` | Gouvernement du Mali (via Mali 24) | Prix du kilo du coton graine maintenu à 300 FCFA | B | 1 obs. | [lien](https://mali24.info/mali-433-700-tonnes-de-coton-produites-le-prix-du-kilo-du-coton-graine-maintenu-a-300-f-cfa/) |
| `MY_PAL_2025` | Malaysian Palm Oil Board (MPOB) | Overview of the Malaysian Oil Palm Industry 2025 : prix des régimes à 1 % OER 47,39 RM ; OER 19,74 % | A | 1 obs. | [lien](https://bepi.mpob.gov.my/images/overview/Overview2025.pdf) |
| `NG_CAC_0926` | Mansa Markets | Nigeria farmgate 5 728,5 NGN/kg (≈4 311 USD/t), 25/09/2026 | C | 1 obs. ; Observations, Change_mensuel | [lien](https://www.mansamarkets.com/blog/cocoa-farmgate-price-vs-world-price) |
| `OCPV` | OCPV (Ministère du Commerce) | Prix à la consommation des produits vivriers (bulletins hebdomadaires 2025-2026) | A | Note p. 4 ; Matrice (prix à la consommation : stade non comparable) | [lien](https://www.ocpv-ci.com/) |
| `OIC_CMR` | Organisation internationale du café | Coffee Market Report (février et août 2026) | A | 1 obs. ; Observations, Cours_mensuels | [lien](https://www.ico.org/documents/cy2025-26/cmr-0826-e.pdf) |
| `OMC_TPR_2017` | OMC | Examen des politiques commerciales UEMOA – Annexe Côte d'Ivoire (WT/TPR/S/362) : DUS 14,6 % CAF ; prélèvements totaux 23,2 % (2016/17) | A | Decomposition (DUS 14,6 % du CAF ; prélèvements 2016/17) | [lien](https://www.wto.org/french/tratop_f/tpr_f/s362-03_f.pdf) |
| `RDT_CACAO` | Wessel & Quist-Wessel (2015), NJAS – Cocoa production in West Africa, a review ; KIT (2018) | Rendements moyens : Côte d'Ivoire ≈500-600 kg/ha ; Ghana ≈400 kg/ha | A | Volumes_Rendements | [lien](https://www.sciencedirect.com/science/article/pii/S1573521415000160) |
| `REG_COT_2526` | Africa Radio | Coton africain : ~300 FCFA au Bénin et au Mali, 310 en Côte d'Ivoire, 325 au Burkina, jusqu'à 350 au Sénégal | C | 3 obs. | [lien](https://www.africaradio.com/actualite-115836-coton-africain-pourquoi-les-producteurs-ouest-africains-perdent-ils-du-terrain) |
| `REG_COT_RDT` | La Marina (Bénin) | Campagne 2024-2025 : rendements Bénin 1 248 kg/ha, Mali 914 kg/ha | C | Volumes_Rendements | [lien](https://lamarinabj.com/index.php/2025/02/05/campagne-cotonniere-2024-2025-en-afrique-le-benin-peut-il-reprendre-sa-place-de-leader/) |
| `SGX_0326` | SGX | SICOM Rubber Monthly Report – mars 2026 | A | 1 obs. ; Observations, Cours_mensuels | [lien](https://api2.sgx.com/sites/default/files/2026-04/SICOM%20SGX%20March%202026%20.pdf) |
| `TH_CAO` | Thai Rubber Association | Prix intérieurs (cup lump 100 %) : 58 THB/kg (2 mai 2025) | B | 1 obs. | [lien](https://www.thainr.com/en/?detail=pr-local) |
| `TZ_ANA_2526` | The Citizen (données TMX/CBT) | Cashew farmers earn Sh1.3tr : 430 961 t vendues pour 1 279 Mds TZS (2025/26) | B | 1 obs. | [lien](https://www.thecitizen.co.tz/tanzania/business/cashew-farmers-earn-sh1-3tr-as-production-heads-toward-record-5311708) |
| `UG_CAF_0726` | Uganda Coffee Development Authority (UCDA) | Monthly report July 2026 : prix bord champ Robusta FAQ moyen 11 500 UGX/kg | A | 1 obs. | [lien](https://ugandacoffee.go.ug/sites/default/files/2026-09/10%20July%202026%20Report%20draft(2)(1)(1).pdf) |
| `USDA_COT` | USDA FAS | Côte d'Ivoire Cotton and Products Annual 2026 : fibre MY2024/25 730 000 balles (480 lb) | A | Parametres | [lien](https://www.fas.usda.gov/data/cote-divoire-cotton-and-products-annual-5) |
| `USDA_PAL` | USDA FAS | Côte d'Ivoire Oilseeds and Products Annual 2025 (huile de palme 575 000 t MY2024/25) | A | Contexte palmier (production d'huile), consulté pour l'analyse | [lien](https://www.fas.usda.gov/data/gain/2026/01/cote-divoire-oilseeds-and-products-report-annual-2025) |
| `USDA_RIZ_CI` | USDA FAS | Côte d'Ivoire Grain and Feed Annual 2026 : paddy bord champ 233 FCFA/kg en moyenne 2025 (+8,5 %) | A | 1 obs. | [lien](https://apps.fas.usda.gov/newgainapi/api/Report/DownloadReportByFileName?fileName=Grain+and+Feed+Annual_Accra_Cote+d%27Ivoire_IV2026-0003) |
| `USDA_RIZ_IMP` | USDA FAS | Côte d'Ivoire Grain and Feed Annual 2026 : production 2026/27 1,75 Mt de riz blanchi ; importations ≈1,75 Mt | A | Note p. 4 (importations de riz ≈1,75 Mt) | [lien](https://www.fas.usda.gov/data/gain/2026/04/cote-divoire-grain-and-feed-annual) |
| `USDA_RIZ_SN` | USDA FAS | Senegal Grain and Feed Annual 2025 : paddy 130 FCFA/kg + subvention 30 FCFA (prix usinier 160) | A | 1 obs. | [lien](https://apps.fas.usda.gov/newgainapi/api/Report/DownloadReportByFileName?fileName=Grain+and+Feed+Annual_Dakar_Senegal_SG2025-0008.pdf) |
| `VN_CAF_0926` | Vietnam.vn (prix Dak Lak) | Prix intérieur du café robusta, Dak Lak : 93 600 VND/kg (28/09/2026) | B | 1 obs. | [lien](https://www.vietnam.vn/en/gia-nong-san-hom-nay-28-9-2026-gia-ca-phe-trong-nuoc-di-nguoc-the-gioi-hang-vu-moi-sap-bat-dau-my-trung-giam-thue-doi-voi-60-ty-usd-hang-hoa) |
| `VN_RIZ` | SGGP News | Paddy frais du delta du Mékong : IR 50404 5 400-5 500 ; OM 5451 5 600-5 700 VND/kg (2025) | B | 1 obs. | [lien](https://en.sggp.org.vn/rice-farmers-in-mekong-delta-struggle-as-prices-plunge-yields-decline-post120063.html) |
<!-- SOURCES:FIN -->
