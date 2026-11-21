# -*- coding: utf-8 -*-
"""Genera «Nuestro servidor de prácticas» (2MT, alumnado): Word + PDF y sus figuras.
Uso: python3 gen_servidor.py
Datos: /home/claude/material-ha/_trabajo/ficha-comun.md (fuente única)."""
import os
import sys
sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

BASE = "/home/claude/material-ha"
FIG = f"{BASE}/_trabajo/fig"
SALIDA = f"{BASE}/alumnado/2MT-HA-servidor.docx"
os.makedirs(FIG, exist_ok=True)

C = E.mpl_estilo()
MM = 1 / 25.4            # 1 unidad del dibujo = 1 mm a tamaño de impresión
NARANJA_RED = C["NARANJA"]   # vmbr1 (red interna)
AZUL_RED = C["AZUL"]         # vmbr0 (red del instituto)
GO = C["GRIS_OSCURO"]
MONO = "Liberation Mono"


def lienzo(ancho_mm, alto_mm):
    fig = plt.figure(figsize=(ancho_mm * MM, alto_mm * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, ancho_mm); ax.set_ylim(0, alto_mm); ax.axis("off")
    return fig, ax


def caja(ax, x, y, w, h, borde, fondo, lw=1.3, ls="-", r=1.2, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fondo, ec=borde, lw=lw, ls=ls, zorder=z))


def t(ax, x, y, s, tam=8, color=None, peso="normal", ha="center", va="center", mono=False, z=5, **kw):
    ax.text(x, y, s, fontsize=tam, color=color or GO, fontweight=peso, ha=ha, va=va,
            family=MONO if mono else None, zorder=z, **kw)


def linea(ax, xs, ys, color, lw=1.6, ls="-", z=3):
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="butt")


def punto(ax, x, y, color):
    ax.plot([x], [y], "o", ms=3.6, color=color, zorder=6)


def flecha(ax, x0, y0, x1, y1, color=None, lw=1.4, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=color or GO, lw=lw, ls=ls,
                                shrinkA=0, shrinkB=0, mutation_scale=10))


def guardar(fig, nombre):
    ruta = f"{FIG}/{nombre}"
    fig.savefig(ruta, dpi=250, bbox_inches=None)
    plt.close(fig)
    return ruta


# ---------------------------------------------------------------------------
# Figura 1 · Instalar HA en una VM (pasos)
# ---------------------------------------------------------------------------
def fig_pasos():
    fig, ax = lienzo(170, 34)
    pasos = ["1  Descargar\nla imagen de HAOS", "2  Crear la VM\n(UEFI, red puente)",
             "3  Poner la imagen\ncomo disco", "4  Arrancar\ny esperar", "5  Navegador y\nasistente inicial"]
    w, g = 29.8, 4.5
    for i, s in enumerate(pasos):
        x = 1 + i * (w + g)
        caja(ax, x, 6, w, 22, C["VERDE"], C["VERDE_CLARO"])
        t(ax, x + w / 2, 17, s, tam=8.5)
        if i < 4:
            flecha(ax, x + w + 0.6, 17, x + w + g - 0.6, 17)
    return guardar(fig, "servidor_pasos.png")


