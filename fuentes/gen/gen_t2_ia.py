# -*- coding: utf-8 -*-
"""2MT-HA-T2-ia: Tema 2 · Configuración de IA con Home Assistant (alumnado).
Apartados: 1 opencode · 2 git · 3 MCP · 4 uso de skills · 5 vibecoding (riesgos y buenas prácticas).
El apartado 3 sale del mismo texto que gen_ia_mcp.py (fuente única). Sin contraseñas, sin IPs y sin datos personales."""
import re
import sys
sys.path.insert(0, "/home/claude/herr")
sys.path.insert(0, "/home/claude/material-ha/_trabajo/gen")
import estilo_ha as E
import gen_ia_mcp as M
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

FIGD = "/home/claude/material-ha/_trabajo/fig/"
OUT = "/home/claude/material-ha/alumnado/2MT-HA-T2-ia.docx"

# ---------------------------------------------------------------- vídeos recomendados (canal MoureDev, de Brais Moure)
GIT = "https://www.youtube.com/watch?v=3GymExBkKjE"
SKL = "https://www.youtube.com/watch?v=UGh6q6rKVM4"
V3 = "https://www.youtube.com/watch?v=aDJNG_f2C3E&t=1897s"


def t(base, h=0, m=0, s=0):
    return "%s&t=%ds" % (base, h * 3600 + m * 60 + s)


def enlace(p, texto, url, tam=9.5):
    """Hipervínculo de Word dentro del párrafo p."""
    rid = p.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                           is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), rid)
    r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    f = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        f.set(qn(a), E.FUENTE)
    rpr.append(f)
    c = OxmlElement("w:color"); c.set(qn("w:val"), "1F5FBF"); rpr.append(c)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(tam * 2))); rpr.append(sz)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rpr.append(u)
    r.append(rpr)
    tx = OxmlElement("w:t"); tx.text = texto; tx.set(qn("xml:space"), "preserve"); r.append(tx)
    h.append(r); p._p.append(h)


def videos(doc, intro, items):
    """Recuadro «Míralo en vídeo» con enlaces. items = [(texto, url)]."""
    tb = E.cajon(doc, "PISTA", "**Míralo en vídeo.** " + intro)
    celda = tb.rows[0].cells[0]
    for texto, url in items:
        p = celda.add_paragraph()
        p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Pt(10)
        r = p.add_run("▶  "); r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0x1F, 0x5F, 0xBF)
        enlace(p, texto, url)
    return tb



def lista_num(doc, items):
    """Lista numerada con sitio para números de dos cifras."""
    from docx.shared import Cm
    ult = None
    for k, it in enumerate(items, 1):
        p = E.lista(doc, [it], numerada=True, inicio=k)
        pf = p.paragraph_format
        pf.tab_stops.clear_all()
        pf.left_indent = Cm(0.85); pf.first_line_indent = Cm(-0.8)
        pf.tab_stops.add_tab_stop(Cm(0.85)); pf.space_after = Pt(3)
        ult = p
    if ult is not None:
        ult.paragraph_format.space_after = Pt(7)
    return ult


# ---------------------------------------------------------------- figuras
def _caja(ax, x, y, w, h, t1, t2, col, fondo, f1=10.5, f2=8.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=fondo, ec=col, lw=2))
    ax.text(x + w / 2, y + h - 4.0, t1, ha="center", va="center", fontsize=f1, fontweight="bold", color="#222")
    ax.text(x + w / 2, y + (h - 6) / 2, t2, ha="center", va="center", fontsize=f2, color="#333", linespacing=1.35)


def fig_piezas():
    C = E.mpl_estilo()
    fig, ax = plt.subplots(figsize=(7.4, 2.9), dpi=260)
    ax.set_xlim(0, 110); ax.set_ylim(0, 33); ax.axis("off")
    datos = [("opencode", "el agente:\nhabla contigo\ny trabaja\npor pasos", C["AZUL"], "#DEEAF6"),
             ("git", "la red de\nseguridad:\nguarda versiones\ny vuelve atrás", C["OCRE"], "#FFF2CC"),
             ("MCP", "las manos:\nherramientas\npara leer y\ncambiar HA", C["VERDE"], "#E2EFDA"),
             ("skills", "el saber hacer:\ninstrucciones\npara cada tipo\nde tarea", C["MORADO"], "#ECE6F4"),
             ("tú", "la cabeza:\ndecides,\nrevisas y\ncompruebas", C["ROJO"], "#FCE4D6")]
    w = 19.6
    for k, (a, b, col, fo) in enumerate(datos):
        _caja(ax, 1 + k * 22, 8, w, 20, a, b, col, fo)
    ax.text(55, 2.6, "Tema 2: cinco piezas para trabajar con IA en Home Assistant sin romper nada.",
            ha="center", fontsize=8.6, fontweight="bold", color="#222")
    p = FIGD + "t2_piezas.png"; fig.savefig(p, bbox_inches="tight", pad_inches=0.08, facecolor="white"); plt.close(fig)
    return p


def fig_git():
    C = E.mpl_estilo()
    fig, ax = plt.subplots(figsize=(7.4, 3.3), dpi=260)
    ax.set_xlim(0, 110); ax.set_ylim(0, 37); ax.axis("off")
    _caja(ax, 1, 11, 18, 19, "Tu carpeta", "los ficheros\ncomo están ahora\n(los cambias tú\no la IA)", C["PIZARRA"], "#EDF0F4")
    _caja(ax, 31, 11, 18, 19, "Preparado", "lo que has\nelegido para la\npróxima foto\n(*staging*)".replace("*", ""), C["OCRE"], "#FFF2CC")
    _caja(ax, 61, 11, 18, 19, "Repositorio", "el historial de\nfotos (commits),\nen la carpeta\n.git", C["VERDE"], "#E2EFDA")
    _caja(ax, 91, 11, 18, 19, "GitHub", "una copia en\ninternet\n(el remoto)", C["AZUL"], "#DEEAF6")

    def fl(x1, x2, y, txt, col, arriba=True):
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
        ax.text((x1 + x2) / 2, y + (1.3 if arriba else -1.5), txt, ha="center", va="bottom" if arriba else "top",
                fontsize=7.6, color=col, family="Liberation Mono")
    fl(20.2, 29.8, 24, "git add", C["OCRE"])
    fl(50.2, 59.8, 24, "git commit", C["VERDE"])
    fl(80.2, 89.8, 24, "git push", C["AZUL"])
    fl(89.8, 80.2, 16, "git pull", C["AZUL"], False)
    fl(60, 19, 6.5, "git restore  (deja un fichero como en la última foto)", C["ROJO"], False)
    ax.text(40, 34, "en tu máquina (o en tu VM de HA)", ha="center", fontsize=8, style="italic", color="#444")
    p = FIGD + "t2_git.png"; fig.savefig(p, bbox_inches="tight", pad_inches=0.08, facecolor="white"); plt.close(fig)
    return p


