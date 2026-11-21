# -*- coding: utf-8 -*-
"""
estilo_ha.py — Estilo común de los documentos Word del tema de Home Assistant
(Instalaciones Domóticas · 2MT · I.E.S. Trinidad Arroyo).

Imita el aspecto de los documentos del módulo (2MT-P4, Tema 2): letra Arial
(en la conversión, Liberation Sans, con las mismas medidas), cabecera con
título corto en verde y centro en gris, títulos con acento verde, cajones de
colores con barra a la izquierda (IDEA CLAVE, ¡OJO!, EJEMPLO, EN EL TALLER,
PISTA, ¿POR QUÉ?), tablas con cabecera verde y «Página N de M» en el pie.

Uso mínimo:

    import sys; sys.path.insert(0, "/home/claude/herr")
    import estilo_ha as E
    doc = E.nuevo_documento("Tu Home Assistant", "Hoja 1 · Cómo entrar y normas")
    E.h1(doc, "1. Cómo entrar")
    E.parrafo(doc, "Abre el navegador y escribe `http://192.0.2.81`. **Sin** `:8123`.")
    E.cajon(doc, "¡OJO!", "El **reset** lo borra todo: haz capturas antes.")
    E.guardar(doc, "/ruta/2MT-HA-hoja1-tu-home-assistant.docx")
    E.a_pdf("/ruta/2MT-HA-hoja1-tu-home-assistant.docx")

Marcado en línea admitido en casi todos los textos:
    **negrita**   *cursiva*   `código` (monoespaciada)
    (para escribir un asterisco o un acento grave literal, escápalo: \\*  \\`)
"""

import os
import re
import shutil
import subprocess
import tempfile

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Emu

# ---------------------------------------------------------------------------
# Paleta (hex sin «#», como la usa Word). Sacada de los PDF del módulo.
# ---------------------------------------------------------------------------
VERDE = "70AD47"          # acento principal: barras, cabeceras de tabla
VERDE_OSCURO = "548235"   # títulos
VERDE_MUY_OSCURO = "385723"  # texto de h1
VERDE_CLARO = "E2EFDA"    # fondo de h1 y de IDEA CLAVE
VERDE_MEDIO = "C5E0B4"    # filas de grupo en tablas
VERDE_FILA = "F3F9EF"     # filas alternas de tablas
ROJO = "C00000"           # ¡OJO! y banda CONFIDENCIAL
ROJO_CLARO = "FCE4D6"
AZUL = "2E75B6"           # PISTA
AZUL_CLARO = "DDEBF7"
MORADO = "6A4C93"         # EN EL TALLER
MORADO_CLARO = "EDE7F6"
OCRE = "BF9000"           # ¿POR QUÉ?
OCRE_CLARO = "FFF2CC"
PIZARRA = "44546A"        # EJEMPLO
PIZARRA_CLARO = "EDF1F4"
NARANJA = "C55A11"        # resaltes (p. ej. «230 Vca» en tablas)
GRIS = "808080"           # cabecera, pies de figura
GRIS_OSCURO = "404040"
GRIS_BORDE = "BFBFBF"
GRIS_CODIGO = "F2F2F2"
NEGRO = "000000"
BLANCO = "FFFFFF"

# Colores de los esquemas de Domótica (criterios del profesor)
FASE = "8B4513"           # 230 Vca: fase marrón
NEUTRO = "1F4E9E"         # 230 Vca: neutro azul
POSITIVO = "D00000"       # 12 Vcc: positivo rojo
NEGATIVO = "000000"       # 12 Vcc: negativo negro
TIERRA = "2E8B57"         # tierra verde (discontinua)

PALETA = {k: v for k, v in globals().items() if isinstance(v, str) and re.fullmatch(r"[0-9A-F]{6}", v or "")}

CAJONES = {
    # tipo: (color del título y de la barra, color de fondo)
    "IDEA CLAVE": (VERDE, VERDE_CLARO, VERDE_OSCURO),
    "¡OJO!": (ROJO, ROJO_CLARO, ROJO),
    "EJEMPLO": (PIZARRA, PIZARRA_CLARO, PIZARRA),
    "EN EL TALLER": (MORADO, MORADO_CLARO, MORADO),
    "PISTA": (AZUL, AZUL_CLARO, AZUL),
    "¿POR QUÉ?": (OCRE, OCRE_CLARO, OCRE),
}

FUENTE = "Arial"              # en LibreOffice → Liberation Sans (mismas medidas)
FUENTE_MONO = "Courier New"   # en LibreOffice → Liberation Mono (mismas medidas)
FUENTE_MPL = ["Liberation Sans", "Arial", "DejaVu Sans"]
TAM = 10.5                    # cuerpo
CENTRO = "I.E.S. Trinidad Arroyo · Instalaciones Domóticas · 2MT"
TEXTO_CONF = "CONFIDENCIAL – solo profesorado"


def rgb(hexa):
    return RGBColor.from_string(hexa.upper())


def mpl_color(nombre_o_hex):
    """Color para matplotlib: mpl_color('VERDE') o mpl_color('70AD47') → '#70AD47'."""
    v = PALETA.get(str(nombre_o_hex).upper(), nombre_o_hex)
    return "#" + v.lstrip("#")


def mpl_estilo():
    """Aplica a matplotlib la fuente y los colores del proyecto. Llamar antes de dibujar.
    Devuelve el diccionario de colores con «#» (p. ej. C['VERDE'])."""
    import matplotlib
    matplotlib.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": FUENTE_MPL,
        "font.size": 10,
        "axes.edgecolor": "#" + GRIS_OSCURO,
        "axes.labelcolor": "#" + GRIS_OSCURO,
        "axes.titlecolor": "#" + VERDE_OSCURO,
        "axes.titleweight": "bold",
        "xtick.color": "#" + GRIS_OSCURO,
        "ytick.color": "#" + GRIS_OSCURO,
        "axes.prop_cycle": matplotlib.cycler(color=["#" + c for c in (VERDE, AZUL, NARANJA, MORADO, OCRE, ROJO, PIZARRA)]),
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "figure.facecolor": "white",
        "svg.fonttype": "none",
    })
    return {k: "#" + v for k, v in PALETA.items()}


# ---------------------------------------------------------------------------
# Utilidades XML
# ---------------------------------------------------------------------------
def _sub(parent, tag, **attrs):
    el = parent.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        parent.append(el)
    for k, v in attrs.items():
        el.set(qn(k), str(v))
    return el


