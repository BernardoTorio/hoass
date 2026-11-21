# estilo_ha.py — estilo común de los Word del tema de Home Assistant (2MT)

Imita los documentos del módulo (2MT-P4, Tema 2): Arial (→ Liberation Sans al pasar a PDF, mismas medidas), código en Courier New (→ Liberation Mono), cabecera «título corto · I.E.S. Trinidad Arroyo · Instalaciones Domóticas · 2MT» con línea verde, títulos con acento verde, cajones de colores, tablas con cabecera verde y «Página N de M» en el pie. Datos del servidor: **siempre** de `/home/claude/material-ha/_trabajo/ficha-comun.md`.

```python
import sys; sys.path.insert(0, "/home/claude/herr")
import estilo_ha as E
doc = E.nuevo_documento("Tu Home Assistant", "Hoja 1 · Cómo entrar y normas",
                        titulo_corto="Hoja 1 · Tu Home Assistant")   # confidencial=True → banda roja
E.h1(doc, "1. Cómo entrar")
E.parrafo(doc, "Escribe en el navegador **la dirección de tu grupo**, por ejemplo `http://10.202.51.81`.")
E.lista(doc, ["Abre el navegador.", "Escribe la dirección.", ["subpunto"]], numerada=True)
E.cajon(doc, "¡OJO!", ["El **reset** lo borra todo.", "- Haz capturas antes."])
E.tabla(doc, ["Grupo", "Dirección"], [["Grupo 1", "http://10.202.51.81"]], anchos_cm=[4, 13], mono_cols=(1,))
E.bloque_codigo(doc, 'virtual/e_tv/set                              TOGGLE')
E.hueco_captura(doc, "Pantalla de inicio de sesión de HA", alto_cm=5)
E.capturas(doc, escribir=True)            # lista de capturas al final (y la devuelve)
E.a_pdf(E.guardar(doc, "/home/claude/material-ha/alumnado/2MT-HA-hoja1-tu-home-assistant.docx"))
```

Funciones
- `nuevo_documento(titulo, subtitulo=None, confidencial=False, margenes_cm=(2,2,2,2), titulo_corto=None, portada=True, linea_info=None, horizontal=False)` — A4; con `portada=True` escribe ya el bloque de título. `confidencial=True`: banda roja «CONFIDENCIAL – SOLO PROFESORADO» en cabecera y pie de todas las páginas.
- `titulo(doc, texto, subtitulo)` (bloque de título suelto), `h1` (banda verde, salto_pagina=True opcional), `h2`, `h3` — usan los estilos «Título 1/2/3» de Word (panel de navegación).
- `parrafo(doc, texto, alineacion="justificado"|"izquierda"|"centro", tam, color, …)`, `nota(doc, texto)` (pequeño gris).
- Marcado en línea en casi todo: `**negrita**`, `*cursiva*`, `` `código` ``; `\*` y `` \` `` para escribirlos literales; `\n` = salto de línea.
- `lista(doc, items, numerada=False)` — una sublista dentro de `items` es un subnivel.
- `cajon(doc, tipo, texto_o_lista, titulo_extra=None)` — IDEA CLAVE, ¡OJO!, EJEMPLO, EN EL TALLER, PISTA, ¿POR QUÉ?. En lista, los elementos que empiezan por «- » llevan viñeta.
- `tabla(doc, cabeceras, filas, anchos_cm=None, mono_cols=(), negrita_col0=False, centrar_cols=(), tam=9.5)` — una fila que sea un texto suelto es una fila de grupo a todo el ancho. Cabecera repetida en cada página; las filas no se parten.
- `bloque_codigo(doc, texto, tam=None, titulo=None)` — respeta los espacios; elige solo el tamaño (9 a 6,5 pt) para que la línea más larga quepa.
- `imagen(doc, ruta, ancho_cm, pie=None)` — pie «Figura N. …» numerado solo.
- `hueco_captura(doc, descripcion, alto_cm=6)` — recuadro discontinuo `[CAPTURA: …]`; `capturas(doc)` devuelve `[(n, descripción, apartado)]`.
- `recortable(doc, tarjetas, columnas=2, alto_cm=3.2)` — tarjetas con borde discontinuo para recortar.
- `salto_pagina(doc)`, `separador(doc)`.
- `guardar(doc, ruta)` (ordena el XML para Word) · `a_pdf(ruta_docx)` (LibreOffice, perfil propio: se puede usar en paralelo) · `revisar_pdf(ruta_pdf, dpi=60)` (PNG por página para mirarlas con Read).
- Colores: `VERDE`, `VERDE_OSCURO`, `VERDE_CLARO`, `ROJO`, `AZUL`, `MORADO`, `OCRE`, `PIZARRA`, `NARANJA`, `GRIS`… (hex sin «#»; `PALETA` los tiene todos). Esquemas: `FASE` marrón, `NEUTRO` azul, `POSITIVO` rojo, `NEGATIVO` negro, `TIERRA` verde.
- matplotlib: `C = E.mpl_estilo()` pone la fuente (Liberation Sans) y los colores; `C["VERDE"]` → `"#70AD47"`; `E.mpl_color("AZUL")`.

Límites: los cajones y huecos son tablas de una celda (en Word se editan como tablas); las listas llevan la viñeta o el número escritos (no son listas automáticas de Word); `NUMPAGES` se actualiza al abrir o imprimir en Word. Demostración: `python3 /home/claude/herr/estilo_ha.py` → `_trabajo/demo-estilo.docx/.pdf` y `demo-estilo-confidencial.docx/.pdf`.
