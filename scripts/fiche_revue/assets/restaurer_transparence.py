"""Restaure la transparence des armoiries sans modifier l'image.

Le fichier armoiries.png disponible dans le dépôt a perdu sa couche de transparence
lors d'un export : le fond est devenu noir pur (0, 0, 0). Une analyse des composantes
connexes montre que tous les pixels noirs purs appartiennent au fond (autour de
l'emblème et dans les trois espaces fermés entre palmiers, écu et listel) ; aucun
élément de l'emblème n'est en noir pur.

Ce script ajoute uniquement un bloc PNG « tRNS » (clé de transparence) déclarant le
noir pur comme transparent. Les données d'image (blocs IDAT) restent identiques octet
pour octet : l'emblème n'est ni redessiné, ni recoloré, ni redimensionné.
"""
import hashlib
import struct
import zlib
from pathlib import Path

ICI = Path(__file__).parent
SOURCE = ICI / "armoiries.png"
CIBLE = ICI / "armoiries_fond_transparent.png"


def blocs(data):
    i = 8
    while i < len(data):
        n, = struct.unpack(">I", data[i:i + 4])
        yield data[i + 4:i + 8], data[i:i + 12 + n]
        i += 12 + n


def main():
    data = SOURCE.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    sortie = [data[:8]]
    for type_, bloc in blocs(data):
        assert type_ != b"tRNS", "le fichier source possède déjà une clé de transparence"
        sortie.append(bloc)
        if type_ == b"IHDR":
            couleur = bloc[8 + 9]
            assert couleur == 2, "image RVB attendue (type de couleur 2)"
            corps = b"\x00\x00" * 3  # clé (R, V, B) = (0, 0, 0) sur 16 bits
            crc = zlib.crc32(b"tRNS" + corps) & 0xFFFFFFFF
            sortie.append(struct.pack(">I", len(corps)) + b"tRNS" + corps + struct.pack(">I", crc))
    resultat = b"".join(sortie)
    idat = lambda d: b"".join(b for t, b in blocs(d) if t == b"IDAT")
    assert idat(resultat) == idat(data), "les données d'image doivent rester identiques"
    CIBLE.write_bytes(resultat)
    print("source :", hashlib.sha256(data).hexdigest())
    print("cible  :", hashlib.sha256(resultat).hexdigest(), "(IDAT identiques)")


if __name__ == "__main__":
    main()
