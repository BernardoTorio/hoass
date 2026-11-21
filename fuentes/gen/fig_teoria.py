"""Figuras de la teoría «Home Assistant y MQTT» (2MT). Uso: python3 fig_teoria.py"""
import sys, math
sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

C = E.mpl_estilo()
FIG = "/home/claude/material-ha/_trabajo/fig/"
CLAROS = {"VERDE": C["VERDE_CLARO"], "AZUL": C["AZUL_CLARO"], "MORADO": C["MORADO_CLARO"],
          "OCRE": C["OCRE_CLARO"], "PIZARRA": C["PIZARRA_CLARO"], "ROJO": C["ROJO_CLARO"]}


def caja(ax, x, y, w, h, texto, color="VERDE", tam=10, negrita=False, sub=None, subtam=8.5, ls="-", ty=0.63, sy=0.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=CLAROS[color], ec=C[color], lw=1.5, ls=ls))
    if sub:
        ax.text(x + w / 2, y + h * ty, texto, ha="center", va="center", fontsize=tam,
                fontweight="bold" if negrita else "normal", color=C["GRIS_OSCURO"])
        ax.text(x + w / 2, y + h * sy, sub, ha="center", va="center", fontsize=subtam,
                color=C["GRIS_OSCURO"], linespacing=1.2)
    else:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=tam,
                fontweight="bold" if negrita else "normal", color=C["GRIS_OSCURO"], linespacing=1.25)


def flecha(ax, x1, y1, x2, y2, color="GRIS_OSCURO", texto=None, tx=0, ty=0.12, tam=8.5, doble=False, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="<|-|>" if doble else "-|>", color=C[color], lw=1.4,
                                mutation_scale=12, ls=ls, shrinkA=0, shrinkB=0))
    if texto:
        ax.text((x1 + x2) / 2 + tx, (y1 + y2) / 2 + ty, texto, ha="center", va="bottom",
                fontsize=tam, color=C[color], family="monospace" if "/" in texto else "sans-serif")


def lienzo(w, h, ancho_in):
    fig, ax = plt.subplots(figsize=(ancho_in, ancho_in * h / w))
    ax.set_xlim(0, w); ax.set_ylim(0, h); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(FIG + nombre, dpi=220)
    plt.close(fig)


# 1. Capas de nuestro Home Assistant ---------------------------------------------------
def capas():
    fig, ax = lienzo(16, 9.6, 6.6)
    # Hardware y Proxmox
    caja(ax, 0.2, 0.2, 15.6, 1.2, "Mini-PC (procesador, memoria, disco y red)", "PIZARRA", 10, True)
    caja(ax, 0.2, 1.6, 15.6, 1.2, "Proxmox VE: el hipervisor, que crea y reparte las máquinas virtuales", "PIZARRA", 10)
    # Máquina virtual de un grupo
    ax.add_patch(FancyBboxPatch((0.2, 3.05), 11.4, 6.3, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="white", ec=C["VERDE_OSCURO"], lw=1.6, ls="--"))
    ax.text(0.45, 9.0, "La VM de tu grupo (ha-alumno0N)", fontsize=9.5, color=C["VERDE_OSCURO"],
            fontweight="bold", va="center")
    caja(ax, 0.5, 3.3, 10.8, 1.2, "HAOS: el sistema operativo, preparado solo para HA", "AZUL", 9.5)
    caja(ax, 0.5, 4.75, 10.8, 1.3, "Supervisor", "MORADO", 10.5, True,
         sub="instala, arranca y actualiza lo de arriba y hace las copias", subtam=8.5)
    caja(ax, 0.5, 6.3, 5.6, 2.35, "Core", "VERDE", 11, True,
         sub="integraciones, entidades,\nautomatizaciones,\ndashboards e interfaz web", subtam=8.5, ty=0.8, sy=0.36)
    caja(ax, 6.35, 6.3, 4.95, 2.35, "Apps", "OCRE", 11, True,
         sub="Mosquitto broker\nFile editor\n(antes «complementos»)", subtam=8.5, ty=0.8, sy=0.36)
    # Otras VMs
    caja(ax, 11.9, 3.05, 3.9, 6.3, "Otras VMs\ny el contenedor\nMQTT\n\n(cada una con\nlo suyo)", "PIZARRA", 9.5,
         ls="--")
    guardar(fig, "teoria_capas.png")


