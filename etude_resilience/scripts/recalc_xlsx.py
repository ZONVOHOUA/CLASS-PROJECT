"""Recalcule les formules du classeur avec LibreOffice (headless) pour stocker les valeurs."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

src = Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory() as d:
    subprocess.run(["soffice", f"-env:UserInstallation=file://{d}/profile", "--headless", "--calc",
                    "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", d, str(src)], check=True,
                   capture_output=True, timeout=300)
    shutil.copy(Path(d) / src.name, src)
print("recalculé :", src)