def _shd(pr, fill):
    """Sombreado (pPr, tcPr o rPr)."""
    old = pr.find(qn("w:shd"))
    if old is not None:
        pr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pr.append(shd)
    return shd


def _orden_ppr(ppr):
    """Reordena hijos de pPr según el esquema OOXML (Word es estricto)."""
    orden = ["w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore", "w:framePr",
             "w:widowControl", "w:numPr", "w:suppressLineNumbers", "w:pBdr", "w:shd",
             "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
             "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
             "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
             "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
             "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
             "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange"]
    hijos = list(ppr)
    def clave(e):
        t = e.tag
        for i, o in enumerate(orden):
            if t == qn(o):
                return i
        return len(orden)
    hijos.sort(key=clave)
    for h in hijos:
        ppr.remove(h)
    for h in hijos:
        ppr.append(h)


def _p_borde(p, lado, color, sz=8, space=4, val="single"):
    ppr = p._p.get_or_add_pPr()
    bdr = ppr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        ppr.append(bdr)
    b = OxmlElement("w:" + lado)
    b.set(qn("w:val"), val)
    b.set(qn("w:sz"), str(sz))
    b.set(qn("w:space"), str(space))
    b.set(qn("w:color"), color)
    # orden top, left, bottom, right
    bdr.append(b)
    orden = ["top", "left", "bottom", "right", "between", "bar"]
    hijos = sorted(list(bdr), key=lambda e: orden.index(e.tag.split("}")[1]))
    for h in hijos:
        bdr.remove(h)
    for h in hijos:
        bdr.append(h)
    _orden_ppr(ppr)


def _p_shd(p, fill):
    ppr = p._p.get_or_add_pPr()
    _shd(ppr, fill)
    _orden_ppr(ppr)


def _celda_shd(cell, fill):
    _shd(cell._tc.get_or_add_tcPr(), fill)


def _celda_bordes(cell, **lados):
    """lados: top/left/bottom/right = (val, sz, color) o None para quitar."""
    tcpr = cell._tc.get_or_add_tcPr()
    old = tcpr.find(qn("w:tcBorders"))
    if old is not None:
        tcpr.remove(old)
    b = OxmlElement("w:tcBorders")
    for lado in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + lado)
        spec = lados.get(lado)
        if spec is None:
            e.set(qn("w:val"), "nil")
        else:
            val, sz, color = spec
            e.set(qn("w:val"), val)
            e.set(qn("w:sz"), str(sz))
            e.set(qn("w:space"), "0")
            e.set(qn("w:color"), color)
        b.append(e)
    # tcBorders va después de tcW/gridSpan/vMerge y antes de shd
    shd = tcpr.find(qn("w:shd"))
    if shd is not None:
        shd.addprevious(b)
    else:
        tcpr.append(b)


def _celda_margenes(cell, top=60, left=110, bottom=60, right=110):
    tcpr = cell._tc.get_or_add_tcPr()
    old = tcpr.find(qn("w:tcMar"))
    if old is not None:
        tcpr.remove(old)
    m = OxmlElement("w:tcMar")
    for lado, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement("w:" + lado)
        e.set(qn("w:w"), str(v))
        e.set(qn("w:type"), "dxa")
        m.append(e)
    # tcMar va antes de vAlign
    va = tcpr.find(qn("w:vAlign"))
    if va is not None:
        va.addprevious(m)
    else:
        tcpr.append(m)


def _orden_tblpr(tbl):
    """Reordena tblPr según el esquema OOXML (Word es estricto)."""
    tblpr = tbl._tbl.tblPr
    orden = ["w:tblStyle", "w:tblpPr", "w:tblOverlap", "w:bidiVisual", "w:tblStyleRowBandSize",
             "w:tblStyleColBandSize", "w:tblW", "w:jc", "w:tblCellSpacing", "w:tblInd",
             "w:tblBorders", "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook",
             "w:tblCaption", "w:tblDescription", "w:tblPrChange"]
    pos = {qn(o): i for i, o in enumerate(orden)}
    hijos = sorted(list(tblpr), key=lambda e: pos.get(e.tag, len(orden)))
    for h in hijos:
        tblpr.remove(h)
    for h in hijos:
        tblpr.append(h)


def _tabla_sin_bordes(tbl):
    tblpr = tbl._tbl.tblPr
    old = tblpr.find(qn("w:tblBorders"))
    if old is not None:
        tblpr.remove(old)
    b = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + lado)
        e.set(qn("w:val"), "nil")
        b.append(e)
    tblpr.append(b)


def _tabla_bordes(tbl, color=GRIS_BORDE, sz=4):
    tblpr = tbl._tbl.tblPr
    old = tblpr.find(qn("w:tblBorders"))
    if old is not None:
        tblpr.remove(old)
    b = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + lado)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        b.append(e)
    tblpr.append(b)


def _tabla_ancho_fijo(tbl, anchos_cm):
    tbl.autofit = False
    tblpr = tbl._tbl.tblPr
    lay = _sub(tblpr, "w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    total = sum(anchos_cm)
    w = _sub(tblpr, "w:tblW")
    w.set(qn("w:w"), str(int(total * 567)))
    w.set(qn("w:type"), "dxa")
    grid = tbl._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
        if i < len(anchos_cm):
            gc.set(qn("w:w"), str(int(anchos_cm[i] * 567)))
    for row in tbl.rows:
        for i, cell in enumerate(row.cells):
            if i < len(anchos_cm):
                cell.width = Cm(anchos_cm[i])
    _orden_tblpr(tbl)


def _fila_no_partir(row, cabecera=False, alto_cm=None, exacto=False):
    trpr = row._tr.get_or_add_trPr()
    if alto_cm is not None:
        h = OxmlElement("w:trHeight")
        h.set(qn("w:val"), str(int(alto_cm * 567)))
        h.set(qn("w:hRule"), "exact" if exacto else "atLeast")
        trpr.append(h)
    cs = OxmlElement("w:cantSplit")
    trpr.append(cs)
    if cabecera:
        th = OxmlElement("w:tblHeader")
        trpr.append(th)


def _lang(rpr, lang="es-ES"):
    l = rpr.find(qn("w:lang"))
    if l is None:
        l = OxmlElement("w:lang")
        rpr.append(l)
    l.set(qn("w:val"), lang)
    l.set(qn("w:eastAsia"), lang)


def _fuente_run(run, nombre):
    run.font.name = nombre
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), nombre)


