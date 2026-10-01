# MÉTHODOLOGIE – Résilience des filières agricoles ivoiriennes aux chocs de prix internationaux

*Annexe méthodologique à la note au Ministre (MINADERPV, Cellule d'études, 1er octobre 2026).*

## 1. Définition opérationnelle

Dans cette étude, la **résilience aux chocs de prix** est la capacité d'une filière à faire trois choses :

- absorber un choc international défavorable ;
- en limiter l'effet sur les producteurs et les opérateurs ;
- revenir à une trajectoire soutenable sans créer de déséquilibre financier excessif.

Elle est décomposée en cinq dimensions, chacune mesurée séparément. Les dimensions ne sont **jamais agrégées en une note unique**.

| Dimension | Question | Indicateurs (onglet de la base) |
|---|---|---|
| A. Exposition | Dans quelle mesure la filière dépend-elle du marché mondial ? | Part exportée, monnaie de référence, concentration des acheteurs (texte de la carte de vulnérabilité) |
| B. Transmission | Quelle part du choc atteint le prix producteur ? | β = Δ% prix producteur / Δ% prix international (EPISODES, SERIES) |
| C. Absorption | Qui absorbe le reste ? | 1 − β ; répartition producteurs / opérateurs / État (STRESS_PARAM) |
| D. Récupération | En combien de temps revient-on au niveau pré-choc ? | Délai en mois (EPISODES) |
| E. Soutenabilité | La protection est-elle financée ? | Coût observé, besoin public, capacité identifiée, déficit (STRESS_TEST) |

**Stabilité et résilience sont deux notions distinctes.** Un β proche de 0 peut traduire un amortisseur financé (réserve, couverture), mais aussi :

- un report du choc dans le temps (ventes anticipées) ;
- une dette (Cocobod) ;
- une subvention récurrente (coton) ;
- un prix administré qui n'est pas respecté (plancher de l'anacarde en 2018).

Le β est donc toujours lu avec le délai, la variation de la recette et le coût.

## 2. Unités et harmonisation

- **Même monnaie.** La transmission est calculée en monnaie locale. Le prix international est converti en monnaie locale par kg : `prix_int × fx × conv`. `fx` est le taux de change moyen de la période (unités locales par USD). `conv` vaut 0,001 pour des USD/t, 2,20462 pour des USD/lb et 1 pour des USD/kg. La variation en USD est aussi fournie (`choc_int_usd`) pour isoler l'effet de change. Exemple : la dépréciation de l'euro, et donc du FCFA, face au dollar a amorti une partie du choc sur l'hévéa en 2011-16.
- **Même stade commercial.** Prix bord champ (producteur) contre prix international de référence (ICCO pour le cacao, Cotlook A pour le coton, TSR20 SICOM pour l'hévéa, huile brute CIF Rotterdam pour le palmier, noix brute CIF Inde pour l'anacarde, robusta ICO/Banque mondiale pour le café, riz thaï 5 % pour le riz).
- **Moyennes de campagne.** Pour le cacao, le prix producteur annuel est une moyenne pondérée : 80 % pour la campagne principale, 20 % pour la campagne intermédiaire. Cette pondération reflète la répartition usuelle des volumes et doit être validée avec le CCC.
- **Recette.** Recette = prix producteur × quantité, en milliards d'unités de monnaie locale. Pour l'hévéa, le prix est exprimé par kg de caoutchouc humide et les volumes en tonnes sèches. Les niveaux de recette sont donc sous-estimés, mais les variations restent valides. Pour le test de stress, le volume est converti en équivalent humide (~2 700 kt).

## 3. Détection des chocs

Deux niveaux de détection sont utilisés :

1. **Séries annuelles (onglet SERIES).** Un choc est une variation annuelle du prix international en monnaie locale inférieure ou égale à −15 % (seuil principal) ou à −20 % (sensibilité). Les comptages figurent dans INDICATEURS, colonnes `nb_chocs_int_15pct` et `nb_chocs_int_20pct`.
2. **Épisodes (onglet EPISODES).** Ce sont des chocs identifiés sur données mensuelles ou dans la littérature, avec quatre points :
   - T0 : situation avant le choc ;
   - T1 : début du choc (décrit dans le commentaire) ;
   - T2 : point bas (ou point haut pour les hausses) ;
   - T3 : reprise (délai de récupération).

   Les dates sont propres à chaque filière. On n'impose jamais un calendrier commun.

