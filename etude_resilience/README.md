# Étude – Résilience des filières agricoles ivoiriennes aux chocs de prix internationaux

| Livrable | Fichier |
|---|---|
| 1. Note ministérielle (5 pages + annexes A à D) | `Note_ministerielle_resilience_CI.pdf` |
| 2. Version Word modifiable | `Note_ministerielle_resilience_CI.docx` |
| 3. Base Excel (données brutes, formules, indicateurs, test de stress) | `Base_resilience_filieres_CI.xlsx` |
| 4. Dossier sources (index des documents à archiver) | `sources/SOURCES.md` |
| 5. Méthodologie | `METHODOLOGIE_RESILIENCE.md` |
| 6. Audit des données | `AUDIT_DONNEES.md` |
| Graphiques (générés depuis la base) | `graphiques/` |

Reconstruction complète : `./scripts/run_all.sh`. Prérequis : Python 3 avec openpyxl, matplotlib et python-docx ; LibreOffice Calc et Writer.
Les données sont saisies dans `scripts/data.py` (codes qualité A/B/C). Les chiffres B/C doivent être validés avant toute diffusion (voir `AUDIT_DONNEES.md`).
