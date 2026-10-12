# Actividad 12. Algoritmos de búsqueda informada (heurísticos)

## Bloque de identificación

- **Asignatura:** Guías de Computación
- **Actividad:** 12. Algoritmos de búsqueda informada (heurísticos)
- **Estudiante:** Juan Pablo Ruiz Gil
- **Repositorio:** agregar aquí la liga del repositorio de GitHub
- **Fecha:** 11 de octubre de 2026

## 1. Objetivo

Implementar y evaluar en FastAPI dos algoritmos de búsqueda en grafos: Greedy Best-First Search (búsqueda voraz) y A*. Se comparan la cantidad de nodos visitados, las rutas obtenidas, el costo de la ruta y el comportamiento observado en grafos de 10, 25 y 50 nodos.

## 2. Organización de la implementación

- `main.py`: conserva las funciones previas de operaciones con lenguajes, evaluación de AFD/AFN y análisis de complejidad; agrega los endpoints de búsqueda.
- `schemas.py`: modelo Pydantic de entrada y validación de origen, destino y pesos no negativos.
- `greedy_search.py`: implementación propia de Greedy Best-First Search.
- `star_search.py`: implementación propia de A*.
- `search_common.py`: utilidades compartidas para contar nodos, calcular heurísticas y reconstruir rutas.
- `grafos/grafos_profesor.json`: grafos transcritos del archivo proporcionado para la actividad.
- `test_search.py`: pruebas automatizadas básicas.

No se usan bibliotecas especializadas de búsqueda. Se usa `heapq`, que forma parte de la biblioteca estándar de Python, para administrar una cola de prioridad.

## 3. Entrada y salida

Los endpoints reciben un JSON con `grafo`, `origen`, `destino` y, opcionalmente, `limite_visitas` y `coordenadas`. El grafo se representa como lista de adyacencia dirigida: cada nodo contiene pares `[vecino, peso]`. Los pesos deben ser no negativos.

Si no se especifica `limite_visitas`, el límite se calcula como el techo del 80 % del número total de nodos. La salida contiene `nodos_visitados`, `visitados`, `solucion`, `ruta`, `costo_ruta`, `T(n)`, `S(n)`, `operaciones_estimadas`, `maximo_elementos_frontera` y la heurística usada. Si no se alcanza el destino antes del límite, `solucion` es `false` y `ruta` es una lista vacía.

Ejemplo de petición:

```json
{
  "grafo": {
    "A": [["B", 15], ["C", 22]],
    "B": [["D", 7]],
    "C": [["D", 10]],
    "D": []
  },
  "origen": "A",
  "destino": "D"
}
```

## 4. Descripción de los algoritmos

### 4.1 Greedy Best-First Search

La búsqueda voraz prioriza el nodo que parece estar más cerca del destino según `h(n)`. No considera el costo acumulado de la ruta para ordenar la frontera, por lo que puede encontrar una solución con costo superior al óptimo.

Cuando todos los nodos tienen coordenadas, la implementación usa la distancia euclidiana al destino. Como los grafos entregados no incluyen coordenadas, en las pruebas se usa como alternativa el mínimo número de aristas hasta el destino, calculado recorriendo el grafo inverso. Esta heurística es topológica, no una distancia física.

### 4.2 A*

A* prioriza `f(n) = g(n) + h(n)`, donde `g(n)` es el costo acumulado desde el origen y `h(n)` estima el costo restante. Si todos los nodos tienen coordenadas, se calcula la distancia euclidiana. Si no hay coordenadas completas, se usa `h(n)=0`; en ese caso A* se comporta como Dijkstra y conserva la optimalidad para pesos no negativos, aunque no aprovecha información heurística.

La distancia euclidiana solo garantiza optimalidad cuando no sobreestima el costo real restante y está expresada en unidades compatibles con los pesos de las aristas.

## 5. Endpoints

- `POST /search/greedy`
- `POST /search/star`

Al iniciar el servidor, se pueden probar en Swagger desde `http://127.0.0.1:8000/docs`.

## 6. Pruebas y resultados

Se ejecutaron tres pares de origen-destino por cada tamaño de grafo. Para cada par se ejecutaron ambos algoritmos con el límite predeterminado del 80 %. La columna “operaciones” representa el contador interno de operaciones de exploración, no tiempo en segundos.