# ---------------------------------------------------------------------------
# Figura 2 · Arquitectura por capas
# ---------------------------------------------------------------------------
def fig_arquitectura():
    W, H = 170, 200
    fig, ax = lienzo(W, H)

    # --- Red del instituto (abajo) ---
    caja(ax, 12, 1, 146, 15, GO, "#FFFFFF", lw=1.2, ls="--")
    t(ax, 85, 11.2, "RED DEL INSTITUTO", tam=9, peso="bold")
    t(ax, 85, 5.6, "Los PCs del aula abren su Home Assistant en el navegador (http://10.202.51.81 … .87)",
      tam=8)

    # --- Capa 1: mini-PC ---
    y1, h1 = 24, 24
    caja(ax, 2, y1, 166, h1, C["PIZARRA"], C["PIZARRA_CLARO"], lw=1.6)
    t(ax, 6, y1 + h1 - 5, "1 · MINI-PC: el ordenador físico, el que se puede tocar", tam=9.5,
      peso="bold", ha="left", color=C["PIZARRA"])
    t(ax, 6, y1 + h1 - 12, "MSI Cubi 5 10M · Intel Core i3-10110U (2 núcleos / 4 hilos)", tam=8, ha="left")
    t(ax, 6, y1 + h1 - 18, "16 GB de RAM · disco NVMe de 500 GB · una sola toma Ethernet", tam=8, ha="left")
    # toma Ethernet
    px = 157
    ax.add_patch(Rectangle((px - 4, y1 - 0.2), 8, 5, fc="#FFFFFF", ec=GO, lw=1.2, zorder=6))
    t(ax, px - 6, y1 + 3.2, "toma Ethernet", tam=8, ha="right")
    linea(ax, [px, px], [y1, 16], GO, lw=2.2)
    t(ax, px - 2, 20, "cable de red", tam=8, ha="right")

    # --- Capa 2: Proxmox ---
    y2, h2 = 54, 44
    y2 += 0
    caja(ax, 2, y2, 166, h2, C["VERDE_OSCURO"], C["VERDE_CLARO"], lw=1.8)
    yb0, yb1 = y2 + h2 - 6, y2 + h2 - 13       # vmbr0 y vmbr1
    linea(ax, [6, 164], [yb0, yb0], AZUL_RED, lw=3.2, z=4)
    linea(ax, [12, 164], [yb1, yb1], NARANJA_RED, lw=3.2, z=4)
    # vmbr0 baja a la toma Ethernet
    linea(ax, [px, px], [yb0, y1 + 4.8], AZUL_RED, lw=2.2, z=3)
    punto(ax, px, yb0, AZUL_RED)
    # leyenda de las redes
    ax.add_patch(Rectangle((6, y2 + 24.2), 7, 2.2, fc=AZUL_RED, ec="none", zorder=5))
    t(ax, 15, y2 + 25.3, "vmbr0 · puente a la red del instituto (sale por la toma Ethernet)",
      tam=8, ha="left")
    ax.add_patch(Rectangle((6, y2 + 18.8), 7, 2.2, fc=NARANJA_RED, ec="none", zorder=5))
    t(ax, 15, y2 + 19.9, "vmbr1 · red interna 192.168.100.0/24, sin salida al exterior",
      tam=8, ha="left")
    t(ax, 6, y2 + 11.6, "2 · PROXMOX VE 9.2 = EL HIPERVISOR", tam=10, peso="bold", ha="left",
      color=C["VERDE_MUY_OSCURO"])
    t(ax, 6, y2 + 6.4, "Instalado directamente en el mini-PC. NO es una máquina virtual: es el que crea",
      tam=8, ha="left")
    t(ax, 6, y2 + 2.6, "y hace funcionar todas las de arriba.", tam=8, ha="left")

    # --- Capa 3: máquinas ---
    y3, h3 = 104, 94
    caja(ax, 2, y3, 166, h3, C["GRIS"], "#FBFBFB", lw=1.2)
    t(ax, 6, y3 + h3 - 5, "3 · LAS MÁQUINAS QUE CREA PROXMOX (todas «de mentira», dentro del mini-PC)",
      tam=9.5, peso="bold", ha="left", color=C["PIZARRA"])

    # VMs de alumnos (fila de abajo)
    vy, vh = y3 + 6, 40
    x0, bw, gap = 11, 22.6, 2.4
    for i in range(6):
        n = i + 1
        x = x0 + i * (bw + gap)
        cx = x + bw / 2
        caja(ax, x, vy, bw, vh, C["VERDE"], "#FFFFFF", lw=1.4)
        t(ax, cx, vy + vh - 4.5, f"VM {120 + n}", tam=8.5, peso="bold")
        t(ax, cx, vy + vh - 10, f"ha-alumno0{n}", tam=8, mono=True)
        t(ax, cx, vy + vh - 16, f"Grupo {n}", tam=9, peso="bold", color=C["VERDE_OSCURO"])
        t(ax, cx, vy + vh - 21.5, "HA · 1,5 GB", tam=8)
        t(ax, cx, vy + 11, f"10.202.51.8{n}", tam=8, color=AZUL_RED, peso="bold")
        t(ax, cx, vy + 6, f"192.168.100.2{n}", tam=8, color=NARANJA_RED, peso="bold")
        # conexiones
        xa, xb = cx - 5, cx + 5
        linea(ax, [xa, xa], [vy, yb0], AZUL_RED, lw=1.6)
        punto(ax, xa, yb0, AZUL_RED)
        linea(ax, [xb, xb], [vy, yb1], NARANJA_RED, lw=1.6)
        punto(ax, xb, yb1, NARANJA_RED)

    # fila de arriba: escaparate, plantilla y contenedor
    ty, th = y3 + 50, 34
    # 127 escaparate
    caja(ax, 11, ty, 48, th, C["AZUL"], "#FFFFFF", lw=1.4)
    t(ax, 35, ty + th - 4.5, "VM 127 · ha-escaparate", tam=8.5, peso="bold")
    t(ax, 35, ty + th - 10.5, "HA con los dashboards", tam=8)
    t(ax, 35, ty + th - 15, "de una vivienda real", tam=8)
    t(ax, 35, ty + th - 20.5, "Invitado · 2 GB", tam=8)
    t(ax, 35, ty + 5, "10.202.51.87", tam=8, color=AZUL_RED, peso="bold")
    xe = 6.5
    linea(ax, [11, xe, xe], [ty + 5, ty + 5, yb0], AZUL_RED, lw=1.6)
    punto(ax, xe, yb0, AZUL_RED)
    # 9000 plantilla
    caja(ax, 63, ty, 44, th, C["GRIS"], "#F2F2F2", lw=1.3, ls="--")
    t(ax, 85, ty + th - 4.5, "9000 · haos-plantilla", tam=8.5, peso="bold", color=C["GRIS"])
    t(ax, 85, ty + th - 11, "el molde del que se", tam=8, color=C["GRIS"])
    t(ax, 85, ty + th - 15.5, "copiaron las VMs", tam=8, color=C["GRIS"])
    t(ax, 85, ty + 6, "APAGADA · 2 GB", tam=8, peso="bold", color=C["GRIS"])
    # 128 contenedor
    caja(ax, 111, ty, 49, th, C["MORADO"], "#FFFFFF", lw=1.4)
    t(ax, 135.5, ty + th - 4.5, "CT 128 · aula-mqtt", tam=8.5, peso="bold")
    t(ax, 135.5, ty + th - 10.5, "contenedor (LXC) · 1 GB", tam=8)
    t(ax, 135.5, ty + th - 15, "Mosquitto común, simulador", tam=8)
    t(ax, 135.5, ty + th - 19, "y Zigbee2MQTT", tam=8)
    t(ax, 135.5, ty + 9.5, "10.202.51.88", tam=8, color=AZUL_RED, peso="bold")
    t(ax, 135.5, ty + 4, "192.168.100.28", tam=8, color=NARANJA_RED, peso="bold")
    xc0, xc1 = 162.5, 165.5
    linea(ax, [160, xc0, xc0], [ty + 9.5, ty + 9.5, yb0], AZUL_RED, lw=1.6)
    punto(ax, xc0, yb0, AZUL_RED)
    linea(ax, [160, xc1, xc1], [ty + 4, ty + 4, yb1], NARANJA_RED, lw=1.6)
    punto(ax, xc1, yb1, NARANJA_RED)
    return guardar(fig, "servidor_arquitectura.png")


