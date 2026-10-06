# Evaluador de AFD y AFN mediante FastAPI

## Identificación

| Dato | Información |
|---|---|
| Actividad | Evaluador de AFD y AFN mediante servicio web |
| Materia | Lenguajes de Computación |
| Docente | Paulo Daniel Vázquez Mora |
| Periodo | Otoño 2026 |

### Integrantes

| Nombre completo | No. de cuenta |
|---|---|
| Juan Pablo Ruiz | 192034 |
| Nombre del integrante 2 | XXXXX |
| Nombre del integrante 3 | XXXXX |
| Nombre del integrante 4 | XXXXX |

---

## Objetivo

Implementar un evaluador de Autómatas Finitos Deterministas (AFD)
y Autómatas Finitos No Deterministas (AFN) mediante un servicio web
desarrollado con FastAPI.

Cada evaluador cuenta con su propio endpoint y permite recibir una
tabla de transición y una o varias cadenas para determinar si son
aceptadas o rechazadas.

---

# 1. Tecnologías utilizadas

- Python
- FastAPI
- Uvicorn
- Jupyter Notebook
- JSON
- REST API

---

# 2. Endpoints

## Evaluador AFD

```http
POST /afd/evaluar