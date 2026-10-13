# Actividad 13. Implementación de algoritmos P, NP y con Heurística

## 1. Bloque de identificación

- **Institución:** Universidad Iberoamericana Puebla
- **Carrera:** Ingeniería en Sistemas Computacionales
- **Actividad:** 13. Implementación de algoritmos P, NP y con Heurística
- **Estudiante:** Juan Pablo Ruiz Gil 192034
- **Fecha:** 13 Octubre de 2026
- **Repositorio:** https://github.com/Juampa2005/Actividad-6-AFD-y-AFN

---

## 2. Objetivo

Implementar y evaluar algoritmos de búsqueda y optimización mediante una API desarrollada con FastAPI, identificando sus diferencias en cuanto a complejidad computacional, tiempo de ejecución, consumo de memoria, nodos recorridos y costo de las soluciones obtenidas.

Los algoritmos implementados son Dijkstra, el problema del agente viajero mediante una solución exacta y el agente viajero mediante una heurística voraz. También se incorpora un endpoint auxiliar para generar grafos sintéticos ponderados que permiten evaluar el comportamiento de los algoritmos con diferentes cantidades de nodos.

## 3. Descripción general de la implementación

La implementación se integra al backend desarrollado en actividades anteriores, conservando los endpoints existentes y agregando nuevas rutas para resolver problemas de grafos.

Se utiliza FastAPI para exponer los algoritmos mediante solicitudes HTTP y Swagger UI para ejecutar las pruebas de forma interactiva.

El sistema incorpora las siguientes funcionalidades:

- Generación de grafos sintéticos ponderados.
- Búsqueda del camino mínimo entre dos nodos mediante Dijkstra.
- Resolución del problema del agente viajero mediante programación dinámica.
- Aproximación de una ruta para el agente viajero mediante una heurística voraz.
- Medición del tiempo de ejecución y del pico de memoria rastreada durante la ejecución.
- Registro del número de nodos o estados procesados y del costo de la ruta obtenida.

### 3.1. Endpoints implementados

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| POST | `/grafos/generar` | Genera un grafo sintético ponderado. |
| POST | `/dijkstra` | Calcula el camino de menor costo entre dos nodos. |
| POST | `/tsp/exacto` | Busca un circuito de costo mínimo mediante programación dinámica. |
| POST | `/tsp/voraz` | Construye un circuito mediante una estrategia voraz. |

### 3.2. Generación de grafos sintéticos

El endpoint `/grafos/generar` permite establecer el número de nodos, la semilla aleatoria y los límites de los pesos de las aristas.

Para las pruebas se utilizan grafos completos, no dirigidos y ponderados. Esto significa que existe una conexión entre cada par de nodos distintos y que las conexiones tienen pesos positivos.

Se utiliza la semilla 42 para facilitar la reproducción de las pruebas. Con los mismos parámetros se genera el mismo grafo.

Ejemplo de solicitud para cinco nodos:

```json
{
  "n": 5,
  "semilla": 42,
  "peso_minimo": 1,
  "peso_maximo": 20
}
```

Para las demás pruebas se modifica el valor de `n` a 10 y 15.

## 4. Descripción de los algoritmos

### 4.1. Algoritmo de Dijkstra

Dijkstra es un algoritmo de búsqueda de caminos mínimos en grafos con pesos no negativos. Su objetivo es encontrar la ruta de menor costo entre un nodo de origen y uno de destino.

El algoritmo mantiene una distancia provisional para cada nodo y utiliza una cola de prioridad para seleccionar el nodo pendiente con la menor distancia conocida. Cuando encuentra una ruta más económica hacia un vecino, actualiza su distancia y registra el nodo anterior para reconstruir el camino final.

**Complejidad temporal:** con una cola de prioridad y listas de adyacencia, su complejidad habitual es \(O((V+E)\log V)\), donde \(V\) representa los vértices y \(E\) las aristas.

