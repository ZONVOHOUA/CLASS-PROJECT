# Les prix agricoles ivoiriens sont-ils compétitifs ?

Benchmark international des prix au producteur des principales filières végétales de la Côte d'Ivoire, préparé pour le Ministre de l'Agriculture, du Développement Rural et des Productions Vivrières. Données arrêtées au 1er octobre 2026.

**Réponse courte : pas dans la plupart des filières.** Pour le cacao, le café, le caoutchouc et le palmier, le producteur ivoirien perçoit 29 à 42 % de moins que ses concurrents et une part plus faible du prix international. L'anacarde est au niveau de l'UEMOA mais 34 % sous le Ghana ; le coton n'est à parité que grâce à une subvention ; le riz paddy est payé au-dessus de la parité FOB du riz importé. Pour les fruits et les vivriers, les données ne permettent pas de conclure.

## Livrables

| Fichier | Contenu |
|---|---|
| [`Note_Benchmark_Prix_Agricoles_CI.pdf`](Note_Benchmark_Prix_Agricoles_CI.pdf) | Note de 5 pages |
| [`Note_Benchmark_Prix_Agricoles_CI.docx`](Note_Benchmark_Prix_Agricoles_CI.docx) | Version Word modifiable |
| [`Base_Prix_Benchmark_CI.xlsx`](Base_Prix_Benchmark_CI.xlsx) | Base de traçabilité : 177 observations, 127 sources, formules visibles |
| [`Base_Prix_Benchmark_CI_observations.csv`](Base_Prix_Benchmark_CI_observations.csv) | Export CSV des observations (`;`, décimale `,`) |
| [`METHODOLOGIE_ET_SOURCES.md`](METHODOLOGIE_ET_SOURCES.md) | Définitions, conversions, choix des pays, difficultés, limites, liens vers les sources |
| [`SOURCES/`](SOURCES/README.md) | Données primaires archivées et liste des sources |
| [`figures/`](figures) | Graphiques de la note (SVG et PNG) |
| [`scripts/`](scripts) | Chaîne de production reproductible |

## Reconstruire

```bash
bash scripts/run_all.sh
```

Détail des étapes et prérequis : section 14 de [`METHODOLOGIE_ET_SOURCES.md`](METHODOLOGIE_ET_SOURCES.md).
