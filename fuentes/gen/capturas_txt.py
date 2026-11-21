"""Escribe la lista de capturas de un documento en _trabajo/capturas_<doc>.txt
(nota interna: en los documentos del alumnado ya no va al final). Busca en el PDF
en qué página sale cada hueco [CAPTURA: …]."""
import re, subprocess
import estilo_ha as E

CARPETA = "/home/claude/material-ha/_trabajo"


def _paginas(pdf):
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    return [re.sub(r"\s+", " ", p) for p in txt.split("\f")]


def escribir(doc, nombre, pdf=None):
    lista = E.capturas(doc)
    pags = _paginas(pdf) if pdf else []
    lineas = [f"Capturas de {nombre} (las hace el profesor)", ""]
    desde = 0
    for n, d, s in lista:
        clave = re.sub(r"\s+", "", d)[:30]
        pag = "?"
        for i in range(desde, len(pags)):
            if clave in re.sub(r"\s+", "", pags[i]):
                pag = str(i + 1); desde = i; break
        lineas.append(f"{n}. p. {pag} · {s} · {d}")
    with open(f"{CARPETA}/capturas_{nombre}.txt", "w") as f:
        f.write("\n".join(lineas) + "\n")
    return lista