# 2. Automatización ----------------------------------------------------------------------
def automatizacion():
    fig, ax = lienzo(16, 5.0, 6.6)
    datos = [("DESENCADENANTE", "¿Cuándo empieza?", "OCRE",
              "La potencia del\nfrigorífico\nsube de 300 W\n(sensor.e_frigo_power)"),
             ("CONDICIÓN", "¿Se cumple? (opcional)", "AZUL",
              "Solo si la persiana\nde la cocina está\nabierta\n(cover.p_cocina)"),
             ("ACCIÓN", "¿Qué hace?", "VERDE",
              "Enciende la tira RGB\nen rojo, como aviso\n\n(light.tira_rgb)")]
    for i, (t, p, col, ej) in enumerate(datos):
        x = 0.2 + i * 5.4
        caja(ax, x, 3.0, 4.6, 1.8, t, col, 9.5 if len(t) > 12 else 11, True, sub=p, subtam=9)
        ax.add_patch(FancyBboxPatch((x, 0.15), 4.6, 2.55, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="white", ec=C[col], lw=1.1, ls="--"))
        ax.text(x + 2.3, 1.42, ej, ha="center", va="center", fontsize=8.8, color=C["GRIS_OSCURO"],
                linespacing=1.25)
        if i < 2:
            flecha(ax, x + 4.65, 3.9, x + 5.35, 3.9)
    ax.text(0.2 + 2 * 5.4 + 2.3, 2.95, "", fontsize=1)
    guardar(fig, "teoria_automatizacion.png")


# 3. Publicación / suscripción --------------------------------------------------------
def pubsub():
    fig, ax = lienzo(16, 7.4, 6.6)
    caja(ax, 6.0, 2.6, 4.0, 2.0, "BROKER", "VERDE", 12, True, sub="Mosquitto de tu VM", subtam=9)
    # publicadores
    caja(ax, 0.2, 4.6, 4.0, 1.6, "Simulador", "PIZARRA", 10, True, sub="publica el estado", subtam=8.5)
    caja(ax, 0.2, 1.0, 4.0, 1.6, "Home Assistant", "AZUL", 10, True, sub="publica órdenes", subtam=8.5)
    # suscriptores
    caja(ax, 11.8, 4.6, 4.0, 1.6, "Home Assistant", "AZUL", 10, True, sub="suscrito al estado", subtam=8.5)
    caja(ax, 11.8, 1.0, 4.0, 1.6, "Simulador", "PIZARRA", 10, True, sub="suscrito a las órdenes", subtam=8.5)
    flecha(ax, 4.25, 5.4, 5.95, 4.2, "OCRE")
    ax.text(8.0, 5.05, "estado de la persiana", fontsize=8.5, color=C["OCRE"], ha="center")
    flecha(ax, 10.05, 4.2, 11.75, 5.4, "OCRE")
    flecha(ax, 4.25, 1.8, 5.95, 3.0, "MORADO")
    ax.text(8.0, 0.35, "orden: virtual/p_cocina/set   {\"position\": 50}", fontsize=8.5, color=C["MORADO"],
            family="monospace", ha="center")
    flecha(ax, 10.05, 3.0, 11.75, 1.8, "MORADO")
    ax.text(8.0, 7.0, "Nadie habla directamente con nadie: todo pasa por el broker", ha="center",
            fontsize=9.5, color=C["GRIS_OSCURO"], style="italic")
    ax.text(2.2, 6.35, "publican", ha="center", fontsize=9, color=C["GRIS"], fontweight="bold")
    ax.text(13.8, 6.35, "reciben", ha="center", fontsize=9, color=C["GRIS"], fontweight="bold")
    guardar(fig, "teoria_pubsub.png")


