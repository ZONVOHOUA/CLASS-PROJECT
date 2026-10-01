#!/usr/bin/env bash
# Regénère les documents de revue documentaire du Cabinet (DOCX + PDF).
#
# Prérequis : Node.js avec le module « docx », Python 3, LibreOffice Writer.
# Rendu PDF : polices Garamond et Calibri, ou leurs équivalents libres EB Garamond
# (alias « Garamond » déclaré dans fontconfig) et Carlito (métriques de Calibri).
#
# Usage : ./generer.sh [fichier de données] [dossier de sortie]
set -euo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
DONNEES="${1:-$ICI/data_ccm_30juin2026.js}"
SORTIE="$(realpath -m "${2:-$ICI/../../fiche-revue-documentaire}")"

python3 "$ICI/assets/restaurer_transparence.py"
node "$ICI/build.js" "$DONNEES" "$SORTIE"
python3 "$ICI/postprocess.py" "$SORTIE"/*.docx

# PDF sans perte : armoiries à pleine résolution, PDF balisé, signets.
FILTRE='pdf:writer_pdf_Export:{"ReduceImageResolution":{"type":"boolean","value":"false"},"UseLosslessCompression":{"type":"boolean","value":"true"},"ExportBookmarks":{"type":"boolean","value":"true"},"UseTaggedPDF":{"type":"boolean","value":"true"}}'
for f in Fiche_Revue_Documentaire_Cabinet Fiche_Suivi_Corrections_Cabinet; do
  soffice --headless --convert-to "$FILTRE" --outdir "$SORTIE" "$SORTIE/$f.docx" >/dev/null 2>&1
  echo "PDF : $SORTIE/$f.pdf ($(pdfinfo "$SORTIE/$f.pdf" | awk '/^Pages/ {print $2}') pages)"
done