def _campo(p, instr, tam=None, color=None, negrita=False):
    """Inserta un campo (PAGE, NUMPAGES…) en el párrafo."""
    def r():
        run = p.add_run()
        if tam:
            run.font.size = Pt(tam)
        if color:
            run.font.color.rgb = rgb(color)
        run.bold = negrita
        return run
    r1 = r(); f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), "begin"); r1._r.append(f)
    r2 = r(); t = OxmlElement("w:instrText"); t.set(qn("xml:space"), "preserve"); t.text = f" {instr} "; r2._r.append(t)
    r3 = r(); f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), "separate"); r3._r.append(f)
    r4 = r(); r4.text = "1"
    r5 = r(); f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), "end"); r5._r.append(f)


def _espaciado(p, antes=0, despues=0, linea=None, juntos=None):
    pf = p.paragraph_format
    pf.space_before = Pt(antes)
    pf.space_after = Pt(despues)
    if linea is not None:
        pf.line_spacing = linea
    if juntos is not None:
        pf.keep_with_next = juntos


# ---------------------------------------------------------------------------
# Texto con marcado sencillo: **negrita**, *cursiva*, `código`
# ---------------------------------------------------------------------------
_TOKEN = re.compile(r"(\\[*`]|\*\*.+?\*\*|`[^`]+`|(?<![\w*])\*(?!\s)[^*]+?(?<!\s)\*(?![\w*]))", re.S)


def texto_rico(p, texto, tam=None, color=None, negrita=False, cursiva=False, mono_tam=None):
    """Añade `texto` al párrafo `p` interpretando **negrita**, *cursiva* y `código`.
    Se puede anidar `código` dentro de **negrita** (**`así`**). Devuelve el párrafo."""
    def add(trozo, b=False, i=False, mono=False):
        if not trozo:
            return
        partes = trozo.split("\n")
        for k, parte in enumerate(partes):
            if k:
                p.add_run().add_break()
            if not parte:
                continue
            run = p.add_run(parte)
            run.bold = negrita or b or None
            run.italic = cursiva or i or None
            if tam:
                run.font.size = Pt(tam)
            if color:
                run.font.color.rgb = rgb(color)
            if mono:
                _fuente_run(run, FUENTE_MONO)
                base = tam or TAM
                run.font.size = Pt(mono_tam or max(base - 1, 7))
                if not color:
                    run.font.color.rgb = rgb("1F3864")

    def procesar(s, b=False, i=False):
        pos = 0
        for m in _TOKEN.finditer(s):
            add(s[pos:m.start()], b, i)
            tok = m.group(0)
            if tok.startswith("\\"):
                add(tok[1], b, i)
            elif tok.startswith("**"):
                procesar(tok[2:-2], True, i)
            elif tok.startswith("`"):
                add(tok[1:-1], b, i, mono=True)
            else:
                procesar(tok[1:-1], b, True)
            pos = m.end()
        add(s[pos:], b, i)

    procesar(texto)
    return p


# ---------------------------------------------------------------------------
# Documento
# ---------------------------------------------------------------------------
def _estilos(doc):
    st = doc.styles["Normal"]
    st.font.name = FUENTE
    st.font.size = Pt(TAM)
    st.font.color.rgb = rgb(NEGRO)
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FUENTE)
    _lang(rpr)
    pf = st.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.12
    pf.widow_control = True

    # Títulos: se usan los estilos «Heading» de Word para que salga el panel de navegación
    for nombre, tam, color in (("Heading 1", 13.5, VERDE_MUY_OSCURO), ("Heading 2", 12, VERDE_OSCURO),
                               ("Heading 3", 11, VERDE_OSCURO)):
        h = doc.styles[nombre]
        h.font.name = FUENTE
        h.font.size = Pt(tam)
        h.font.bold = True
        h.font.italic = False
        h.font.color.rgb = rgb(color)
        hr = h.element.get_or_add_rPr()
        rf = hr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts"); hr.insert(0, rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), FUENTE)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        hpf = h.paragraph_format
        hpf.keep_with_next = True
        hpf.line_spacing = 1.0
        if nombre == "Heading 1":
            hpf.space_before = Pt(14)
            hpf.space_after = Pt(8)
        else:
            hpf.space_before = Pt(10)
            hpf.space_after = Pt(4)
    # Banda verde clara con barra a la izquierda para h1 (como «4.0 Antes de empezar»)
    h1s = doc.styles["Heading 1"].element.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    for lado, sz, color, space in (("top", 2, VERDE_CLARO, 2), ("left", 36, VERDE, 4),
                                   ("bottom", 2, VERDE_CLARO, 2)):
        b = OxmlElement("w:" + lado)
        b.set(qn("w:val"), "single"); b.set(qn("w:sz"), str(sz))
        b.set(qn("w:space"), str(space)); b.set(qn("w:color"), color)
        bdr.append(b)
    h1s.append(bdr)
    _shd(h1s, VERDE_CLARO)
    ind = OxmlElement("w:ind"); ind.set(qn("w:left"), "113"); h1s.append(ind)
    _orden_ppr(h1s)