# 4. Árbol de temas -----------------------------------------------------------------------
def temas():
    fig, ax = lienzo(16, 7.0, 6.6)
    def nodo(x, y, t, col="VERDE", w=None):
        w = w or (0.27 * len(t) + 0.5)
        ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.32), w, 0.64, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    fc=CLAROS[col], ec=C[col], lw=1.2))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.5, family="monospace", color=C["GRIS_OSCURO"])
    def linea(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1 - 0.32, y2 + 0.32], color=C["GRIS"], lw=1)
    # raíz virtual
    nodo(3.7, 6.3, "virtual", "PIZARRA")
    hijos = [(1.6, "p_cocina"), (3.8, "e_tv"), (6.0, "tira_rgb")]
    for x, t in hijos:
        linea(3.7, 6.3, x, 4.8); nodo(x, 4.8, t, "AZUL")
        linea(x, 4.8, x, 3.3); nodo(x, 3.3, "set", "OCRE")
    ax.text(3.8, 2.35, "virtual/+/set", ha="center", fontsize=9.5, family="monospace",
            color=C["ROJO"], fontweight="bold")
    ax.text(3.8, 1.85, "recoge las órdenes de\ntodos los dispositivos virtuales", ha="center",
            va="top", fontsize=8.5, color=C["GRIS_OSCURO"])
    # raíz zigbee2mqtt
    nodo(11.5, 6.3, "zigbee2mqtt", "PIZARRA")
    hijos = [(9.4, "bridge"), (13.3, "aula_persiana1")]
    for x, t in hijos:
        linea(11.5, 6.3, x, 4.8); nodo(x, 4.8, t, "AZUL")
    linea(9.4, 4.8, 9.4, 3.3); nodo(9.4, 3.3, "state", "OCRE")
    linea(13.3, 4.8, 13.3, 3.3); nodo(13.3, 3.3, "set", "OCRE")
    ax.text(11.5, 2.35, "zigbee2mqtt/#", ha="center", fontsize=9.5, family="monospace",
            color=C["ROJO"], fontweight="bold")
    ax.text(11.5, 1.85, "recoge todo lo que cuelga\nde zigbee2mqtt, a cualquier nivel", ha="center",
            va="top", fontsize=8.5, color=C["GRIS_OSCURO"])
    ax.plot([7.6, 7.6], [0.3, 6.7], color=C["GRIS_BORDE"], lw=1, ls=":")
    ax.text(0.1, 0.35, "Cada caja es un nivel; los niveles se separan con «/». aula_persiana1: nombre previsto (pendiente).",
            fontsize=8, color=C["GRIS"], style="italic")
    guardar(fig, "teoria_temas.png")


# 5. Red Zigbee en malla ----------------------------------------------------------------
def zigbee():
    fig, ax = lienzo(16, 8.0, 6.6)
    nodos = {"C": (3.0, 4.2), "R1": (7.0, 6.4), "R2": (7.6, 2.6), "R3": (11.4, 4.6),
             "F1": (11.6, 7.2), "F2": (14.4, 3.0), "F3": (11.2, 0.8)}
    enlaces = [("C", "R1"), ("C", "R2"), ("R1", "R2"), ("R1", "R3"), ("R2", "R3"),
               ("R1", "F1"), ("R3", "F2"), ("R2", "F3")]
    for a, b in enlaces:
        (x1, y1), (x2, y2) = nodos[a], nodos[b]
        fin = b.startswith("F")
        ax.plot([x1, x2], [y1, y2], color=C["GRIS"], lw=1.3, ls="--" if fin else "-", zorder=1)
    estilo = {"C": ("ROJO", 0.75), "R": ("AZUL", 0.6), "F": ("VERDE", 0.45)}
    for k, (x, y) in nodos.items():
        col, r = estilo[k[0]]
        ax.add_patch(Circle((x, y), r, fc=CLAROS[col], ec=C[col], lw=1.8, zorder=2))
        ax.text(x, y, k, ha="center", va="center", fontsize=9.5, fontweight="bold", color=C[col], zorder=3)
    ax.text(3.0, 3.1, "coordinador\n(SLZB-06)", ha="center", va="top", fontsize=8.5, color=C["GRIS_OSCURO"])
    ax.text(7.0, 7.15, "enchufe", ha="center", va="bottom", fontsize=8.5, color=C["GRIS_OSCURO"])
    ax.text(7.6, 1.85, "módulo de\npersiana", ha="center", va="top", fontsize=8.5, color=C["GRIS_OSCURO"])
    ax.text(12.15, 4.6, "termostato", ha="left", va="center", fontsize=8.5, color=C["GRIS_OSCURO"])
    ax.text(12.2, 7.2, "sensor de puerta", ha="left", va="center", fontsize=8.5, color=C["GRIS_OSCURO"])
    ax.text(14.4, 2.4, "sensor de\ntemperatura", ha="center", va="top", fontsize=8.5, color=C["GRIS_OSCURO"])
    ax.text(11.8, 0.8, "sensor de agua", ha="left", va="center", fontsize=8.5, color=C["GRIS_OSCURO"])
    # Zigbee2MQTT
    caja(ax, 0.1, 6.0, 3.6, 1.6, "Zigbee2MQTT", "PIZARRA", 9.5, True, sub="→ temas MQTT", subtam=8.5)
    ax.plot([2.0, 3.0], [6.0, 4.95], color=C["GRIS_OSCURO"], lw=1.5)
    ax.text(2.25, 5.35, "USB", fontsize=8, color=C["GRIS_OSCURO"], ha="right")
    # leyenda
    ly = 0.55
    for i, (k, t) in enumerate([("C", "coordinador (uno por red)"), ("R", "router: alimentación fija, reenvía"),
                                ("F", "dispositivo final: a pilas, no reenvía")]):
        col, r = estilo[k]
        y = ly + (2 - i) * 0.62
        ax.add_patch(Circle((0.35, y), 0.2, fc=CLAROS[col], ec=C[col], lw=1.4))
        ax.text(0.7, y, t, va="center", fontsize=8.5, color=C["GRIS_OSCURO"])
    guardar(fig, "teoria_zigbee.png")