def fig_flujo():
    C = E.mpl_estilo()
    fig, ax = plt.subplots(figsize=(7.4, 2.5), dpi=260)
    ax.set_xlim(0, 110); ax.set_ylim(0, 25); ax.axis("off")
    pasos = [("1 · Guarda", "commit de lo\nque funciona", C["OCRE"], "#FFF2CC"),
             ("2 · Planea", "agente Plan:\nque explique\nqué va a\nhacer", C["AZUL"], "#DEEAF6"),
             ("3 · Un cambio", "agente Build:\nuna cosa\npequeña\ncada vez", C["VERDE"], "#E2EFDA"),
             ("4 · Comprueba", "míralo tú\nen HA y lee\nlos cambios\n(git diff)", C["ROJO"], "#FCE4D6"),
             ("5 · Guarda", "commit con un\nmensaje claro", C["OCRE"], "#FFF2CC")]
    for k, (a, b, col, fo) in enumerate(pasos):
        x = 1 + k * 22
        _caja(ax, x, 1.5, 18.5, 22, a, b, col, fo, f1=9, f2=8.2)
        if k < 4:
            ax.annotate("", xy=(x + 21.6, 12.5), xytext=(x + 19.2, 12.5),
                        arrowprops=dict(arrowstyle="-|>", color="#555", lw=2))
    p = FIGD + "t2_flujo.png"; fig.savefig(p, bbox_inches="tight", pad_inches=0.08, facecolor="white"); plt.close(fig)
    return p


