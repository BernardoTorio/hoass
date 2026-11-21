# hoass · Home Assistant en Instalaciones Domóticas (2MT)

Material de clase del bloque de **Home Assistant** del módulo de Instalaciones Domóticas (grupo 2MT), I.E.S. Trinidad Arroyo (Palencia).

## Temas

| Tema | Qué es | Documento |
|---|---|---|
| **Tema 1 · Home Assistant** | Qué es Home Assistant, cómo está hecho, MQTT y nuestro servidor de prácticas | pendiente de subir (ver «Qué falta») |
| **Tema 2 · Configuración de IA con Home Assistant** | opencode, git, MCP, uso de skills y vibecoding (riesgos y buenas prácticas) | [`tema2/2MT-HA-T2-ia.pdf`](tema2/2MT-HA-T2-ia.pdf) |

Hojas sueltas: [`hojas/2MT-HA-hoja2-chuleta-mqtt.pdf`](hojas/2MT-HA-hoja2-chuleta-mqtt.pdf) (chuleta MQTT de los dispositivos virtuales).

## Estructura

```
tema1/      Tema 1 en PDF (teoría, servidor, práctica 1)
tema2/      Tema 2 en PDF (y sus prácticas, cuando estén)
hojas/      hojas de una cara para tener al lado del ordenador
fuentes/    de dónde salen los documentos: estilo_ha.py (estilo común de los Word),
            gen/ (un generador por documento) y fig/ (figuras)
```

## Normas de este repositorio

- Es **público**: aquí no va **nada del profesorado** (soluciones, credenciales, operación del servidor), **ninguna contraseña** y **ningún dato personal**.
- Los documentos se suben **solo en PDF**. Los Word (`.docx`) no se suben: están fuera de git.
- Los PDF salen de los generadores de `fuentes/gen/` (Python con python-docx y LibreOffice). Tienen rutas de la sesión en la que se hicieron (`/home/claude/...`): para regenerarlos hay que ajustarlas.

## Qué falta

- Subir el Tema 1 (teoría, servidor, hoja 1 y práctica 1): llevan las direcciones internas del aula y está por decidir si se publican así.
- Práctica de puesta en marcha (opencode, git y MCP en Home Assistant y en el PC) y práctica de los dos dashboards (tablet y móvil).