Épisodes retenus : cacao 2016-17, 2023-25 (hausse) et 2025-26 ; café 2023-25 et 2025-26 ; coton 2020 et 2021-22 (hausse) ; anacarde 2018-19 et 2024 (hausse) ; hévéa 2011-16 et 2026 (hausse) ; palmier 2022 ; riz importé 2023 (choc consommateur).

## 4. Calculs par épisode

| Mesure | Formule (Excel, onglet EPISODES) |
|---|---|
| Choc international | `int_local_t2 / int_local_t0 − 1` |
| Choc producteur | `prod_t2 / prod_t0 − 1` |
| Transmission β | `choc_prod / choc_int` |
| Amortissement | `1 − β` |
| Variation de recette | `(prod_t2 × q_t2) / (prod_t0 × q_t0) − 1` |
| Délai de réaction | mois entre le début du choc international et le premier changement du prix producteur (saisie) |
| Délai de récupération | mois entre T2 et le retour au prix producteur pré-choc (saisie ; « non récupéré » le cas échéant) |
| Part producteur | `prix producteur / prix international en monnaie locale` |

**Lecture de β.**

- β ≈ 1 : transmission complète.
- β < 1 : amortissement.
- β ≈ 0 : isolement complet du choc, à qualifier (qui paie ?).
- β > 1 : sur-transmission (coûts fixes de commercialisation, plancher non respecté, mesure commerciale nationale).

**Transmission dans le temps.** La transmission est mesurée à deux horizons :

- **pendant la campagne** (β1, sur le prix moyen de campagne) : environ 0,2 pour le cacao en 2016/17 et en 2025/26 ;
- **à la campagne suivante** (β2, sur les prix fixés) : 1,11 en 2017 et 0,88 en 2026.

C'est cette distinction qui montre que le système cacao **reporte** le choc plutôt qu'il ne l'absorbe.

## 5. Indicateurs harmonisés (onglet INDICATEURS)

| N° | Indicateur | Calcul |
|---|---|---|
| I1 | Volatilité internationale | CV = écart-type / moyenne du prix international en monnaie locale |
| I2 | Volatilité du prix producteur | CV du prix producteur |
| I3 | Transmission des baisses | moyenne des β annuels lorsque Δ prix int. < −5 % ; et β moyen des épisodes de baisse |
| I4 | Transmission des hausses | idem pour Δ > +5 % ; et épisodes de hausse |
| I5 | Amortissement des chocs négatifs | 1 − I3 |
| I6 | Baisse maximale du prix producteur | min(prix / maximum cumulé − 1) (drawdown) |
| I7 | Baisse maximale de recette | min des variations annuelles de recette |
| I8 | Temps de récupération | max des délais de récupération des épisodes |
| I9 | Coût de stabilisation observé | somme des coûts documentés (Mds FCFA) |
| I10 | Capacité financière | réserves publiées / besoin maximal (STRESS_TEST) ; 0 si réserves non publiées |
| — | Décomposition de la recette | part de Var(Δln Q) dans Var(Δln P) + Var(Δln Q) ; corrélation (Δln P, Δln Q) |

La **décomposition prix/volume** sert à déterminer si une **garantie de recette** est pertinente. Elle l'est lorsque la part due à Q est élevée et la corrélation P-Q faible ou positive. Exemple : coton, 99 %, contre 27 % pour le cacao.

## 6. Test de stress

Paramètres (onglet STRESS_PARAM, base 2026/27) :

- P0 : prix producteur actuel ;
- Q0 : volume ;
- β1 : transmission pendant la campagne ;
- β2 : transmission à la campagne suivante ;
- part publique : part de la charge non transmise qui revient au régulateur ou à l'État ;
- capacité : réserves publiées.

Scénarios :

- S1 : −10 % ;
- S2 : −20 % ;
- S3 : −30 % ;
- S4 : −30 % sur le prix et −10 % sur la production ;
- S5 : −30 % pendant deux campagnes.