def nuevo_documento(titulo, subtitulo=None, confidencial=False, margenes_cm=(2.0, 2.0, 2.0, 2.0),
                    titulo_corto=None, portada=True, antetitulo="INSTALACIONES DOMÓTICAS · 2MT",
                    linea_info=None, horizontal=False):
    """Crea un documento A4 con el estilo del proyecto.

    titulo        Título del documento (se escribe arriba en grande si portada=True).
    subtitulo     Línea verde bajo el título (opcional).
    confidencial  True → banda roja «CONFIDENCIAL – solo profesorado» en cabecera y pie
                  de todas las páginas (y una línea roja bajo el título).
    margenes_cm   (superior, inferior, izquierdo, derecho) del texto.
    titulo_corto  Texto verde de la izquierda de la cabecera (por defecto, `titulo`).
    portada       True → escribe el bloque de título (antetítulo, título, subtítulo, línea).
    linea_info    Línea gris pequeña bajo el subtítulo (por defecto, «Home Assistant · I.E.S.
                  Trinidad Arroyo (Palencia)»).
    horizontal    True → A4 apaisado.
    """
    doc = Document()
    doc._capturas = []
    doc._figuras = 0
    doc._seccion_actual = ""
    doc._confidencial = confidencial
    _estilos(doc)
    cp = doc.core_properties
    cp.title = titulo
    cp.subject = "Instalaciones Domóticas · 2MT"
    cp.author = "I.E.S. Trinidad Arroyo"
    cp.language = "es-ES"
    cp.comments = ""
    cp.keywords = "Home Assistant; MQTT; 2MT"

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    if horizontal:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    sup, inf, izq, der = margenes_cm
    extra = 0.7 if confidencial else 0.0
    sec.top_margin = Cm(sup + 0.4 + extra)
    sec.bottom_margin = Cm(inf + 0.2 + extra)
    sec.left_margin = Cm(izq)
    sec.right_margin = Cm(der)
    sec.header_distance = Cm(0.9)
    sec.footer_distance = Cm(0.8)
    ancho_txt = (sec.page_width - sec.left_margin - sec.right_margin)
    doc._ancho_cm = ancho_txt / 360000.0

    # --- Cabecera
    hdr = sec.header
    hp = hdr.paragraphs[0]
    if confidencial:
        _banda_conf(doc, hp)
        hp = hdr.add_paragraph()
    hp.style = doc.styles["Normal"]
    hp.paragraph_format.tab_stops.add_tab_stop(ancho_txt, WD_TAB_ALIGNMENT.RIGHT)
    _espaciado(hp, 0, 0, 1.0)
    r = hp.add_run(titulo_corto or titulo)
    r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = rgb(VERDE_OSCURO)
    r = hp.add_run("\t" + CENTRO)
    r.font.size = Pt(8.5); r.font.color.rgb = rgb(GRIS)
    _p_borde(hp, "bottom", VERDE, sz=6, space=3)

    # --- Pie
    ftr = sec.footer
    fp = ftr.paragraphs[0]
    fp.style = doc.styles["Normal"]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _espaciado(fp, 0, 0, 1.0)
    r = fp.add_run("Página "); r.font.size = Pt(8.5); r.font.color.rgb = rgb(GRIS)
    _campo(fp, "PAGE", tam=9.5, color=GRIS_OSCURO, negrita=True)
    r = fp.add_run(" de "); r.font.size = Pt(8.5); r.font.color.rgb = rgb(GRIS)
    _campo(fp, "NUMPAGES", tam=8.5, color=GRIS)
    if confidencial:
        fb = ftr.add_paragraph()
        _espaciado(fb, 4, 0, 1.0)
        _banda_conf(doc, fb)

    # El documento nuevo trae un párrafo vacío: lo usamos para el primer contenido
    if portada:
        titulo_bloque(doc, titulo, subtitulo, antetitulo=antetitulo, linea_info=linea_info,
                      _usar_primero=True)
    return doc


def _banda_conf(doc, p):
    p.style = doc.styles["Normal"]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _espaciado(p, 0, 3, 1.0)
    r = p.add_run(TEXTO_CONF.upper())
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = rgb(BLANCO)
    _p_shd(p, ROJO)
    for lado in ("top", "bottom"):
        _p_borde(p, lado, ROJO, sz=12, space=1)


def _primer_parrafo(doc):
    ps = doc.paragraphs
    if len(ps) == 1 and not ps[0].text and not ps[0].runs:
        return ps[0]
    return doc.add_paragraph()


def titulo_bloque(doc, texto, subtitulo=None, antetitulo="INSTALACIONES DOMÓTICAS · 2MT",
                  linea_info=None, _usar_primero=False):
    """Bloque de título como el de la Práctica 4: antetítulo gris, título verde grande
    con barra verde a la izquierda, subtítulo verde y línea gris pequeña."""
    p = _primer_parrafo(doc) if _usar_primero else doc.add_paragraph()
    _espaciado(p, 0, 2, 1.0, juntos=True)
    r = p.add_run(antetitulo); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = rgb("595959")

    p = doc.add_paragraph()
    _espaciado(p, 0, 2, 1.0, juntos=True)
    _p_borde(p, "left", VERDE, sz=36, space=8)
    p.paragraph_format.left_indent = Cm(0.35)
    r = p.add_run(texto.upper())
    r.bold = True; r.font.size = Pt(20); r.font.color.rgb = rgb(VERDE_OSCURO)

    if subtitulo:
        p = doc.add_paragraph()
        _espaciado(p, 2, 0, 1.0, juntos=True)
        p.paragraph_format.left_indent = Cm(0.35)
        texto_rico(p, subtitulo, tam=13, color=VERDE_OSCURO)
    info = linea_info if linea_info is not None else "Home Assistant · I.E.S. Trinidad Arroyo (Palencia)"
    p = doc.add_paragraph()
    _espaciado(p, 2, 10, 1.0)
    p.paragraph_format.left_indent = Cm(0.35)
    if info:
        r = p.add_run(info); r.font.size = Pt(8.5); r.font.color.rgb = rgb(GRIS)
    if getattr(doc, "_confidencial", False):
        r = p.add_run(("   ·   " if info else "") + TEXTO_CONF)
        r.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = rgb(ROJO)
    return p


def titulo(doc, texto, subtitulo=None, **kw):
    """Título grande de documento (lo mismo que hace nuevo_documento con portada=True)."""
    return titulo_bloque(doc, texto, subtitulo, **kw)


def h1(doc, texto, salto_pagina=False):
    """Título de apartado: banda verde clara con barra verde (estilo «Heading 1»)."""
    p = doc.add_paragraph(style="Heading 1")
    p.paragraph_format.page_break_before = bool(salto_pagina)
    texto_rico(p, texto)
    doc._seccion_actual = texto
    return p


def h2(doc, texto):
    """Subapartado: texto verde en negrita (estilo «Heading 2»)."""
    p = doc.add_paragraph(style="Heading 2")
    texto_rico(p, texto)
    doc._seccion_actual = (doc._seccion_actual.split(" › ")[0] + " › " + texto) if doc._seccion_actual else texto
    return p


def h3(doc, texto):
    p = doc.add_paragraph(style="Heading 3")
    texto_rico(p, texto)
    return p


