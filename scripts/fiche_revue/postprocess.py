"""Post-traitement des DOCX générés par docx-js.

1. Convertit les traits d'union insécables (U+2011) des références OBS-xx, A-x, V-x
   en élément Word natif <w:noBreakHyphen/>, rendu à l'identique par Word et LibreOffice.
2. Remplace les marqueurs §§STATUT:valeur§§ (fiche de suivi) par un contrôle de contenu
   Word « liste déroulante » proposant les cinq statuts de suivi.
Usage : python3 postprocess.py fichier.docx [...]
"""
import os
import random
import re
import shutil
import sys
import tempfile
import zipfile

NBH = "\u2011"
T_RE = re.compile(r"<w:t(?: [^>]*)?>([^<]*)</w:t>")
STATUTS = ["À CORRIGER", "CORRIGÉ", "À VÉRIFIER", "À ARBITRER", "MAINTENU"]
STATUT_RE = re.compile(r"<w:r>(<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)<w:t(?: [^>]*)?>§§STATUT:([^<§]+)§§</w:t></w:r>", re.S)
_alea = random.Random(2026)


def _liste_deroulante(m):
    rpr, valeur = m.group(1), m.group(2)
    assert valeur in STATUTS, valeur
    items = "".join(f'<w:listItem w:displayText="{v}" w:value="{v}"/>' for v in STATUTS)
    return (f'<w:sdt><w:sdtPr>{rpr}<w:alias w:val="Statut"/><w:tag w:val="statut"/>'
            f'<w:id w:val="{_alea.randint(10**8, 2**31 - 1)}"/>'
            f'<w:dropDownList w:lastValue="{valeur}">{items}</w:dropDownList></w:sdtPr>'
            f'<w:sdtContent><w:r>{rpr}<w:t xml:space="preserve">{valeur}</w:t></w:r></w:sdtContent></w:sdt>')


def _scinder(m):
    texte = m.group(1)
    if NBH not in texte:
        return m.group(0)
    morceaux = texte.split(NBH)
    t = lambda s: f'<w:t xml:space="preserve">{s}</w:t>' if s else ""
    return "<w:noBreakHyphen/>".join(t(s) for s in morceaux)


def traiter(chemin):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
    n_traits, n_listes = 0, 0
    with zipfile.ZipFile(chemin) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.match(r"word/(document|footer\d*|header\d*)\.xml$", item.filename):
                xml = data.decode("utf-8")
                n_traits += xml.count(NBH)
                xml = T_RE.sub(_scinder, xml)
                xml, k = STATUT_RE.subn(_liste_deroulante, xml)
                n_listes += k
                assert NBH not in xml and "§§STATUT" not in xml, item.filename
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, chemin)
    os.chmod(chemin, 0o644)
    print(f"post-traité : {chemin} ({n_traits} trait(s) d'union insécable(s), {n_listes} liste(s) déroulante(s))")


if __name__ == "__main__":
    for f in sys.argv[1:]:
        traiter(f)
