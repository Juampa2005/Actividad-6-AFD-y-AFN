# API de Análisis de Complejidad de Programas

## 1. Descripción

Esta API extiende el backend desarrollado previamente para la evaluación de **Autómatas Finitos Deterministas (AFD)** y **Autómatas Finitos No Deterministas (AFN)**.

La nueva funcionalidad permite analizar programas escritos en Python para identificar su complejidad algorítmica utilizando notación asintótica.

El sistema incorpora tres nuevos endpoints:

- `POST /complejidad/analizar`
- `POST /complejidad/peor-caso`
- `POST /complejidad/mejor-caso`

El análisis identifica estructuras de control como ciclos `for`, ciclos `while`, estructuras condicionales y funciones, y asigna una complejidad aproximada a las líneas correspondientes.

Además, el endpoint de análisis genera un nuevo archivo Python en el que se agregan comentarios indicando la complejidad de cada línea y un bloque final con el resumen del análisis.

---

# 2. Requisitos

## Python

Se requiere Python 3.9 o superior.

## Dependencias

Instalar las dependencias con:

```bash
pip install fastapi uvicorn python-multipart
```

También puede utilizarse un archivo `requirements.txt`:

```text
fastapi
uvicorn
python-multipart
```

---

# 3. Ejecución del servidor

Para iniciar la API:

```bash
uvicorn main:app --reload
```

Por defecto, el servidor estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva de Swagger estará disponible en:

```text
http://127.0.0.1:8000/docs
```

También se puede consultar la documentación alternativa de ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 4. Endpoints existentes

El backend conserva los endpoints desarrollados anteriormente para el análisis de autómatas.

## 4.1 Evaluación de AFD

```http
POST /afd/evaluar
```

Recibe la definición de un Autómata Finito Determinista y las cadenas que deben evaluarse.

### Body

El endpoint recibe un objeto JSON con la siguiente estructura:

```json
{
    "estados": ["q0", "q1"],
    "alfabeto": ["0", "1"],
    "inicial": "q0",
    "finales": ["q1"],
    "transiciones": {
        "q0": {
            "0": "q0",
            "1": "q1"
        },
        "q1": {
            "0": "q0",
            "1": "q1"
        }
    },
    "cadenas": [
        "1",
        "01",
        "101"
    ]
}
```

---

## 4.2 Evaluación de AFN

```http
POST /afn/evaluar
```

Recibe la definición de un Autómata Finito No Determinista y las cadenas que deben evaluarse.

La estructura del JSON es la misma utilizada para el endpoint del AFD, con la diferencia de que una transición puede tener múltiples estados destino.

---

# 5. Nuevos endpoints de complejidad

## 5.1 Analizar archivo y generar archivo comentado

```http
POST /complejidad/analizar
```

### Descripción

Este endpoint recibe un archivo de código fuente Python y analiza su contenido.

El sistema:

1. Recibe el archivo `.py`.
2. Lee su contenido.
3. Analiza su estructura sintáctica.
4. Identifica estructuras de control.
5. Asigna una complejidad aproximada a las líneas correspondientes.
6. Agrega comentarios de complejidad al código.
7. Calcula la complejidad dominante.
8. Calcula la suma de las complejidades individuales.
9. Calcula una estimación del mejor caso mediante Big-Omega.
10. Genera un nuevo archivo Python.

El archivo generado conserva el código original y añade comentarios.

### Método

```http
POST
```

### URL

```text
/complejidad/analizar
```

### Parámetro

El endpoint recibe un archivo mediante `multipart/form-data`.

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `archivo` | File | Sí | Archivo Python `.py` que será analizado |

### Ejemplo de archivo de entrada

```python
n = 10

for i in range(n):
    print(i)

for i in range(n):
    for j in range(n):
        print(i, j)
```

### Ejemplo con cURL

```bash
curl -X POST "http://127.0.0.1:8000/complejidad/analizar" \
  -H "accept: text/plain" \
  -H "Content-Type: multipart/form-data" \
  -F "archivo=@programa.py" \
  -o programa_analizado.py
```

El resultado se guarda en:

```text
programa_analizado.py
```

### Ejemplo de respuesta

El endpoint devuelve directamente el archivo generado.

```python
n = 10  # Complejidad: O(1)

for i in range(n):  # Complejidad: O(n)
    print(i)  # Complejidad: O(1)

for i in range(n):  # Complejidad: O(n)
    for j in range(n):  # Complejidad: O(n^2)
        print(i, j)  # Complejidad: O(1)

# ==================================================
# RESUMEN DE COMPLEJIDAD
# ==================================================
# Suma de complejidades individuales: O(1) + O(n) + O(1) + O(n) + O(n^2) + O(1)
# Complejidad de mayor grado: O(n^2)
# Peor caso (Big-O): O(n^2)
# Mejor caso (Big-Omega): Ω(1)
# ==================================================
```

