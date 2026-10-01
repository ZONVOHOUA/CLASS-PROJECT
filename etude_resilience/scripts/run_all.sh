#!/usr/bin/env bash
# Reconstruit l'ensemble des livrables : base Excel -> recalcul -> graphiques -> note Word -> PDF
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_excel.py
python3 scripts/recalc_xlsx.py Base_resilience_filieres_CI.xlsx
python3 scripts/build_charts.py
python3 scripts/build_docx.py
soffice --headless --convert-to pdf --outdir . Note_ministerielle_resilience_CI.docx >/dev/null 2>&1 || echo "PDF non généré (LibreOffice Writer requis)"
