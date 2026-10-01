# Fiche de revue et de sécurisation documentaire – Cabinet du Ministre

Fiche de revue destinée au Cabinet du Ministre de l’Agriculture, du Développement Rural et des Productions Vivrières, appliquée à la **Communication en Conseil des Ministres relative à la collecte et à l’utilisation des redevances de la filière café-cacao au 30 juin 2026** (version du 12 août 2026, 17 pages).

## Livrables

| Fichier | Contenu |
|---|---|
| `Fiche_Revue_Documentaire_Cabinet.docx` / `.pdf` | Fiche de revue (4 pages) : synthèse Cabinet en page 1, 21 observations OBS-01 à OBS-21, 2 arbitrages, 4 vérifications, suite à donner. |
| `Fiche_Suivi_Corrections_Cabinet.docx` / `.pdf` | Fiche de suivi des corrections (2 pages) : statut de chaque observation (liste déroulante sous Word), réponse de la structure émettrice, visas. |
| `Modele_Fiche_Revue_Documentaire_Cabinet.docx` | Modèle vierge réutilisable, avec une page de consignes à supprimer avant transmission. |

## Lecture à deux niveaux

- **Page 1, lecture Cabinet** : identification du document, « Coup d’œil Cabinet » (21 observations : 1 critique, 6 majeures, 8 à corriger, 6 de forme), statut global, points critiques et majeurs en une ligne, arbitrages attendus.
- **Pages 2 à 4, lecture technique** : tableau détaillé (référence, localisation, catégorie, constat, correction attendue, priorité), puis arbitrages, vérifications et suite à donner.

## Sources et méthode

- **Document examiné** : `outputs/CCM_AU_30_JUIN_2026_corrigee_suivi_modif.docx` (branche `claude/modest-hypatia-cobil4`). La version transmise a été reconstituée en retenant les modifications de l’auteur et en écartant les corrections proposées ultérieurement.
- **Observations** : commentaires de relecture présents dans le fichier (11 et 20 août 2026), complétés par une vérification arithmétique de l’ensemble des données du document (`scripts/fiche_revue/verif_ccm.py`). Aucune donnée extérieure n’a été utilisée : les montants recalculés sont présentés comme « à confirmer par la Direction ».
- **Localisation** : par partie, section, paragraphe (§) et tableau, la pagination du document examiné dépendant du logiciel et de l’affichage des révisions.

## Insignes

- Seules les armoiries de la République figurent dans le dépôt (`dashboards/assets/armoiries.png`, branche `claude/wonderful-fermi-6du6s3`). Aucun logo propre au Ministère ou au Cabinet n’y figure : l’en-tête reprend la forme textuelle de l’en-tête officiel de la communication examinée.
- Le fichier des armoiries avait perdu sa transparence (fond noir). Une clé de transparence a été ajoutée sans modifier les données d’image (`scripts/fiche_revue/assets/restaurer_transparence.py`) ; l’emblème est reproduit à l’identique, proportions conservées, à pleine résolution dans le PDF. Il peut être remplacé par le fichier officiel du Ministère s’il est disponible.
- Aucune mention de confidentialité n’existe dans les modèles disponibles ; aucune n’a été ajoutée.

## Typographie et rendu

- Garamond pour le texte courant, Calibri pour les tableaux et libellés.
- Les PDF sont produits par LibreOffice avec EB Garamond (équivalent libre de Garamond) et Carlito (métriques identiques à Calibri). Sous Word, les tableaux conservent exactement la même mise en page ; les paragraphes en Garamond peuvent varier très légèrement, une réserve de 6,8 cm étant laissée en fin de fiche.

## Regénération

```bash
scripts/fiche_revue/generer.sh            # DOCX + PDF dans fiche-revue-documentaire/
python3 scripts/fiche_revue/verif_ccm.py  # contrôle arithmétique du document examiné
```

Les données de la fiche sont dans `scripts/fiche_revue/data_ccm_30juin2026.js` ; une nouvelle revue se prépare en copiant ce fichier (ou `data_modele.js`) et en relançant `generer.sh` avec le nouveau fichier de données.
