# AUDIT DES DONNÉES – points de contrôle avant diffusion

**Statut : document de travail. Les chiffres de qualité B et C doivent être validés par les institutions sources avant toute diffusion extérieure.**

Codes qualité (colonne `qualite` de la base) :

- **A** : confirmé en septembre-octobre 2026 sur une source officielle ou de presse citant une source officielle (URL fournie) ;
- **B** : valeur publiée connue, non re-téléchargée pendant l'étude (accès réseau restreint) ;
- **C** : estimation ou reconstitution de l'équipe.

## 1. Valeurs confirmées (A)

| Donnée | Valeur | Source |
|---|---|---|
| Prix bord champ cacao 2025/26 (principale) | 2 800 FCFA/kg | Gouvernement, Fraternité Matin, 1er oct. 2025 |
| Prix café 2025/26 / 2026/27 | 1 700 / 1 300 FCFA/kg | idem ; gouv.ci, 1er sept. 2026 |
| Prix cacao intermédiaire 2025/26 | 1 200 FCFA/kg (4 mars 2026) | Jeune Afrique, France 24, KOACI |
| Prix cacao 2026/27 | 1 200 FCFA/kg | gouv.ci, AIP |
| Invendus cacao 2026 | 123 000 t (février), ~200 000 t (mars) ; dispositif d'achat annoncé le 20 janv. 2026 | AllAfrica, 7info |
| Prix ICCO | 8 399 USD/t (avril 2025) → ~2 863 USD/t (2 mars 2026) | presse spécialisée citant l'ICCO |
| Ghana | 58 000 GHS/t (3 oct. 2025) → 41 392 (12 fév. 2026, 90 % du FOB à 4 200 USD/t) → 42 400 (25 sept. 2026, 71,18 % du FOB) ; dette héritée Cocobod 5,8 Mds GHS ; défaut sur facilité relais de 70 M USD ; production 2023/24 de 432 145 t | ISD Ghana, GNA, MyJoyOnline |
| Ghana–CI | Déclaration conjointe du 16 juin 2026 (alignement des prix en USD et des calendriers à partir de 2026/27) | presse |
| Coton 2025/26 | 310 FCFA/kg (1er choix), 285 FCFA/kg (2e choix) ; subvention 25,3 Mds FCFA (44 FCFA/kg) | KOACI, economie-ivoirienne.ci |
| Anacarde 2026 | plancher 400 FCFA (bord champ) / 425 (magasin intérieur) / 454 (usine) / 484 (port) | KOACI, APA |
| Hévéa 2026 | 401 (avr.) → 439 (mai) → 493 (juil.) FCFA/kg ; part producteur portée de 63 % à 66 % au 1er mai 2026 | Sika Finance, AIP, KOACI |

## 2. Données manquantes

