"""Genera «Teoría: Home Assistant y MQTT» (2MT, alumnado): Word + PDF.
Uso: python3 gen_teoria.py   (antes, si cambian las figuras: python3 fig_teoria.py)"""
import sys
sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E
from docx.shared import Cm

FIG = "/home/claude/material-ha/_trabajo/fig/"
SALIDA = "/home/claude/material-ha/alumnado/2MT-HA-teoria.docx"

doc = E.nuevo_documento("Home Assistant y MQTT", "Teoría · Lo que necesitas para entender tu sistema",
                        titulo_corto="Teoría · Home Assistant y MQTT")

E.parrafo(doc, "En el aula cada grupo tiene **su propio Home Assistant** funcionando en una máquina virtual, "
          "con un **kit de 13 dispositivos virtuales** (persianas, toldo, luces, tira RGB, enchufes con medida y "
          "termostatos). Estos apuntes explican las piezas de Home Assistant y el protocolo **MQTT**, que es "
          "por donde llegan los dispositivos. Todos los ejemplos son de nuestro sistema: lo que leas aquí lo "
          "vas a ver en tu HA.")

# =====================================================================================
E.h1(doc, "Parte 1 · Home Assistant")

E.h2(doc, "1. Qué es Home Assistant")
E.parrafo(doc, "**Home Assistant** es un programa libre para **controlar y automatizar una vivienda** desde el "
          "navegador o el móvil, sin depender de la nube de cada fabricante. A partir de aquí lo llamaremos **HA**.")
E.lista(doc, [
    "**Junta aparatos de muchas marcas** en una sola pantalla: luces, persianas, enchufes, termostatos, sensores…",
    "**Automatiza**: hace cosas solo («al anochecer, baja las persianas»).",
    "**Mide y guarda**: temperaturas, consumos, cuándo se encendió cada cosa.",
    "**Funciona en local**: si se cae internet, la casa sigue funcionando.",
])
E.cajon(doc, "EJEMPLO", ["En el **escaparate** (`http://10.202.51.87`, entras como Invitado) tienes una vivienda "
                         "real ya terminada: dashboards de Home, Luces, Persianas, Energía, Aerotermia, Clima… "
                         "Míralo para hacerte una idea de hasta dónde se puede llegar."])

E.h2(doc, "2. Formas de instalarlo")
E.parrafo(doc, "La documentación oficial de HA ofrece hoy **dos tipos de instalación**: **Home Assistant OS** "
          "(la recomendada) y **Home Assistant Container**. Hay otras dos que todavía verás en internet, pero "
          "que ya no tienen soporte oficial.")
E.tabla(doc, ["Tipo", "Qué es", "Apps", "Situación hoy"], [
    ["Home Assistant OS (HAOS)", "Un sistema operativo completo preparado solo para HA. Se instala en un aparato "
     "(Home Assistant Green, Raspberry Pi, un PC) o en una máquina virtual.", "Sí", "**Recomendada** por HA"],
    ["Home Assistant Container", "HA dentro de un contenedor Docker, en un ordenador que ya tiene su sistema. "
     "Tú te encargas del sistema y de las actualizaciones.", "No", "Soportada"],
    ["Home Assistant Core", "HA instalado a mano como programa de Python.", "No",
     "Sin soporte oficial desde la versión 2025.12; queda para desarrolladores"],
    ["Home Assistant Supervised", "El Supervisor de HA instalado encima de tu propio Linux.", "Sí",
     "Sin soporte oficial desde la versión 2025.12"],
], anchos_cm=[3.6, 7.6, 1.4, 4.4], negrita_col0=True, centrar_cols=(2,))
E.parrafo(doc, "**Nosotros usamos HAOS en una máquina virtual (VM)**: un mini-PC lleva instalado **Proxmox VE**, "
          "que es el **hipervisor** (el programa que reparte el ordenador entre varias VMs), y encima funcionan "
          "las VMs de HA, una por grupo. Cada VM lleva **HAOS 18.4** con **Home Assistant 2026.11.2**.")
