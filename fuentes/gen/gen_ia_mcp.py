# -*- coding: utf-8 -*-
"""2MT-HA-IA-mcp: capítulo «MCP: cómo se conecta la IA con Home Assistant» (alumnado).
Será un apartado del tema de IA aplicada a Home Assistant. Sin contraseñas, sin IPs y sin datos personales."""
import sys
sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

FIG = "/home/claude/material-ha/_trabajo/fig/ia_mcp_cadena.png"
OUT = "/home/claude/material-ha/alumnado/2MT-HA-IA-mcp.docx"


def figura():
    C = E.mpl_estilo()
    fig, ax = plt.subplots(figsize=(7.4, 3.2), dpi=260)
    ax.set_xlim(0, 110); ax.set_ylim(0, 39); ax.axis("off")

    def caja(x, y, w, h, t1, t2, col, fondo):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                    fc=fondo, ec=col, lw=2))
        ax.text(x + w / 2, y + h - 4.3, t1, ha="center", va="center", fontsize=10.5, fontweight="bold", color="#222")
        ax.text(x + w / 2, y + h / 2 - 2.6, t2, ha="center", va="center", fontsize=7.8, color="#333", linespacing=1.35)

    y, h = 9, 21
    caja(1, y, 14, h, "Tú", "escribes lo\nque quieres,\ncon tus\npalabras", C["PIZARRA"], "#EDF0F4")
    caja(27, y, 22, h, "opencode", "el cliente MCP:\nhabla con el\nmodelo de IA y\npide herramientas", C["AZUL"], "#DEEAF6")
    caja(62, y, 21, h, "ha-mcp", "el servidor MCP:\nofrece las\nherramientas\ny las ejecuta", C["VERDE"], "#E2EFDA")
    caja(96, y, 13.5, h, "Home\nAssistant", "\n\nentidades,\ndashboards,\nlogs…", C["OCRE"], "#FFF2CC")

    def flecha(x1, x2, yy, txt, col, arriba=True):
        ax.annotate("", xy=(x2, yy), xytext=(x1, yy), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
        ax.text((x1 + x2) / 2, yy + (1.6 if arriba else -1.8), txt, ha="center",
                va="bottom" if arriba else "top", fontsize=7.4, color=col)

    flecha(16.2, 25.8, 23, "petición", C["PIZARRA"])
    flecha(25.8, 16.2, 15, "respuesta", C["PIZARRA"], False)
    flecha(50.4, 60.6, 23, "«usa esta\nherramienta»", C["AZUL"])
    flecha(60.6, 50.4, 15, "resultado", C["VERDE_OSCURO"] if "VERDE_OSCURO" in C else C["VERDE"], False)
    flecha(84.4, 94.6, 23, "lee o\ncambia", C["VERDE_OSCURO"] if "VERDE_OSCURO" in C else C["VERDE"])
    flecha(94.6, 84.4, 15, "datos", C["OCRE"], False)

    ax.text(38.5, 35.5, "en el terminal de HA o en tu PC", ha="center", fontsize=7.6, color=C["AZUL"], style="italic")
    ax.text(72.5, 35.5, "dentro de tu HA", ha="center", fontsize=7.6, color=C["VERDE"], style="italic")
    ax.text(55, 3.2, "La IA nunca toca Home Assistant directamente: todo pasa por el servidor MCP.",
            ha="center", fontsize=8.2, color="#222", fontweight="bold")
    fig.savefig(FIG, bbox_inches="tight", pad_inches=0.08, facecolor="white")
    plt.close(fig)


def main():
    figura()
    doc = E.nuevo_documento("MCP: Model Context Protocol",
                            "IA aplicada a Home Assistant · Qué es y qué servidor usamos",
                            titulo_corto="IA en Home Assistant · MCP", margenes_cm=(1.6, 1.8, 1.6, 1.8))

    # ------------------------------------------------------------------ 1
    E.h1(doc, "1. Qué es MCP")
    E.h2(doc, "Dicho con precisión")
    E.parrafo(doc, "**MCP** (*Model Context Protocol*, protocolo de contexto para modelos) es un **protocolo abierto** que "
                   "define cómo una aplicación de IA se conecta con programas externos para usar sus datos y sus funciones. "
                   "Es un estándar público: cualquier aplicación de IA y cualquier programa pueden usarlo, sean de quien sean.")
    E.lista(doc, [
        "Sigue una arquitectura **cliente-servidor**. El **cliente** va dentro de la aplicación de IA; el **servidor** "
        "es el programa que da acceso a algo (aquí, a Home Assistant).",
        "Los dos se mandan **mensajes JSON-RPC 2.0**: peticiones y respuestas escritas en formato JSON.",
        "Los mensajes viajan por un **transporte**: **stdio** si el servidor es un programa del mismo ordenador, o "
        "**HTTP** si está en otra máquina de la red. El nuestro va por HTTP.",
        "Al conectarse, el cliente pide al servidor la **lista de herramientas** (`tools/list`). Cada herramienta tiene "
        "un **nombre**, una **descripción** y un **esquema** que dice qué datos necesita.",
        "El **modelo** lee esa lista y decide cuál usar. El cliente manda entonces la **llamada** (`tools/call`) con los "
        "datos; el servidor la ejecuta y devuelve el **resultado**, que vuelve al modelo.",
    ])
    E.bloque_codigo(doc, '{"jsonrpc": "2.0", "id": 7, "method": "tools/call",\n'
                         ' "params": {"name": "ha_get_state", "arguments": {"entity_id": "cover.p_cocina"}}}',
                    titulo="Así es, por dentro, una llamada a una herramienta (tú no la escribes: la manda opencode)")
    E.h2(doc, "Dicho en llano")
    E.parrafo(doc, "Un modelo de IA, él solo, **solo sabe escribir texto**. No puede mirar cómo está tu persiana ni cambiar "
                   "un dashboard. Para eso necesita «manos»: unas **herramientas** que alguien le deja usar. MCP es el "
                   "«enchufe» común para dárselas: quien hace el servidor decide qué herramientas hay, y cualquier "
                   "aplicación de IA que hable MCP puede usarlas. Hay dos papeles:")
    E.lista(doc, [
        "El **cliente MCP** es la aplicación de IA con la que hablas. En clase es **opencode**.",
        "El **servidor MCP** es un programa que **ofrece herramientas** y las ejecuta cuando el cliente se lo pide. "
        "En clase está **dentro de tu HA**.",
    ])
    E.imagen(doc, FIG, 14.5, pie="La cadena completa: tú, el cliente (opencode), el servidor MCP y Home Assistant.")
    _p = E.parrafo(doc, "Un servidor MCP puede ofrecer tres cosas:")
    if _p is not None: _p.paragraph_format.keep_with_next = True
    E.tabla(doc, ["Qué ofrece", "Qué es", "Ejemplo con HA"], [
        ["Herramientas (*tools*)", "Acciones que la IA puede pedir. Es lo más importante.",
         "leer el estado de una entidad, crear una automatización"],
        ["Recursos (*resources*)", "Información que la IA puede leer.", "un resumen de las entidades de la casa"],
        ["*Prompts*", "Instrucciones ya preparadas para la IA.", "cómo usar bien las herramientas"],
    ], anchos_cm=[4.2, 6.6, 6.2], negrita_col0=True)
    E.cajon(doc, "IDEA CLAVE", "La IA **no toca** Home Assistant directamente. Lee la lista de herramientas, elige una, "
                               "y el **servidor MCP** es el que la ejecuta y le devuelve el resultado. Si una cosa no tiene "
                               "herramienta, la IA no puede hacerla.")
    E.cajon(doc, "EJEMPLO", ["Escribes en opencode: «¿Por qué no baja la persiana de la cocina?». La IA, paso a paso:",
                             "- busca la entidad de la persiana (`cover.p_cocina`);",
                             "- lee su estado y sus atributos;",
                             "- mira los registros (*logs*) y las automatizaciones que la usan;",
                             "- te explica lo que ha encontrado y te propone un arreglo.",
                             "Cada uno de esos pasos es **una herramienta** del servidor MCP."])

    # ------------------------------------------------------------------ 2
    E.h1(doc, "2. Dos servidores MCP para Home Assistant")
    E.parrafo(doc, "Para HA hay dos servidores MCP distintos. Hacen cosas parecidas, pero no llegan igual de lejos.")

    E.h2(doc, "2.1 ha-mcp: el de la comunidad")
    E.parrafo(doc, "**ha-mcp** es un proyecto de la comunidad (está en GitHub, en `homeassistant-ai/ha-mcp`). **No es oficial** "
                   "de Home Assistant. Sirve para que la IA **configure, automatice y busque fallos** en HA. Se instala "
                   "dentro de HA y los clientes se conectan a él con una dirección que lleva una **parte secreta**.")
    E.parrafo(doc, "Tiene **más de 80 herramientas**, repartidas en unos 30 grupos. Todas empiezan por `ha_`. Algunas:")
    E.tabla(doc, ["Para qué", "Herramientas (ejemplos)"], [
        ["Buscar y mirar", "`ha_search`, `ha_get_state`, `ha_get_overview`"],
        ["Automatizaciones y scripts", "`ha_config_set_automation`, `ha_config_set_script`"],
        ["Dashboards", "`ha_config_set_dashboard`"],
        ["Mandar órdenes", "`ha_call_service`, `ha_bulk_control`"],
        ["Buscar fallos", "`ha_get_logs`, `ha_get_history`, `ha_get_automation_traces`"],
        ["Plantillas", "`ha_eval_template` (calcula una plantilla y devuelve el resultado)"],
        ["Sistema", "`ha_manage_backup`, `ha_restart`, `ha_manage_updates`"],
        ["Ayuda para la propia IA", "`ha_search_tools` (encontrar la herramienta que necesita) y "
                                    "`ha_get_skill_guide` (guía de buenas prácticas de HA)"],
    ], anchos_cm=[4.6, 12.4], negrita_col0=True)
    E.parrafo(doc, "También trae medidas de seguridad: un **modo de solo lectura**, la posibilidad de apagar herramientas "
                   "una a una, pedir tu permiso antes de usar algunas y **copias automáticas antes de cambiar** cosas.")

    E.h2(doc, "2.2 El servidor MCP de Home Assistant: el oficial")
    E.parrafo(doc, "Home Assistant trae su propio servidor MCP: la integración **Model Context Protocol**. Existe desde la "
                   "versión 2025.2 y se activa en **Ajustes → Sistema → IA**. Para entrar se usa tu usuario de HA "
                   "(por defecto, solo administradores).")
    _p = E.parrafo(doc, "Sus herramientas van en grupos:")
    if _p is not None: _p.paragraph_format.keep_with_next = True
    E.tabla(doc, ["Grupo", "Qué puede hacer", "Quién"], [
        ["Control de dispositivos", "Leer y manejar las entidades que estén expuestas a los asistentes de voz.",
         "Cualquier usuario"],
        ["Home Assistant", "Leer todas las entidades, los registros y el historial; buscar dispositivos y automatizaciones; "
                           "ver información del sistema; llamar a cualquier acción; listar y recargar integraciones.",
         "Solo administrador"],
        ["Los de otras integraciones", "Una integración puede añadir su propio grupo (por ejemplo, KNX).", "Según el grupo"],
    ], anchos_cm=[4.2, 9.8, 3.0], negrita_col0=True)
    E.parrafo(doc, "Tiene una opción de **solo lectura**: con ella, el servidor esconde todas las herramientas que cambian "
                   "algo. Es una protección de verdad, porque la pone el servidor y la IA no puede saltársela.")
    E.cajon(doc, "¡OJO!", "El servidor oficial **todavía no edita** dashboards ni automatizaciones, ni calcula plantillas, "
                          "ni hace copias de seguridad. Sirve muy bien para **preguntar y diagnosticar**, pero no para "
                          "construir lo que vamos a construir en las prácticas.")

    # ------------------------------------------------------------------ 3
    E.h1(doc, "3. Comparación")
    E.tabla(doc, ["", "ha-mcp (comunidad)", "MCP de Home Assistant (oficial)"], [
        ["Quién lo hace", "Voluntarios de la comunidad", "El propio proyecto Home Assistant"],
        ["Cómo llega", "Se instala aparte, dentro de HA", "Viene con HA: se activa en Ajustes → Sistema → IA"],
        ["Herramientas", "Más de 80", "Pocas, en grupos"],
        ["Leer entidades, registros e historial y mandar órdenes", "Sí", "Sí"],
        ["Crear y editar automatizaciones", "Sí", "No"],
        ["Crear y editar dashboards", "Sí", "No"],
        ["Plantillas y copias de seguridad", "Sí", "No"],
        ["Solo lectura", "Sí (modo y dirección de solo lectura)", "Sí (opción del servidor)"],
        ["Cómo se entra", "Dirección con parte secreta (o usuario de HA)", "Usuario de HA, por defecto administrador"],
        ["Actualizaciones", "Van por su cuenta: a veces un cambio rompe algo", "Llegan con cada versión de HA"],
        ["Gasto de la IA", "Mayor: hay muchas herramientas que describir", "Menor: es ligero"],
    ], anchos_cm=[5.2, 5.9, 5.9], negrita_col0=True, tam=9)

    # ------------------------------------------------------------------ 4
    E.h1(doc, "4. Cuál usamos en clase")
    E.parrafo(doc, "En clase usamos **ha-mcp**. La razón es sencilla: vamos a pedirle a la IA que nos ayude a hacer "
                   "**dashboards y automatizaciones**, y hoy eso solo lo hace ha-mcp.")
    E.cajon(doc, "¿POR QUÉ?", ["**¿Y por qué no el oficial?** Porque es **reciente y mejora muy deprisa**, pero todavía le "
                               "falta lo que necesitamos:",
                               "- nació en la versión 2025.2;",
                               "- en la 2026.10 pasó a activarse con un clic;",
                               "- en la 2026.11 ganó casi todo lo de diagnóstico: información del sistema, buscar y llamar "
                               "acciones, listar y recargar integraciones.",
                               "Cuando sepa editar dashboards y automatizaciones, será la opción natural. Lo que aprendas "
                               "aquí te vale igual: **cambia el servidor, no la forma de trabajar**."])
    E.cajon(doc, "PISTA", "Se pueden tener los dos: ha-mcp para trabajar y el oficial en **solo lectura** para consultas. "
                          "Pero **no conectes los dos a la vez en el mismo cliente**: la IA ve herramientas repetidas y se lía.")

    # ------------------------------------------------------------------ 5
    E.h1(doc, "5. Trabajar con cabeza")
    E.parrafo(doc, "Con MCP la IA ya no solo opina: **puede cambiar tu Home Assistant**. Por eso:")
    E.lista(doc, [
        "**Lee antes de aceptar.** opencode te enseña qué herramienta quiere usar y con qué datos. Si no lo entiendes, pregunta antes de decir que sí.",
        "**Guarda antes de cambiar.** Haz un *commit* de git (lo verás en este tema) o una copia antes de un cambio grande. Así puedes volver atrás.",
        "**La dirección del servidor es como una contraseña.** Lleva una parte secreta: no la enseñes, no la pegues en un chat ni la subas a GitHub.",
        "**La IA se equivoca.** Puede inventarse una entidad que no existe o dar por hecho algo que no ha mirado. Pídele que lo **compruebe** con una herramienta.",
        "**Para solo mirar, solo lectura.** Si únicamente quieres preguntar o buscar un fallo, no hace falta darle permiso para cambiar nada.",
    ])
    E.h2(doc, "Cosas raras de ha-mcp que conviene conocer")
    E.tabla(doc, ["Qué pasa", "Por qué", "Qué hacer"], [
        ["Una herramienta ha cambiado o ya no está", "Es un proyecto que cambia rápido; alguna vez un cambio rompe lo que funcionaba",
         "Pide a la IA que busque la herramienta actual con `ha_search_tools`"],
        ["Error de `config_hash` al guardar un dashboard", "El dashboard ha cambiado desde que la IA lo leyó "
                                                          "(por ejemplo, lo ha tocado tu compañero)",
         "Que lo **vuelva a leer** y repita el cambio"],
        ["La IA pide otra vez la guía de buenas prácticas", "La clave de esa guía caduca cada cierto tiempo",
         "Nada: es normal, deja que la lea"],
    ], anchos_cm=[4.8, 6.4, 5.8], tam=9)

    # ------------------------------------------------------------------ repaso
    E.h1(doc, "Preguntas de repaso")
    E.lista(doc, [
        "¿Qué puede hacer un modelo de IA sin herramientas? ¿Qué le da MCP?",
        "En clase, ¿quién es el cliente MCP y quién es el servidor MCP?",
        "Verdadero o falso: «Con MCP, la IA entra directamente en Home Assistant y cambia lo que quiere». Justifícalo.",
        "Di tres cosas que la IA puede hacer con ha-mcp y que no puede hacer con el servidor MCP oficial.",
        "¿Para qué sirve el modo de solo lectura? ¿Cuándo lo usarías?",
        "¿Por qué usamos ha-mcp en clase y no el oficial? ¿Cuándo tendría sentido cambiar?",
        "La IA te dice que ha apagado la tira RGB, pero sigue encendida. ¿Qué le pides?",
        "Al guardar un dashboard sale un error de `config_hash`. ¿Qué ha pasado y cómo se arregla?",
    ], numerada=True)

    pdf = E.a_pdf(E.guardar(doc, OUT))
    print(pdf)


if __name__ == "__main__":
    main()