def parrafo(doc, texto="", alineacion="justificado", tam=None, color=None, negrita=False,
            cursiva=False, antes=None, despues=None, juntos=None, sangria_cm=None):
    """Párrafo normal con **negrita**, *cursiva* y `código`.
    alineacion: 'justificado' (por defecto), 'izquierda', 'centro', 'derecha'."""
    p = doc.add_paragraph()
    p.alignment = {"justificado": WD_ALIGN_PARAGRAPH.JUSTIFY, "izquierda": WD_ALIGN_PARAGRAPH.LEFT,
                   "centro": WD_ALIGN_PARAGRAPH.CENTER, "derecha": WD_ALIGN_PARAGRAPH.RIGHT}[alineacion]
    if antes is not None:
        p.paragraph_format.space_before = Pt(antes)
    if despues is not None:
        p.paragraph_format.space_after = Pt(despues)
    if juntos is not None:
        p.paragraph_format.keep_with_next = juntos
    if sangria_cm is not None:
        p.paragraph_format.left_indent = Cm(sangria_cm)
    texto_rico(p, texto, tam=tam, color=color, negrita=negrita, cursiva=cursiva)
    return p


def nota(doc, texto, color=GRIS):
    """Texto pequeño gris (aclaraciones, fuentes)."""
    return parrafo(doc, texto, alineacion="izquierda", tam=8.5, color=color, despues=4)


def lista(doc, items, numerada=False, inicio=1, tam=None, _nivel=0, _cont=None):
    """Lista con viñetas verdes o numerada (1., 2., …).
    items: lista de textos; un elemento que sea a su vez una lista se añade como
    subnivel del anterior. Admite **negrita**, *cursiva* y `código`."""
    n = inicio
    sangria = 0.55 + 0.6 * _nivel
    ultimo = None
    for it in items:
        if isinstance(it, (list, tuple)):
            lista(doc, it, numerada=False, tam=tam, _nivel=_nivel + 1)
            continue
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = p.paragraph_format
        pf.left_indent = Cm(sangria)
        pf.first_line_indent = Cm(-0.5)
        pf.tab_stops.add_tab_stop(Cm(sangria))
        pf.space_after = Pt(3)
        if numerada and _nivel == 0:
            r = p.add_run(f"{n}.\t"); r.bold = True; r.font.color.rgb = rgb(VERDE_OSCURO)
            n += 1
        else:
            r = p.add_run(("•" if _nivel == 0 else "–") + "\t"); r.bold = True
            r.font.color.rgb = rgb(VERDE if _nivel == 0 else VERDE_OSCURO)
        if tam:
            r.font.size = Pt(tam)
        texto_rico(p, it, tam=tam)
        ultimo = p
    if ultimo is not None and _nivel == 0:
        ultimo.paragraph_format.space_after = Pt(7)
    return ultimo


def _hueco(doc, pt=4):
    p = doc.add_paragraph()
    _espaciado(p, 0, 0, 1.0)
    r = p.add_run(); r.font.size = Pt(pt)
    p.paragraph_format.line_spacing = Pt(pt)
    return p


def _caja(doc, fondo, barra, ancho_cm=None, barra_sz=36, borde_fino=None, discontinua=False):
    """Tabla 1×1 que hace de recuadro. Devuelve la celda."""
    ancho = ancho_cm or doc._ancho_cm
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    _tabla_sin_bordes(t)
    _tabla_ancho_fijo(t, [ancho])
    c = t.cell(0, 0)
    if fondo:
        _celda_shd(c, fondo)
    if discontinua:
        spec = ("dashed", 8, barra)
        _celda_bordes(c, top=spec, left=spec, bottom=spec, right=spec)
    else:
        fino = ("single", 4, borde_fino) if borde_fino else None
        _celda_bordes(c, top=fino, left=("single", barra_sz, barra), bottom=fino, right=fino)
    _celda_margenes(c, 90, 160, 90, 140)
    _fila_no_partir(t.rows[0])
    return t, c


def cajon(doc, tipo, texto_o_lista, titulo_extra=None):
    """Cajón de color: tipo ∈ IDEA CLAVE, ¡OJO!, EJEMPLO, EN EL TALLER, PISTA, ¿POR QUÉ?

    texto_o_lista: un texto (puede llevar \\n para varios párrafos) o una lista:
      - el primer elemento va en la misma línea que el título del cajón;
      - los que empiezan por «- » salen con viñeta;
      - los demás, como párrafos.
    titulo_extra: texto en negrita tras el nombre del cajón («¡OJO! Antes del reset: …»)."""
    clave = tipo.strip().upper().replace("POR QUE", "POR QUÉ")
    if clave not in CAJONES:
        raise ValueError(f"Tipo de cajón desconocido: {tipo!r}. Usa uno de {list(CAJONES)}")
    barra, fondo, color_tit = CAJONES[clave]
    _hueco(doc, 3)
    t, c = _caja(doc, fondo, barra)
    if isinstance(texto_o_lista, str):
        elementos = texto_o_lista.split("\n")
    else:
        elementos = list(texto_o_lista)
    p = c.paragraphs[0]
    _espaciado(p, 0, 2, 1.1)
    r = p.add_run(clave); r.bold = True; r.font.size = Pt(TAM - 0.5); r.font.color.rgb = rgb(color_tit)
    p.add_run("  ")
    if titulo_extra:
        texto_rico(p, titulo_extra + " ", tam=TAM - 0.5, negrita=True)
    primero = True
    for el in elementos:
        if primero and not el.startswith("- "):
            texto_rico(p, el, tam=TAM - 0.5)
            primero = False
            continue
        primero = False
        q = c.add_paragraph()
        _espaciado(q, 0, 2, 1.1)
        if el.startswith("- "):
            q.paragraph_format.left_indent = Cm(0.45)
            q.paragraph_format.first_line_indent = Cm(-0.35)
            q.paragraph_format.tab_stops.add_tab_stop(Cm(0.45))
            rr = q.add_run("•\t"); rr.bold = True; rr.font.color.rgb = rgb(barra); rr.font.size = Pt(TAM - 0.5)
            texto_rico(q, el[2:], tam=TAM - 0.5)
        else:
            texto_rico(q, el, tam=TAM - 0.5)
    _hueco(doc, 5)
    return t