E.cajon(doc, "¿POR QUÉ?", ["¿Por qué HAOS y no Container? Porque HAOS trae las **apps** (necesitamos el broker "
                           "Mosquitto) y **copias de seguridad completas** (con las apps). Y al ir en una VM, el profesor "
                           "puede devolverla a su estado inicial (la instantánea `limpio`) entre clases."])

E.h2(doc, "3. Cómo está hecho por dentro")
E.parrafo(doc, "Un HAOS tiene **cuatro piezas**: el sistema operativo abajo, el Supervisor encima y, sobre él, "
          "Core y las apps, una al lado de la otra:")
E.imagen(doc, FIG + "teoria_capas.png", 16.6, "Las capas de tu Home Assistant, dentro de la VM de tu grupo.")
E.tabla(doc, ["Capa", "Qué hace", "En tu VM"], [
    ["Sistema operativo (HAOS)", "Arranca la VM y hace funcionar todo lo demás. No se toca.", "HAOS 18.4"],
    ["Supervisor", "Vigila y gestiona el resto: instala y actualiza HA y las apps, y hace las copias de seguridad.", "—"],
    ["Core", "El programa principal de HA: integraciones, entidades, automatizaciones e interfaz web.", "2026.11.2"],
    ["Apps (antes llamadas complementos)", "Programas extra que funcionan al lado de HA y se instalan desde él.",
     "Mosquitto broker 7.1.3 y File editor 6.3.1"],
], anchos_cm=[4.2, 8.6, 4.2], negrita_col0=True)
E.cajon(doc, "¡OJO!", ["«Core» significa dos cosas: la **capa** principal de HA (la que usas siempre) y el "
                       "**método de instalación** «Home Assistant Core», que ya no tiene soporte. No las confundas."])

# -------------------------------------------------------------------------------------
E.h2(doc, "4. Las piezas de Home Assistant")

E.h3(doc, "4.1 Integraciones, dispositivos y entidades")
E.lista(doc, [
    "Una **integración** es la pieza de HA que sabe hablar con una marca, un servicio o un protocolo. "
    "Ejemplos: **MQTT** (por ella llega todo nuestro kit) y **Met.no** (el tiempo).",
    "Un **dispositivo** es un aparato tal como lo ve HA, por ejemplo la persiana `p_cocina`. Los de nuestro kit "
    "tienen como fabricante «Virtual (aula)».",
    "Una **entidad** es cada cosa que se puede leer o mandar de un dispositivo. El enchufe del frigorífico tiene, "
    "entre otras, una entidad para encenderlo y otra que mide su potencia.",
])
E.parrafo(doc, "Cada entidad tiene un nombre interno único, el **`entity_id`**: **tipo, punto y nombre**, "
          "siempre en minúsculas. El tipo (el *dominio*) dice qué clase de cosa es:")
E.tabla(doc, ["entity_id", "Tipo", "Qué es"], [
    ["cover.p_cocina", "cover (persiana, toldo)", "persiana de la cocina"],
    ["light.tira_rgb", "light (luz)", "tira RGB"],
    ["switch.e_frigo", "switch (interruptor)", "enchufe del frigorífico: encender y apagar"],
    ["sensor.e_frigo_power", "sensor", "potencia del frigorífico (W)"],
    ["sensor.e_frigo_summation_delivered", "sensor", "energía gastada por el frigorífico (kWh)"],
    ["climate.ter_salon", "climate (clima)", "termostato del salón"],
    ["binary_sensor.ter_salon_valve", "binary_sensor (sí/no)", "válvula del termostato del salón"],
    ["switch.virtual_bridge_permit_join", "switch", "permitir emparejar (Virtual Bridge)"],
], anchos_cm=[6.6, 4.4, 6.0], mono_cols=(0,), tam=9)
E.hueco_captura(doc, "Ajustes → Dispositivos y servicios → MQTT → dispositivo p_cocina: página del dispositivo "
                "con el fabricante «Virtual (aula)», el modelo «… (virtual)» y la lista de sus entidades", alto_cm=3.5)

