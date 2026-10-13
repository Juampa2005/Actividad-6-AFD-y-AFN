
## 1. Bloque de identificación

- **Nombre del alumno:** Juan Pablo Ruiz Gil
- **Matricula** 192034
- **Materia:** Lenguajes de computacion
- **Actividad:** 12 Algoritmos de búsqueda informada (heurísticos)



# Backend de algoritmos con FastAPI

## 1. Descripción del proyecto

Este repositorio contiene un backend desarrollado con **FastAPI** para implementar y probar algoritmos de autómatas, análisis de complejidad y búsqueda en grafos.

La API permite ejecutar solicitudes HTTP y consultar sus resultados en formato JSON mediante Swagger UI.

En la Actividad 13 se agregan los siguientes algoritmos:

- **Dijkstra:** búsqueda del camino de menor costo.
- **TSP exacto:** resolución del problema del agente viajero mediante programación dinámica.
- **TSP voraz:** construcción de una ruta mediante una heurística voraz.
- **Generador de grafos:** creación de grafos sintéticos ponderados para realizar pruebas.

## 2. Instalación y ejecución

Instala las dependencias necesarias:

```bash
pip install fastapi uvicorn
```

Desde la carpeta donde se encuentra `main.py`, ejecuta:

```bash
python -m uvicorn main:app --reload
```

Abre la documentación interactiva:

**Swagger UI:** http://127.0.0.1:8000/docs

> Si tu archivo principal o tu instancia de FastAPI tienen otro nombre, ajusta el comando según tu proyecto.