1. **Fonds de réserve de prévoyance (FRP) cacao.** Le solde, les règles d'alimentation et de décaissement et l'utilisation en 2016-17 et en 2026 ne sont pas publiés. La capacité financière est fixée à 0 dans le test de stress. **Point bloquant** pour l'indicateur I10.
2. **Coût réel du dispositif de rachat 2026.** Les 240 Mds FCFA sont une estimation (200 kt × écart entre 2 800 FCFA et une valeur de revente d'environ 1 600 FCFA/kg). Le prix et les volumes de revente effectifs (Transcao) sont à obtenir auprès du CCC et du Trésor.
3. **Séries mensuelles de prix producteur** (cacao, café, coton, anacarde, hévéa, régimes de palme). Sans elles, l'estimation NARDL et la mesure précise des délais de réaction sont impossibles.
4. **Montant du soutien au coton en 2020/21** (choc COVID) : non documenté dans la base.
5. **Prix réellement payés pour l'anacarde** (distincts du plancher) : seules des fourchettes de presse spécialisée sont disponibles.
6. **Prix des régimes de palme (AIPH/CHPC)** : aucune série officielle trouvée ; les valeurs 2022 sont des ordres de grandeur.
7. **Revenu net des producteurs** (coûts de production) : non disponible. La « garantie de revenu » n'est donc discutée que qualitativement.
8. **Nombre de producteurs par filière** : nécessaire pour exprimer les coûts par producteur (registres CCC et CHPC à mobiliser).
9. **Documents sources.** L'accès réseau de l'environnement de travail n'a pas permis de télécharger les PDF. Le dossier `sources/` contient l'index des documents à archiver.

## 3. Comparaisons fragiles

- **Cameroun, Équateur, Tanzanie, Indonésie, Thaïlande (prix producteurs)** : qualité C. Les β correspondants (1,05 ; 0,96 ; 0,83 ; 1,50 ; 1,05) indiquent un sens et un ordre de grandeur, pas un chiffre à citer seul.
- **Ghana en monnaie locale** : les fortes variations du cedi (≈ 4 → 15 GHS/USD) dominent les indicateurs de volatilité. Le CV de 106 % reflète l'inflation, pas une instabilité du système.
- **Cacao CI 2023/24 : part du prix spot de 28 %.** Elle est calculée par rapport au prix comptant. Les ventes anticipées de cette campagne avaient été conclues à des prix inférieurs, donc la part rapportée au CAF réalisé est plus élevée. **Ne pas présenter 28 % comme une « captation ».** Inversement, la part de 93 % en 2025/26 traduit un report du coût, pas une générosité du système.
- **Hévéa** : prix humide et volumes secs (voir la méthodologie, section 2). Les variations de recette sont valides, les niveaux non.
- **Coton** : la transmission est mesurée entre Cotlook A (fibre) et coton-graine. Le rendement à l'égrenage (~42 %) et les coûts fixes rendent le β non directement comparable à celui des autres filières.
- **Riz** : le β de 0,42 porte sur le prix consommateur, pas sur un prix producteur.

## 4. Hypothèses structurantes

| Hypothèse | Valeur | Sensibilité |
|---|---|---|
| Pondération des campagnes cacao (principale / intermédiaire) | 80 / 20 | Affecte les β annuels et la part producteur, pas les épisodes (prix fixés) ; à remplacer par les volumes réels par campagne (CCC) |
| β1 cacao (pendant la campagne) | 0,2 | Si 0,4 : la perte des producteurs double en campagne 1 et la charge hors producteurs baisse de 25 % |
| Part publique cacao | 0,3 (récolte non vendue à terme) | Si les exportateurs font défaut sur 20 % de leurs contrats : ~0,45 |
| Part publique coton | 0,5 (État / sociétés cotonnières) | Non documentée ; à valider avec Intercoton |
| Volume hévéa (humide) | 2 700 kt | Teneur en caoutchouc sec de 0,55 à 0,65 : 2 460 à 2 900 kt |
| Prix des régimes de palme P0 | 100 FCFA/kg | À remplacer par le prix du CHPC |
| Capacité financière | 0 partout | Remplacer dès la publication du FRP et de tout autre fonds |
| Coût des options de vente (put) cacao | 3 à 6 % de la valeur couverte | Ordre de grandeur pour des options à 6-12 mois proches de la monnaie, très sensible à la volatilité implicite (élevée en 2024-2026) ; à coter auprès de courtiers ICE |

## 5. Points nécessitant une validation institutionnelle

| Institution | Objet |
|---|---|
| Conseil du Café-Cacao | Situation du FRP ; volumes et prix moyens des ventes anticipées 2024/25 à 2026/27 ; exportateurs défaillants (volumes) ; coût des rachats 2026 ; prix mensuels |
| Ministère du Budget / Trésor | Coût budgétaire du soutien coton (2020/21, 2025/26) ; recettes DUS et droits d'enregistrement cacao |
| Conseil du Coton et de l'Anacarde | Prix effectivement payés pour l'anacarde 2016-2026 ; taux de transformation locale ; mécanisme coton (existence d'une réserve) |
| CHPC (ex-APROMAC/AIPH) | Prix mensuels hévéa et régimes 2011-2026 ; formule de prix ; volumes en sec et en humide |
| INS / BCEAO | Taux de change moyens par campagne ; indices de prix pour le passage en termes réels |
| Douanes | Exportations par destination (concentration des acheteurs) |

## 6. Contrôle qualité final (section 24 de la commande)

| Critère | Statut |
|---|---|
| Même période (prix int. et producteur) | OK pour les épisodes ; moyennes de campagne pour les séries |
| Même produit et qualité | OK pour cacao, café robusta et coton (1er choix). Écart : anacarde (plancher contre prix réel) |
| Même stade commercial | Bord champ contre référence internationale : OK |
| Même unité et devise | Conversion systématique en monnaie locale/kg ; la variation en USD est aussi fournie |
| Définition identique du prix | Pondération cacao à valider |
| Exactitude des dates | A pour 2025-2026 ; B/C pour les épisodes antérieurs |
| Source primaire | Partielle (voir section 2.9) |
| Subventions identifiées | Coton (A) ; cacao (estimation) ; autres : aucune connue |
| Volatilité ≠ résilience | Traité explicitement (note, section 1) |
| Prix ≠ recette | Traité explicitement (constat 5, décomposition de la variance) |
| Temporaire ≠ structurel | Hévéa (structurel, prix non récupéré) ; café (déclin structurel des volumes) ; cacao 2026 (en cours) |