E.h3(doc, "4.2 Estados y atributos")
E.parrafo(doc, "El **estado** es el valor principal de una entidad en este momento. Los **atributos** son datos "
          "extra que acompañan al estado.")
E.tabla(doc, ["Entidad", "Estado (ejemplo)", "Atributos (ejemplos)"], [
    ["light.tira_rgb", "on / off", "brillo, color, efecto"],
    ["cover.p_cocina", "open / closed / opening / closing", "posición (0 a 100 %)"],
    ["climate.ter_salon", "el modo: heat (calor), cool (frío), off…", "temperatura de la sala, temperatura de consigna, velocidad del ventilador"],
    ["sensor.e_frigo_power", "un número, por ejemplo 85", "unidad (W)"],
], anchos_cm=[4.2, 5.6, 7.2], mono_cols=(0,), tam=9)
E.parrafo(doc, "Los estados se guardan en inglés (`on`, `open`, `heat`…), aunque la interfaz te los enseñe en español.")
E.hueco_captura(doc, "Ventana de la entidad light.tira_rgb (al pulsarla en un dashboard o en la lista de entidades), "
                "encendida, con su estado y los atributos desplegados (brillo y color)", alto_cm=3.5)

E.h3(doc, "4.3 Áreas y ayudantes")
E.lista(doc, [
    "Un **área** es una zona de la casa (cocina, salón, habitación 1…). Si asignas `p_cocina` y `ter_cocina` "
    "al área «Cocina», HA los agrupa y te los enseña juntos.",
    "Un **ayudante** es una entidad que creas tú a mano para guardar un dato o hacer un cálculo: un interruptor "
    "«modo vacaciones», un número con la temperatura deseada, un temporizador… Luego lo usas en las "
    "automatizaciones como cualquier otra entidad.",
])

E.h3(doc, "4.4 Automatizaciones")
E.parrafo(doc, "Una **automatización** es una regla que HA ejecuta solo. Tiene tres partes; la condición es opcional:")
E.imagen(doc, FIG + "teoria_automatizacion.png", 16.6, "Las tres partes de una automatización, con un ejemplo de tu kit.")
E.lista(doc, [
    "**Desencadenante**: lo que la pone en marcha. Una hora, un cambio de estado, un número que pasa de un "
    "valor, un mensaje MQTT…",
    "**Condición** (opcional): lo que tiene que cumplirse para seguir. Si no se cumple, no hace nada.",
    "**Acción**: lo que hace. Encender, apagar, mover una persiana, mandar un aviso…",
])
E.cajon(doc, "EJEMPLO", ["Dicho con palabras: «**Cuando** la potencia del frigorífico (`sensor.e_frigo_power`) "
                         "pase de 300 W, **si** la persiana de la cocina (`cover.p_cocina`) está abierta, "
                         "**enciende** la tira RGB (`light.tira_rgb`) en rojo». Si la persiana está cerrada, la "
                         "condición no se cumple y no pasa nada."])
E.hueco_captura(doc, "Editor de una automatización (Ajustes → Automatizaciones y escenas): bloques «Cuando», "
                "«Y si» y «Entonces haz» con el ejemplo del frigorífico, la persiana y la tira RGB", alto_cm=3.5)

E.h3(doc, "4.5 Scripts y escenas")
E.lista(doc, [
    "Un **script** es una lista de acciones con nombre. **No tiene desencadenante**: se lanza a mano (con un "
    "botón) o desde una automatización. Ejemplo: «Cerrar todo» baja las tres persianas, recoge el toldo y "
    "apaga las luces.",
    "Una **escena** es una «foto» de cómo deben quedar varias entidades, y se aplica de golpe. Ejemplo: "
    "«Película»: la tira RGB en azul con poco brillo y la persiana de la cocina bajada.",
])
E.cajon(doc, "PISTA", ["El script **hace cosas una detrás de otra** (y puede esperar entre ellas). La escena "
                       "solo dice **cómo tiene que quedar todo**."])

E.h3(doc, "4.6 Plantillas")
E.parrafo(doc, "Una **plantilla** (*template*) es un pequeño texto con código que calcula un valor a partir de "
          "otras entidades. Va entre llaves dobles. Por ejemplo, esta plantilla escribe una frase con la "
          "potencia del frigorífico:")
