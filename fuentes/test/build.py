# -*- coding: utf-8 -*-
"""Monta test_ha.html con el motor de test_bloque2.html (Domótica) y las preguntas de preguntas.py."""
import json, re, random, base64, io, sys
from PIL import Image
from preguntas import Q

SRC = '/home/claude/testha/test_bloque2.html'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/testha/test_ha.html'
FIG = '/home/claude/material-ha/_trabajo/fig/'
FIGS = {'capas.png': ('teoria_capas.png', 'Teoría, figura 1: las capas de tu Home Assistant.'),
        'temas.png': ('teoria_temas.png', 'Teoría, figura 4: los temas forman un árbol; los comodines eligen ramas.'),
        'zigbee.png': ('teoria_zigbee.png', 'Teoría, figura 6: red Zigbee en malla (C coordinador, R routers, F dispositivos finales).')}


# ---- falsas alargadas a mano para que la buena no sea casi siempre la más larga (nº: (índice, texto))
LARGAS = {
 4:(0,"Las automatizaciones, que solo existen en Home Assistant OS"),
 5:(0,"Es la instalación recomendada hoy por la documentación oficial"),
 8:(0,"El sistema operativo que arranca la máquina virtual y hace funcionar todo lo demás, y que no se toca"),
 10:(1,"Una regla que HA ejecuta solo cuando pasa algo, con su desencadenante, su condición y su acción"),
 15:(2,"No tiene estado: una luz solo tiene atributos, y el brillo es el principal"),
 20:(0,"Estado, atributo y entidad, que es lo que sale en la ficha de cada dispositivo"),
 22:(0,"Que la persiana de la cocina esté abierta en ese momento"),
 23:(0,"Que la potencia del frigorífico pase de 300 W"),
 29:(0,"Una máquina virtual apagada que sirve de molde para copiar las máquinas virtuales de los grupos"),
 31:(2,"La lista de usuarios que pueden ver ese dashboard y cambiarlo"),
 33:(0,"Un sensor de potencia, en W, como sensor.e_frigo_power"),
 36:(0,"Normal: solo puede usar la casa, sin cambiar ningún ajuste, y entra desde cualquier sitio"),
 40:(0,"La integración Met.no, que reparte los mensajes del tiempo"),
 41:(2,"Crear un usuario y una contraseña en el broker para ese tema"),
 43:(2,"No, porque el segundo tiene un nivel más que el primero"),
 50:(2,"Manda a HA la potencia que está midiendo en ese momento"),
 51:(1,"Publicando SET 22 en virtual/bridge/request/device/add, como al añadir un dispositivo"),
 52:(2,"Que el broker lo guarda para siempre y se lo entrega a todos los clientes nuevos"),
 55:(0,"Un mensaje que el broker no deja pasar porque el cliente no ha puesto bien el usuario o la contraseña"),
 56:(0,"Para apagar todos los aparatos de la casa cuando se cierra Home Assistant, y que no se queden encendidos de noche"),
 61:(0,"El aparato que da internet a la casa y reparte las direcciones a los ordenadores y a los móviles"),
 63:(2,"Para pasar los temas de un broker a otro por la red interna del servidor del aula"),
 64:(2,"Hace de broker MQTT del aula y reparte los mensajes entre todas las máquinas virtuales"),
 65:(0,"Porque Mosquitto solo admite un cliente a la vez y en el aula hay seis grupos trabajando al mismo tiempo"),
 68:(0,"Emparejar aparatos nuevos, borrarlos y cambiarles el nombre, como hace el profesor"),
 69:(2,"La app de Home Assistant que hace las copias de seguridad de las máquinas virtuales"),
 70:(0,"Sí: es la máquina virtual número 1 y las demás máquinas virtuales se conectan a ella por la red"),
 73:(0,"El Home Assistant del profesor, con las contraseñas de todos los grupos"),
 76:(2,"Con :8883, que es el puerto cifrado"),
 78:(0,"Un texto entre llaves dobles que calcula un valor a partir de otras entidades de Home Assistant"),
 80:(1,"Una copia de la máquina virtual guardada en otro ordenador del instituto"),
 81:(1,"Solo los dispositivos añadidos al kit; los dashboards y las automatizaciones se quedan como estaban"),
 85:(0,"Con un Home Assistant vacío, sin dispositivos: cada grupo los añade"),
 86:(0,"Porque su nombre empieza por aula_ y en la lista sale con un icono distinto al de los demás"),
 89:(1,"En la app File editor, creando un archivo de texto con el tema y guardándolo en la carpeta de MQTT"),
 91:(0,"Solo tu grupo, porque cada grupo tiene sus propios dispositivos reales"),
 96:(1,"Del GPS del móvil del primero que entra con el usuario del grupo"),
 99:(0,"Nada: Home Assistant junta los cambios de los dos"),
}
Q = [list(x) for x in Q]
for n,(k,txt) in LARGAS.items():
    Q[n-1][7] = list(Q[n-1][7]); Q[n-1][7][k] = txt