# ---------------------------------------------------------------------------
# Figura 3 · MQTT del aula
# ---------------------------------------------------------------------------
def fig_mqtt():
    W, H = 170, 122
    fig, ax = lienzo(W, H)
    PEND = "#9A9A9A"
    PUENTE = C["VERDE_OSCURO"]
    VIRT = C["MORADO"]

    # contenedor
    caja(ax, 34, 80, 134, 40, C["MORADO"], "#FBF9FD", lw=1.3)
    t(ax, 38, 116, "CT 128 · aula-mqtt (contenedor)", tam=8.5, peso="bold", ha="left", color=C["MORADO"])
    # Zigbee2MQTT (pendiente)
    caja(ax, 40, 97, 46, 14, PEND, "#F2F2F2", lw=1.3, ls="--")
    t(ax, 63, 106.5, "Zigbee2MQTT 2.14.3", tam=8, peso="bold", color=PEND)
    t(ax, 63, 101.2, "PARADO · PENDIENTE", tam=8, peso="bold", color=PEND)
    # Mosquitto común
    caja(ax, 40, 83, 46, 11, PUENTE, C["VERDE_CLARO"], lw=1.5)
    t(ax, 63, 90.8, "Mosquitto común", tam=8.5, peso="bold")
    t(ax, 63, 86, "192.168.100.28", tam=8)
    flecha(ax, 63, 97, 63, 94.2, color=PEND, ls="--")
    # simulador
    caja(ax, 112, 83, 50, 20, VIRT, C["MORADO_CLARO"], lw=1.5)
    t(ax, 137, 97.5, "Simulador", tam=8.5, peso="bold")
    t(ax, 137, 92.5, "virtual-sim", tam=8, mono=True)
    t(ax, 137, 87.5, "(dispositivos virtuales)", tam=8)
    # coordinador (pendiente)
    caja(ax, 1, 97, 26, 14, PEND, "#F2F2F2", lw=1.3, ls="--")
    t(ax, 14, 106.5, "Coordinador", tam=8, peso="bold", color=PEND)
    t(ax, 14, 101.2, "SLZB-06 · PEND.", tam=8, color=PEND)
    flecha(ax, 27, 104, 40, 104, color=PEND, ls="--")
    # «USB» en el hueco entre el coordinador y el borde del contenedor (no pisa el borde)
    t(ax, 30.5, 107, "USB", tam=8, color=PEND)

    # columnas de los grupos
    cxs = [16 + i * 27.4 for i in range(6)]
    bw = 23
    yP, yV = 66, 58            # buses: puentes y virtual
    for i, cx in enumerate(cxs):
        n = i + 1
        caja(ax, cx - bw / 2, 30, bw, 15, C["AZUL"], C["AZUL_CLARO"], lw=1.3)
        t(ax, cx, 40.3, "Mosquitto", tam=8, peso="bold")
        t(ax, cx, 34.5, f"de la VM {120 + n}", tam=8)
        caja(ax, cx - bw / 2, 3, bw, 15, C["VERDE"], "#FFFFFF", lw=1.4)
        t(ax, cx, 13.3, "HA del", tam=8, peso="bold")
        t(ax, cx, 7.5, f"Grupo {n}", tam=8.5, peso="bold", color=C["VERDE_OSCURO"])
        flecha(ax, cx, 30, cx, 18.2)
        # bajadas de los buses
        linea(ax, [cx - 5, cx - 5], [yP, 45], PUENTE, lw=1.6)
        punto(ax, cx - 5, yP, PUENTE)
        linea(ax, [cx + 5, cx + 5], [yV, 45], VIRT, lw=1.6)
        punto(ax, cx + 5, yV, VIRT)
    # buses
    linea(ax, [cxs[0] - 5, cxs[-1] - 5], [yP, yP], PUENTE, lw=3)
    linea(ax, [cxs[0] + 5, cxs[-1] + 5], [yV, yV], VIRT, lw=3)
    # del común al bus de puentes
    linea(ax, [63, 63], [83, yP], PUENTE, lw=2.2)
    punto(ax, 63, yP, PUENTE)
    # del simulador al bus virtual (cruza el de puentes sin unirse)
    linea(ax, [158, 158], [83, yV], VIRT, lw=2.2)
    punto(ax, 158, yV, VIRT)
    # etiquetas de los buses
    t(ax, 60, 77.5, "puentes de Mosquitto", tam=8, ha="right", color=PUENTE, peso="bold")
    t(ax, 60, 73.3, "por la red interna (usuario puente)", tam=8, ha="right", color=PUENTE)
    t(ax, 60, 69.1, "temas zigbee2mqtt/… y homeassistant/…", tam=8, ha="right", color=PUENTE)
    t(ax, 155, 75.5, "temas virtual/…", tam=8, ha="right", color=VIRT, peso="bold")
    t(ax, 155, 71.3, "(no pasan por los puentes)", tam=8, ha="right", color=VIRT)
    return guardar(fig, "servidor_mqtt.png")


# ---------------------------------------------------------------------------
# Figura 4 · Cómo funciona el kit virtual
# ---------------------------------------------------------------------------
def fig_virtual():
    fig, ax = lienzo(170, 56)
    VIRT = C["MORADO"]
    caja(ax, 2, 12, 42, 30, VIRT, C["MORADO_CLARO"], lw=1.5)
    t(ax, 23, 33, "Simulador", tam=9, peso="bold")
    t(ax, 23, 27, "virtual-sim", tam=8, mono=True)
    t(ax, 23, 20.5, "(en el CT 128)", tam=8)
    caja(ax, 64, 12, 42, 30, C["AZUL"], C["AZUL_CLARO"], lw=1.5)
    t(ax, 85, 30, "Mosquitto", tam=9, peso="bold")
    t(ax, 85, 23.5, "de tu VM", tam=9)
    caja(ax, 126, 12, 42, 30, C["VERDE"], C["VERDE_CLARO"], lw=1.5)
    t(ax, 147, 33, "Home Assistant", tam=9, peso="bold")
    t(ax, 147, 26.5, "de tu grupo", tam=8.5)
    t(ax, 147, 20, "dispositivos y entidades", tam=8)
    # ida
    flecha(ax, 44, 36, 64, 36, color=VIRT); flecha(ax, 106, 36, 126, 36, color=VIRT)
    t(ax, 85, 51.5, "1 · El simulador presenta cada aparato (MQTT discovery) y publica su estado",
      tam=8, color=VIRT, peso="bold")
    t(ax, 54, 45.5, "virtual/…", tam=8, mono=True, color=VIRT)
    t(ax, 116, 45.5, "lo descubre", tam=8, color=VIRT)
    # vuelta
    flecha(ax, 64, 18, 44, 18, color=C["VERDE_OSCURO"]); flecha(ax, 126, 18, 106, 18, color=C["VERDE_OSCURO"])
    t(ax, 85, 4, "2 · Tus órdenes (un botón, una automatización, Publicar un paquete) vuelven al simulador",
      tam=8, color=C["VERDE_OSCURO"], peso="bold")
    t(ax, 54, 9.5, "virtual/…/set", tam=8, mono=True, color=C["VERDE_OSCURO"])
    t(ax, 116, 9.5, "orden", tam=8, color=C["VERDE_OSCURO"])
    return guardar(fig, "servidor_virtual.png")