E.bloque_codigo(doc, "El frigorífico está gastando {{ states('sensor.e_frigo_power') }} W")
E.cajon(doc, "¡OJO!", ["La **plantilla de HA** (código que calcula un valor) no tiene nada que ver con la "
                       "**plantilla de VM** de Proxmox (`haos-plantilla`, la VM apagada de la que se copiaron "
                       "las vuestras). Misma palabra, dos cosas distintas."])

E.h3(doc, "4.7 Dashboards y tarjetas")
E.parrafo(doc, "Un **dashboard** (panel) es una pantalla para ver y manejar la casa. Está hecho de **tarjetas**: "
          "cada recuadro es una (una persiana, un termostato, una gráfica de consumo, el tiempo…). Puedes tener "
          "varios dashboards: uno general, uno de luces, uno de energía… Un dashboard puede tener varias **vistas** "
          "(como pestañas), y cada vista tiene sus tarjetas. Los dashboards se crean desde **Ajustes** (en el "
          "menú puede salir como *Paneles de control*: es lo mismo que *dashboards*). Mira cómo están "
          "organizados los del escaparate.")

E.h3(doc, "4.8 Historial y estadísticas")
E.lista(doc, [
    "El **historial** guarda cada cambio de estado. Así puedes ver a qué hora se bajó una persiana o una gráfica "
    "de la potencia del frigorífico. Por defecto guarda el detalle de unos 10 días.",
    "Las **estadísticas** son resúmenes (medias, máximos, totales por hora) que se guardan mucho más tiempo. "
    "Las usan las gráficas largas y el panel de Energía.",
])

E.h3(doc, "4.9 Panel de Energía")
E.parrafo(doc, "El **panel de Energía** enseña cuánta energía se gasta y en qué. Para cada aparato necesita un "
          "sensor de **energía** (en kWh), como `sensor.e_frigo_summation_delivered`, que va sumando lo que ha "
          "gastado el frigorífico.")
E.cajon(doc, "¡OJO!", ["**Potencia no es energía.** `sensor.e_frigo_power` dice cuánto gasta **ahora** (en W). "
                       "`sensor.e_frigo_summation_delivered` dice cuánto ha gastado **en total** (en kWh). "
                       "Al panel de Energía se le da el de kWh."])

E.h3(doc, "4.10 Usuarios y permisos")
E.parrafo(doc, "Cada persona entra con su **usuario**. Un usuario puede ser **administrador** (puede cambiar los "
          "ajustes) o normal (solo usa la casa). En cada VM hay tres:")
E.tabla(doc, ["Usuario", "Para qué"], [
    ["admin", "el del profesor"],
    ["userN (user1 … user6)", "tu grupo. Es administrador y solo puede entrar desde la red local del aula"],
    ["puente", "usuario del sistema para el MQTT; no sirve para entrar"],
], anchos_cm=[5, 12], mono_cols=(0,), tam=9.5)

E.h3(doc, "4.11 Copias de seguridad")
E.parrafo(doc, "Una **copia de seguridad** guarda la configuración de HA (dispositivos, automatizaciones, "
          "dashboards…) y sus apps, para recuperarla si algo se rompe. En HAOS la hace el Supervisor.")
E.cajon(doc, "EN EL TALLER", ["Cuando el profesor hace el **reset** —normalmente entre clases—, tu VM vuelve a "
                              "la instantánea `limpio` y **se borra todo** lo que hayáis hecho, también una copia de seguridad "
                              "que se haya quedado dentro de la VM.",
                              "- Haz capturas de pantalla de lo que quieras conservar.",
                              "- Si tienes que entregar algo, expórtalo o cópialo fuera antes de acabar la clase."])

# =====================================================================================
E.h1(doc, "Parte 2 · MQTT, lo necesario para entender nuestro sistema")

E.h2(doc, "5. Publicar y suscribirse: broker y clientes")
E.parrafo(doc, "**MQTT** es un protocolo ligero de mensajes. Los aparatos **no se hablan directamente**: todos "
          "se conectan a un servidor central, el **broker**, que recibe los mensajes y los reparte.")