### Errores posibles

Si se envía un archivo que no sea `.py`, la API devuelve:

```json
{
    "detail": "Por el momento solamente se aceptan archivos Python (.py)"
}
```

Si el archivo contiene errores de sintaxis:

```json
{
    "detail": "El archivo contiene un error de sintaxis: ..."
}
```

---

# 6. Endpoint de peor caso — Big-O

```http
POST /complejidad/peor-caso
```

## Descripción

Este endpoint recibe un archivo Python y determina la complejidad identificada como la de mayor grado.

La notación utilizada es **Big-O**, que representa una cota superior asintótica y se utiliza para expresar el comportamiento del algoritmo en el peor caso.

Por ejemplo:

```text
O(1)
O(n)
O(n²)
O(n³)
```

Si un programa contiene ciclos anidados con una profundidad de dos, la complejidad dominante identificada será:

```text
O(n²)
```

---

## Parámetros

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `archivo` | File | Sí | Archivo Python `.py` |

---

## Ejemplo con cURL

```bash
curl -X POST "http://127.0.0.1:8000/complejidad/peor-caso" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "archivo=@programa.py"
```

---

## Ejemplo de respuesta

```json
{
    "archivo": "programa.py",
    "tipo": "Peor caso",
    "notacion": "Big-O",
    "complejidad": "O(n^2)",
    "suma_complejidades": "O(1) + O(n) + O(1) + O(n) + O(n^2) + O(1)"
}
```

### Descripción de la respuesta

| Campo | Descripción |
|---|---|
| `archivo` | Nombre del archivo analizado |
| `tipo` | Indica que se trata del peor caso |
| `notacion` | Notación utilizada: Big-O |
| `complejidad` | Complejidad dominante identificada |
| `suma_complejidades` | Suma de las complejidades individuales identificadas |

---

# 7. Endpoint de mejor caso — Big-Omega

```http
POST /complejidad/mejor-caso
```

## Descripción

Este endpoint analiza un archivo Python y devuelve una estimación de la complejidad correspondiente al mejor caso.

La notación utilizada es **Big-Omega (Ω)**.

Big-Omega representa una cota inferior asintótica del comportamiento de un algoritmo.

---

## Parámetros

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `archivo` | File | Sí | Archivo Python `.py` |

---

## Ejemplo con cURL

```bash
curl -X POST "http://127.0.0.1:8000/complejidad/mejor-caso" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "archivo=@programa.py"
```

---

## Ejemplo de respuesta

```json
{
    "archivo": "programa.py",
    "tipo": "Mejor caso",
    "notacion": "Big-Omega",
    "complejidad": "Ω(1)",
    "suma_complejidades": "O(1) + O(n) + O(1) + O(n) + O(n^2) + O(1)"
}
```

---

# 8. Análisis de complejidad

El analizador utiliza el módulo `ast` de Python para construir un árbol sintáctico abstracto del programa.

Esto permite identificar estructuras del código sin depender únicamente de la búsqueda de palabras dentro del archivo.

Las principales estructuras consideradas son:

| Estructura | Complejidad identificada |
|---|---|
| Instrucción simple | `O(1)` |
| Asignación | `O(1)` |
| Condicional `if` | `O(1)` |
| Un ciclo `for` | `O(n)` |
| Un ciclo `while` | `O(n)` |
| Dos ciclos anidados | `O(n²)` |
| Tres ciclos anidados | `O(n³)` |
| `n` ciclos anidados | `O(n^n)` según la representación del analizador |

La complejidad dominante corresponde a la estructura de mayor grado identificada dentro del programa.

---

# 9. Ejemplo de análisis

Se puede utilizar el siguiente programa como prueba:

```python
def buscar(n):
    resultado = 0

    for i in range(n):
        resultado += i

    for i in range(n):
        for j in range(n):
            resultado += i + j

    return resultado
```

El programa contiene:

- Operaciones constantes.
- Un ciclo con complejidad `O(n)`.
- Dos ciclos anidados con complejidad `O(n²)`.

Por lo tanto, la complejidad dominante identificada es:

```text
O(n²)
```

El archivo generado incluirá comentarios como:

```python
for i in range(n):  # Complejidad: O(n)
```

y:

```python
for i in range(n):  # Complejidad: O(n)
    for j in range(n):  # Complejidad: O(n^2)
```

Al final se agrega:

```python
# ==================================================
# RESUMEN DE COMPLEJIDAD
# ==================================================
# Suma de complejidades individuales: ...
# Complejidad de mayor grado: O(n^2)
# Peor caso (Big-O): O(n^2)
# Mejor caso (Big-Omega): Ω(1)
# ==================================================
```

