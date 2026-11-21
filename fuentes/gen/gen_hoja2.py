#!/usr/bin/env python3
"""Hoja 2 del alumnado · «Chuleta MQTT de los dispositivos virtuales» (2MT). Genera el .docx y el .pdf.
Datos: /home/claude/material-ha/_trabajo/ficha-comun.md (apartados 2.9, 2.10 y 2.11).
Las órdenes se copian TAL CUAL del bloque literal de la ficha (2.11)."""
import sys
sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E
from docx.shared import Cm, Pt

E.TAM = 9.5  # cuerpo un poco más pequeño para que quepa en una hoja (mínimo pedido: 9,5 pt)

SALIDA = "/home/claude/material-ha/alumnado/2MT-HA-hoja2-chuleta-mqtt.docx"


def compactar(doc):
    h = doc.styles["Heading 1"]
    h.font.size = Pt(12)
    h.paragraph_format.space_before = Pt(5)
    h.paragraph_format.space_after = Pt(4)
    doc.styles["Normal"].paragraph_format.space_after = Pt(3)
    doc.styles["Normal"].paragraph_format.line_spacing = 1.08


doc = E.nuevo_documento("Chuleta MQTT", "Órdenes para los dispositivos virtuales",
                        titulo_corto="Hoja 2 · Chuleta MQTT",
                        margenes_cm=(1.2, 1.2, 1.5, 1.5), linea_info="")
compactar(doc)
_vacio = doc.paragraphs[-1]
if not _vacio.text.strip():
    _vacio._p.getparent().remove(_vacio._p)
doc.paragraphs[-1].paragraph_format.space_after = Pt(6)

def mono85(t):
    """Temas y mensajes a 8,5 pt (mínimo pedido para código: 8 pt) para que quepan en una línea."""
    for row in t.rows[1:]:
        for c in row.cells[1:]:
            for p in c.paragraphs:
                for r in p.runs:
                    if r.font.name == E.FUENTE_MONO or "Courier" in str(r._r.xml[:400]):
                        r.font.size = Pt(8.5)
    return t


# 1 ---------------------------------------------------------------------------
E.h1(doc, "1. Dónde se publica")
E.tabla(doc, ["1 · Abre", "2 · Publica", "3 · Comprueba"], [[
    "**Ajustes → Dispositivos y servicios → MQTT → Configurar**",
    "En *Publicar un paquete*, escribe el **tema** (*topic*) y el **mensaje** (copiados de las tablas) y publícalo.",
    "En *Escuchar un tema*, escribe `virtual/#` y empieza a escuchar: verás las órdenes y las respuestas.",
]], anchos_cm=[5.6, 6.2, 6.2], alterna=False)

# 2 ---------------------------------------------------------------------------
E.h1(doc, "2. Mandar órdenes a un dispositivo")
mono85(E.tabla(doc, ["Para qué", "Tema", "Mensaje"], [
    ["Persiana", "virtual/p_cocina/set", '{"position": 50}\no bien `OPEN`, `CLOSE` o `STOP`'],
    ["Enchufe: encender ↔ apagar", "virtual/e_tv/set", "TOGGLE"],
    ["Tira RGB: color y brillo", "virtual/tira_rgb/set",
     '{"state": "ON",\n"color": {"hex": "#ff8000"},\n"brightness": 150}'],
    ["Termostato: consigna", "virtual/ter_salon/set/current_heating_setpoint", "22"],
], anchos_cm=[5.0, 6.3, 6.7], mono_cols=(1, 2)))
E.parrafo(doc, "Para otro dispositivo del kit, cambia su nombre en el tema (por ejemplo, `virtual/p_hab1/set`), con el mensaje de su tipo.")

# 3 ---------------------------------------------------------------------------
E.h1(doc, "3. Gestionar el kit")
mono85(E.tabla(doc, ["Para qué", "Tema", "Mensaje"], [
    ["Permitir añadir", "virtual/bridge/request/permit_join", '{"time": 254}'],
    ["Añadir", "virtual/bridge/request/device/add",
     '{"tipo": "persiana", "nombre": "p_hab2",\n"recorrido": 18}'],
    ["Quitar", "virtual/bridge/request/device/remove", '{"id": "p_hab2"}'],
    ["Renombrar", "virtual/bridge/request/device/rename", '{"from": "p_hab2",\n"to": "p_dormitorio"}'],
    ["Volver al kit inicial", "virtual/bridge/request/kit/restablecer", "{}"],
], anchos_cm=[3.2, 7.2, 7.6], mono_cols=(1, 2)))
E.tabla(doc, ["Para añadir", "Qué puedes poner"], [
    ['`"tipo"`', "`persiana`, `toldo`, `enchufe`, `luz`, `luz_regulable`, `luz_rgb`, `termostato`"],
    ["Opciones del enchufe", '`"perfil": "pc|frigo|tv|generico"` (uno de los cuatro), `"potencia": 60`'],
], anchos_cm=[4.4, 13.6])

E.parrafo(doc, "**Reglas del kit**", despues=2, juntos=True)
E.lista(doc, [
    "**Primero `permit_join`:** sin él activo, *añadir* se rechaza. El dispositivo aparece **a los 3 s**.",
    "**Nombres:** solo minúsculas, números y `_` (como `p_hab2`). Como mucho, **40 dispositivos por grupo**.",
    "**Respuestas** en `virtual/bridge/response/…` y **avisos** en `virtual/bridge/logging`.",
    "**¡Ojo!** Todo lo que añadas **desaparece con el reset**.",
])

# 4 ---------------------------------------------------------------------------
E.h1(doc, "4. Comodines para *Escuchar un tema*")
E.tabla(doc, ["Escribe", "Y escuchas"], [
    ["`virtual/#`", "todo lo de los dispositivos virtuales: `#` vale por **todos los niveles que sigan** (va al final)"],
    ["`virtual/bridge/#`", "lo del kit: peticiones, respuestas y avisos"],
    ["`virtual/+/set`", "las órdenes de un nivel a cualquier dispositivo (la consigna del termostato tiene un nivel más): `+` vale por **un nivel**"],
], anchos_cm=[4.4, 13.6])
E.cajon(doc, "IDEA CLAVE", "Los **virtuales** usan temas que empiezan por `virtual/`. Los **reales** "
                           "(pendiente: aún no funcionan) usarán `zigbee2mqtt/`. Nunca se mezclan.")

E.a_pdf(E.guardar(doc, SALIDA))
print("OK", SALIDA)
