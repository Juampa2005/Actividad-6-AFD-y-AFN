# Actividad 11. Análisis de complejidad

## 1. Bloque de identificación

- **Nombre del alumno:** Juan Pablo Ruiz Gil
- **Materia:** Lenguajes de computacion
- **Actividad:** 11. Análisis de complejidad
- **Fecha de entrega:** [Fecha de entrega]


---

## 2. Nombre de la actividad

**Actividad 11. Implementación de endpoints para el análisis de complejidad.**

## 3. Objetivo

Implementar una API utilizando FastAPI que permita analizar la complejidad de algoritmos y consultar su comportamiento en el mejor y el peor caso, mediante endpoints específicos.

## 4. Enlace del repositorio

El código fuente de la implementación se encuentra disponible en el siguiente repositorio:

**[Actividad-6-AFD-y-AFN — GitHub](https://github.com/Juampa2005/Actividad-6-AFD-y-AFN)**

La API incluye los siguientes endpoints relacionados con el análisis de complejidad:

- `/complejidad/analizar`
- `/complejidad/peor-caso`
- `/complejidad/mejor-caso`

La documentación interactiva de FastAPI permite consultar los parámetros y probar las rutas disponibles en `/docs`, una vez iniciado el servidor.

## 5. Descripción general de la implementación

La aplicación está desarrollada con FastAPI, un framework de Python que permite crear servicios web y definir endpoints para recibir solicitudes y devolver respuestas estructuradas.

La implementación divide el análisis en tres operaciones principales:

### 5.1. Análisis general de complejidad

**Endpoint:** `/complejidad/analizar`

Este endpoint permite solicitar un análisis de complejidad de acuerdo con los datos y el algoritmo contemplados en la implementación.

Su propósito es centralizar el análisis y presentar el resultado de manera estructurada.

### 5.2. Análisis del peor caso

**Endpoint:** `/complejidad/peor-caso`

Este endpoint permite consultar el comportamiento de un algoritmo en el escenario que representa el mayor costo computacional dentro del modelo analizado.

El peor caso es importante porque permite estudiar cómo se comporta un algoritmo ante entradas desfavorables.

### 5.3. Análisis del mejor caso

**Endpoint:** `/complejidad/mejor-caso`

Este endpoint permite consultar el comportamiento del algoritmo en condiciones que representan el menor costo computacional.

El mejor caso ayuda a identificar situaciones en las que el algoritmo necesita realizar menos operaciones.

### 5.4. Conceptos teóricos

Para interpretar los resultados se consideran los siguientes conceptos:

- **Notación O grande, O(f(n)):** representa una cota asintótica superior del crecimiento de un algoritmo.
- **Notación Omega, Ω(f(n)):** representa una cota asintótica inferior.
- **Notación Theta, Θ(f(n)):** representa una cota asintótica ajustada cuando se cumplen las condiciones correspondientes.

La complejidad depende del algoritmo estudiado, de su implementación y de las características de la entrada.

> Nota: los métodos HTTP, los parámetros y las estructuras exactas de las respuestas deben coincidir con el código implementado en el repositorio.

## 6. Pruebas efectuadas y resultados

Las pruebas permiten comprobar la disponibilidad de la API, el funcionamiento de sus endpoints y el manejo de solicitudes válidas e inválidas.

### 6.1. Pruebas funcionales

| ID | Prueba | Procedimiento | Resultado esperado |
|---|---|---|---|
| P01 | Disponibilidad de la API | Iniciar el servidor y abrir `/docs`. | La documentación interactiva se muestra correctamente. |
| P02 | Análisis general | Enviar una solicitud válida a `/complejidad/analizar`. | La API devuelve el análisis correspondiente. |
| P03 | Peor caso | Enviar una solicitud válida a `/complejidad/peor-caso`. | La API devuelve el resultado correspondiente al peor caso. |
| P04 | Mejor caso | Enviar una solicitud válida a `/complejidad/mejor-caso`. | La API devuelve el resultado correspondiente al mejor caso. |
| P05 | Validación de datos | Enviar datos incompletos o con tipos incorrectos. | La API responde de acuerdo con las reglas de validación implementadas. |
| P06 | Consistencia | Comparar las respuestas con los resultados esperados para los datos de entrada. | Los resultados son coherentes con la lógica del algoritmo. |

### 6.2. Registro de resultados reales

La siguiente tabla debe completarse después de ejecutar las pruebas. No se deben marcar como exitosas pruebas que todavía no se hayan realizado.

| ID | Estado | Observaciones |
|---|---|---|
| P01 | Pendiente de verificar | Registrar si `/docs` abre correctamente. |
| P02 | Pendiente de verificar | Registrar el código HTTP y la respuesta obtenida. |
| P03 | Pendiente de verificar | Registrar el código HTTP y la respuesta obtenida. |
| P04 | Pendiente de verificar | Registrar el código HTTP y la respuesta obtenida. |
| P05 | Pendiente de verificar | Registrar el comportamiento ante datos inválidos. |
| P06 | Pendiente de verificar | Comparar los resultados con los valores esperados. |

## 7. Procedimiento para ejecutar las pruebas

1. Clonar el repositorio de GitHub.
2. Instalar las dependencias indicadas por el proyecto.
3. Iniciar la aplicación FastAPI utilizando el comando de ejecución configurado.
4. Abrir la dirección `http://127.0.0.1:8000/docs`, si se utiliza el puerto predeterminado.
5. Localizar los endpoints de análisis de complejidad.
6. Utilizar la opción **Try it out** para enviar solicitudes de prueba.
7. Introducir los parámetros requeridos por cada endpoint.
8. Ejecutar las solicitudes y revisar los códigos HTTP y las respuestas.
9. Registrar los resultados obtenidos y conservar capturas de pantalla como evidencia, si son solicitadas.

## 8. Resultados y conclusiones

La actividad aborda la implementación de una API para analizar la complejidad de algoritmos mediante endpoints específicos. La separación entre análisis general, mejor caso y peor caso facilita organizar las operaciones y probarlas de forma independiente.

FastAPI proporciona una documentación interactiva que permite enviar solicitudes y revisar las respuestas sin necesidad de utilizar una herramienta externa.

La validación final requiere ejecutar cada prueba, verificar que los resultados correspondan a la implementación y registrar las evidencias obtenidas.

## 9. Referencias

- Repositorio del proyecto: https://github.com/Juampa2005/Actividad-6-AFD-y-AFN
- Documentación oficial de FastAPI: https://fastapi.tiangolo.com/
