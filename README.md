# hoass · Home Assistant en Instalaciones Domóticas (2MT)

Material de clase del bloque de **Home Assistant** del módulo de Instalaciones Domóticas (grupo 2MT), I.E.S. Trinidad Arroyo (Palencia).

## Temas

| Tema | Qué es | Documento |
|---|---|---|
| **Tema 1 · Home Assistant** | Qué es Home Assistant, cómo está hecho y MQTT; nuestro servidor de prácticas; Práctica 1 (dashboard del tiempo) | [`tema1/2MT-HA-teoria.pdf`](tema1/2MT-HA-teoria.pdf) · [`tema1/2MT-HA-servidor.pdf`](tema1/2MT-HA-servidor.pdf) · [`tema1/2MT-HA-P1.pdf`](tema1/2MT-HA-P1.pdf) |
| **Tema 2 · Configuración de IA con Home Assistant** | opencode, git, MCP, uso de skills y vibecoding (riesgos y buenas prácticas) | [`tema2/2MT-HA-T2-ia.pdf`](tema2/2MT-HA-T2-ia.pdf) |

Hojas sueltas: [`hojas/2MT-HA-hoja1-tu-home-assistant.pdf`](hojas/2MT-HA-hoja1-tu-home-assistant.pdf) (cómo entrar, normas y dispositivos) y [`hojas/2MT-HA-hoja2-chuleta-mqtt.pdf`](hojas/2MT-HA-hoja2-chuleta-mqtt.pdf) (chuleta MQTT de los dispositivos virtuales).

## Estructura

```
tema1/      Tema 1 en PDF (teoría, servidor, práctica 1)
tema2/      Tema 2 en PDF (y sus prácticas, cuando estén)
hojas/      hojas de una cara para tener al lado del ordenador
fuentes/    de dónde salen los documentos: estilo_ha.py (estilo común de los Word),
            gen/ (un generador por documento) y fig/ (figuras)
```

## Normas de este repositorio

- Es **público**: aquí no va **nada del profesorado** (soluciones, credenciales, operación del servidor), **ninguna contraseña** y **ningún dato personal**. Las direcciones internas del aula sí aparecen: solo valen dentro de la red del instituto.
- Los documentos se suben **solo en PDF**. Los Word (`.docx`) no se suben: están fuera de git.
- Los PDF salen de los generadores de `fuentes/gen/` (Python con python-docx y LibreOffice). Tienen rutas de la sesión en la que se hicieron (`/home/claude/...`): para regenerarlos hay que ajustarlas.

## Qué falta

- Práctica de puesta en marcha (opencode, git y MCP en Home Assistant y en el PC) y práctica de los dos dashboards (tablet y móvil).