**Complejidad espacial:** \(O(V+E)\) para representar el grafo y almacenar las estructuras auxiliares.

**Clasificación:** algoritmo polinómico, perteneciente a la clase P.

**Resultado esperado:** una ruta entre el origen y el destino, su costo total y las métricas de ejecución.

### 4.2. Agente viajero exacto

El problema del agente viajero (Traveling Salesperson Problem o TSP) consiste en encontrar un circuito de costo mínimo que visite cada nodo una sola vez y regrese al nodo inicial.

En esta implementación se utiliza programación dinámica mediante el algoritmo de Held-Karp. Este método almacena los mejores costos parciales para diferentes subconjuntos de nodos y aprovecha los resultados calculados previamente para construir una solución óptima.

**Complejidad temporal:** \(O(n^2 2^n)\).

**Complejidad espacial:** \(O(n2^n)\).

Aunque Held-Karp es más eficiente que enumerar todas las permutaciones, su crecimiento sigue siendo exponencial. El problema de optimización TSP es NP-difícil; su versión de decisión pertenece a NP.

**Resultado esperado:** un circuito que comience y termine en el nodo inicial, visite todos los nodos y tenga el menor costo posible.

### 4.3. Agente viajero con heurística voraz

La heurística voraz construye una ruta seleccionando, en cada paso, el nodo no visitado que tenga el menor peso desde la posición actual. Después de visitar todos los nodos, intenta regresar al nodo inicial.

Este método toma decisiones locales sin evaluar todas las combinaciones posibles. Por esa razón, generalmente es más rápido que una búsqueda exacta, pero puede producir un circuito cuyo costo sea superior al óptimo.

**Complejidad temporal:** \(O(n^2)\) para la implementación sobre un grafo completo representado mediante listas de adyacencia en forma de diccionarios.

**Complejidad espacial auxiliar:** \(O(n)\), sin contar el almacenamiento del grafo.

**Clasificación:** heurística voraz de tiempo polinómico. No constituye un algoritmo exacto para resolver el TSP.

**Resultado esperado:** un circuito completo, su costo y las métricas de ejecución.

## 5. Métricas evaluadas

Cada endpoint de algoritmos devuelve las siguientes métricas:

- **Tiempo de ejecución (ms):** duración de la ejecución medida con `time.perf_counter()`.
- **Memoria pico (bytes y KB):** máximo de memoria rastreada por `tracemalloc` durante la ejecución.
- **Nodos recorridos:** cantidad de nodos procesados por Dijkstra o la cantidad de nodos/estados contabilizados por los algoritmos TSP.
- **Costo del camino:** suma de los pesos de las aristas que componen la ruta o el circuito encontrado.

Es importante considerar que la métrica `nodos_recorridos` no representa exactamente la misma operación en los tres algoritmos. En Dijkstra cuenta los nodos extraídos de la cola de prioridad y procesados; en el TSP exacto contabiliza estados parciales generados por la implementación; y en el TSP voraz contabiliza los nodos visitados.

La memoria reportada corresponde al pico rastreado por Python, no al consumo total de memoria del proceso del servidor.

## 6. Procedimiento de pruebas

Las pruebas se ejecutan desde Swagger UI, disponible en:

`http://127.0.0.1:8000/docs`

Se siguen estos pasos:

1. Iniciar el servidor FastAPI.
2. Generar un grafo ponderado de cinco nodos.
3. Utilizar el grafo generado para probar Dijkstra, TSP exacto y TSP voraz.
4. Repetir el procedimiento con diez nodos.
5. Repetir el procedimiento con quince nodos.
6. Registrar los resultados de cada ejecución.
7. Comparar el tiempo, la memoria, los nodos recorridos y el costo de los circuitos.

Para Dijkstra se utiliza `N0` como origen y `N4`, `N9` o `N14` como destino, según el tamaño del grafo. Para los dos algoritmos TSP se utiliza `N0` como nodo inicial.

## 7. Pruebas y resultados

### 7.1. Prueba con cinco nodos

