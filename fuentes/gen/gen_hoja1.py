#!/usr/bin/env python3
"""Hoja 1 del alumnado · «Tu Home Assistant» (2MT). Genera el .docx y el .pdf.
Datos: /home/claude/material-ha/_trabajo/ficha-comun.md (apartados 2.5 a 2.13)."""
import sys
sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E
from docx.shared import Cm, Pt

E.TAM = 10  # cuerpo un poco más pequeño para que quepa en una cara (mínimo pedido: 9,5 pt)


def compactar(doc):
    """Títulos de apartado más juntos: es una hoja de consulta de una cara."""
    h = doc.styles["Heading 1"]
    h.font.size = Pt(12)
    h.paragraph_format.space_before = Pt(5)
    h.paragraph_format.space_after = Pt(4)
    doc.styles["Normal"].paragraph_format.space_after = Pt(3)
    doc.styles["Normal"].paragraph_format.line_spacing = 1.08

SALIDA = "/home/claude/material-ha/alumnado/2MT-HA-hoja1-tu-home-assistant.docx"

doc = E.nuevo_documento("Tu Home Assistant", "Cómo entrar, normas y qué tienes",
                        titulo_corto="Hoja 1 · Tu Home Assistant",
                        margenes_cm=(1.2, 1.2, 1.5, 1.5), linea_info="")
compactar(doc)
# el párrafo vacío de la «línea de información» del título no hace falta aquí
_vacio = doc.paragraphs[-1]
if not _vacio.text.strip():
    _vacio._p.getparent().remove(_vacio._p)
doc.paragraphs[-1].paragraph_format.space_after = Pt(6)

E.parrafo(doc, "En el aula hay un **mini-PC** con **Proxmox VE**, el **hipervisor**, que lo reparte en varias "
               "**máquinas virtuales** (VMs). **Cada grupo tiene su propia VM con Home Assistant** (HA).")

# 1 ---------------------------------------------------------------------------
E.h1(doc, "1. Tu grupo y el escaparate")
filas = [[f"Grupo {n}", f"user{n}", f"http://10.202.51.8{n}", ""] for n in range(1, 7)]
filas.append(["Escaparate\n(todos)", "Invitado,\nsin contraseña", "http://10.202.51.87",
              "*Los dashboards de una vivienda real (Home, Luces, Persianas, Energía, Aerotermia, Clima…) "
              "con su histórico. Míralo para sacar ideas.*"])
t = E.tabla(doc, ["Grupo", "Usuario", "Dirección", "Nombres (escríbelos tú)"], filas,
            anchos_cm=[2.5, 2.9, 4.6, 8.0], mono_cols=(2,), negrita_col0=True)
# usuario en monoespaciada solo en las filas de los grupos (no en «Invitado»)
for row in t.rows[1:7]:
    for r in row.cells[1].paragraphs[0].runs:
        E._fuente_run(r, E.FUENTE_MONO); r.font.size = Pt(9); r.font.color.rgb = E.rgb("1F3864")
for row in t.rows[1:7]:
    row.height = Cm(0.56)

# 2 ---------------------------------------------------------------------------
E.h1(doc, "2. Cómo entrar")
E.lista(doc, [
    "Abre el navegador en un PC del aula. **Solo funciona desde la red del aula.**",
    "Escribe la **dirección de tu grupo** tal cual, **sin** `:8123` (por ejemplo, `http://10.202.51.81`).",
    "Usuario: el de tu grupo (`user1` … `user6`). Contraseña: **te la da el profesor**.",
], numerada=True)

# 3 ---------------------------------------------------------------------------
E.h1(doc, "3. Normas")
E.lista(doc, [
    "Tu usuario es **administrador** y puede tocarlo casi todo, pero **no cambies las contraseñas** "
    "ni **instales nada** sin permiso del profesor.",
    "**No toques** la app (antes llamada complemento) **Mosquitto broker** ni la **integración MQTT**: sin ellas no van los dispositivos.",
    "**No toques los usuarios** `admin` (el del profesor) ni `puente` (lo usa el MQTT; no sirve para entrar).",
    "**Cada VM es independiente:** lo que hagas no afecta a los demás grupos, pero **sí a tus compañeros de grupo**.",
])
E.cajon(doc, "¡OJO!", [
    "Cuando el profesor hace el reset —normalmente entre clases—, tu VM vuelve a la instantánea `limpio` "
    "y **se borra todo** lo que hayas hecho "
    "(también lo que hayas añadido al kit). **Antes de terminar, haz capturas** de lo que tengas que entregar.",
], titulo_extra="El reset lo borra todo.")

# 4 ---------------------------------------------------------------------------
E.h1(doc, "4. Tus dispositivos virtuales")
E.parrafo(doc, "El **simulador** imita aparatos Zigbee y tu HA los descubre solo. Cada grupo tiene un **kit de 13** "
               "(más el «Virtual Bridge», que gestiona el kit). Están en **Ajustes → Dispositivos y servicios → MQTT**.",
          despues=3)
E.tabla(doc, ["Nombre", "Qué es"], [
    ["`p_cocina`, `p_hab1`, `p_pc`", "3 persianas: suben, bajan, paran y van a una posición"],
    ["`toldo`", "toldo: como una persiana, pero más lento"],
    ["`luz_escaleras1`", "luz de encender y apagar"],
    ["`luz_salon_cajon`", "luz regulable: brillo y blanco cálido–frío"],
    ["`tira_rgb`", "tira RGB: brillo, color y efectos"],
    ["`enchufe_pc`, `e_frigo`, `e_tv`", "3 enchufes con medida: potencia, corriente, tensión y energía"],
    ["`ter_hab1`, `ter_salon`, `ter_cocina`", "3 termostatos de fan-coil: calor, frío, ventilación o apagado; 4 velocidades y válvula"],
], anchos_cm=[6.0, 12.0], tam=9)
E.parrafo(doc, "**¿Virtual o real?** Los virtuales tienen fabricante **«Virtual (aula)»** y modelo **«… (virtual)»**. "
               "Los reales (pendiente: aún no funcionan) llevarán nombres que empiezan por `aula_`.")

E.a_pdf(E.guardar(doc, SALIDA))
print("OK", SALIDA)