E.lista(doc, [
    "**Publicar** es enviar un mensaje a un tema.",
    "**Suscribirse** es pedir al broker que te envíe los mensajes de uno o varios temas.",
    "Un **cliente** es cualquier programa o aparato conectado al broker. En el aula: tu HA (con la integración "
    "MQTT), el simulador y, cuando funcione, Zigbee2MQTT.",
])
E.imagen(doc, FIG + "teoria_pubsub.png", 16.6, "Publicar y suscribirse: el broker hace de cartero.")
E.parrafo(doc, "En tu VM, el broker es la app **Mosquitto broker**. Cuando mueves la persiana desde HA, HA publica "
          "una orden; el simulador, que está suscrito, la recibe, «mueve» la persiana y publica su nuevo estado; "
          "HA, que está suscrito al estado, lo recibe y te lo enseña.")

E.h2(doc, "6. Temas y comodines")
E.parrafo(doc, "Un **tema** (*topic*) es la «dirección» de un mensaje. Tiene **niveles separados por `/`**, "
          "de lo general a lo concreto, como las carpetas de un ordenador. Distingue mayúsculas y minúsculas: "
          "`virtual/p_cocina/set` y `Virtual/P_cocina/set` son temas distintos.")
E.tabla(doc, ["Tema de nuestro sistema", "Para qué"], [
    ["virtual/p_cocina/set", "órdenes a la persiana virtual de la cocina"],
    ["virtual/ter_salon/set/current_heating_setpoint", "cambiar la temperatura de consigna del termostato del salón"],
    ["virtual/bridge/request/device/add", "pedir al simulador un dispositivo nuevo"],
    ["virtual/bridge/response/…", "respuestas del simulador"],
    ["zigbee2mqtt/<dispositivo>", "estado de un dispositivo Zigbee real (pendiente)"],
    ["zigbee2mqtt/<dispositivo>/set", "órdenes a un dispositivo Zigbee real (pendiente)"],
    ["homeassistant/<componente>/<id>/config", "presentación de un dispositivo a HA (MQTT discovery, apartado 10)"],
], anchos_cm=[8.4, 8.6], mono_cols=(0,), tam=9)
E.parrafo(doc, "Para **suscribirse a muchos temas a la vez** se usan dos **comodines**:")
E.lista(doc, [
    "`+` vale por **un nivel** cualquiera, exactamente uno. Puede ir en medio.",
    "`#` vale por **todos los niveles que sigan**, sean los que sean. Solo puede ir al final.",
])
E.imagen(doc, FIG + "teoria_temas.png", 16.6, "Los temas forman un árbol; los comodines eligen ramas.")
E.tabla(doc, ["Te suscribes a…", "Recibes…", "No recibes…"], [
    ["virtual/+/set", "`virtual/p_cocina/set`, `virtual/e_tv/set`…", "`virtual/ter_salon/set/current_heating_setpoint` (tiene un nivel de más)"],
    ["virtual/#", "todo lo del simulador, a cualquier nivel", "nada de `zigbee2mqtt/…`"],
    ["virtual/bridge/response/#", "todas las respuestas del simulador", "las órdenes a los dispositivos"],
    ["zigbee2mqtt/#", "todo lo de Zigbee2MQTT", "nada de `virtual/…`"],
    ["zigbee2mqtt/+/set", "las órdenes a cualquier dispositivo real", "`zigbee2mqtt/<dispositivo>/set/<algo>` (un nivel de más)"],
], anchos_cm=[4.4, 6.2, 6.4], mono_cols=(0,), tam=9)
E.cajon(doc, "PISTA", ["Para ver todo lo que pasa en tu kit, en **Ajustes → Dispositivos y servicios → MQTT → "
                       "Configurar**, en *Escuchar un tema*, escribe `virtual/#`."])
E.hueco_captura(doc, "Ajustes → Dispositivos y servicios → MQTT → Configurar → Escuchar un tema, suscrito a "
                "virtual/#, con varios mensajes recibidos después de mover la persiana p_cocina", alto_cm=3)