**Objetivo:** comprobar el funcionamiento de los algoritmos en un grafo pequeño.

| Algoritmo | Tiempo (ms) | Memoria pico (KB) | Nodos/estados recorridos | Costo |
|---|---:|---:|---:|---:|
| Dijkstra | [0.0332] | [.224] | [5] | [7] |
| TSP exacto | [0.336] | [3.05] | [28] | [19] |
| TSP voraz | [0.0871] | [1.24] | [5] | [19] |

**Resultado de la prueba:** [Indicar si los tres endpoints respondieron correctamente y describir brevemente los resultados obtenidos].

### 7.2. Prueba con diez nodos

**Objetivo:** evaluar el comportamiento de los algoritmos con un grafo de mayor tamaño.

| Algoritmo | Tiempo (ms) | Memoria pico (KB) | Nodos/estados recorridos | Costo |
|---|---:|---:|---:|---:|
| Dijkstra | [0.0653] | [0.99] | [5] | [4] |
| TSP exacto | [39.4499] | [307.96] | [2295] | [26] |
| TSP voraz | [0.1184] | [1.35] | [10] | [32] |

**Resultado de la prueba:** [Describir las diferencias observadas respecto a la prueba de cinco nodos].

### 7.3. Prueba con quince nodos

**Objetivo:** observar el comportamiento de los algoritmos ante un grafo de mayor tamaño y comparar la solución exacta con la aproximación voraz.

| Algoritmo | Tiempo (ms) | Memoria pico (KB) | Nodos/estados recorridos | Costo |
|---|---:|---:|---:|---:|
| Dijkstra | [0.146] | [1.64] | [12] | [6] |
| TSP exacto | [3117.2929] | [19937.4] | [114674] | [36] |
| TSP voraz | [0.1706] | [1.51] | [15] | [36] |


## 8. Análisis comparativo

Dijkstra resuelve un problema de camino mínimo en tiempo polinómico y no necesita explorar todas las rutas posibles. Por ello, su costo computacional suele crecer moderadamente al aumentar el tamaño del grafo.

El TSP exacto busca garantizar el menor costo del circuito. La programación dinámica de Held-Karp reduce considerablemente el trabajo respecto a la enumeración de todas las permutaciones, pero su complejidad exponencial provoca un crecimiento importante de las operaciones y de la memoria utilizada.

La heurística voraz selecciona la opción localmente más económica en cada paso. Esto permite construir una solución sin explorar todas las combinaciones, aunque no garantiza obtener el circuito óptimo.

La comparación de las pruebas permite estudiar el equilibrio entre calidad de la solución y costo computacional. Los resultados numéricos deben analizarse a partir de las mediciones obtenidas durante la ejecución real de los endpoints.

## 9. Conclusiones

La implementación permite comparar un algoritmo polinómico de búsqueda de caminos mínimos con dos estrategias para resolver el problema del agente viajero.

Dijkstra demuestra cómo es posible obtener caminos mínimos de manera eficiente cuando los pesos son no negativos. Por su parte, Held-Karp obtiene una solución óptima para el TSP, pero requiere un costo computacional considerablemente mayor conforme aumenta el número de nodos.

La heurística voraz ofrece una alternativa más sencilla y eficiente para construir circuitos, aunque la solución obtenida puede no ser óptima.

Finalmente, la generación de grafos sintéticos y la medición del tiempo de ejecución, memoria, nodos recorridos y costo de las soluciones permiten observar experimentalmente las diferencias entre los algoritmos y relacionarlas con su complejidad teórica.

## 10. Evidencias

Se deben anexar capturas de pantalla de Swagger UI que muestren:

1. La generación de grafos de 5, 10 y 15 nodos.
2. La ejecución de Dijkstra para los tres tamaños.
3. La ejecución del TSP exacto para los tres tamaños.
4. La ejecución del TSP voraz para los tres tamaños.
5. Las respuestas JSON que incluyan las métricas solicitadas.