assert len(Q) == 100, len(Q)
# ---- letras de la buena: 25 de cada una, sin tres iguales seguidas (siempre igual: semilla fija)
rnd = random.Random(2026)
while True:
    L = list('abcd') * 25
    rnd.shuffle(L)
    if not any(L[i] == L[i+1] == L[i+2] for i in range(98)):
        break

DATA, largas = [], []
for n, (tema, t, dif, tipo, cat, q, ok, d, j, img) in enumerate(Q, 1):
    assert len(d) == 3 and ok not in d, n
    assert dif in 'MD'
    for s in [q, ok, j] + d:
        assert '“' not in s and '”' not in s, (n, s)
    if all(len(ok) > len(x) for x in d):
        largas.append(n)
    DATA.append({"n": n, "ans": L[n-1], "tema": tema, "t": t, "dif": dif, "tipo": tipo, "q": q, "ok": ok, "d": d,
                 "j": j, "img": img, "cap": FIGS[img][1] if img else "", "cat": cat})
print('buena = la más larga en', len(largas), 'preguntas:', largas)
from collections import Counter
print(Counter(x['tema'] for x in DATA), Counter(x['dif'] for x in DATA), Counter(x['tipo'] for x in DATA))

IMGS = {}
for k, (f, _) in FIGS.items():
    im = Image.open(FIG + f).convert('RGB')
    w = 1200
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im = im.quantize(colors=64, method=Image.MEDIANCUT)
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    IMGS[k] = 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
    print(k, len(b.getvalue()) // 1024, 'kB')

TEMAS = {"HA": "Teoría · Home Assistant", "MQ": "Teoría · MQTT", "SRV": "Nuestro servidor", "P1": "Práctica 1"}
TIPO = {"CON": "Qué es cada cosa", "ENT": "Entidades, estados y energía", "AUT": "Automatizar",
        "MQT": "MQTT: broker, temas y mensajes", "ORD": "Órdenes a los dispositivos", "ZIG": "Zigbee y puentes",
        "SER": "El servidor por dentro", "VIR": "Dispositivos virtuales y reales", "NOR": "Usuarios, normas y reset",
        "PRA": "Dashboard del tiempo"}
CATS = [["Home Assistant", [["quees", "Qué es"], ["instalar", "Formas de instalarlo"], ["capas", "Las capas: Supervisor, Core y apps"],
                            ["entidades", "Integraciones, dispositivos y entidades"], ["estados", "Estados y atributos"],
                            ["auto", "Automatizaciones, scripts y escenas"], ["piezas", "Áreas, ayudantes, plantillas e historial"],
                            ["dash", "Dashboards, vistas y tarjetas"], ["energia", "Panel de Energía"], ["usuarios", "Usuarios"]]],
        ["MQTT", [["pubsub", "Broker, publicar y suscribirse"], ["temas", "Temas y comodines"], ["ordenes", "Órdenes y carga útil"],
                  ["qos", "QoS, retenidos, último deseo y puerto"], ["discovery", "MQTT discovery"], ["zigbee", "Zigbee y Zigbee2MQTT"],
                  ["puentes", "Puentes entre brokers"]]],
        ["Nuestro servidor", [["montaje", "El montaje: mini-PC, Proxmox y máquinas"], ["instalarvm", "Instalar HA en una máquina virtual"],
                              ["reset", "El reset y la instantánea"], ["kit", "El kit de dispositivos virtuales"],
                              ["reales", "Dispositivos reales (pendiente)"]]],
        ["Práctica 1", [["tiempo", "El tiempo"], ["reloj", "La hora"]]],
        ["Otras", [["figuras", "Preguntas con figura"]]]]
usadas = {c for x in DATA for c in x['cat']}
defin = {k for _, it in CATS for k, _ in it}
assert usadas <= defin, usadas - defin

s = open(SRC, encoding='utf-8').read()
def sub1(pat, rep, flags=0):
    global s
    s2, k = re.subn(pat, lambda m: rep, s, count=1, flags=flags)
    assert k == 1, pat
    s = s2
J = lambda o: json.dumps(o, ensure_ascii=False)
sub1(r'const DATA = \[.*?\];\nconst IMGS', 'const DATA = ' + J(DATA) + ';\nconst IMGS', re.S)
sub1(r'const IMGS = \{.*?\};\nconst TEMAS', 'const IMGS = ' + J(IMGS) + ';\nconst TEMAS', re.S)
sub1(r'const TEMAS = \{.*?\};\nconst TIPO', 'const TEMAS = ' + J(TEMAS) + ';\nconst TIPO', re.S)
sub1(r'const TIPO = \{.*?\};\nconst CATS', 'const TIPO = ' + J(TIPO) + ';\nconst CATS', re.S)
sub1(r'const CATS = \[.*?\];\nconst app', 'const CATS = ' + J(CATS) + ';\nconst app', re.S)
sub1(r'<title>.*?</title>', '<title>Test de Home Assistant · Domótica 2MT (provisional)</title>')
sub1(r'<nav class="crumbs">.*?</nav>',
     '<nav class="crumbs"><a href="index.html">Provisional</a> › <a href="index.html#ha">Home Assistant</a> › <b>Test de Home Assistant</b></nav>')
n = s.count("index.html#tests"); assert n >= 3, n
s = s.replace("index.html#tests", "index.html#ha")
sub1(r'<h1>Test Bloque 2 · <span>Domótica</span></h1>', '<h1>Test de Home Assistant · <span>Domótica</span></h1>')
sub1(r'<p class="sub">\$\{N\} preguntas del Tema 2.*?</p>',
     '<p class="sub">${N} preguntas de Home Assistant y MQTT: la teoría, nuestro servidor de prácticas con sus dispositivos virtuales y la Práctica 1 (el dashboard del tiempo). Versión provisional.</p>', re.S)
sub1(r"\$\{q\.tema === 'T2' \? 'Tema 2' : TEMAS\[q\.tema\]\}", '${TEMAS[q.tema]}')
sub1(r'\(por ejemplo, temporizadores o la persiana\)', '(por ejemplo, los temas de MQTT o las automatizaciones)')
sub1(r'<legend>Tema y prácticas</legend>', '<legend>De dónde sale</legend>')
s = s.replace('alt="Esquema: ', 'alt="Figura: ').replace('alt="Esquema ampliado"', 'alt="Figura ampliada"')
sub1(r"'testModoDom'\) \|\| 'orden'", "'testModoHA') || 'orden'")
sub1(r"localStorage\.setItem\('testModoDom', m\)", "localStorage.setItem('testModoHA', m)")
for resto in ['Bloque 2', 'LOGO', 'Tema 2', 'Práctica 4', 'borne']:
    for m in re.finditer(resto, s):
        ctx = s[max(0, m.start()-60):m.end()+60].replace('\n', ' ')
        if 'base64' not in ctx:
            print('QUEDA:', resto, '->', ctx)
open(OUT, 'w', encoding='utf-8').write(s)
print('escrito', OUT, len(s) // 1024, 'kB')
json.dump(DATA, open('/home/claude/testha/data.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