def tabla(doc, cabeceras, filas, anchos_cm=None, mono_cols=(), tam=9.5, negrita_col0=False,
          centrar_cols=(), alterna=True, color_cab=VERDE):
    """Tabla con cabecera verde (se repite en cada página), filas alternas y filas que
    no se parten entre páginas.

    cabeceras  lista de textos.
    filas      lista de filas (cada una, lista de textos con **negrita**/`código`).
               Si una fila es un texto suelto, sale como fila de grupo verde que ocupa
               todo el ancho («Bloque 1 · …»).
    anchos_cm  anchos de columna; por defecto, reparto igual del ancho de texto.
    mono_cols  índices de columnas en monoespaciada (IPs, entidades, temas…).
    negrita_col0  primera columna en negrita.
    centrar_cols  índices de columnas centradas."""
    ncol = len(cabeceras)
    if not anchos_cm:
        anchos_cm = [doc._ancho_cm / ncol] * ncol
    t = doc.add_table(rows=1, cols=ncol)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    _tabla_bordes(t)
    for i, txt in enumerate(cabeceras):
        c = t.rows[0].cells[i]
        _celda_shd(c, color_cab)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        _celda_margenes(c, 50, 90, 50, 90)
        p = c.paragraphs[0]
        _espaciado(p, 0, 0, 1.05)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in centrar_cols else WD_ALIGN_PARAGRAPH.LEFT
        texto_rico(p, txt, tam=tam, color=BLANCO, negrita=True)
    _fila_no_partir(t.rows[0], cabecera=True)
    k = 0
    for fila in filas:
        row = t.add_row()
        _fila_no_partir(row)
        if isinstance(fila, str):
            a = row.cells[0].merge(row.cells[-1])
            _celda_shd(a, VERDE_MEDIO)
            _celda_margenes(a, 40, 90, 40, 90)
            p = a.paragraphs[0]
            _espaciado(p, 0, 0, 1.05)
            texto_rico(p, fila, tam=tam, negrita=True, color=VERDE_MUY_OSCURO)
            k = 0
            continue
        for i in range(ncol):
            txt = fila[i] if i < len(fila) else ""
            c = row.cells[i]
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            _celda_margenes(c, 40, 90, 40, 90)
            if alterna and k % 2 == 1:
                _celda_shd(c, VERDE_FILA)
            p = c.paragraphs[0]
            _espaciado(p, 0, 0, 1.05)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in centrar_cols else WD_ALIGN_PARAGRAPH.LEFT
            txt = "" if txt is None else str(txt)
            lineas = txt.split("\n")
            for j, ln in enumerate(lineas):
                if j:
                    p = c.add_paragraph(); _espaciado(p, 0, 0, 1.05)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in centrar_cols else WD_ALIGN_PARAGRAPH.LEFT
                if i in mono_cols and ln and "`" not in ln:
                    run = p.add_run(ln)
                    _fuente_run(run, FUENTE_MONO)
                    run.font.size = Pt(tam - 0.5)
                    run.font.color.rgb = rgb("1F3864")
                    if negrita_col0 and i == 0:
                        run.bold = True
                else:
                    texto_rico(p, ln, tam=tam, negrita=(negrita_col0 and i == 0))
        k += 1
    _tabla_ancho_fijo(t, anchos_cm)
    _hueco(doc, 6)
    return t


def bloque_codigo(doc, texto, tam=None, titulo=None):
    """Bloque monoespaciado con fondo gris (temas MQTT, comandos). Respeta los espacios.
    Si no se da `tam`, se elige el tamaño (de 9 a 6,5 pt) para que la línea más larga
    quepa sin partirse. `titulo`: rótulo pequeño opcional encima del código."""
    texto = texto.replace("\r", "").strip("\n")
    lineas = texto.split("\n")
    ancho_pt = (doc._ancho_cm - 0.55) * 28.35
    maxlen = max((len(l) for l in lineas), default=1)
    if tam is None:
        tam = max(6.5, min(9.0, ancho_pt / (0.6 * max(maxlen, 1)) - 0.05))
        tam = int(tam * 2) / 2.0
    _hueco(doc, 3)
    t, c = _caja(doc, GRIS_CODIGO, "A6A6A6", barra_sz=18)
    _celda_margenes(c, 80, 140, 80, 100)
    p = c.paragraphs[0]
    _espaciado(p, 0, 0, 1.0)
    if titulo:
        r = p.add_run(titulo); r.bold = True; r.font.size = Pt(8); r.font.color.rgb = rgb(GRIS)
        p = c.add_paragraph(); _espaciado(p, 2, 0, 1.0)
    for j, ln in enumerate(lineas):
        if j:
            p = c.add_paragraph()
            _espaciado(p, 0, 0, 1.0)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(ln if ln else " ")
        _fuente_run(run, FUENTE_MONO)
        run.font.size = Pt(tam)
        run.font.color.rgb = rgb("1A1A1A")
        tnode = run._r.find(qn("w:t"))
        if tnode is not None:
            tnode.set(qn("xml:space"), "preserve")
    _hueco(doc, 5)
    return t