## 3. Endpoints de la Actividad 13

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/grafos/generar` | Genera un grafo ponderado. |
| POST | `/dijkstra` | Calcula el camino mínimo entre dos nodos. |
| POST | `/tsp/exacto` | Calcula un circuito de costo mínimo mediante Held-Karp. |
| POST | `/tsp/voraz` | Construye un circuito mediante una heurística voraz. |

Los endpoints anteriores del proyecto se mantienen disponibles. Consulta `/docs` para revisar sus rutas y parámetros.

## 4. Pruebas del generador de grafos

En Swagger, selecciona `POST /grafos/generar`, pulsa **Try it out**, pega el JSON y ejecuta la solicitud.

### 4.1. Grafo de 5 nodos

```json
{
  "n": 5,
  "semilla": 42,
  "peso_minimo": 1,
  "peso_maximo": 20
}
```

### 4.2. Grafo de 10 nodos

```json
{
  "n": 10,
  "semilla": 42,
  "peso_minimo": 1,
  "peso_maximo": 20
}
```

### 4.3. Grafo de 15 nodos

```json
{
  "n": 15,
  "semilla": 42,
  "peso_minimo": 1,
  "peso_maximo": 20
}
```

Copia el objeto `grafo` devuelto por el generador y úsalo en los tres algoritmos siguientes. Así podrás comparar los resultados sobre el mismo grafo.

## 5. Prueba de Dijkstra

**Endpoint:** `POST /dijkstra`

Ejemplo para un grafo de cinco nodos:

```json
{
  "grafo": {
    "N0": {"N1": 4, "N2": 8, "N3": 6, "N4": 7},
    "N1": {"N0": 4, "N2": 3, "N3": 5, "N4": 9},
    "N2": {"N0": 8, "N1": 3, "N3": 2, "N4": 4},
    "N3": {"N0": 6, "N1": 5, "N2": 2, "N4": 3},
    "N4": {"N0": 7, "N1": 9, "N2": 4, "N3": 3}
  },
  "inicio": "N0",
  "destino": "N4"
}
```

Para los grafos generados, utiliza los siguientes pares:

| Tamaño | Inicio | Destino |
|---|---|---|
| 5 nodos | `N0` | `N4` |
| 10 nodos | `N0` | `N9` |
| 15 nodos | `N0` | `N14` |

La respuesta contiene el camino encontrado, su costo y las métricas de ejecución.

## 6. Prueba del TSP exacto

**Endpoint:** `POST /tsp/exacto`

Utiliza el mismo formato de grafo, pero incluye solamente el nodo inicial. No incluyas `destino`.

```json
{
  "grafo": {
    "N0": {"N1": 4, "N2": 8, "N3": 6, "N4": 7},
    "N1": {"N0": 4, "N2": 3, "N3": 5, "N4": 9},
    "N2": {"N0": 8, "N1": 3, "N3": 2, "N4": 4},
    "N3": {"N0": 6, "N1": 5, "N2": 2, "N4": 3},
    "N4": {"N0": 7, "N1": 9, "N2": 4, "N3": 3}
  },
  "inicio": "N0"
}
```

Este ejemplo utiliza cinco nodos. Para las pruebas de 10 y 15 nodos, sustituye el grafo por el resultado del generador correspondiente.

El algoritmo busca un circuito que visite todos los nodos y regrese al nodo inicial, minimizando el costo total.

## 7. Prueba del TSP voraz

**Endpoint:** `POST /tsp/voraz`

Utiliza el mismo formato y el mismo grafo que en el TSP exacto:

```json
{
  "grafo": {
    "N0": {"N1": 4, "N2": 8, "N3": 6, "N4": 7},
    "N1": {"N0": 4, "N2": 3, "N3": 5, "N4": 9},
    "N2": {"N0": 8, "N1": 3, "N3": 2, "N4": 4},
    "N3": {"N0": 6, "N1": 5, "N2": 2, "N4": 3},
    "N4": {"N0": 7, "N1": 9, "N2": 4, "N3": 3}
  },
  "inicio": "N0"
}
```

La heurística selecciona en cada paso el vecino no visitado con menor peso. Puede ser más rápida que el algoritmo exacto, pero no garantiza encontrar el circuito óptimo.

## 8. Pruebas de AFD y AFN

El proyecto también contiene esquemas relacionados con los autómatas finitos deterministas (AFD) y no deterministas (AFN).

Para probarlos:

1. Abre Swagger UI.
2. Localiza los endpoints correspondientes a AFD y AFN.
3. Expande cada endpoint y pulsa **Try it out**.
4. Revisa el esquema de la solicitud para conocer los campos obligatorios.
5. Introduce una cadena que deba ser aceptada y otra que deba ser rechazada.

Los nombres exactos de las propiedades dependen de la implementación de los modelos `AFD` y `AFN` en el backend.

## 9. Pruebas de análisis de complejidad

El proyecto incluye modelos relacionados con las siguientes operaciones:

- Análisis general de complejidad.
- Evaluación del mejor caso.
- Evaluación del peor caso.

Para ejecutarlas, localiza los endpoints de complejidad en Swagger UI y revisa el esquema de cada cuerpo de solicitud. Completa los campos obligatorios indicados por la documentación de la API y ejecuta cada prueba.

## 10. Métricas de los algoritmos

Los endpoints de grafos reportan las siguientes métricas:

- **Tiempo de ejecución:** tiempo empleado durante la ejecución, medido en milisegundos.
- **Memoria pico:** máximo de memoria rastreada por Python durante la ejecución.
- **Nodos recorridos:** contador específico de cada algoritmo.
- **Costo del camino:** suma de los pesos de las aristas de la ruta o circuito encontrado.

Los tiempos y el consumo de memoria pueden variar entre ejecuciones.

En la implementación de Held-Karp, el contador de estados parciales no representa necesariamente el número de nodos originales del grafo. Por ello, la comparación debe considerar qué mide cada algoritmo.

## 11. Resumen de complejidad

### Dijkstra

Encuentra caminos mínimos en grafos con pesos no negativos. Con una cola de prioridad y listas de adyacencia, su complejidad temporal habitual es:

`O((V + E) log V)`

Es un algoritmo polinómico.

### TSP exacto mediante Held-Karp

Utiliza programación dinámica para encontrar un circuito óptimo del agente viajero.

- Tiempo: `O(n² · 2ⁿ)`
- Memoria: `O(n · 2ⁿ)`

Tiene complejidad exponencial. El problema de optimización TSP es NP-difícil, mientras que su versión de decisión pertenece a NP.

### TSP voraz

Construye un circuito seleccionando la conexión más económica hacia un nodo todavía no visitado.

Para la implementación sobre un grafo completo representado mediante diccionarios, su complejidad temporal es `O(n²)`. Es una heurística polinómica que no garantiza la solución óptima.

## 12. Registro de resultados

Completa la siguiente tabla con los valores reales obtenidos en Swagger.

| Nodos | Algoritmo | Tiempo (ms) | Memoria pico (KB) | Nodos/estados recorridos | Costo |
|---:|---|---:|---:|---:|---:|
| 5 | Dijkstra | | | | |
| 5 | TSP exacto | | | | |
| 5 | TSP voraz | | | | |
| 10 | Dijkstra | | | | |
| 10 | TSP exacto | | | | |
| 10 | TSP voraz | | | | |
| 15 | Dijkstra | | | | |
| 15 | TSP exacto | | | | |
| 15 | TSP voraz | | | | |

## 13. Conclusión

La implementación permite comparar un algoritmo polinómico de caminos mínimos con dos estrategias para el problema del agente viajero. Dijkstra busca una ruta óptima entre dos nodos; Held-Karp obtiene un circuito óptimo con un costo computacional exponencial; y la heurística voraz construye una solución generalmente más rápida, sin garantizar que sea óptima.

Las pruebas con grafos de 5, 10 y 15 nodos permiten observar las diferencias de tiempo, memoria y costo de las soluciones.

## 14. Repositorio

[Actividad-6-AFD-y-AFN — GitHub](https://github.com/Juampa2005/Actividad-6-AFD-y-AFN)
