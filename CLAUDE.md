# hoass · Home Assistant (Instalaciones Domóticas, 2MT) — I.E.S. Trinidad Arroyo (Palencia)

Material de clase del bloque de Home Assistant: Tema 1 (Home Assistant y MQTT) y Tema 2 (configuración de IA con Home Assistant: opencode, git, MCP, skills y vibecoding), con sus prácticas y hojas. Repositorio `BernardoTorio/hoass`, **público**.

## Lo que no se sube nunca
- Nada del **profesorado**: soluciones, credenciales, inventario, operación del servidor. Las contraseñas solo están en las hojas del profesorado, fuera de git.
- **Ningún dato personal** del profesor ni de los alumnos. La casa que sirve de modelo es «una vivienda real»: no se dice de quién es ni dónde está.
- Ni `.docx` ni `.zip` (están en `.gitignore`). Los documentos van **solo en PDF**.
- Las direcciones internas del aula (`10.202.51.x`, `192.168.100.x`) **sí** se pueden publicar (lo decidió el profesor el 21/11/2026). Las de casa, el acceso al servidor (SSH, Proxmox) y los comandos del host, **no**: son del profesorado.

## Cómo son los documentos
- Alumnos de FP de grado medio (16-17 años): lenguaje sencillo, sin fórmulas, frases cortas. Español de España.
- Estilo del proyecto: cabecera verde y cajones IDEA CLAVE, ¡OJO!, EJEMPLO, EN EL TALLER, PISTA y ¿POR QUÉ? Se generan con `fuentes/estilo_ha.py` (ver `fuentes/LEEME-estilo.md`), un generador por documento en `fuentes/gen/`.
- Sin fechas en los documentos. Se trabaja por grupos («grupo N»), no por parejas.
- Las capturas de Home Assistant las hace el profesor: huecos `[CAPTURA: qué debe verse]`.
- Ficheros `2MT-HA-…`.
- El apartado de MCP del Tema 2 sale de `gen_ia_mcp.py` (fuente única); `gen_t2_ia.py` lo incluye.
- Vídeos recomendados: canal MoureDev (Brais Moure), con enlace al minuto de cada lección.

## Decisiones del Tema 2
- Modelos gratuitos de opencode; opencode en la VM de Home Assistant y en el PC del alumno.
- Una cuenta de GitHub por alumno.
- Servidor MCP: ha-mcp por ahora; el oficial de Home Assistant es reciente y mejora rápido.