E.h2(doc, "7. El mensaje: la carga útil")
_p = E.parrafo(doc, "Lo que va dentro del mensaje se llama **carga útil** (*payload*). Puede ser una palabra o un "
          "número, o un texto en formato **JSON** (pares `\"nombre\": valor` entre llaves). Órdenes de nuestro "
          "simulador, tal cual:")
_p.paragraph_format.keep_with_next = True
_t7 = E.tabla(doc, ["Tema", "Carga útil"], [
    ["virtual/p_cocina/set", '{"position": 50}\n(o `OPEN` / `CLOSE` / `STOP`)'],
    ["virtual/e_tv/set", "TOGGLE"],
    ["virtual/tira_rgb/set", '{"state": "ON",\n"color": {"hex": "#ff8000"},\n"brightness": 150}'],
    ["virtual/ter_salon/set/current_heating_setpoint", "22"],
], anchos_cm=[8.8, 8.2], mono_cols=(0, 1), tam=9.5)

E.h2(doc, "8. QoS, mensajes retenidos y último deseo")
E.parrafo(doc, "Cuando se publica, se eligen unas opciones que dicen cómo tiene que tratar el broker el mensaje.")
E.tabla(doc, ["QoS", "Qué garantiza", "Cuándo se usa"], [
    ["0", "Se envía una vez, sin confirmar. Puede perderse.", "datos que se repiten a menudo (una potencia cada pocos segundos)"],
    ["1", "Llega **al menos una vez** (puede llegar repetido).", "cuando importa que el mensaje llegue"],
    ["2", "Llega **exactamente una vez**. Es el más lento.", "cuando repetir un mensaje sería un problema"],
], anchos_cm=[1.3, 7.7, 8.0], centrar_cols=(0,), tam=9)
E.lista(doc, [
    "**Mensaje retenido**: el broker guarda el último mensaje de ese tema y se lo entrega al momento a quien se "
    "suscriba después. Así, si HA se reinicia, recibe enseguida el último estado sin esperar a que cambie.",
    "**Último deseo (LWT)**: un mensaje que el cliente deja preparado al conectarse. Si se desconecta de golpe "
    "(se cuelga, se queda sin red), el broker lo publica por él. Sirve para saber que un aparato se ha caído, y "
    "HA puede enseñarlo como «No disponible».",
])

E.h2(doc, "9. Usuario, contraseña y puerto")
E.parrafo(doc, "Nuestros brokers no dejan conectarse a cualquiera: cada cliente se presenta con un **usuario y una "
          "contraseña**. Por ejemplo, los puentes del aula (apartado 12) entran con el usuario `puente`. Las "
          "contraseñas no se apuntan en ningún sitio a la vista.")
E.parrafo(doc, "Los clientes se conectan al broker por un **puerto**. El puerto habitual de MQTT es el **1883** "
          "(sin cifrar); para MQTT cifrado se suele usar el **8883**.")

E.h2(doc, "10. MQTT discovery: cómo aparece solo un dispositivo")
E.parrafo(doc, "Con **MQTT discovery**, un aparato **se presenta solo** a HA. Publica su descripción en un tema "
          "con esta forma:")
E.bloque_codigo(doc, "homeassistant/<componente>/<id>/config")
E.parrafo(doc, "`<componente>` es el tipo de entidad (`cover`, `light`, `switch`, `sensor`, `climate`…) e `<id>` "
          "identifica al aparato. En la descripción va su nombre, su fabricante y a qué temas hay que mandar las "
          "órdenes y escuchar el estado. HA está suscrito a esos temas, la lee y **crea el dispositivo y sus "
          "entidades sin configurar nada a mano**.")