---

# 10. Uso mediante Swagger

FastAPI genera automáticamente una interfaz Swagger para probar los endpoints.

Después de iniciar el servidor:

```bash
uvicorn main:app --reload
```

se debe abrir:

```text
http://127.0.0.1:8000/docs
```

En Swagger aparecerán los endpoints disponibles.

Dentro de la sección correspondiente a complejidad se encontrarán:

```text
POST /complejidad/analizar
POST /complejidad/peor-caso
POST /complejidad/mejor-caso
```

---

## 10.1 Probar `/complejidad/analizar`

1. Seleccionar:

```text
POST /complejidad/analizar
```

2. Presionar:

```text
Try it out
```

3. En el campo `archivo`, seleccionar un archivo `.py`.

Por ejemplo:

```text
programa.py
```

4. Presionar:

```text
Execute
```

5. El servidor analizará el archivo y devolverá el archivo Python modificado.

---

## 10.2 Probar `/complejidad/peor-caso`

Seleccionar:

```text
POST /complejidad/peor-caso
```

Presionar:

```text
Try it out
```

Seleccionar el archivo:

```text
programa.py
```

Presionar:

```text
Execute
```

Swagger mostrará una respuesta similar a:

```json
{
    "archivo": "programa.py",
    "tipo": "Peor caso",
    "notacion": "Big-O",
    "complejidad": "O(n^2)",
    "suma_complejidades": "O(1) + O(n) + O(n^2)"
}
```

---

## 10.3 Probar `/complejidad/mejor-caso`

Seleccionar:

```text
POST /complejidad/mejor-caso
```

Presionar:

```text
Try it out
```

Seleccionar:

```text
programa.py
```

Presionar:

```text
Execute
```

La respuesta tendrá una estructura similar a:

```json
{
    "archivo": "programa.py",
    "tipo": "Mejor caso",
    "notacion": "Big-Omega",
    "complejidad": "Ω(1)",
    "suma_complejidades": "O(1) + O(n) + O(n^2)"
}
```

---

# 11. Códigos HTTP

Los endpoints utilizan códigos HTTP para indicar el resultado de la operación.

| Código | Significado |
|---:|---|
| `200` | Operación realizada correctamente |
| `400` | Archivo inválido, extensión incorrecta o error de sintaxis |
| `422` | Error de validación de los parámetros enviados |
| `500` | Error interno del servidor |

---

# 12. Restricciones actuales

La versión actual del analizador trabaja con archivos:

```text
.py
```

El archivo debe utilizar codificación:

```text
UTF-8
```

Actualmente el análisis está orientado a identificar:

- instrucciones constantes;
- asignaciones;
- estructuras `if`;
- ciclos `for`;
- ciclos `while`;
- ciclos anidados;
- funciones.

La complejidad calculada representa una **estimación basada en la estructura sintáctica identificada**, por lo que no pretende sustituir un análisis matemático exhaustivo del algoritmo.

---

# 13. Resumen de endpoints

| Endpoint | Método | Entrada | Salida |
|---|---|---|---|
| `/afd/evaluar` | POST | JSON | JSON |
| `/afn/evaluar` | POST | JSON | JSON |
| `/complejidad/analizar` | POST | Archivo `.py` | Archivo `.py` comentado |
| `/complejidad/peor-caso` | POST | Archivo `.py` | JSON |
| `/complejidad/mejor-caso` | POST | Archivo `.py` | JSON |

---

# 14. Flujo general

El funcionamiento de los nuevos endpoints puede resumirse de la siguiente manera:

```text
                 Archivo Python
                       │
                       ▼
             ┌───────────────────┐
             │   FastAPI recibe  │
             │      archivo      │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Análisis mediante │
             │       AST         │
             └─────────┬─────────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       Complejidad línea    Complejidad
          por línea          global
              │                 │
              │          ┌──────┴───────┐
              │          │              │
              ▼          ▼              ▼
          Comentarios   Big-O        Big-Omega
              │
              ▼
       Archivo generado
```

---

# 15. Conclusión

La ampliación permite que el backend original de evaluación de autómatas también funcione como un servicio de análisis de complejidad de programas.

Los nuevos endpoints permiten:

- analizar un archivo Python;
- obtener la complejidad de cada línea;
- generar un nuevo archivo con comentarios;
- obtener la suma de las complejidades identificadas;
- determinar la complejidad dominante;
- consultar el peor caso mediante Big-O;
- consultar el mejor caso mediante Big-Omega;
- probar todos los servicios mediante Swagger.

La documentación interactiva generada por FastAPI permite realizar pruebas directamente desde el navegador sin necesidad de desarrollar un cliente adicional.