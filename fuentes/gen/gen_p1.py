#!/usr/bin/env python3
"""Genera la Práctica 1 de Home Assistant (alumnado): 2MT-HA-P1.docx y .pdf.

Uso:  python3 gen_p1.py
Datos: /home/claude/material-ha/_trabajo/ficha-comun.md (fuente única).
"""
import sys
sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E
from docx.shared import Pt, Cm

SALIDA = "/home/claude/material-ha/alumnado/2MT-HA-P1.docx"


def pregunta(doc, n, texto, renglones=2):
    """Pregunta y renglones punteados en una sola tabla que no se parte entre páginas."""
    ancho = doc._ancho_cm
    t = doc.add_table(rows=renglones + 1, cols=1)
    E._tabla_sin_bordes(t)
    E._tabla_ancho_fijo(t, [ancho])
    for i, fila in enumerate(t.rows):
        c = fila.cells[0]
        p = c.paragraphs[0]
        E._espaciado(p, 0, 0, 1.0)
        if i < renglones:
            p.paragraph_format.keep_with_next = True
        if i == 0:
            E._fila_no_partir(fila)
            E._celda_margenes(c, 0, 0, 0, 0)
            E.texto_rico(p, f"**{n}.** {texto}")
        else:
            E._fila_no_partir(fila, alto_cm=0.56, exacto=True)
            E._celda_margenes(c, 0, 340, 0, 0)
            E._celda_bordes(c, bottom=("dotted", 6, "8C8C8C"))
    E._hueco(doc, 5)


doc = E.nuevo_documento(
    "Práctica 1 de Home Assistant",
    "Dashboard del tiempo",
    titulo_corto="Práctica 1 · Dashboard del tiempo",
)

E.parrafo(doc, "**Grupo:** ______     **Nombres:** ______________________________________________", alineacion="izquierda", despues=4)

# ------------------------------------------------------------------ 1
E.h1(doc, "1. Qué vas a hacer")
E.parrafo(doc, "Vas a crear en tu Home Assistant un **dashboard nuevo** que enseñe solo dos cosas: "
               "**el tiempo** que hace en el instituto (ahora y la previsión de los próximos días) y "
               "**la hora con segundos**. Nada más: en esta práctica no se tocan los dispositivos "
               "virtuales, ni las automatizaciones, ni MQTT.")
E.parrafo(doc, "**Qué vas a aprender:**", despues=0, juntos=True)
E.lista(doc, [
    "Entrar en el HA de tu grupo.",
    "Crear un dashboard nuevo sin estropear el que ya viene hecho.",
    "Añadir tarjetas a un dashboard y cambiar sus opciones.",
    "Saber qué entidad usa cada tarjeta y de qué integración sale.",
])

# ------------------------------------------------------------------ 2
E.h1(doc, "2. Qué necesitas y normas")
E.lista(doc, [
    "Un ordenador del aula con navegador.",
    "La dirección de tu grupo (`http://10.202.51.8N`, donde N es tu número de grupo: el grupo 3 "
    "entra en `http://10.202.51.83`) y tu usuario (`userN`). Lo tienes en la hoja **«Tu Home Assistant»**.",
])
E.cajon(doc, "¡OJO!", [
    "Normas de esta práctica:",
    "- **Sin inteligencia artificial.** No uses ChatGPT, Copilot ni ningún otro asistente de IA. "
    "Sí puedes usar la ayuda oficial de HA (home-assistant.io), tus apuntes y preguntar al profesor.",
    "- **Uno edita y los demás miran.** Si dos del grupo cambian el dashboard a la vez, lo que guarda "
    "uno puede borrar lo del otro. Turnaos.",
    "- **No cambies la ubicación de la casa** ni las cuentas de usuario, y no toques Mosquitto ni la "
    "integración MQTT.",
    "- **El reset lo borra todo.** Cuando el profesor hace el reset —normalmente entre clases—, tu VM "
    "vuelve a la instantánea `limpio` y se borra todo lo que hayas hecho: haz la captura **antes de irte**.",
])

# ------------------------------------------------------------------ 3
E.h1(doc, "3. Paso a paso")
E.parrafo(doc, "Cada paso te dice qué tienes que conseguir y dónde mirar. Cómo se hace exactamente lo "
               "tienes que encontrar tú: prueba, mira las opciones y fíjate en lo que cambia.")

E.h2(doc, "Paso 1 · Entra en tu HA")
E.parrafo(doc, "Abre el navegador, escribe la dirección de tu grupo y entra con tu usuario. "
               "Fíjate en la barra lateral de la izquierda: ahí salen los dashboards y, abajo, **Ajustes**.")

E.h2(doc, "Paso 2 · ¿Tienes ya una entidad del tiempo?")
E.parrafo(doc, "Para enseñar el tiempo, HA necesita una **entidad del tiempo**. Todas tienen un "
               "`entity_id` que empieza por `weather.…` (por ejemplo, el de una luz empieza por `light.…`). Ese dato lo da la integración **Met.no** "
               "(el instituto meteorológico de Noruega, gratis y sin registrarse).")
E.lista(doc, [
    "Mira en **Ajustes → Dispositivos y servicios** si ya está la integración Met.no.",
    "**Si ya está:** busca qué entidad `weather.…` ha creado y apunta su `entity_id` (pregunta 1).",
    "**Si no está:** añádela desde esa misma pantalla, con el botón para añadir una integración. "
    "Busca «Met.no» y sigue los pasos. Deja la ubicación que te propone.",
], numerada=True)
E.cajon(doc, "PISTA", "Si no sabes qué entidad es, abre la integración: dentro verás su dispositivo y "
                      "sus entidades. Al pulsar en una entidad, en sus ajustes sale el `entity_id`.")

