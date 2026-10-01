#!/usr/bin/env bash
# Reconstruit tous les livrables à partir de scripts/inputs.py et de SOURCES/donnees_primaires/.
# Prérequis : Python 3 (pandas, openpyxl, matplotlib, playwright), LibreOffice + python3-uno, Node.js + docx (npm).
# Polices : Inter converti en TrueType (« Inter TT ») attendu dans /usr/local/share/fonts/intertt ; à défaut, repli
# automatique sur Liberation Sans / Arial (la mise en page peut alors varier légèrement : vérifier les 5 pages).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_base.py     # 1. base Excel : observations, change, cours, indicateurs (formules visibles)
python3 scripts/recalc_lo.py      # 2. recalcul LibreOffice et contrôle : aucune erreur de formule tolérée
python3 scripts/make_charts.py    # 3. graphiques : lisent uniquement les valeurs recalculées de la base
python3 scripts/make_note.py      # 4. note PDF de 5 pages (HTML rendu par Chromium) + scripts/note_content.json
node scripts/make_docx.js         # 5. version Word modifiable (même contenu que le PDF)
python3 scripts/export_csv.py     # 6. CSV des observations, liste des sources, tableau des sources du .md
