
## 1. Bloque de identificación

- **Nombre del alumno:** Juan Pablo Ruiz Gil
- **Matricula** 192034
- **Materia:** Lenguajes de computacion
- **Actividad:** 12 Algoritmos de búsqueda informada (heurísticos)



---
# Actividad 12 — Algoritmos de búsqueda informada

## Instalación y ejecución

Requiere Python 3.10 o posterior.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre `http://127.0.0.1:8000/docs` para probar los endpoints en Swagger.

## Endpoints nuevos

- `POST /search/greedy`: búsqueda voraz Greedy Best-First Search.
- `POST /search/star`: búsqueda A*.

Los endpoints anteriores de operaciones con lenguajes, AFD, AFN y complejidad se conservan en `main.py`.

## Formato de entrada

```json
{
  "grafo": {
    "A": [["B", 15], ["C", 22]],
    "B": [["D", 7]],
    "C": [["D", 10]],
    "D": []
  },
  "origen": "A",
  "destino": "D",
  "limite_visitas": 3,
  "coordenadas": {
    "A": [0, 0], "B": [1, 0], "C": [0, 1], "D": [2, 0]
  }
}
```

`limite_visitas` y `coordenadas` son opcionales. Si no se indica el límite, se usa `ceil(0.8 * V)`, donde `V` es el total de nodos distintos entre las claves y los vecinos del grafo. Las aristas son dirigidas y los pesos deben ser no negativos.

## Campos de salida

- `nodos_visitados` y `visitados`: cantidad y orden de nodos expandidos.
- `solucion`: `true` si se alcanzó el destino dentro del límite.
- `ruta`: secuencia de nodos; lista vacía si no se encontró solución.
- `costo_ruta`: suma de pesos de la ruta, cuando existe.
- `T(n)` y `S(n)`: estimaciones teóricas de complejidad temporal y espacial.
- `operaciones_estimadas` y `maximo_elementos_frontera`: contadores empíricos para comparar ejecuciones.

## Heurísticas

Greedy prioriza únicamente `h(n)`. Si se proporcionan coordenadas para los nodos necesarios, usa la distancia euclidiana al destino; en caso contrario, usa como alternativa el mínimo número de aristas al destino calculado sobre el grafo inverso. Esta alternativa es una estimación topológica, no una distancia física.

A* prioriza `f(n) = g(n) + h(n)`, donde `g(n)` es el costo acumulado. Usa la distancia euclidiana solo cuando todos los nodos tienen coordenadas; si no, usa `h(n)=0`, por lo que se comporta como Dijkstra y conserva optimalidad para pesos no negativos. Para que la distancia euclidiana garantice optimalidad, sus unidades/escala deben ser compatibles con los costos de las aristas y no sobreestimar el costo restante.

## Complejidad reportada

Con una cola de prioridad binaria, se reporta como cota general de referencia `O((V+E) log V)` en tiempo y `O(V+E)` en espacio. La cantidad real de nodos expandidos depende del grafo, del origen/destino, del límite y de la heurística. En A*, el rendimiento también depende de la calidad de la heurística.