E.imagen(doc, FIG + "teoria_discovery.png", 16.6, "MQTT discovery: el aparato se presenta («soy una persiana, mis órdenes van a tal tema y mi estado sale en tal otro») y HA lo da de alta.")
E.cajon(doc, "EJEMPLO", ["Así llega tu kit: el simulador publica la descripción de los 13 dispositivos y el Virtual Bridge, y aparecen "
                         "en **Ajustes → Dispositivos y servicios → MQTT**. Para añadir uno nuevo, primero abres el "
                         "emparejamiento y después lo pides (aparece a los 3 s):",
                         "`virtual/bridge/request/permit_join`  `{\"time\": 254}`",
                         "`virtual/bridge/request/device/add`",
                         "`{\"tipo\": \"persiana\", \"nombre\": \"p_hab2\", \"recorrido\": 18}`",
                         "Sin `permit_join` activo, el simulador rechaza la petición. Lo añadido desaparece con el reset."])

E.h2(doc, "11. Zigbee y Zigbee2MQTT")
E.parrafo(doc, "**Zigbee** es un protocolo **inalámbrico de bajo consumo** para aparatos domóticos. Los aparatos "
          "forman una **red en malla**: los mensajes pueden ir saltando de un aparato a otro hasta llegar.")
E.imagen(doc, FIG + "teoria_zigbee.png", 16.6, "Red Zigbee en malla (ejemplo): coordinador, routers y dispositivos finales.")
E.tabla(doc, ["Papel", "Qué es", "Ejemplos"], [
    ["Coordinador", "Crea y dirige la red. Hay uno por red.", "el SLZB-06, por USB al mini-PC (pendiente)"],
    ["Router", "Aparato con alimentación fija que, además de funcionar, reenvía mensajes de otros y amplía la red.",
     "enchufes, módulos de persiana"],
    ["Dispositivo final", "Normalmente a pilas. Solo habla con su router o con el coordinador; no reenvía.",
     "sensores de puerta, de temperatura"],
], anchos_cm=[3.2, 9.2, 4.6], negrita_col0=True, tam=9)
E.lista(doc, [
    "**Emparejamiento**: para que un aparato nuevo entre en la red, la red tiene que estar abierta. Se abre con "
    "**`permit_join`** durante un tiempo y después se cierra sola.",
    "**Zigbee2MQTT** habla con el coordinador y traduce cada aparato a temas MQTT: publica su estado en "
    "`zigbee2mqtt/<dispositivo>` y recibe las órdenes en `zigbee2mqtt/<dispositivo>/set`.",
    "Nuestro simulador imita a Zigbee2MQTT: su «Virtual Bridge» tiene la entidad "
    "`switch.virtual_bridge_permit_join` para abrir el emparejamiento.",
])
E.cajon(doc, "¡OJO!", ["Los **dispositivos reales** del aula **todavía no funcionan (pendiente)**. Están previstos un "
                       "coordinador SLZB-06, un termostato Tuya TYBAC-006 y dos módulos de persiana TS130F, con "
                       "nombres que empezarán por `aula_`. Zigbee2MQTT (versión 2.14.3) está instalado pero parado "
                       "hasta que se conecte el coordinador. Cuando funcionen, para ti serán otras entidades MQTT en tu HA."])

E.h2(doc, "12. Puentes entre brokers")
E.parrafo(doc, "**Problema**: HA solo admite **un** broker MQTT. Pero los dispositivos reales estarán en un "
          "**broker común** del aula, y cada grupo necesita el suyo para que lo que haga uno no afecte a los demás.")
E.parrafo(doc, "**Solución**: cada VM tiene **su propio Mosquitto**, y el **Mosquitto común** (en el contenedor "
          "`aula-mqtt`) se une a los seis con **puentes**. Un **puente entre brokers** copia de un broker a otro "
          "solo los temas elegidos. Van por la red interna del servidor (`192.168.100.0/24`).")
E.imagen(doc, FIG + "teoria_puentes.png", 16.6, "El Mosquitto común y los puentes hacia el Mosquitto de cada VM "
         "(se dibujan cuatro VMs; las seis funcionan igual).")