| Sortie | Formule |
|---|---|
| ΔP producteur (campagne 1) | β1 × choc |
| ΔP producteur (campagne 2, S5) | β2 × choc |
| Δ recette | (1 + ΔP)(1 + ΔQ) − 1 |
| Perte de recette producteurs | −Δ recette × P0 × Q0 |
| Charge hors producteurs | (1 − β1) × \|choc\| × P0 × Q0 × (1 + ΔQ) [+ (1 − β2) × \|choc\| × P0 × Q0 en S5] |
| Besoin public | charge × part publique |
| Déficit de financement | max(0 ; besoin public − capacité) |
| Coût d'une protection totale du prix | β1 × \|choc\| × P0 × Q0 × (1 + ΔQ) |
| Coût d'une garantie de recette à 90 % | max(0 ; 0,9 − (1 + Δ recette)) × P0 × Q0 |

**Calibrage.** Les β1 et β2 sont tirés des épisodes observés. La part publique du cacao (0,3) correspond à la récolte non vendue à terme (environ 70 % de la récolte est vendue par anticipation). L'ordre de grandeur du besoin public estimé pour un choc de −30 % (156 Mds) est cohérent avec le coût estimé des rachats de 2026 (~240 Mds pour un choc de −64 %).

## 7. Asymétrie

Les β de hausse et de baisse sont estimés **séparément**, par épisode et sur les séries annuelles. La note ne présente que ces résultats directement interprétables.

Une estimation économétrique NARDL (Shin, Yu & Greenwood-Nimmo, 2014) est recommandée lorsque les séries **mensuelles** de prix producteur auront été obtenues auprès du CCC, du CCA et du CHPC. Spécification :

`Δp_t = α + ρ p_{t-1} + θ⁺ w⁺_{t-1} + θ⁻ w⁻_{t-1} + Σ φ_i Δp_{t-i} + Σ (π⁺_j Δw⁺_{t-j} + π⁻_j Δw⁻_{t-j}) + ε_t`

où w⁺ et w⁻ sont les sommes partielles des hausses et des baisses du prix mondial en monnaie locale. Tests prévus : test de Wald θ⁺/(−ρ) = θ⁻/(−ρ) pour l'asymétrie de long terme, et test des bornes de Pesaran pour la cointégration.

**Pour les filières à prix administré, l'économétrie continue est inadaptée.** Pour le cacao, le café et le coton, préférer des régressions avec variables muettes d'annonce de prix et des modèles à seuil sur le ratio prix producteur / CAF.

## 8. Sélection des pays de référence

| Filière | Pays retenus | Justification |
|---|---|---|
| Cacao | Ghana, Cameroun, Équateur | Ghana : concurrent direct à prix administré. Cameroun : marché libéralisé en zone FCFA (même change). Équateur : marché libre dollarisé, croissance rapide de la production. Nigeria écarté faute de données de prix producteur fiables. |
| Café | Vietnam | Premier exportateur de robusta, marché libre, référence de productivité. Ouganda et Brésil dans la revue qualitative (FUNCAFÉ). |
| Coton | Mali, Burkina Faso, Brésil | Mêmes structures intégrées en zone FCFA. Mécanismes contrastés : prix administré (Mali), fonds de lissage (Burkina Faso), instruments de marché (Brésil). |
| Anacarde | Tanzanie, Vietnam, Bénin | Tanzanie : récépissés d'entrepôt et enchères. Vietnam : acheteur et transformateur. Bénin : interdiction d'exporter la noix brute (2024). |
| Hévéa | Thaïlande, Malaisie, Indonésie | Trois premiers producteurs (avec la Côte d'Ivoire) ; politiques de soutien au revenu documentées. |
| Palmier à huile | Indonésie, Malaisie | Fonds BPDPKS, formule de prix des régimes MPOB. |

## 9. Reproductibilité

```bash
cd etude_resilience
./scripts/run_all.sh   # data.py -> Excel (formules) -> recalcul LibreOffice -> graphiques -> Word -> PDF
```

- Les données brutes sont saisies une seule fois, dans `scripts/data.py`.
- Les calculs sont des formules Excel visibles dans la base.
- Graphiques et note lisent les valeurs recalculées.
- Aucun chiffre n'est ressaisi à la main dans la note.