E.h2(doc, "Paso 3 · Crea un dashboard nuevo")
E.parrafo(doc, "Los dashboards se crean desde **Ajustes** (en el menú puede salir como *Paneles de control*: es lo mismo "
               "que *dashboards*). Crea uno **vacío, desde cero** (no copies "
               "el que ya viene hecho) y ponle de nombre **«Tiempo grupo N»** con tu número de grupo. "
               "Haz que salga en la barra lateral para encontrarlo fácil.")
E.hueco_captura(doc, "Ajustes → pantalla de los dashboards, con el botón para añadir uno nuevo", alto_cm=2.4)

E.h2(doc, "Paso 4 · Añade el tiempo: ahora y los próximos días")
E.parrafo(doc, "Abre tu dashboard y ponlo en modo de edición (el lápiz de arriba a la derecha). "
               "Añade **una tarjeta** que use tu entidad `weather.…` y que enseñe **a la vez** el tiempo "
               "de ahora y la **previsión por días**. Recuerda: un dashboard puede tener varias **vistas** (como "
               "pestañas), y cada vista tiene sus tarjetas.")
E.cajon(doc, "PISTA", "Al añadir una tarjeta puedes buscar por el nombre de la tarjeta o elegir primero "
                      "la entidad. Hay varias tarjetas que aceptan una entidad del tiempo, pero no todas "
                      "enseñan la previsión. Mira las opciones de la tarjeta hasta que salgan los próximos días.")

E.h2(doc, "Paso 5 · Añade la hora con segundos")
E.parrafo(doc, "Añade otra tarjeta que enseñe **la hora con los segundos corriendo**. HA trae de serie "
               "una tarjeta pensada solo para esto: búscala y revisa **todas** sus opciones.")
E.cajon(doc, "PISTA", "Si los segundos no salen a la primera, no busques otra tarjeta todavía: mira las "
                      "opciones de esa misma tarjeta (estilo, tamaño, formato de la hora…). No hace falta "
                      "instalar nada.")

E.h2(doc, "Paso 6 · Ordena, guarda y comprueba")
E.lista(doc, [
    "Pon las tarjetas ordenadas, con un título que se entienda, y quita lo que sobre.",
    "Guarda y sal del modo de edición.",
    "Comprueba que la previsión es del instituto y que los segundos avanzan solos.",
    "Haz la captura (Windows + Mayús + S) **antes de irte**.",
], numerada=True)

E.cajon(doc, "EN EL TALLER", "**Si te sobra tiempo:** añade una segunda tarjeta con la previsión "
        "**por horas**, o cambia el reloj a otro estilo y compáralos. Sin salirte del tema.")

# ------------------------------------------------------------------ 4
E.h1(doc, "4. Preguntas", salto_pagina=True)
E.parrafo(doc, "Contesta con tus palabras, en frases cortas.", despues=2)
pregunta(doc, 1, "¿Qué `entity_id` usa tu tarjeta del tiempo? ¿De qué integración sale?", 2)
pregunta(doc, 2, "No has escrito las coordenadas del instituto en ningún sitio. ¿De dónde saca HA "
                 "la ubicación para el tiempo?", 3)
pregunta(doc, 3, "HA puede tener una entidad que da la hora, `sensor.time`, pero solo cambia una vez por "
                 "minuto. ¿Te serviría para tu reloj con segundos? ¿Por qué?", 3)
pregunta(doc, 4, "Explica la diferencia entre **dashboard**, **vista** y **tarjeta**. Pon como ejemplo "
                 "lo que has hecho en esta práctica.", 3)
pregunta(doc, 5, "¿Por qué hemos creado un dashboard nuevo en vez de cambiar el que ya viene hecho?", 3)

# ------------------------------------------------------------------ 5
E.h1(doc, "5. Qué tienes que entregar")
E.lista(doc, [
    "**Una captura** del dashboard terminado (fuera del modo de edición) en la que se vean: "
    "el nombre del dashboard con tu número de grupo, el tiempo de ahora, la previsión y la hora con segundos.",
    "**Las respuestas** a las cinco preguntas.",
    "Se entrega como te indique el profesor.",
])

E.h2(doc, "Cómo se valora")
E.tabla(doc, ["Criterio", "Bien", "A medias", "No", "Puntos"], [
    ["Dashboard nuevo", "Nuevo, vacío al empezar, con «Tiempo grupo N»", "Nuevo pero sin el nombre pedido",
     "Se ha cambiado el que venía hecho", "1,5"],
    ["Tiempo del IES", "Tiempo de ahora y previsión por días", "Solo una de las dos cosas",
     "No hay tiempo", "2,5"],
    ["Hora con segundos", "Los segundos se ven (y avanzan, en tu pantalla)", "Hora sin segundos", "No hay hora", "2,5"],
    ["Acabado", "Ordenado, con títulos, sin tarjetas sobrantes; captura clara",
     "Algo desordenado o la captura no se lee bien", "Sin captura", "1,5"],
    ["Respuestas", "Las cinco bien explicadas", "Alguna mal o incompleta", "Sin contestar", "2"],
], anchos_cm=[3.0, 4.6, 3.9, 3.6, 1.9], negrita_col0=True, centrar_cols=(4,), tam=8.5)
E.nota(doc, "Bien = todos los puntos del criterio · A medias = la mitad · No = 0. Total: 10 puntos. "
            "Lo que no se ve en la captura lo comprueba el profesor en tu pantalla.")


PDF = E.a_pdf(E.guardar(doc, SALIDA))
import capturas_txt
capturas_txt.escribir(doc, "2MT-HA-P1", PDF)
print("OK", SALIDA)