def imagen(doc, ruta, ancho_cm, pie=None, numerar=True):
    """Imagen centrada con pie opcional «Figura N. pie» (numeración automática)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _espaciado(p, 4, 2, 1.0, juntos=bool(pie))
    p.add_run().add_picture(ruta, width=Cm(min(ancho_cm, doc._ancho_cm)))
    if pie:
        q = doc.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _espaciado(q, 0, 8, 1.0)
        if numerar:
            doc._figuras += 1
            texto_rico(q, f"Figura {doc._figuras}. {pie}", tam=8.5, color="595959", cursiva=True)
        else:
            texto_rico(q, pie, tam=8.5, color="595959", cursiva=True)
    return p


def hueco_captura(doc, descripcion, alto_cm=6, ancho_cm=None):
    """Recuadro discontinuo con «[CAPTURA: descripcion]» para que el profesor pegue
    ahí su captura. Queda apuntada en la lista que devuelve capturas(doc)."""
    doc._capturas.append((descripcion, doc._seccion_actual))
    n = len(doc._capturas)
    _hueco(doc, 3)
    ancho = ancho_cm or doc._ancho_cm
    t, c = _caja(doc, "FAFAFA", "8C8C8C", ancho_cm=ancho, discontinua=True)
    trpr = t.rows[0]._tr.get_or_add_trPr()
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), str(int(alto_cm * 567)))
    h.set(qn("w:hRule"), "atLeast")
    trpr.insert(0, h)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _espaciado(p, 0, 0, 1.1)
    r = p.add_run(f"[CAPTURA: {descripcion}]")
    r.font.size = Pt(9.5); r.font.color.rgb = rgb("7F7F7F"); r.italic = True
    q = c.add_paragraph(); q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _espaciado(q, 2, 0, 1.0)
    r = q.add_run(f"captura {n}"); r.font.size = Pt(7.5); r.font.color.rgb = rgb("A6A6A6")
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    _hueco(doc, 6)
    return t


def capturas(doc, escribir=False, titulo_lista="Capturas que faltan"):
    """Devuelve la lista de capturas [(n, descripción, apartado)] del documento.
    escribir=True → además la añade al final del documento como tabla."""
    lista_c = [(i + 1, d, s) for i, (d, s) in enumerate(doc._capturas)]
    if escribir and lista_c:
        h2(doc, titulo_lista)
        tabla(doc, ["N.º", "Qué debe verse", "Apartado"],
              [[str(n), d, s] for n, d, s in lista_c],
              anchos_cm=[1.2, doc._ancho_cm - 6.2, 5.0], centrar_cols=(0,))
    return lista_c


def salto_pagina(doc):
    p = doc.add_paragraph()
    _espaciado(p, 0, 0, 1.0)
    p.add_run().add_break(WD_BREAK.PAGE)
    return p


def separador(doc):
    """Línea fina verde a todo el ancho."""
    p = doc.add_paragraph()
    _espaciado(p, 2, 6, 1.0)
    _p_borde(p, "bottom", VERDE, sz=4, space=1)
    return p


def recortable(doc, tarjetas, columnas=2, alto_cm=3.2):
    """Tarjetas recortables (p. ej. usuario y contraseña de cada grupo).
    tarjetas: lista de textos con marcado (\\n para varias líneas). Bordes discontinuos."""
    ancho = doc._ancho_cm / columnas
    filas = (len(tarjetas) + columnas - 1) // columnas
    t = doc.add_table(rows=filas, cols=columnas)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    _tabla_sin_bordes(t)
    _tabla_ancho_fijo(t, [ancho] * columnas)
    for i in range(filas * columnas):
        c = t.cell(i // columnas, i % columnas)
        spec = ("dashed", 6, "7F7F7F")
        _celda_bordes(c, top=spec, left=spec, bottom=spec, right=spec)
        _celda_margenes(c, 120, 200, 120, 200)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        if i < len(tarjetas):
            p = c.paragraphs[0]
            _espaciado(p, 0, 0, 1.15)
            texto_rico(p, tarjetas[i])
    for row in t.rows:
        _fila_no_partir(row, alto_cm=alto_cm)
    _hueco(doc, 6)
    return t


# ---------------------------------------------------------------------------
# Guardar y convertir
# ---------------------------------------------------------------------------
_ORDEN_XML = {
    "tcPr": ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap",
             "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark"],
    "tblPr": ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
              "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders",
              "shd", "tblLayout", "tblCellMar", "tblLook"],
    "rPr": ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike",
            "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish",
            "webHidden", "color", "spacing", "w", "kern", "position", "sz", "szCs", "highlight",
            "u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang",
            "eastAsianLayout", "specVanish", "oMath"],
}


def _ordenar_xml(elemento):
    """Pone en el orden que exige Word los hijos de tcPr, tblPr, rPr y pPr."""
    for tag, orden in _ORDEN_XML.items():
        pos = {qn("w:" + o): i for i, o in enumerate(orden)}
        for el in elemento.iter(qn("w:" + tag)):
            hijos = list(el)
            nuevos = sorted(hijos, key=lambda e: pos.get(e.tag, len(orden)))
            if nuevos != hijos:
                for h in hijos:
                    el.remove(h)
                for h in nuevos:
                    el.append(h)
    for ppr in elemento.iter(qn("w:pPr")):
        _orden_ppr(ppr)


def guardar(doc, ruta_docx):
    """Guarda el .docx (crea la carpeta si no existe). Antes ordena el XML para que
    Word lo abra sin quejas. Fija las propiedades (autor, fechas de hoy, palabras
    clave). Devuelve la ruta."""
    import datetime as _dt
    cp = doc.core_properties
    ahora = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0, tzinfo=None)
    cp.author = "I.E.S. Trinidad Arroyo"
    cp.last_modified_by = "I.E.S. Trinidad Arroyo"
    cp.created = ahora
    cp.modified = ahora
    # espacio duro en «Home Assistant»: LibreOffice parte las palabras clave por los espacios
    cp.keywords = "Home\u00a0Assistant; MQTT; 2MT"
    _ordenar_xml(doc.element)
    _ordenar_xml(doc.styles.element)
    for sec in doc.sections:
        for parte in (sec.header, sec.footer):
            if not parte.is_linked_to_previous:
                _ordenar_xml(parte._element)
    d = os.path.dirname(os.path.abspath(ruta_docx))
    os.makedirs(d, exist_ok=True)
    doc.save(ruta_docx)
    return ruta_docx


def a_pdf(ruta_docx, carpeta=None, timeout=180):
    """Convierte el .docx a PDF con LibreOffice y devuelve la ruta del PDF.
    Usa un perfil de LibreOffice propio en cada llamada para que varios procesos
    puedan convertir a la vez sin bloquearse."""
    ruta_docx = os.path.abspath(ruta_docx)
    carpeta = os.path.abspath(carpeta or os.path.dirname(ruta_docx))
    perfil = tempfile.mkdtemp(prefix="lo_perfil_")
    try:
        cmd = ["soffice", f"-env:UserInstallation=file://{perfil}", "--headless",
               "--convert-to", "pdf", "--outdir", carpeta, ruta_docx]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        pdf = os.path.join(carpeta, os.path.splitext(os.path.basename(ruta_docx))[0] + ".pdf")
        if not os.path.exists(pdf):
            raise RuntimeError("No se generó el PDF:\n" + res.stdout + res.stderr)
        return pdf
    finally:
        shutil.rmtree(perfil, ignore_errors=True)


def revisar_pdf(ruta_pdf, carpeta_png=None, dpi=60):
    """Rasteriza el PDF en PNG (una imagen por página) para mirarlo. Devuelve las rutas."""
    import glob
    carpeta_png = carpeta_png or os.path.splitext(ruta_pdf)[0] + "_png"
    os.makedirs(carpeta_png, exist_ok=True)
    base = os.path.join(carpeta_png, "p")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", ruta_pdf, base], check=True)
    return sorted(glob.glob(base + "*.png"))


# ---------------------------------------------------------------------------
# Demostración
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    out = "/home/claude/material-ha/_trabajo"
    os.makedirs(out, exist_ok=True)

    # Figura de prueba con matplotlib y los colores del proyecto
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    C = mpl_estilo()
    fig, ax = plt.subplots(figsize=(7, 2.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 2.6); ax.axis("off")
    cajas = [(0.2, "Simulador\n(CT 128)", C["MORADO"], C["MORADO_CLARO"]),
             (3.6, "Mosquitto\nde tu VM", C["AZUL"], C["AZUL_CLARO"]),
             (7.0, "Home Assistant\n(tu grupo)", C["VERDE"], C["VERDE_CLARO"])]
    for x, txt, borde, fondo in cajas:
        ax.add_patch(FancyBboxPatch((x, 0.5), 2.8, 1.5, boxstyle="round,pad=0.05",
                                    fc=fondo, ec=borde, lw=1.6))
        ax.text(x + 1.4, 1.25, txt, ha="center", va="center", fontsize=10, color=C["GRIS_OSCURO"])
    for x in (3.05, 6.45):
        ax.annotate("", xy=(x + 0.5, 1.25), xytext=(x, 1.25),
                    arrowprops=dict(arrowstyle="-|>", color=C["GRIS_OSCURO"], lw=1.4))
    ax.text(3.3, 2.2, "virtual/…", fontsize=9, family="monospace", color=C["GRIS_OSCURO"], ha="center")
    ax.text(6.7, 2.2, "discovery", fontsize=9, color=C["GRIS_OSCURO"], ha="center")
    png = os.path.join(out, "demo-figura.png")
    fig.savefig(png); plt.close(fig)

    doc = nuevo_documento("Demostración del estilo", "Todos los elementos del módulo **estilo_ha**",
                          titulo_corto="Demo · estilo común")
    h1(doc, "1. Texto")
    parrafo(doc, "Párrafo normal justificado con **negrita**, *cursiva* y `código` en línea, "
                 "por ejemplo la entidad `cover.p_cocina` o la dirección **`http://192.0.2.81`**. "
                 "Las comillas son «españolas». Un asterisco suelto se escribe con barra: 2 \\* 3.")
    h2(doc, "1.1. Listas")
    lista(doc, ["Primer punto con **negrita**.", "Segundo punto con `light.tira_rgb`.",
                ["Subpunto A.", "Subpunto B."], "Tercer punto."])
    lista(doc, ["Entra en tu HA.", "Ve a **Ajustes → Dispositivos y servicios → MQTT**.",
                "Pulsa *Configurar*."], numerada=True)
    h1(doc, "2. Cajones")
    cajon(doc, "IDEA CLAVE", "Un **broker** reparte los mensajes: los aparatos no se hablan directamente.")
    cajon(doc, "¡OJO!", ["El **reset** lo borra todo.", "- Haz capturas antes.", "- Exporta lo que quieras guardar."])
    cajon(doc, "EJEMPLO", "Publicar `{\"position\": 50}` en `virtual/p_cocina/set` deja la persiana a media altura.")
    cajon(doc, "EN EL TALLER", "Abre *Escuchar un tema* con `virtual/#` antes de publicar.")
    cajon(doc, "PISTA", "El comodín `+` vale por un nivel; `#`, por todos los que sigan.")
    cajon(doc, "¿POR QUÉ?", "¿Por qué cada VM tiene su propio Mosquitto? Porque Home Assistant solo admite **un** broker.",
          titulo_extra="¿Un broker o siete?")
    h1(doc, "3. Tablas")
    tabla(doc, ["Grupo", "Usuario", "VM", "Dirección"],
          ["Grupos del aula"] +
          [[f"Grupo {n}", f"user{n}", f"ha-alumno0{n} ({120 + n})", f"http://192.0.2.8{n}"] for n in range(1, 7)],
          anchos_cm=[2.5, 2.5, 5.0, 7.0], mono_cols=(1, 3), negrita_col0=True)
    tabla(doc, ["Nombre", "Tipo", "Imita a", "Comportamiento"],
          [["`p_cocina`, `p_hab1`, `p_pc`", "persiana", "módulo TS130F",
            "sube, baja, para y va a una posición; recorrido 20 / 22 / 25 s"],
           ["`enchufe_pc`, `e_frigo`, `e_tv`", "enchufe con medida", "TS011F",
            "potencia (W), corriente (A), tensión (V) y energía (kWh)\nPC variable, frigorífico con ciclos de compresor"]],
          anchos_cm=[4.2, 2.8, 2.8, 7.2])
    h1(doc, "4. Código")
    ordenes = (
        'virtual/bridge/request/permit_join            {"time": 254}\n'
        'virtual/bridge/request/device/add             {"tipo": "persiana", "nombre": "p_hab2", "recorrido": 18}\n'
        '    tipos: persiana, toldo, enchufe, luz, luz_regulable, luz_rgb, termostato\n'
        'virtual/p_cocina/set                          {"position": 50}      (o OPEN / CLOSE / STOP)\n'
        'virtual/ter_salon/set/current_heating_setpoint   22')
    bloque_codigo(doc, ordenes, titulo="Órdenes del simulador (extracto)")
    bloque_codigo(doc, "zigbee2mqtt/#\nhomeassistant/#")
    h1(doc, "5. Figuras y capturas")
    imagen(doc, png, 15, pie="Del simulador a tu Home Assistant (figura de prueba con mpl_estilo()).")
    hueco_captura(doc, "Ajustes → Dispositivos y servicios → MQTT con los 13 dispositivos del kit", alto_cm=5)
    h2(doc, "5.1. Tarjetas recortables")
    recortable(doc, [f"**Grupo {n}**\nUsuario: `user{n}`\nDirección: `http://192.0.2.8{n}`" for n in range(1, 5)],
               alto_cm=2.4)
    hueco_captura(doc, "Dashboard terminado con el tiempo y la hora con segundos", alto_cm=4)
    capturas(doc, escribir=True)
    ruta = guardar(doc, os.path.join(out, "demo-estilo.docx"))
    pdf = a_pdf(ruta)
    print("PDF:", pdf)

    doc2 = nuevo_documento("Demostración confidencial", "Página de prueba de la banda roja",
                           confidencial=True, titulo_corto="Demo · confidencial")
    h1(doc2, "Inventario")
    tabla(doc2, ["ID", "Nombre", "IP instituto"],
          [["121", "ha-alumno01", "192.0.2.81"], ["128", "aula-mqtt", "192.0.2.88"]],
          anchos_cm=[2, 6, 9], mono_cols=(1, 2))
    cajon(doc2, "¡OJO!", "Esta hoja no se deja nunca a la vista del alumnado.")
    bloque_codigo(doc2, "bash /root/reset-aula.sh")
    ruta2 = guardar(doc2, os.path.join(out, "demo-estilo-confidencial.docx"))
    print("PDF:", a_pdf(ruta2))