# 6. Puentes entre brokers ------------------------------------------------------------------
def puentes():
    fig, ax = lienzo(16, 9.4, 6.6)
    ax.set_ylim(-0.8, 8.6)
    ax.add_patch(FancyBboxPatch((0.2, 5.2), 15.6, 3.2, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="white", ec=C["PIZARRA"], lw=1.3, ls="--"))
    ax.text(0.45, 8.05, "Contenedor aula-mqtt (192.168.100.28)", fontsize=9, color=C["PIZARRA"], fontweight="bold")
    caja(ax, 0.6, 5.5, 3.6, 1.9, "Zigbee2MQTT", "PIZARRA", 9.5, True, sub="(pendiente)\ndispositivos reales", subtam=8)
    caja(ax, 5.6, 5.5, 4.4, 1.9, "Mosquitto común", "VERDE", 10.5, True, sub="broker común", subtam=8.5)
    caja(ax, 11.4, 5.5, 4.0, 1.9, "Simulador", "PIZARRA", 9.5, True, sub="dispositivos virtuales", subtam=8)
    flecha(ax, 4.25, 6.45, 5.55, 6.45, doble=True)
    # VMs
    xs = [0.4, 3.0, 5.6, 8.2]
    for i, x in enumerate(xs):
        etiqueta = "VM 0" + str(i + 1) if i < 3 else "VM 06"
        caja(ax, x, 0.2, 2.3, 2.4, "Mosquitto", "AZUL", 9, True, sub="de la " + etiqueta + "\n↓\nsu HA", subtam=8)
        flecha(ax, 7.8, 5.45, x + 1.15, 2.65, "VERDE", doble=True)
    # simulador → cada VM (virtual/): una línea como un bus por debajo de las VMs, con una flecha a cada una
    yb = -0.5
    ax.plot([13.4, 13.4], [5.45, yb], color=C["OCRE"], lw=1.4)
    ax.plot([xs[0] + 1.15, 13.4], [yb, yb], color=C["OCRE"], lw=1.4)
    for x in xs:
        ax.annotate("", xy=(x + 1.15, 0.17), xytext=(x + 1.15, yb),
                    arrowprops=dict(arrowstyle="-|>", color=C["OCRE"], lw=1.4, mutation_scale=12,
                                    shrinkA=0, shrinkB=0))
    ax.text(13.55, 3.3, "virtual/…\nva directo\nal Mosquitto\nde cada VM\n(no pasa por\nlos puentes)", fontsize=8,
            color=C["OCRE"], va="center")
    ax.text(9.8, 4.0, "puentes", fontsize=9, color=C["VERDE_OSCURO"], fontweight="bold", ha="left")
    ax.text(9.8, 3.05, "por la red interna\n192.168.100.0/24", fontsize=8, color=C["VERDE_OSCURO"], ha="left")
    guardar(fig, "teoria_puentes.png")


# 7. MQTT discovery -----------------------------------------------------------------------
def discovery():
    fig, ax = lienzo(16, 3.4, 6.6)
    caja(ax, 0.2, 0.15, 3.6, 2.1, "Aparato", "PIZARRA", 10, True, sub="(o el simulador)", subtam=8.5)
    caja(ax, 6.2, 0.15, 3.6, 2.1, "Broker", "VERDE", 10, True, sub="lo reparte", subtam=8.5)
    caja(ax, 12.0, 0.15, 3.8, 2.1, "Home Assistant", "AZUL", 10, True, sub="crea el dispositivo\ny sus entidades", subtam=8)
    flecha(ax, 3.85, 1.2, 6.15, 1.2, "OCRE")
    flecha(ax, 9.85, 1.2, 11.95, 1.2, "OCRE")
    ax.text(8.0, 2.75, "homeassistant/cover/<id>/config", ha="center", fontsize=9, family="monospace",
            color=C["OCRE"])
    guardar(fig, "teoria_discovery.png")


if __name__ == "__main__":
    capas(); automatizacion(); pubsub(); temas(); zigbee(); puentes(); discovery()
    print("ok")