E.tabla(doc, ["Sentido del puente", "Temas", "Para qué"], [
    ["del común a tu VM", "zigbee2mqtt/#\nhomeassistant/#", "ves los dispositivos reales y se presentan solos en tu HA"],
    ["de tu VM al común", "zigbee2mqtt/+/set\nzigbee2mqtt/+/set/+\nzigbee2mqtt/+/get",
     "puedes mandarles órdenes y pedirles el estado"],
], anchos_cm=[3.6, 5.2, 8.2], mono_cols=(1,), negrita_col0=True, tam=9)
E.lista(doc, [
    "Hacia el común **solo pasan órdenes** a los dispositivos (`set` y `get`). Nada más: no se puede gestionar "
    "Zigbee2MQTT desde una VM.",
    "Los temas `virtual/…` **no pasan por los puentes**: el simulador publica directamente en el Mosquitto de "
    "cada VM. Por eso los dispositivos virtuales de un grupo nunca se mezclan con los de otro ni con los reales.",
])
E.cajon(doc, "¡OJO!", ["«Puente» también significa dos cosas: el **puente entre brokers** MQTT (este apartado) "
                       "y el **puente de red** de Proxmox (`vmbr0`, `vmbr1`), que es como un switch dentro del "
                       "servidor. Y `puente` es además el usuario con el que se conectan los puentes MQTT."])

# =====================================================================================
E.h1(doc, "Preguntas de repaso")
E.parrafo(doc, "Contesta en tu cuaderno. Las de verdadero o falso, justifícalas en una línea.")
E.lista(doc, [
    "¿Qué tipo de instalación de HA usamos en el aula y sobre qué funciona?",
    "Verdadero o falso: «Home Assistant Container trae apps, como el broker Mosquitto».",
    "¿Qué hace el Supervisor? Di dos cosas.",
    "¿Qué diferencia hay entre un dispositivo y una entidad? Pon un ejemplo con el enchufe del frigorífico.",
    "En `climate.ter_salon`, ¿qué parte es el tipo (dominio) y qué parte es el nombre?",
    "La tira RGB está encendida, con brillo 150 y color naranja. ¿Cuál es su estado y cuáles son sus atributos?",
    "Pon nombre a las tres partes de una automatización y di cuál es opcional.",
    "Verdadero o falso: «Un script se pone en marcha solo cuando pasa algo, igual que una automatización».",
    "¿Qué sensor le darías al panel de Energía para el frigorífico: `sensor.e_frigo_power` o "
    "`sensor.e_frigo_summation_delivered`? ¿Por qué?",
    "¿Qué le pasa a tu configuración después del reset? ¿Qué tienes que hacer antes?",
    "¿Qué es el broker? ¿Cuál usa tu HA?",
    "¿A qué tema publicarías para bajar la persiana de la cocina hasta la mitad? ¿Con qué carga útil?",
    "¿A qué tema publicarías para apagar o encender la televisión de un golpe? ¿Con qué carga útil?",
    "¿Qué comodín usarías para recibir todos los mensajes del simulador? Escribe el tema completo.",
    "Verdadero o falso: «Suscrito a `virtual/+/set` recibes `virtual/ter_salon/set/current_heating_setpoint`».",
    "¿Qué es un mensaje retenido? ¿Para qué le sirve a HA cuando se reinicia?",
    "¿Para qué sirve el último deseo (LWT)?",
    "¿En qué tema publica un aparato su descripción para el MQTT discovery? ¿Qué hace HA al leerla?",
    "En una red Zigbee, ¿qué diferencia hay entre un router y un dispositivo final? Pon un ejemplo de cada uno.",
    "¿Por qué cada VM tiene su propio Mosquitto en vez de conectarse todas al broker común? ¿Pasan los temas "
    "`virtual/…` por los puentes?",
], numerada=True)
for par in doc.paragraphs[-20:]:      # sangría francesa más ancha para que quepan los números de dos cifras
    pf = par.paragraph_format
    pf.left_indent = Cm(0.8); pf.first_line_indent = Cm(-0.8)
    pf.tab_stops.clear_all(); pf.tab_stops.add_tab_stop(Cm(0.8))

pdf = E.a_pdf(E.guardar(doc, SALIDA))
import capturas_txt
capturas_txt.escribir(doc, "2MT-HA-teoria", pdf)
print(pdf)