# ---------------------------------------------------------------------------
# Documento
# ---------------------------------------------------------------------------
def documento(figs):
    doc = E.nuevo_documento("Nuestro servidor de prácticas",
                            "Cómo está montado el Home Assistant del aula y de dónde salen sus dispositivos",
                            titulo_corto="Nuestro servidor de prácticas")

    E.parrafo(doc, "En el aula hay **un solo ordenador** que hace funcionar **siete Home Assistant** a la vez: "
              "uno para cada grupo y otro de ejemplo. En este documento verás cómo se instala un Home Assistant "
              "en una máquina virtual, cómo está montado exactamente nuestro servidor, de dónde salen los "
              "dispositivos virtuales con los que vas a practicar y cómo se conectarán los aparatos reales.")
    E.nota(doc, "Qué es MQTT, qué es una entidad o una automatización está en el documento «Teoría: Home "
                "Assistant y MQTT». Cómo entrar en tu HA y las normas del aula, en la «Hoja 1 · Tu Home Assistant».")

    # ======================= 1 =======================
    E.h1(doc, "1. Cómo se instala un Home Assistant en una máquina virtual")
    E.parrafo(doc, "Antes de ver nuestro servidor, mira cómo se monta un Home Assistant **normal** en una "
              "**máquina virtual** (VM). Es lo que harías en casa o en una empresa con un ordenador que ya "
              "tiene un **hipervisor**: el programa que reparte el procesador, la memoria y el disco de un "
              "ordenador físico entre varias VMs. Aquí solo importa **entender qué se hace** en cada paso.")
    E.imagen(doc, figs["pasos"], 17, pie="Los cinco pasos para tener Home Assistant en una VM.")

    E.h2(doc, "Paso 1 · Descargar la imagen de HAOS")
    E.parrafo(doc, "**HAOS** (Home Assistant Operating System) es un sistema operativo preparado solo para "
              "ejecutar Home Assistant. No se instala desde un CD como Windows: se descarga una **imagen de "
              "disco** que ya trae todo instalado. Hay una para cada tipo de hipervisor: `.qcow2` para KVM "
              "(el que usa Proxmox VE), `.vmdk` para VMware y `.vdi` para VirtualBox.")

    E.h2(doc, "Paso 2 · Crear la VM")
    E.parrafo(doc, "En el hipervisor se crea una VM vacía y se eligen sus características:")
    E.lista(doc, [
        "**Memoria y procesador**: la documentación oficial pide como mínimo **2 GB de RAM y 2 procesadores "
        "virtuales (vCPU)**.",
        "**Firmware UEFI**: es el «arranque» moderno de los ordenadores (lo que sustituye a la BIOS). "
        "**HAOS no arranca sin UEFI.** En KVM se usa el UEFI llamado **OVMF**, en su versión **sin Secure "
        "Boot** (el arranque seguro, que solo deja arrancar sistemas firmados).",
        "**Tipo de máquina**: en Proxmox se elige **q35**, que imita una placa base moderna.",
        "**Red en modo puente**: la VM se enchufa a un «switch» interno que la une a la red de verdad. Así "
        "recibe su propia dirección IP y se ve en la red como un ordenador más.",
        "**Agente QEMU** (opcional): un pequeño programa dentro de la VM que le cuenta al hipervisor su "
        "dirección IP y le deja apagarla de forma ordenada.",
    ])

    E.h2(doc, "Paso 3 · Poner la imagen como disco")
    E.parrafo(doc, "La imagen descargada se **importa como disco duro** de la VM (no se monta como un CD). "
              "Ese disco ya es Home Assistant: no hay que «instalar» nada más. Después se puede agrandar; lo "
              "normal son **32 GB**.")

    E.h2(doc, "Paso 4 · Arrancar y esperar")
    E.parrafo(doc, "Al encender la VM, HAOS arranca y prepara Home Assistant. La primera vez **tarda**: la "
              "documentación avisa de que puede llevar bastantes minutos. En la pantalla de la VM aparece la "
              "dirección en la que se puede abrir.")

    E.h2(doc, "Paso 5 · Abrirlo en el navegador y hacer el asistente inicial")
    E.parrafo(doc, "Desde otro ordenador de la misma red se abre `http://homeassistant.local` o `http://IP` "
              "(la IP de la VM). Sale el **asistente inicial**, que pide, por este orden:")
    E.lista(doc, [
        "Crear la cuenta del **propietario** (nombre, usuario y contraseña). Es una cuenta de administrador. "
        "También se puede **restaurar una copia de seguridad** en vez de empezar de cero.",
        "La **ubicación** de la casa, en el mapa (sirve para la hora, el tiempo, la salida del sol…).",
        "Qué datos de uso se comparten con el proyecto (por defecto, ninguno).",
        "Los **dispositivos que ha encontrado** solo en la red, si hay alguno.",
        "*Terminar*: se abre el dashboard principal.",
    ], numerada=True)
    E.cajon(doc, "IDEA CLAVE", [
        "**¿Con `:8123` o sin puerto?** Durante años, Home Assistant se abría con `:8123` al final "
        "(`http://IP:8123`) y lo verás así en casi todos los tutoriales. Según la documentación oficial, "
        "un HAOS **recién instalado** con las versiones actuales ya se abre **sin puerto** (usa el puerto "
        "80, el normal de las páginas web). Se sigue usando `:8123` en otras formas de instalarlo y en las "
        "instalaciones anteriores.",
        "**En nuestro servidor se entra sin puerto**: `http://10.202.51.81`, por ejemplo.",
    ])

    # ======================= 2 =======================
    E.h1(doc, "2. Nuestro montaje exacto")
    E.parrafo(doc, "Nuestro servidor está montado **por capas**, como un edificio. Abajo, el ordenador "
              "físico. Encima, el hipervisor. Y encima del hipervisor, las máquinas virtuales y un "
              "contenedor. Mira la figura de la página siguiente y sigue la explicación capa a capa.")

    E.h2(doc, "Capa 1 · El mini-PC")
    E.tabla(doc, ["Pieza", "Qué lleva"], [
        ["Equipo", "Mini-PC **MSI Cubi 5 10M**. Antes era el servidor de Home Assistant de una vivienda real."],
        ["Procesador", "Intel **Core i3-10110U**: 2 núcleos y 4 hilos, diseñado para unos 15 W"],
        ["Memoria", "**16 GB instalados** (DDR4, dos módulos de 8 GB). Con todo encendido se usan unos **12 GB**."],
        ["Disco", "NVMe de **500 GB**"],
        ["Red", "**Una sola** toma Ethernet"],
    ], anchos_cm=[3.2, 13.8], negrita_col0=True)
    E.parrafo(doc, "Las cuentas de la memoria cuadran: seis VMs de 1,5 GB, el escaparate con 2 GB y el "
              "contenedor con 1 GB suman unos 12 GB. La plantilla está apagada y no gasta memoria.")

    E.h2(doc, "Capa 2 · Proxmox VE, el hipervisor")
    E.parrafo(doc, "**Proxmox VE 9.2** es el hipervisor. Está instalado **directamente en el mini-PC**, como "
              "si fuera su Windows: no hay nada debajo. Se instaló desde un pendrive en el que se grabó la "
              "imagen de Proxmox con el programa Rufus en **modo DD** (copia exacta, byte a byte). Proxmox "
              "es gratuito; usamos su repositorio de actualizaciones sin suscripción.")
    E.parrafo(doc, "El disco está preparado con **LVM-thin**, una forma de repartirlo que solo gasta el "
              "espacio que de verdad se usa y que permite hacer **instantáneas** (luego verás para qué). "
              "Con todo apagado, el servidor y todas sus VMs tardan unos **2,5 minutos** en arrancar.")

    E.imagen(doc, figs["arquitectura"], 17,
             pie="Nuestro servidor por capas. Azul: red del instituto (vmbr0). Naranja: red interna (vmbr1).")
    E.cajon(doc, "IDEA CLAVE", [
        "**Proxmox NO es una máquina virtual.** Es el programa que está instalado en el mini-PC físico y "
        "que crea y hace funcionar todas las máquinas virtuales. Las VMs están **encima** de Proxmox, "
        "no al lado.",
    ])

    E.h2(doc, "Capa 3 · Las máquinas")
    E.parrafo(doc, "Encima de Proxmox funcionan **siete VMs con Home Assistant**, **un contenedor** y "
              "**una plantilla** apagada. Un **contenedor (LXC)** es parecido a una VM pero más ligero: "
              "comparte el núcleo del sistema del servidor y solo aísla los programas.")
    E.tabla(doc, ["ID", "Nombre", "Qué es", "Memoria", "Dirección en el instituto", "Red interna"], [
        ["121", "ha-alumno01", "HA del Grupo 1", "1,5 GB", "http://10.202.51.81", "192.168.100.21"],
        ["122", "ha-alumno02", "HA del Grupo 2", "1,5 GB", "http://10.202.51.82", "192.168.100.22"],
        ["123", "ha-alumno03", "HA del Grupo 3", "1,5 GB", "http://10.202.51.83", "192.168.100.23"],
        ["124", "ha-alumno04", "HA del Grupo 4", "1,5 GB", "http://10.202.51.84", "192.168.100.24"],
        ["125", "ha-alumno05", "HA del Grupo 5", "1,5 GB", "http://10.202.51.85", "192.168.100.25"],
        ["126", "ha-alumno06", "HA del Grupo 6", "1,5 GB", "http://10.202.51.86", "192.168.100.26"],
        ["127", "ha-escaparate", "HA con los dashboards de una vivienda real", "2 GB",
         "http://10.202.51.87", "—"],
        ["128", "aula-mqtt", "Contenedor: Mosquitto común, simulador y Zigbee2MQTT", "1 GB",
         "10.202.51.88", "192.168.100.28"],
        ["9000", "haos-plantilla", "Plantilla de la que se copiaron las VMs (apagada)", "2 GB", "—", "—"],
    ], anchos_cm=[1.1, 2.9, 4.6, 1.6, 3.9, 2.9], mono_cols=(1, 4, 5), centrar_cols=(0, 3), tam=8.5)
    E.parrafo(doc, "Cada VM de alumno tiene **2 vCPU** y un disco de **32 GB**, y arrancan solas, en orden, "
              "al encender el servidor. Fíjate en el truco de las direcciones: en el instituto, cada "
              "máquina tiene la dirección `10.202.51.` seguida de **su ID menos 40** (121 − 40 = 81).")
    E.cajon(doc, "¿POR QUÉ?", [
        "**¿Por qué 1,5 GB, si la documentación pide 2 GB?** Para que quepan siete Home Assistant en 16 GB. "
        "Es algo menos de lo recomendado: es el precio de tener un HA propio para cada grupo en un solo "
        "mini-PC.",
    ])
    E.parrafo(doc, "La **plantilla** es una VM preparada y apagada que sirve de **molde**: las "
              "VMs se copiaron (clonaron) de ella. No la confundas con las plantillas (*templates*) de "
              "Home Assistant, que son otra cosa.")

    E.h2(doc, "Las dos redes")
    E.parrafo(doc, "Dentro de Proxmox hay dos **puentes de red**: dos «switches» internos que conectan las "
              "máquinas entre sí o con la red de verdad.")
    E.tabla(doc, ["Red", "Qué es", "Quién está conectado"], [
        ["vmbr0", "Puente a la **red del instituto**, por la única toma Ethernet del mini-PC. Por aquí "
                  "entras tú desde los PCs del aula.", "Las 7 VMs con HA y el contenedor"],
        ["vmbr1", "**Red interna** `192.168.100.0/24`, **sin salida al exterior**. Solo existe dentro del "
                  "mini-PC.", "Las 6 VMs de alumnos y el contenedor (para el MQTT)"],
    ], anchos_cm=[2.0, 10.0, 5.0], mono_cols=(0,), negrita_col0=True)
    E.parrafo(doc, "Desde el instituto, las VMs pueden salir a internet para abrir páginas web (por "
              "ejemplo, para el tiempo), pero el *ping* a internet no funciona: no te asustes si lo pruebas.")

    E.h2(doc, "Home Assistant en las VMs de alumnos")
    E.tabla(doc, ["Elemento", "Qué hay"], [
        ["Sistema operativo", "**HAOS 18.4** (la imagen para KVM/Proxmox)"],
        ["Home Assistant Core", "**2026.11.2**"],
        ["Idioma y ubicación", "En español y con la ubicación del instituto"],
        ["Apps (antes llamadas complementos)", "**Mosquitto broker 7.1.3** (con la integración MQTT ya puesta) y "
                                               "**File editor 6.3.1**"],
        ["Aparatos de la vivienda real", "Ninguno: se quitaron las integraciones que hablaban con aparatos de la vivienda"],
        ["Tiempo (Met.no)", "**Por comprobar** si viene configurada. Si no, la añadiréis vosotros."],
    ], anchos_cm=[5.0, 12.0], negrita_col0=True)
    E.parrafo(doc, "Cada VM es **independiente**: lo que haga un grupo no afecta a los demás. En cada una "
              "hay tres usuarios:")
    E.tabla(doc, ["Usuario", "Para qué sirve"], [
        ["admin", "El del profesor."],
        ["userN", "El de tu grupo: `user1` el Grupo 1, `user2` el Grupo 2… Es **administrador** y **solo puede "
                  "entrar desde la red local**."],
        ["puente", "Usuario de sistema que usan los puentes MQTT. **No sirve para entrar**: no lo toques."],
    ], anchos_cm=[2.5, 14.5], mono_cols=(0,))

    E.h2(doc, "El reset y la instantánea «limpio»")
    E.parrafo(doc, "Una **instantánea** (*snapshot*) es una «foto» del estado de una VM en un momento, a la "
              "que se puede volver cuando se quiera. Cada VM de alumno tiene una llamada `limpio`: es su "
              "estado de partida, recién preparado.")
    E.parrafo(doc, "Cuando el profesor hace el **reset** —normalmente entre clases—, tu VM vuelve a la "
              "instantánea `limpio` y se borra todo (el reset devuelve a la vez las seis VMs de alumnos a "
              "`limpio`). El escaparate y el contenedor no se tocan. Los dispositivos virtuales del kit "
              "vuelven solos, más o menos un minuto después.")
    E.cajon(doc, "¡OJO!", [
        "El reset **lo borra TODO** lo que haya hecho tu grupo: dashboards, automatizaciones, ayudantes, "
        "dispositivos añadidos… No hay forma de recuperarlo.",
        "- Antes de terminar, haz **capturas** o **exporta** lo que quieras guardar.",
    ])

    E.h2(doc, "El escaparate")
    E.parrafo(doc, "La VM 127 es un Home Assistant de ejemplo con los dashboards de **una vivienda real** "
              "(Home, Luces, Persianas, Energía, Aerotermia, Clima…) y su histórico. Sirve para ver cómo "
              "queda una casa terminada. Es una **foto fija**: no maneja ningún aparato y el profesor la "
              "actualiza de vez en cuando. Se entra desde la red del aula en `http://10.202.51.87`, como "
              "**Invitado**, sin contraseña.")

    E.h2(doc, "El MQTT del aula")
    E.parrafo(doc, "Home Assistant solo admite **un** broker MQTT. Por eso cada VM tiene **su propio "
              "Mosquitto**, y en el contenedor hay un **Mosquitto común** para los aparatos que compartirá "
              "toda la clase. El común se une con el Mosquitto de cada VM mediante **puentes** de Mosquitto: "
              "conexiones que copian de un broker a otro solo los temas elegidos. Van por la red interna, "
              "con el usuario `puente`.")
    E.tabla(doc, ["Sentido del puente", "Temas que pasan", "Para qué"], [
        ["Del común a tu VM", "`zigbee2mqtt/#` y `homeassistant/#`", "Que veas los dispositivos reales"],
        ["De tu VM al común", "`zigbee2mqtt/+/set`, `zigbee2mqtt/+/set/+` y `zigbee2mqtt/+/get`",
         "Que les puedas mandar órdenes, pero no gestionar Zigbee2MQTT"],
    ], anchos_cm=[3.4, 7.6, 6.0], negrita_col0=True)
    E.parrafo(doc, "**Zigbee2MQTT 2.14.3** ya está instalado en el contenedor, pero **parado** hasta que "
              "se conecte el coordinador Zigbee (**pendiente**, lo verás en el apartado 4).")

    E.imagen(doc, figs["mqtt"], 17,
             pie="El MQTT del aula. Flechas negras: la integración MQTT de cada HA. En gris y a trazos, lo pendiente.")

    # ======================= 3 =======================
    E.h1(doc, "3. El sistema de dispositivos virtuales")
    E.h2(doc, "Por qué virtuales")
    E.parrafo(doc, "Para practicar hacen falta persianas, luces, enchufes y termostatos. No hay un aparato "
              "real para cada grupo, y si seis grupos manejaran a la vez la misma persiana sería un lío. "
              "Con los **dispositivos virtuales**, cada grupo tiene **los suyos**, puede probar todo lo que "
              "quiera y **no rompe nada**. Un dispositivo virtual no existe físicamente: lo imita un "
              "programa, pero en HA se ve y se maneja como uno real.")

    E.h2(doc, "Cómo funciona")
    E.parrafo(doc, "En el contenedor funciona un programa, el **simulador** (`virtual-sim`), que imita "
              "dispositivos Zigbee igual que lo haría Zigbee2MQTT. Los publica en **el Mosquitto de tu VM** "
              "y tu HA los descubre solo por **MQTT discovery**: aparecen en **Ajustes → Dispositivos y "
              "servicios → MQTT**, sin configurar nada.")
    E.imagen(doc, figs["virtual"], 17, pie="Ida y vuelta de los mensajes entre el simulador y tu HA.")

    E.h2(doc, "El kit de cada grupo")
    E.parrafo(doc, "Cada grupo empieza con un **kit de 13 dispositivos** (99 entidades en total), más un "
              "dispositivo especial, el **«Virtual Bridge»**, que sirve para gestionar el kit. Los nombres "
              "están sacados de una vivienda real.")
    E.tabla(doc, ["Nombre", "Tipo", "Imita a", "Qué hace"], [
        ["p_cocina, p_hab1, p_pc", "Persiana", "Módulo TS130F",
         "Sube, baja, para y va a una posición. Tarda 20, 22 y 25 s en hacer el recorrido."],
        ["toldo", "Toldo", "Interruptor de toldo BSEED", "Igual que una persiana; recorrido de 40 s."],
        ["luz_escaleras1", "Luz", "Relé", "Enciende y apaga."],
        ["luz_salon_cajon", "Luz regulable", "Bombilla TS0502B", "Brillo y blanco cálido o frío."],
        ["tira_rgb", "Tira RGB", "Controlador ZB-CL01", "Brillo, color y efectos (por ejemplo, `colorloop`)."],
        ["enchufe_pc, e_frigo, e_tv", "Enchufe con medida", "TS011F",
         "Potencia (W), corriente (A), tensión (V) y energía (kWh, vale para el panel de Energía). El PC "
         "varía; el frigorífico hace ciclos con pico de arranque; la TV gasta unos 85 W."],
        ["ter_hab1, ter_salon, ter_cocina", "Termostato de fan-coil", "Tuya TYBAC-006",
         "Calor, frío, ventilación o apagado; 4 velocidades y válvula. La temperatura de la sala sube o "
         "baja según la válvula."],
    ], anchos_cm=[3.9, 2.6, 3.2, 7.3], mono_cols=(0,), tam=8.5)
    E.parrafo(doc, "Algunos `entity_id` del kit: `cover.p_cocina` (la persiana de la cocina), "
              "`light.tira_rgb`, `switch.e_frigo` (encender o apagar el frigorífico), "
              "`sensor.e_frigo_power` (su potencia), `sensor.e_frigo_summation_delivered` (su energía), "
              "`climate.ter_salon` y `binary_sensor.ter_salon_valve` (la válvula del salón).",
              alineacion="izquierda")
    E.hueco_captura(doc, "Ajustes → Dispositivos y servicios → MQTT, lista de dispositivos de un grupo "
                         "recién reseteado: los 13 del kit y el «Virtual Bridge»", alto_cm=5.5)

    E.h2(doc, "Cómo distinguirlos de los reales")
    E.parrafo(doc, "Abre la ficha del dispositivo: en los virtuales, el **fabricante** es **«Virtual "
              "(aula)»** y el **modelo** termina en **«(virtual)»**. Los reales llevarán el fabricante y el "
              "modelo de verdad.")
    E.hueco_captura(doc, "Ficha de un dispositivo virtual (por ejemplo, p_cocina) donde se lean el "
                         "fabricante «Virtual (aula)» y el modelo «… (virtual)»", alto_cm=4.5)

    E.h2(doc, "Altas, bajas y cambios de nombre")
    E.parrafo(doc, "Al kit se le pueden **añadir**, **quitar** y **cambiar de nombre** dispositivos "
              "publicando mensajes MQTT. Se hace en **Ajustes → Dispositivos y servicios → MQTT → "
              "Configurar** → *Publicar un paquete*: arriba el **tema** (*topic*) y debajo la **carga** "
              "(el mensaje). Las respuestas se ven con *Escuchar un tema*. Estas son las órdenes, "
              "tal cual (a la izquierda el tema, en el centro el mensaje):")
    _ts = E.tabla(doc, ["Tema", "Mensaje", "Qué hace"], [
        ["virtual/bridge/request/permit_join", '{"time": 254}',
         "Abre el emparejamiento durante un tiempo (en segundos), como en una red Zigbee de verdad. "
         "**Sin él, no se puede añadir nada.**"],
        ["virtual/bridge/request/device/add", '{"tipo": "persiana",\n"nombre": "p_hab2",\n"recorrido": 18}',
         "Añade un dispositivo del tipo y con el nombre que digas. Aparece en HA a los 3 s."],
        ["virtual/bridge/request/device/remove", '{"id": "p_hab2"}', "Quita el dispositivo que digas."],
        ["virtual/bridge/request/device/rename", '{"from": "p_hab2",\n"to": "p_dormitorio"}',
         "Le cambia el nombre (de `from` a `to`)."],
        ["virtual/bridge/request/kit/restablecer", "{}", "Deja el kit como al principio."],
        ["virtual/p_cocina/set", '{"position": 50}\n(o `OPEN` / `CLOSE` / `STOP`)',
         "Persiana de la cocina: a la posición 50 (o abrir, cerrar, parar)."],
        ["virtual/e_tv/set", "TOGGLE", "Enchufe de la TV: cambia de encendido a apagado o al revés."],
        ["virtual/tira_rgb/set", '{"state": "ON",\n"color":\n{"hex": "#ff8000"},\n"brightness": 150}',
         "Tira RGB: encendida, en naranja y con brillo 150."],
        ["virtual/ter_salon/set/\ncurrent_heating_setpoint", "22", "Termostato del salón: consigna a 22."],
    ], anchos_cm=[7.25, 4.6, 5.15], mono_cols=(0, 1), tam=9)
    E.tabla(doc, ["Para device/add", "Qué puedes poner"], [
        ["tipos", "`persiana`, `toldo`, `enchufe`, `luz`, `luz_regulable`, `luz_rgb`, `termostato`"],
        ["enchufe", '`"perfil": "pc|frigo|tv|generico"`, `"potencia": 60`'],
    ], anchos_cm=[3.4, 13.6], mono_cols=(0,), tam=9)
    E.parrafo(doc, "Las órdenes `.../set` mandan una orden a un dispositivo, igual que si tocaras su tarjeta en "
              "HA. El Virtual Bridge tiene además la entidad `switch.virtual_bridge_permit_join`.", alineacion="izquierda")
    E.parrafo(doc, "Las respuestas del simulador llegan a `virtual/bridge/response/…` y sus avisos, a "
              "`virtual/bridge/logging`. Escucha `virtual/bridge/#` para verlo todo.", alineacion="izquierda")
    E.hueco_captura(doc, "Pantalla Publicar un paquete (MQTT → Configurar) con el tema "
                         "virtual/bridge/request/permit_join y la carga {\"time\": 254} escritos",
                    alto_cm=5.5)
    E.cajon(doc, "¡OJO!", [
        "Límites del simulador:",
        "- Nombres solo con **minúsculas, números y `_`** (nada de espacios, tildes ni mayúsculas).",
        "- Como mucho **40 dispositivos** por grupo.",
        "- Todo lo que añadas **desaparece con el reset**. Después del reset vuelve el kit de 13.",
    ])
    E.cajon(doc, "¿POR QUÉ?", [
        "**¿Por qué no se mezclan con los reales?** Los virtuales usan temas que empiezan por "
        "`virtual/`, y los puentes solo dejan pasar `zigbee2mqtt/…` y `homeassistant/…`. Así, lo que "
        "hagas con tus virtuales se queda en tu VM y nunca llega al broker común ni a otros grupos.",
    ])

    # ======================= 4 =======================
    E.h1(doc, "4. De virtual a real (pendiente)")
    E.cajon(doc, "¡OJO!", [
        "**PENDIENTE: esto todavía no funciona.** Aquí se explica cómo se va a montar. Hasta entonces, "
        "en tu HA solo hay dispositivos virtuales.",
    ])
    E.h2(doc, "Cómo se montan los aparatos reales")
    E.lista(doc, [
        "Un **coordinador Zigbee SLZB-06** (el aparato que crea y dirige la red Zigbee) se conecta por "
        "**USB** al mini-PC. Proxmox se lo pasa al contenedor `aula-mqtt`.",
        "En el contenedor, **Zigbee2MQTT** habla con el coordinador y convierte cada aparato en temas "
        "MQTT del **Mosquitto común** (`zigbee2mqtt/…`).",
        "Los **puentes** copian esos temas al Mosquitto de cada VM.",
        "El Home Assistant de cada grupo los ve con su integración MQTT, como los virtuales.",
    ], numerada=True)
    E.parrafo(doc, "Serán **tres aparatos**, iguales a los de la vivienda real: **un termostato Tuya "
              "TYBAC-006** y **dos módulos de persiana TS130F**. Se emparejan antes de llevarlos al aula y "
              "sus nombres empezarán por `aula_` (por ejemplo, `aula_persiana1` o `aula_termostato`).")

    E.h2(doc, "Qué cambia y qué no para ti")
    E.parrafo(doc, "**Tu forma de trabajar no cambia**: siguen siendo entidades MQTT en tu HA, y las "
              "tarjetas, automatizaciones y scripts se hacen igual. Lo que cambia está en la tabla:", juntos=True)
    _tvr = E.tabla(doc, ["", "Dispositivos virtuales", "Dispositivos reales (pendiente)"], [
        ["Qué son", "Programas que imitan aparatos", "Aparatos físicos en el aula"],
        ["De quién son", "De tu grupo: cada grupo tiene los suyos", "**Compartidos por todos los grupos**"],
        ["Cuántos", "El kit de 13, y puedes añadir más", "3: un termostato y dos persianas"],
        ["Nombres", "`p_cocina`, `tira_rgb`, `ter_salon`…", "Con el prefijo `aula_`"],
        ["Fabricante y modelo", "«Virtual (aula)» y «… (virtual)»", "Los de verdad (Tuya…)"],
        ["Tema MQTT", "`virtual/…`", "`zigbee2mqtt/…`"],
        ["Por dónde llegan", "Del simulador al Mosquitto de tu VM", "Del Mosquitto común, por los puentes"],
        ["Altas y bajas", "Tú, con `virtual/bridge/request/…`", "No: solo se mandan órdenes"],
        ["Con el reset", "Vuelve el kit; lo añadido se pierde", "El reset es de tu VM: los aparatos reales no están en ella"],
        ["En tu HA", "Entidades MQTT", "Entidades MQTT (igual)"],
    ], anchos_cm=[3.4, 6.8, 6.8], negrita_col0=True, tam=9)
    # la tabla entera en una sola página (con su título y el párrafo de antes)
    for _f in _tvr.rows[:-1]:
        for _c in _f.cells:
            for _p in _c.paragraphs:
                _p.paragraph_format.keep_with_next = True
    E.cajon(doc, "PISTA", [
        "Como los reales serán **de todos**, si tu automatización sube una persiana real, la verá "
        "subir toda la clase. Prueba primero con tus virtuales y pasa a los reales solo cuando funcione.",
    ])

    return doc


if __name__ == "__main__":
    figs = {"pasos": fig_pasos(), "arquitectura": fig_arquitectura(),
            "mqtt": fig_mqtt(), "virtual": fig_virtual()}
    doc = documento(figs)
    ruta = E.guardar(doc, SALIDA)
    pdf = E.a_pdf(ruta)
    import capturas_txt
    capturas_txt.escribir(doc, "2MT-HA-servidor", pdf)
    print(ruta, pdf)