# ---------------------------------------------------------------- documento
def main():
    M.figura()
    f_piezas, f_git, f_flujo = fig_piezas(), fig_git(), fig_flujo()
    doc = E.nuevo_documento("Tema 2 · Configuración de IA con Home Assistant",
                            "opencode, git, MCP, skills y vibecoding",
                            titulo_corto="Tema 2 · IA con Home Assistant")
    E.parrafo(doc, "En el Tema 1 viste qué es Home Assistant (HA) y cómo funciona por dentro. En este tema vas a usar una "
                   "**inteligencia artificial (IA)** para **configurarlo** y para **buscar fallos**. No es magia: son cinco "
                   "piezas que hay que entender, porque la IA trabaja deprisa, pero también se equivoca deprisa.")
    E.imagen(doc, f_piezas, 17, pie="Las cinco piezas del tema.")
    E.tabla(doc, ["Apartado", "Qué vas a aprender"], [
        ["1. opencode", "Qué es un agente de IA, cómo se usa opencode en HA y en tu PC, y cómo pedirle las cosas."],
        ["2. git", "Guardar versiones de tu configuración con *commits* y volver atrás cuando algo se rompe."],
        ["3. MCP", "Cómo se conecta la IA con Home Assistant y qué servidor MCP usamos."],
        ["4. Uso de skills", "Qué es una *skill*, en qué se diferencia de un fichero Markdown normal y cómo la usa la IA."],
        ["5. Vibecoding", "Qué es, qué riesgos tiene y las buenas prácticas para trabajar con cabeza."],
    ], anchos_cm=[3.6, 13.4], negrita_col0=True)
    E.nota(doc, "Qué es una entidad, un dashboard o una automatización está en el Tema 1 («Teoría: Home Assistant y MQTT»). "
                "Cómo se instala y se conecta cada herramienta, paso a paso, está en la práctica de puesta en marcha.")

    # ================================================================== 1 OPENCODE
    E.h1(doc, "1. opencode", salto_pagina=True)
    E.h2(doc, "1.1 Qué es un agente de IA")
    E.parrafo(doc, "Un **chat de IA** contesta y ya está: tú copias y pegas. Un **agente** va más allá: recibe un encargo y "
                   "**trabaja por pasos** hasta terminarlo. En cada paso decide qué hacer, usa una **herramienta** (leer un "
                   "fichero, ejecutar un comando, preguntar a HA…), mira el resultado y sigue.")
    E.tabla(doc, ["Pieza", "Qué es", "En clase"], [
        ["Modelo", "El «cerebro»: la IA que lee y escribe texto. Está en internet.", "un modelo gratuito de los que ofrece opencode"],
        ["Agente", "El programa que habla con el modelo, le da herramientas y repite el ciclo.", "**opencode**"],
        ["Herramientas", "Lo que el agente puede hacer: leer y editar ficheros, ejecutar comandos, usar MCP.",
         "las de opencode y las de ha-mcp"],
        ["Contexto", "Todo lo que el modelo tiene delante en ese momento: tu petición, los ficheros leídos, los "
                     "resultados. Es limitado: si se llena, la IA «olvida» lo primero.", "se vacía al empezar una sesión nueva"],
    ], anchos_cm=[2.9, 8.6, 5.5], negrita_col0=True)
    E.parrafo(doc, "**opencode** es un agente de programación de **código abierto**. Se usa en un **terminal**, en una "
                   "**aplicación de escritorio** o en el **navegador**, y sirve con modelos de muchas empresas distintas.")
    E.cajon(doc, "IDEA CLAVE", "opencode **no es la IA**: es el programa que la maneja. El modelo se puede cambiar por otro "
                               "y opencode sigue siendo el mismo. Lo mismo pasa con otros agentes (Claude Code, Codex, Cursor…): "
                               "lo que aprendas aquí te vale para todos.")

    E.h2(doc, "1.2 Dónde lo usamos: en HA y en tu PC")
    E.tabla(doc, ["", "opencode en Home Assistant", "opencode en tu PC"], [
        ["Qué es", "Una app de HA: un terminal dentro del navegador, en la barra lateral", "La aplicación de escritorio o el programa de terminal"],
        ["Qué ve", "Los **ficheros de configuración** de tu HA (la carpeta `/config`) y sus registros",
         "Las carpetas de tu PC que le abras. HA lo ve **solo por MCP**"],
        ["Para qué", "Editar YAML, buscar en los registros, usar **git** sobre tu configuración",
         "Dashboards y automatizaciones por MCP, documentación, tus apuntes"],
        ["Ojo", "Lo que hace ahí va **directo a tu HA**", "No puede tocar los ficheros de HA; solo lo que deje el servidor MCP"],
    ], anchos_cm=[2.2, 7.4, 7.4], negrita_col0=True, tam=9)
    E.hueco_captura(doc, "La app de opencode abierta desde la barra lateral de Home Assistant, con el terminal y el cursor "
                         "listo para escribir", alto_cm=4.2)
    E.cajon(doc, "¡OJO!", "En HA, **guardar un fichero no es aplicarlo**. Después de cambiar YAML hay que **comprobar la "
                          "configuración** y **recargar** (o reiniciar). Pídele a la IA que lo compruebe antes de dar nada por hecho.")

    E.h2(doc, "1.3 El modelo: los gratuitos")
    E.parrafo(doc, "opencode ofrece algunos **modelos gratuitos** que se pueden usar sin pagar. En clase usamos esos. Se "
                   "eligen con `/models`.")
    E.lista(doc, [
        "**Cambian a menudo.** Son gratis «por tiempo limitado»: hoy hay unos (por ejemplo, Big Pickle o DeepSeek V4.1 "
        "Flash Free) y dentro de un mes puede haber otros. Si uno desaparece o falla, se elige otro.",
        "**No son los mejores.** Son más flojos que los de pago: se equivocan más y se lían antes. Razón de más para "
        "revisar lo que hacen.",
        "**Pueden tener límites** de peticiones al día o ir lentos cuando hay mucha gente.",
    ])
    E.cajon(doc, "¡OJO!", ["**Lo que escribes no es privado.** Varios modelos gratuitos **guardan lo que les mandas** y lo "
                           "usan para mejorar el modelo. Por eso, a la IA **nunca** se le da:",
                           "- contraseñas, ni la dirección secreta del servidor MCP;",
                           "- datos personales tuyos, de tus compañeros o de tu familia;",
                           "- nada que no enseñarías en la pizarra."])

    E.h2(doc, "1.4 Primeros pasos")
    E.parrafo(doc, "opencode trabaja **dentro de una carpeta**: lo que hay en ella es su «proyecto». Se entra en la "
                   "carpeta y se arranca:")
    E.bloque_codigo(doc, "cd /config        (en HA: la carpeta de configuración)\nopencode")
    E.parrafo(doc, "Después escribes lo que quieres, con tus palabras, y pulsas **Intro**.")
    E.cajon(doc, "IDEA CLAVE", "opencode tiene **muchísimas** opciones: agentes a medida, órdenes propias, temas, "
                               "servidores… **Casi todo nos queda fuera.** Para trabajar en clase basta con estas seis cosas:")
    E.tabla(doc, ["Escribes", "Qué hace", "Cuándo"], [
        ["`/models`", "Elegir el modelo", "Al empezar, o si el modelo falla"],
        ["`/agents`  (o Mayús+Tab)", "Cambiar entre **Plan** y **Build** (apartado 1.5)", "Antes de cada encargo"],
        ["`@fichero`", "Adjuntar un fichero a tu mensaje (por ejemplo, `@automations.yaml`)", "Para que mire justo ese fichero"],
        ["`/undo`", "Deshacer tu último mensaje **y lo que la IA hizo después**", "Cuando se ha equivocado"],
        ["`/new`", "Empezar una sesión nueva, con el contexto vacío", "Cuando se lía o cambias de tarea"],
        ["`/connect`", "Conectar un proveedor de modelos", "Solo en la puesta en marcha"],
    ], anchos_cm=[4.4, 7.6, 5.0])
    videos(doc, "En el canal **MoureDev** (Brais Moure) hay un vídeo sobre esto. **No hace falta verlo entero**: "
                "mira solo la parte enlazada, que es la que usamos.", [
        ("Vídeo de MoureDev, desde el minuto 31:37", V3),
    ])

    E.h2(doc, "1.5 Dos agentes: Plan y Build")
    E.tabla(doc, ["Agente", "Qué hace", "Cuándo"], [
        ["**Plan**", "Mira, lee y **propone un plan**. No cambia tus ficheros.", "Siempre **primero**, y para preguntar o diagnosticar"],
        ["**Build**", "**Hace** los cambios: edita ficheros, ejecuta comandos, usa las herramientas.", "Cuando el plan te convence"],
    ], anchos_cm=[2.4, 8.6, 6.0])
    E.cajon(doc, "EN EL TALLER", "Es como en el cuadro eléctrico: **primero el esquema, después el cableado**. Con Plan "
                                 "ves el esquema de lo que la IA piensa hacer; si está mal, corregirlo cuesta una frase. "
                                 "Con Build ya está cableando.")

    E.h2(doc, "1.6 Permisos e instrucciones")
    E.lista(doc, [
        "**Permisos.** Cada acción puede estar **permitida**, **prohibida** o **con pregunta** (opencode te pide permiso "
        "antes). Cuando pregunte, **lee** qué quiere hacer: qué fichero, qué comando, qué herramienta.",
        "**Instrucciones del proyecto.** En un fichero de texto (lo habitual es `AGENTS.md`) le dejas escrito lo que "
        "tiene que saber siempre: cómo se llaman tus cosas, qué no debe tocar, cómo quieres que trabaje. Lo lee al "
        "empezar cada sesión.",
    ])
    E.bloque_codigo(doc, "# Mi Home Assistant (Grupo 3)\n"
                         "- Es un HA de prácticas con dispositivos virtuales (fabricante «Virtual (aula)»).\n"
                         "- No toques la app Mosquitto broker ni la integración MQTT.\n"
                         "- Antes de cambiar nada, enséñame el plan. Un cambio cada vez.\n"
                         "- Después de cada cambio, comprueba la configuración.",
                    titulo="Ejemplo de AGENTS.md")
    E.hueco_captura(doc, "opencode pidiendo permiso antes de usar una herramienta o editar un fichero, con las opciones "
                         "de aceptar o rechazar a la vista", alto_cm=4.2)

    E.h2(doc, "1.7 Cómo pedir las cosas")
    E.parrafo(doc, "La IA no sabe lo que tienes en la cabeza. Una buena petición dice **cuatro cosas**: qué hay, qué "
                   "quieres, qué no debe tocar y cómo se comprueba.")
    E.tabla(doc, ["Mal", "Bien"], [
        ["«Hazme un dashboard chulo.»",
         "«Crea un dashboard nuevo llamado “Persianas grupo 3” con una tarjeta para cada una de las tres persianas "
         "(`cover.p_cocina` y las otras dos: búscalas) y otra para el toldo. No toques los demás dashboards. Al terminar, "
         "dime qué entidades has usado.»"],
        ["«No va la persiana, arréglalo.»",
         "«La persiana `cover.p_cocina` no baja cuando pulso su tarjeta. **No cambies nada todavía.** Mira su estado, los "
         "registros y las automatizaciones que la usan, y dime qué crees que pasa.»"],
    ], anchos_cm=[4.6, 12.4], tam=9)
    E.cajon(doc, "PISTA", "Peticiones **pequeñas**, una detrás de otra. Si la conversación se alarga y la IA empieza a "
                          "repetirse o a olvidar cosas, abre una **sesión nueva** (`/new`) y cuéntale solo lo necesario.")

    # ================================================================== 2 GIT
    E.h1(doc, "2. git", salto_pagina=True)
    E.h2(doc, "2.1 Qué es y por qué lo necesitas")
    E.parrafo(doc, "**git** es un programa de **control de versiones**: guarda «fotos» de una carpeta cada vez que tú se "
                   "lo dices, y te deja ver qué ha cambiado entre una y otra y **volver a cualquiera de ellas**. Lo usan "
                   "casi todos los programadores del mundo.")
    E.cajon(doc, "¿POR QUÉ?", "**¿Por qué con IA es imprescindible?** Porque la IA puede cambiar veinte líneas en tres "
                              "ficheros en cinco segundos. Sin git, si algo deja de funcionar, no sabes qué ha tocado ni "
                              "cómo estaba antes. Con git lo ves línea a línea y lo deshaces con una orden.")
    E.cajon(doc, "IDEA CLAVE", ["**¿Cuánto git vamos a usar? Muy poco.** git es un programa enorme y complicado "
                                "(ramas, fusiones, conflictos…) y casi todo **nos queda muy fuera**. En clase:",
                                "- usamos solo **dos órdenes**: `git add` y `git commit`;",
                                "- y casi siempre **las ejecuta la IA**: tú se lo pides («guarda un commit con lo que funciona»).",
                                "Lo que sí tienes que entender es **cómo está organizado** un repositorio, para saber "
                                "**consultar** el historial y **volver a una versión anterior** cuando haga falta."])
    E.h2(doc, "2.2 Las palabras de git")
    E.tabla(doc, ["Palabra", "Qué es"], [
        ["Repositorio (*repo*)", "Una carpeta vigilada por git, con todo su historial. El historial vive en la subcarpeta escondida `.git`."],
        ["*Commit*", "Una **foto** de la carpeta en un momento, con un mensaje que explica el cambio. Es lo más importante (apartado 2.3)."],
        ["Preparar (*add*, *staging*)", "Elegir qué cambios entran en la próxima foto."],
        ["Historial (*log*)", "La lista de commits, del más nuevo al más viejo."],
        ["Diferencia (*diff*)", "Qué líneas se han añadido, quitado o cambiado."],
        ["`.gitignore`", "Fichero con la lista de lo que git **no** debe guardar (contraseñas, bases de datos, registros)."],
        ["Remoto", "Una copia del repositorio en otro sitio, normalmente en **GitHub**."],
    ], anchos_cm=[4.4, 12.6], negrita_col0=True)
    E.imagen(doc, f_git, 17, pie="Por dónde pasa un cambio: tu carpeta, lo preparado, el repositorio y GitHub.")

    E.h2(doc, "2.3 Qué es exactamente un commit")
    E.parrafo(doc, "Un commit guarda cinco cosas: el **estado de los ficheros**, un **mensaje**, el **autor**, la **fecha** "
                   "y un **identificador** único (una ristra de letras y números; con las siete primeras basta para "
                   "nombrarlo, por ejemplo `a3f9c21`). Los commits se encadenan: cada uno sabe cuál es el anterior.")
    E.tabla(doc, ["Mensaje malo", "Mensaje bueno", "Por qué"], [
        ["`cambios`", "`Añade dashboard de persianas del grupo 3`", "Dice **qué** se ha hecho"],
        ["`arreglo`", "`Corrige la entidad del toldo en la automatización del viento`", "Dentro de un mes se entiende"],
        ["`cosas de la IA`", "`Tira RGB en rojo si el frigorífico pasa de 300 W`", "Un commit, **un** cambio"],
    ], anchos_cm=[3.4, 8.8, 4.8], tam=9)
    E.cajon(doc, "IDEA CLAVE", "**Commits pequeños y frecuentes.** Un commit por cada cosa que funciona. Si haces uno solo "
                               "al final de la clase con todo junto, cuando algo falle no sabrás en qué cambio se rompió.")

    E.h2(doc, "2.4 Las dos órdenes que usamos")
    E.tabla(doc, ["Orden", "Qué hace"], [
        ["`git add .`", "**Prepara** todos los cambios para la próxima foto"],
        ["`git commit -m \"mensaje\"`", "**Hace la foto** de lo preparado, con su mensaje"],
    ], anchos_cm=[5.6, 11.4])
    E.parrafo(doc, "Van siempre juntas y en ese orden: primero preparar, después la foto. Normalmente no las escribes "
                   "tú: **se lo pides a la IA** y ella las ejecuta. Tú lees lo que va a hacer y dices que sí.")
    E.bloque_codigo(doc, "Tú:  Antes de empezar, guarda un commit con lo que hay ahora.\n"
                         "IA:  git add .\n"
                         "     git commit -m \"Antes de pedir el dashboard de persianas\"\n\n"
                         "       ... la IA hace el dashboard y tú compruebas que funciona ...\n\n"
                         "Tú:  Funciona. Guarda un commit que diga lo que has hecho.\n"
                         "IA:  git add .\n"
                         "     git commit -m \"Añade dashboard de persianas del grupo 3\"",
                    titulo="Una sesión normal: tú pides y la IA ejecuta")
    E.hueco_captura(doc, "opencode en el terminal de HA ejecutando «git add .» y «git commit» después de pedírselo, "
                         "con el mensaje del commit a la vista", alto_cm=3.6)

    E.h2(doc, "2.5 Consultar y volver atrás")
    E.parrafo(doc, "Aquí es donde hace falta **entender la estructura**: como cada commit es una foto con su mensaje "
                   "y su identificador, puedes pedirle a la IA que mire o recupere cualquiera de ellas.")
    E.tabla(doc, ["Lo que quieres", "Lo que le pides a la IA", "Lo que ella usa"], [
        ["Saber qué ha cambiado desde la última foto", "«¿Qué ficheros has tocado? Enséñame los cambios.»", "`git status`, `git diff`"],
        ["Ver las fotos que hay", "«Enséñame el historial de commits.»", "`git log --oneline`"],
        ["Ver cómo estaba algo antes", "«¿Cómo era el dashboard en el commit a3f9c21?»", "`git show`, `git diff`"],
        ["Tirar un cambio que **aún no** tiene commit", "«Deja `automations.yaml` como en el último commit.»", "`git restore`"],
        ["Deshacer un commit **ya hecho**", "«Deshaz el commit a3f9c21 con un commit nuevo.»", "`git revert`"],
    ], anchos_cm=[5.2, 7.6, 4.2], tam=9)
    E.cajon(doc, "PISTA", "Por eso importan los **mensajes claros**: dentro de dos semanas, «el commit del dashboard de "
                          "persianas» se encuentra; «cambios» no.")
    E.cajon(doc, "¡OJO!", "`git reset --hard` **borra** los cambios sin preguntar y no se recupera lo que no estaba en un "
                          "commit. Si la IA propone usarla, **di que no** y pídele `restore` o `revert`.")

    E.h2(doc, "2.6 Qué repositorios hay")
    E.parrafo(doc, "Cuando se habla de «el repositorio» conviene saber **de cuál**. En tu montaje hay **tres sitios** "
                   "con repositorios, y solo uno está dentro de Home Assistant:")
    E.tabla(doc, ["", "Dónde está", "Qué guarda", "Quién hace los commits"], [
        ["**1. El de tu Home Assistant**", "Dentro de tu VM, en la carpeta `/config`", "La configuración de tu HA. **Es el importante**",
         "La IA cuando se lo pides (o tú)"],
        ["**2. Los de tu PC**", "En carpetas de tu ordenador", "Repositorios que te bajas de GitHub para mirarlos, y tus notas",
         "Casi nunca haces commits: sobre todo **lees**"],
        ["**3. Los de GitHub**", "En internet", "**El tuyo**: la copia del nº 1, privada. **Los de otros**: públicos, para sacar ideas",
         "El tuyo recibe lo que subes desde el nº 1. En los de otros no escribes"],
    ], anchos_cm=[4.0, 3.9, 5.2, 3.9], tam=9)
    E.cajon(doc, "IDEA CLAVE", "**No se mezclan solos.** Un commit hecho en tu HA se queda en tu HA hasta que se **sube** "
                               "a GitHub. Y lo que hay en GitHub no llega a tu HA hasta que alguien lo **baja**. Cuando la IA "
                               "diga «he hecho commit», pregúntate: ¿en cuál de los tres?")

    E.h2(doc, "2.7 El repositorio de tu Home Assistant")
    E.lista(doc, [
        "**Dónde está.** En la carpeta de configuración de HA: el historial vive en `/config/.git`. Según por dónde "
        "entres, esa misma carpeta puede aparecer con otro nombre, `/homeassistant`: **es la misma**, no hay dos.",
        "**Quién hace commits.** Las sesiones de opencode (la IA, cuando se lo pides) y tú. En una instalación de "
        "verdad se suele añadir además un **commit automático cada noche**, para que nunca pase un día sin foto.",
        "**No todo es YAML.** Lo que haces desde la interfaz (dashboards, muchas automatizaciones, ayudantes) se "
        "guarda en la carpeta escondida `.storage`, en ficheros JSON que escribe el propio HA. git también los vigila, "
        "pero no se editan a mano: se cambian desde la interfaz o por MCP.",
        "**Hay cosas que se dejan fuera a propósito**, con `.gitignore`: contraseñas, bases de datos, registros y lo "
        "que instala HACS.",
    ])
    E.tabla(doc, ["Se queda fuera de git", "Por qué", "Cómo se recupera"], [
        ["`secrets.yaml` y los ficheros de acceso", "Son contraseñas y claves", "No se recuperan de git: se guardan aparte"],
        ["Bases de datos (`*.db`) y registros (`*.log`)", "Son enormes y cambian cada segundo", "No hace falta: HA los vuelve a crear"],
        ["Lo de HACS: `www/community/` y `custom_components/`", "Es código de otros, y ocupa mucho", "Se vuelve a instalar, o sale de una **copia de seguridad** de HA"],
        ["Imágenes y ficheros grandes", "git está pensado para texto", "De la copia de seguridad"],
    ], anchos_cm=[5.6, 5.2, 6.2], tam=9)
    E.bloque_codigo(doc, "secrets.yaml\n*.db\n*.db-shm\n*.db-wal\n*.log*\n.storage/auth*\n.cloud/\nbackups/\ntts/\n"
                         "www/community/\ncustom_components/",
                    titulo="Un .gitignore para /config")

    E.h2(doc, "2.8 GitHub: tu copia y los repositorios de otros")
    E.parrafo(doc, "**git** es el programa; **GitHub** es una web donde se guardan repositorios de git. No son lo mismo: "
                   "git funciona sin GitHub y sin internet. Un repositorio guardado en GitHub se llama **remoto**.")
    E.lista(doc, [
        "**Cada alumno, su cuenta.** La cuenta de GitHub es **personal**: no se comparte. Así cada commit lleva el "
        "nombre de quien lo hizo, y la cuenta y el trabajo son tuyos cuando acabe el curso.",
        "**El remoto del grupo.** El repositorio de vuestra VM se sube a un repositorio **privado** de GitHub, al que "
        "entráis todos los del grupo. Sirve para dos cosas: **compartir** el trabajo entre vosotros y tener una "
        "**copia fuera de la VM**. Cómo se hace lo verás en la práctica; también lo ejecuta la IA.",
        "**Los de otros.** En GitHub hay miles de repositorios públicos con dashboards, tarjetas y automatizaciones. "
        "Se pueden **leer** para sacar ideas o **copiar** a tu PC. Lo verás en la práctica de los dashboards.",
    ])
    E.cajon(doc, "¡OJO!", "Lo que se sube a un repositorio **público** lo ve todo el mundo, y borrarlo después no lo "
                          "borra del historial. **Antes de subir nada**, pregunta a la IA qué ficheros van a subirse y míralos.")

    E.h2(doc, "2.9 Se puede trabajar en local")
    E.parrafo(doc, "git **no necesita** GitHub ni internet. En muchas casas el repositorio de `/config` **no tiene "
                   "remoto** y nunca se sube a ningún sitio, porque la configuración de una vivienda es privada. Se "
                   "trabaja **en local**, y funciona. Pero hay que saber qué te protege y qué no.")
    E.tabla(doc, ["Lo que te protege", "El punto débil: todo en la misma caja"], [
        ["**git es tu máquina del tiempo.** Con el historial puedes volver a cualquier commit.",
         "Si Home Assistant y sus copias están en el **mismo aparato** y ese aparato muere (avería, subida de tensión, "
         "robo, un virus que lo cifra todo), **se pierde todo a la vez**."],
        ["**La carpeta `.git` va dentro de cada copia de seguridad completa de HA.** Con una sola copia recuperas la "
         "configuración **y todo su historial**.",
         "Copiar `.git` a otra carpeta del mismo aparato **apenas ayuda**: sigue siendo la misma caja."],
        ["**Trabajar directamente sobre `/config`**, sin una copia de pruebas, es lo normal en un HA de casa. Si un "
         "cambio sale mal, se deshace con git o con una copia de seguridad.",
         "Hace falta **al menos una copia fuera**: en otro aparato o en la nube. Y mejor en **dos sitios**: si la única "
         "copia de fuera falla, ya no queda ninguna."],
    ], anchos_cm=[8.5, 8.5], tam=9.5)
    E.parrafo(doc, "Para la **configuración**, una copia de fuera basta, porque lleva el historial de git completo. Lo "
                   "que más se pierde en un desastre es otra cosa: la **base de datos de históricos** (meses de "
                   "temperaturas y consumos), que no está en git.")
    E.tabla(doc, ["", "En una casa", "En el aula"], [
        ["La «caja»", "El aparato donde está HA y, a veces, también sus copias", "Tu VM: el **reset** la devuelve a `limpio` y borra tu repositorio"],
        ["La copia de fuera", "La copia de seguridad de HA en otro aparato o en la nube", "El **remoto privado del grupo** en GitHub"],
        ["Si no la tienes", "Un fallo del aparato y lo pierdes todo", "Acaba la clase y lo pierdes todo"],
    ], anchos_cm=[3.4, 6.8, 6.8], negrita_col0=True, tam=9.5)
    E.cajon(doc, "IDEA CLAVE", "**git no es una copia de seguridad: es el historial.** Te salva de un cambio malo, no de "
                               "perder la máquina. Para eso hace falta que el historial esté **también en otro sitio**.")

    videos(doc, "git es complicado y casi todo nos queda fuera. Del curso de Git y GitHub de **MoureDev** (Brais "
                "Moure), que dura cinco horas, **solo necesitas una lección**: la 8, donde explica `git add` y "
                "`git commit`. Es lo único que usamos, y aun así lo ejecuta la IA; verla te sirve para entender qué "
                "está haciendo.", [
        ("Lección 8 · git add y git commit (minuto 45:21, unos ocho minutos)", t(GIT, 0, 45, 21)),
    ])

    # ================================================================== 3 MCP (fuente única: gen_ia_mcp.py)
    E.h1(doc, "3. MCP: Model Context Protocol")
    src = open("/home/claude/material-ha/_trabajo/gen/gen_ia_mcp.py", encoding="utf-8").read()
    a = src.index('    E.h2(doc, "Dicho con precisión")')
    b = src.index("    # ------------------------------------------------------------------ repaso")
    cuerpo = src[a:b]
    cuerpo = cuerpo.replace("E.h2(doc, ", "E.h3(doc, ")
    cuerpo = re.sub(r'E\.h3\(doc, "2\.\d ', 'E.h3(doc, "', cuerpo)
    cuerpo = re.sub(r'E\.h1\(doc, "(\d)\. ', lambda m: 'E.h2(doc, "3.%d ' % (int(m.group(1)) - 1), cuerpo)
    cuerpo = "\n".join(l[4:] if l.startswith("    ") else l for l in cuerpo.split("\n"))
    E.h2(doc, "3.1 Qué es MCP")
    cuerpo = cuerpo.replace('E.h2(doc, "3.1 Dos servidores', 'E.h2(doc, "3.2 Dos servidores') \
                   .replace('E.h2(doc, "3.2 Comparación', 'E.h2(doc, "3.3 Comparación') \
                   .replace('E.h2(doc, "3.3 Cuál usamos', 'E.h2(doc, "3.4 Cuál usamos') \
                   .replace('E.h2(doc, "3.4 Trabajar con cabeza', 'E.h2(doc, "3.5 Trabajar con cabeza')
    cuerpo = cuerpo.replace("(lo verás en este tema)", "(apartado 2)")
    exec(cuerpo, {"E": E, "doc": doc, "FIG": M.FIG, "_p": None})

    # ================================================================== 4 SKILLS
    E.h1(doc, "4. Uso de skills", salto_pagina=True)
    E.h2(doc, "4.1 Qué es una skill")
    E.parrafo(doc, "Una **skill** (habilidad) es un **fichero de instrucciones** que le enseña al agente **cómo hacer "
                   "bien un tipo de tarea**. Es una carpeta con un fichero llamado `SKILL.md` y, si hace falta, ficheros "
                   "de apoyo. El agente **solo la lee cuando la tarea lo pide**: así no gasta contexto en lo que no usa.")
    E.tabla(doc, ["", "Qué le da a la IA", "Cuándo se carga", "Comparación"], [
        ["MCP", "**Herramientas**: poder hacer cosas", "Al conectar el servidor", "Las manos y la caja de herramientas"],
        ["Skill", "**Instrucciones** para una tarea concreta", "Solo cuando la tarea lo pide", "El procedimiento de trabajo"],
        ["`AGENTS.md`", "**Normas generales** de tu proyecto", "Siempre, al empezar", "Las normas del taller"],
    ], anchos_cm=[2.6, 5.6, 4.3, 4.5], negrita_col0=True, tam=9)
    E.cajon(doc, "IDEA CLAVE", "MCP y skills **se complementan**. Con MCP la IA **puede** crear una automatización; con "
                               "una skill **sabe hacerla bien**, como la haría alguien con experiencia en Home Assistant.")

    E.cajon(doc, "¿POR QUÉ?", "**¿Qué vamos a hacer con las skills? Usarlas, no fabricarlas.** Crear skills con ficheros de "
                              "apoyo y programas **nos queda fuera**. En clase usamos las que **ya vienen hechas** (la guía "
                              "de buenas prácticas de ha-mcp) y nos basta con entender **qué son** y **cuándo las usa la "
                              "IA**, para saber pedírselo y notar cuándo se la ha saltado.")

    E.h2(doc, "4.2 Markdown: el formato en el que se escribe todo")
    E.parrafo(doc, "**Markdown** es una forma de escribir **texto con formato usando solo caracteres normales**: una "
                   "almohadilla para un título, dos asteriscos para la negrita, un guion para una lista. Los ficheros "
                   "acaban en `.md`. Es el formato que usan las IA para casi todo: las respuestas de opencode, el "
                   "`AGENTS.md`, los `README.md` de GitHub… y también las skills (`SKILL.md`).")
    E.tabla(doc, ["Escribes", "Sirve para"], [
        ["# Título      ## Apartado", "Títulos (más almohadillas, título más pequeño)"],
        ["**negrita**      *cursiva*", "Resaltar"],
        ["- una cosa", "Lista con viñetas"],
        ["1. primer paso", "Lista numerada: pasos en orden"],
        ["\\`cover.p_cocina\\`", "Código o nombres exactos (entre acentos graves)"],
        ["[texto](https://…)", "Un enlace"],
    ], anchos_cm=[6.2, 10.8], mono_cols=(0,))
    E.parrafo(doc, "No hace falta aprenderlo de memoria: se lee igual de bien sin saberlo, y la IA lo escribe sola. "
                   "Lo importante es otra cosa: **un fichero Markdown cualquiera no es una skill**.")
    E.tabla(doc, ["", "Un `.md` normal", "`AGENTS.md`", "Una skill (`SKILL.md`)"], [
        ["Qué es", "Un documento: apuntes, notas, un `README.md`", "Las normas de tu proyecto", "Las instrucciones de un tipo de tarea"],
        ["Para quién", "Para personas (y para la IA, si se lo das)", "Para la IA", "Para la IA"],
        ["Cuándo lo lee la IA", "**Solo si se lo das**: con `@fichero` o pidiéndole que lo lea", "**Siempre**, al empezar la sesión",
         "**Sola**, cuando tu petición encaja con su descripción"],
        ["Qué necesita", "Nada especial", "Llamarse así y estar en la carpeta del proyecto", "Una **cabecera con descripción** y estar en la **carpeta de skills**"],
        ["Ejemplo", "Notas de cómo está montada tu casa", "«No toques la integración MQTT»", "«Cómo revisar una automatización»"],
    ], anchos_cm=[3.0, 4.8, 4.2, 5.0], negrita_col0=True, tam=9)
    E.cajon(doc, "IDEA CLAVE", "**Toda skill es un fichero Markdown, pero no todo fichero Markdown es una skill.** Lo que "
                               "convierte un `.md` en skill es la **cabecera** (con su descripción) y el **sitio** donde "
                               "está. Sin eso, es solo un documento: la IA no lo usará si tú no se lo das.")
    E.cajon(doc, "PISTA", "La IA **no recuerda** la sesión anterior. Al terminar, pídele que deje en un fichero `.md` un "
                          "resumen de lo hecho y de lo que falta. La próxima vez se lo adjuntas con `@` y sigue donde lo dejó.")
    videos(doc, "En el curso de Git y GitHub de **MoureDev** hay una lección corta sobre Markdown. Es la única otra "
                "parte de ese curso que te puede servir aquí.", [
        ("Lección 40 · Markdown en GitHub (minuto 3:56:53, unos cuatro minutos)", t(GIT, 3, 56, 53)),
    ])

    E.h2(doc, "4.3 Cómo es una skill por dentro")
    E.bloque_codigo(doc, "---\n"
                         "name: Revisar una automatización\n"
                         "description: Revisa una automatización de Home Assistant antes de darla por buena\n"
                         "---\n\n"
                         "1. Lee la automatización completa. No cambies nada todavía.\n"
                         "2. Comprueba que todas las entidades existen (búscalas con las herramientas de HA).\n"
                         "3. Mira si usa entity_id y no device_id.\n"
                         "4. Di qué pasa si el desencadenante se repite muy seguido.\n"
                         "5. Enseña los problemas en una lista y espera mi visto bueno antes de editar.",
                    titulo=".opencode/skills/revisar-automatizacion/SKILL.md")
    E.lista(doc, [
        "**Cabecera** (entre las dos líneas `---`): el **nombre** y, sobre todo, la **descripción**. La IA decide si usa "
        "la skill leyendo **solo la descripción**: si no la tiene, o es vaga, no la usará nunca.",
        "**Cuerpo**: los pasos, escritos como se los explicarías a un compañero nuevo.",
        "**Identificador**: el nombre de la carpeta (`revisar-automatizacion`). En minúsculas, con guiones y sin espacios.",
        "**Dónde va**: en el proyecto, en `.opencode/skills/`; para todos tus proyectos, en `~/.config/opencode/skills/`. "
        "opencode también lee las carpetas `.claude/skills` y `.agents/skills`, así que las skills hechas para otros "
        "agentes le valen.",
    ])
    E.h2(doc, "4.4 Cómo se usa")
    E.lista(doc, [
        "**Sola.** En cada paso, la IA ve la lista de skills (nombre y descripción). Si tu petición encaja con una, la "
        "carga y sigue sus pasos.",
        "**Pidiéndola tú.** Escribe `@` y su identificador en tu mensaje: «`@revisar-automatizacion` mira la del "
        "frigorífico».",
        "**Con permiso.** Como todo en opencode, cada skill puede estar permitida, prohibida o con pregunta.",
    ], numerada=True)

    E.h2(doc, "4.5 Las skills de Home Assistant")
    E.parrafo(doc, "El servidor **ha-mcp** trae ya una **guía de buenas prácticas de Home Assistant**. La IA la consulta "
                   "con la herramienta `ha_get_skill_guide` antes de crear o cambiar automatizaciones, scripts o "
                   "dashboards. Algunas de las cosas que enseña:")
    E.lista(doc, [
        "usar las **opciones propias de HA** antes que una plantilla, cuando existen;",
        "usar el `entity_id` y no el identificador interno del dispositivo;",
        "elegir bien el **modo** de una automatización (qué pasa si se dispara otra vez mientras está en marcha);",
        "usar un **ayudante** en vez de escribir un valor fijo dentro de la automatización;",
        "no cambiar el nombre de una entidad sin mirar antes quién la usa.",
    ])
    E.cajon(doc, "PISTA", "Si la IA hace algo raro en HA (una plantilla enrevesada, un valor escrito a fuego), pregúntale: "
                          "«¿has consultado la guía de buenas prácticas?». Muchas veces se la ha saltado.")

    E.h2(doc, "4.6 Skills de otros y skills tuyas")
    E.lista(doc, [
        "**De otros.** Hay colecciones públicas de skills en GitHub. Para usar una, se **copia su carpeta** a "
        "`.opencode/skills/`.",
        "**Tuyas.** Una skill sencilla, como la del ejemplo, es solo un fichero de texto con pasos. Si te ves "
        "explicándole a la IA **lo mismo por tercera vez**, puedes pedirle que lo escriba como skill.",
    ])
    E.cajon(doc, "¡OJO!", "Una skill son **órdenes que la IA va a obedecer**, y puede traer programas (*scripts*) que "
                          "se ejecutan en tu máquina. **Léela entera antes de instalarla** y usa solo las de sitios de "
                          "confianza. Una skill maliciosa puede pedirle a la IA que borre ficheros o que mande tus datos fuera.")
    videos(doc, "Del taller de *Agent Skills* de **MoureDev** solo nos interesan dos trozos: **qué es una skill** y "
                "**cómo se usan las de otros**. El resto (crearlas desde cero, referencias, scripts) no lo usamos.", [
        ("Qué es una skill y cómo funciona (minuto 5:11)", t(SKL, 0, 5, 11)),
        ("Skills de terceros: gestores y recursos (minuto 1:19:02)", t(SKL, 1, 19, 2)),
    ])

    # ================================================================== 5 VIBECODING
    E.h1(doc, "5. Vibecoding: riesgos y buenas prácticas", salto_pagina=True)
    E.h2(doc, "5.1 Qué es el vibecoding")
    E.parrafo(doc, "**Vibecoding** (programar «dejándose llevar») es una palabra de 2025: describir lo que quieres con "
                   "tus palabras, dejar que la IA lo escriba y **aceptarlo sin leerlo**, corrigiendo a base de pedir "
                   "otra vez. Va rapidísimo y, para probar una idea, funciona. El problema llega cuando lo que haces "
                   "**tiene que seguir funcionando mañana**… o maneja la calefacción de una casa.")
    E.tabla(doc, ["", "Vibecoding puro", "Trabajar con IA con cabeza"], [
        ["Quién entiende lo hecho", "Nadie", "Tú"],
        ["Si falla", "«Arréglalo» una y otra vez", "Miras qué cambió y decides"],
        ["Vale para", "Prototipos, pruebas, aprender jugando", "Lo que se va a usar de verdad"],
        ["Volver atrás", "Con suerte", "Con git"],
        ["Quién responde", "«Lo hizo la IA»", "**Tú**: quien lo instala, responde"],
    ], anchos_cm=[4.4, 6.0, 6.6], negrita_col0=True)
    E.cajon(doc, "IDEA CLAVE", "En una instalación, **el responsable es el instalador**, no su herramienta. Si la IA "
                               "configura mal un termostato y tú lo dejas así, el fallo es tuyo. La IA es un ayudante muy "
                               "rápido que **no firma el trabajo**.")

    E.h2(doc, "5.2 Los riesgos")
    E.tabla(doc, ["Riesgo", "Cómo se nota", "Qué lo evita"], [
        ["**Se inventa cosas** (alucina)", "Usa una entidad, una opción o una tarjeta que no existe", "Que lo **compruebe** con una herramienta; mirarlo tú en HA"],
        ["**Dice que ya está** y no está", "«Hecho», pero la persiana no se mueve", "Probarlo siempre; pedirle que lea el estado real"],
        ["**Cambia de más**", "Pediste una tarjeta y ha «mejorado» medio dashboard", "Peticiones pequeñas; `git diff` antes del commit"],
        ["**Rompe lo que funcionaba**", "Algo que iba bien deja de ir", "Commit antes de empezar; `git restore` o `revert`"],
        ["**Borra**", "Desaparecen ficheros o automatizaciones", "Leer lo que pide permiso para hacer; git; copias"],
        ["**Se filtra un secreto**", "Una contraseña acaba en el chat o en GitHub", "No dárselos; `.gitignore`; `git status` antes de `push`"],
        ["**Tus datos se quedan fuera**", "Los modelos gratuitos guardan lo que escribes", "Nada personal ni privado en las peticiones"],
        ["**Obedece a quien no debe**", "Lee una web, un repositorio o una skill con instrucciones escondidas y las sigue",
         "Solo fuentes de confianza; leer las skills; desconfiar si de pronto hace algo que no pediste"],
        ["**Se lía y da vueltas**", "Repite el mismo arreglo, cada vez peor", "Parar, `/undo`, sesión nueva y explicarlo mejor"],
        ["**Tú no aprendes**", "Funciona, pero no sabes explicarlo", "Pedirle que te lo **explique**; hacerlo tú alguna vez"],
    ], anchos_cm=[4.3, 6.2, 6.5], tam=9)

    E.h2(doc, "5.3 Las diez reglas")
    lista_num(doc, [
        "**Commit antes de empezar.** Lo que funciona, guardado.",
        "**Primero Plan, después Build.** Que explique qué va a hacer antes de hacerlo.",
        "**Un cambio cada vez.** Pequeño y con un final claro.",
        "**Di qué no debe tocar.** La IA no conoce tus límites si no se los cuentas.",
        "**Lee antes de aceptar.** Qué fichero, qué herramienta, con qué datos.",
        "**Compruébalo tú.** Abre el dashboard, mueve la persiana, mira el estado. «Hecho» no es una prueba.",
        "**Mira el `git diff`.** ¿Ha cambiado solo lo que pediste?",
        "**Commit cuando funcione**, con un mensaje que lo explique.",
        "**Si se lía, para.** `/undo` o git, sesión nueva y otra forma de pedirlo. No insistas veinte veces.",
        "**Entiende lo que entregas.** Si no sabes explicar cómo funciona, no está terminado.",
    ])
    E.imagen(doc, f_flujo, 17, pie="El ciclo de trabajo: guarda, planea, un cambio, comprueba y guarda.")

    E.h2(doc, "5.4 En una casa de verdad")
    E.parrafo(doc, "En el aula trabajas con dispositivos virtuales: si la IA se equivoca, no pasa nada. En una vivienda, "
                   "Home Assistant mueve **cosas reales**. Hay acciones que no se dejan nunca a una IA sin supervisión:")
    E.lista(doc, [
        "**cerraduras, puertas de garaje y alarmas**: seguridad de las personas y de la casa;",
        "**calefacción, caldera, aerotermia y agua**: averías caras, heladas, inundaciones;",
        "**cargas grandes** (horno, cargador de coche, termo): riesgo eléctrico y de incendio;",
        "**lo que afecta a otras personas**: apagar la luz a alguien, subir una persiana de noche.",
    ])
    E.cajon(doc, "EN EL TALLER", "Igual que no se da tensión a un cuadro sin revisarlo, **no se pone en marcha una "
                                 "automatización hecha por la IA sin probarla**. Primero con los dispositivos virtuales; "
                                 "a los reales, solo cuando funcione y la entiendas.")
    E.cajon(doc, "PISTA", "La IA sirve muy bien para lo contrario del vibecoding: **para aprender**. Pídele que te "
                          "explique una automatización línea a línea, que te diga por qué ha elegido una tarjeta o qué "
                          "pasaría si cambias un valor.")

    # ================================================================== repaso y enlaces
    E.h1(doc, "Preguntas de repaso", salto_pagina=True)
    lista_num(doc, [
        "¿Qué diferencia hay entre un chat de IA y un agente? ¿Y entre opencode y el modelo?",
        "¿Qué puede ver opencode cuando está en HA y qué puede ver cuando está en tu PC?",
        "Di tres cosas que nunca hay que escribirle a un modelo gratuito y por qué.",
        "¿Para qué sirve el agente Plan? ¿Por qué se usa antes que Build?",
        "¿Qué hace `/undo`? ¿Y `/new`? ¿Cuándo usas cada una?",
        "Escribe una buena petición para que la IA te diga por qué no se enciende la tira RGB.",
        "¿Qué es un commit y qué cinco cosas guarda?",
        "¿Cuáles son las dos órdenes de git que usamos, en qué orden van y quién las ejecuta normalmente?",
        "Mejora este mensaje de commit: «cambios varios».",
        "La IA ha estropeado `automations.yaml` y no has hecho commit. ¿Qué le pides?",
        "¿Qué tres sitios con repositorios hay en tu montaje? ¿Cuál está dentro de Home Assistant?",
        "Di dos cosas que se dejan fuera de git en `/config`, por qué y cómo se recuperan.",
        "Si las órdenes las ejecuta la IA, ¿para qué necesitas tú entender cómo está organizado un repositorio?",
        "¿Se puede usar git sin GitHub? ¿Qué te protege trabajando en local y cuál es el punto débil?",
        "¿Por qué git no es una copia de seguridad? ¿Qué pasa con tu repositorio cuando hay un reset?",
        "En clase, ¿quién es el cliente MCP y quién es el servidor MCP?",
        "Di tres cosas que la IA puede hacer con ha-mcp y no con el servidor MCP oficial de HA.",
        "¿En qué se diferencian una herramienta de MCP, una skill y el fichero `AGENTS.md`?",
        "¿Qué es Markdown? ¿Qué le falta a un fichero `.md` normal para ser una skill?",
        "¿Por qué es tan importante la descripción de una skill?",
        "¿Qué hay que hacer antes de instalar una skill de otra persona? ¿Por qué?",
        "¿Qué es el vibecoding? Di dos situaciones en las que vale y dos en las que no.",
        "La IA dice «Hecho». ¿Qué tres cosas haces antes de creértelo?",
    ])

    E.h1(doc, "Para saber más")
    E.parrafo(doc, "Para clase te basta con los trozos enlazados en cada apartado. Si quieres **ir más lejos por tu "
                   "cuenta**, estos son los vídeos completos del canal **MoureDev**, de Brais Moure: es técnico y "
                   "explica con mucha claridad.")
    for texto, url in [("Curso completo de Git y GitHub desde cero (cinco horas; de clase, solo la lección 8)", GIT),
                       ("Taller de Agent Skills desde cero: Claude Code, OpenCode, Codex, Cursor, VS Code…", SKL),
                       ("El vídeo enlazado en el apartado de opencode", "https://www.youtube.com/watch?v=aDJNG_f2C3E")]:
        p = E.parrafo(doc, "▶  ", alineacion="izquierda")
        enlace(p, texto, url, tam=10.5)
    E.nota(doc, "Documentación oficial: opencode.ai/docs · home-assistant.io/integrations/mcp_server · "
                "github.com/homeassistant-ai/ha-mcp · git-scm.com/doc")

    cap = E.capturas(doc)
    open("/home/claude/material-ha/_trabajo/capturas_2MT-HA-T2-ia.txt", "w", encoding="utf-8").write(
        "\n".join("%s. %s — %s" % c for c in cap))
    print(E.a_pdf(E.guardar(doc, OUT)))
    print(cap)


if __name__ == "__main__":
    main()