| Grafo | Origen → destino | Algoritmo | Solución | Nodos visitados | Ruta obtenida | Costo | Operaciones |
|---|---|---|---|---:|---|---:|---:|
| grafo-10 (10) | A → D | Greedy | True | 2 | A → D | 10.0 | 5 |
| grafo-10 (10) | A → D | A* | True | 2 | A → D | 10.0 | 5 |
| grafo-10 (10) | B → H | Greedy | True | 3 | B → E → H | 47.0 | 7 |
| grafo-10 (10) | B → H | A* | True | 6 | B → E → H | 47.0 | 13 |
| grafo-10 (10) | C → J | Greedy | True | 3 | C → G → J | 95.0 | 7 |
| grafo-10 (10) | C → J | A* | True | 6 | C → E → H → J | 46.0 | 14 |
| grafo-25 (25) | A → D | Greedy | True | 2 | A → D | 36.0 | 4 |
| grafo-25 (25) | A → D | A* | True | 2 | A → D | 36.0 | 4 |
| grafo-25 (25) | D → I | Greedy | True | 2 | D → I | 22.0 | 5 |
| grafo-25 (25) | D → I | A* | True | 3 | D → E → I | 17.0 | 8 |
| grafo-25 (25) | B → G | Greedy | True | 2 | B → G | 30.0 | 4 |
| grafo-25 (25) | B → G | A* | True | 5 | B → G | 30.0 | 14 |
| grafo-50 (50) | A → F | Greedy | True | 2 | A → F | 28.0 | 5 |
| grafo-50 (50) | A → F | A* | True | 2 | A → F | 28.0 | 5 |
| grafo-50 (50) | B → I | Greedy | True | 2 | B → I | 30.0 | 4 |
| grafo-50 (50) | B → I | A* | True | 2 | B → I | 30.0 | 4 |
| grafo-50 (50) | K → R | Greedy | True | 2 | K → R | 24.0 | 3 |
| grafo-50 (50) | K → R | A* | True | 2 | K → R | 24.0 | 3 |

### Interpretación

- En el grafo de 10 nodos, para `C → J`, Greedy encuentra `C → G → J` con costo 95, mientras A* encuentra `C → E → H → J` con costo 46. Esto ilustra que la ruta que parece más cercana por la heurística voraz no necesariamente es la más barata.
- Para `B → H` en el grafo de 10 nodos, ambos encuentran la misma ruta y costo, pero Greedy visita menos nodos en esta ejecución.
- En los casos seleccionados de los grafos de 25 y 50 nodos, ambos algoritmos encuentran una solución dentro del límite. A* puede expandir más nodos cuando no dispone de coordenadas y usa `h(n)=0`.
- Estos resultados dependen de los orígenes, destinos, pesos, orden de vecinos y límite de visitas. No demuestran que Greedy siempre sea más rápido ni que A* siempre visite menos nodos.

## 7. Complejidad computacional

Para ambas implementaciones, la respuesta informa las siguientes cotas generales de referencia con cola de prioridad:

- **Tiempo, `T(n)`:** `O((V + E) log V)` como referencia para grafos representados con listas de adyacencia y una cola de prioridad.
- **Espacio, `S(n)`:** `O(V + E)` considerando la representación del grafo y las estructuras auxiliares.

`V` es el número de nodos y `E` el número de aristas. La cantidad real de nodos expandidos y el contador de operaciones se incluyen como mediciones empíricas adicionales. En A*, el rendimiento depende de la calidad de la heurística; con `h(n)=0`, se obtiene el comportamiento de Dijkstra.

## 8. Instalación y ejecución

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Después, abrir `http://127.0.0.1:8000/docs`. Para correr las pruebas automatizadas:

```bash
pip install pytest
python -m pytest -q
```

## 9. Conclusión

La búsqueda voraz puede reducir la exploración en ciertos casos, pero no garantiza una ruta de costo mínimo. A* incorpora el costo acumulado y puede obtener rutas óptimas cuando se cumplen las condiciones de su heurística. Los grafos de la actividad no contienen coordenadas, por lo que las pruebas de A* usan `h(n)=0` y las de Greedy usan una heurística basada en saltos; esto queda señalado para no presentar una distancia euclidiana inexistente como si proviniera del archivo original.
