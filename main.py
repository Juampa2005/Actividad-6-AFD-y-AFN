from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import List, Dict
from pydantic import BaseModel
import itertools
import ast
app = FastAPI(
    title="API de Operaciones con Lenguajes, AFD, AFN y Complejidad",
    description="API para operaciones con lenguajes, evaluación de AFD y AFN y análisis de complejidad de programas",
    version="2.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Lenguaje(BaseModel):
    L: List[str] = []
    M: List[str] = []
    sigma: List[str] = []
    resultado: List[str] = []
    k: int = 3
class AFD(BaseModel):
    estados: List[str]
    alfabeto: List[str]
    transiciones: Dict[str, Dict[str, str]]
    inicial: str
    finales: List[str]
    cadena: str
class AFN(BaseModel):
    estados: List[str]
    alfabeto: List[str]
    transiciones: Dict[str, Dict[str, List[str]]]
    inicial: str
    finales: List[str]
    cadena: str
@app.get("/")

def inicio():
    return {
        "mensaje": "API de Operaciones con Lenguajes, AFD, AFN y Complejidad",
        "operaciones": [
            "/union",
            "/interseccion",
            "/diferencia",
            "/concatenar",
            "/lenguajes/complemento",
            "/lenguajes/Kleene",
            "/afd",
            "/afn",
            "/complejidad/analizar",
            "/complejidad/peor-caso",
            "/complejidad/mejor-caso"
        ]
    }
@app.get("/union")

def union(L: str, M: str):
    conjunto_L = set(L.split(","))
    conjunto_M = set(M.split(","))
    resultado = conjunto_L.union(conjunto_M)
    return {
        "operacion": "union",
        "L": list(conjunto_L),
        "M": list(conjunto_M),
        "resultado": list(resultado)
    }
@app.get("/interseccion")

def interseccion(L: str, M: str):
    conjunto_L = set(L.split(","))
    conjunto_M = set(M.split(","))
    resultado = conjunto_L.intersection(conjunto_M)
    return {
        "operacion": "interseccion",
        "L": list(conjunto_L),
        "M": list(conjunto_M),
        "resultado": list(resultado)
    }
@app.get("/diferencia")

def diferencia(L: str, M: str):
    conjunto_L = set(L.split(","))
    conjunto_M = set(M.split(","))
    resultado = conjunto_L.difference(conjunto_M)
    return {
        "operacion": "diferencia",
        "L": list(conjunto_L),
        "M": list(conjunto_M),
        "resultado": list(resultado)
    }
@app.get("/concatenar")
def concatenar(L: str, M: str):
    conjunto_L = set(L.split(","))
    conjunto_M = set(M.split(","))
    resultado = set()
    for x in conjunto_L:
        for y in conjunto_M:
            resultado.add(x + y)
    return {
        "operacion": "concatenacion",
        "L": list(conjunto_L),
        "M": list(conjunto_M),
        "resultado": list(resultado)
    }
def generar_universo(sigma: set, k: int) -> set:
    universo = {""}
    for longitud in range(1, k + 1):
        for combinacion in itertools.product(
            sigma,
            repeat=longitud
        ):
            universo.add("".join(combinacion))
    return universo
@app.post("/lenguajes/complemento")

def complemento_lenguajes(parametro: Lenguaje):
    universo = generar_universo(
        set(parametro.sigma),
        parametro.k
    )
    resultado = universo.difference(
        set(parametro.L)
    )
    return {
        "operacion": "complemento de lenguaje",
        "L": parametro.L,
        "sigma": parametro.sigma,
        "k": parametro.k,
        "resultado": list(resultado)
    }
# =========================================================
# CERRADURA DE KLEENE
# =========================================================
@app.post("/lenguajes/Kleene")

def kleene(parametro: Lenguaje):
    L = set(parametro.L)
    k = parametro.k
    resultado = {""}
    auxiliar = {""}
    for _ in range(k):
        auxiliar = concatenar_conjuntos(
            auxiliar,
            L
        )
        resultado = resultado.union(
            auxiliar
        )
    return {
        "operacion": "cerradura de Kleene",
        "L": parametro.L,
        "k": parametro.k,
        "resultado": list(resultado)
    }





def concatenar_conjuntos(L: set, M: set) -> set:
    resultado = set()
    for x in L:
        for y in M:
            resultado.add(x + y)
    return resultado
# =========================================================
# EVALUADOR DE AFD
# =========================================================
@app.post("/afd")

def evaluar_afd(afd: AFD):
    estado_actual = afd.inicial
    recorrido = [estado_actual]
    # Verificar que el estado inicial exista
    if estado_actual not in afd.estados:
        return {
            "operacion": "AFD",
            "error": "El estado inicial no existe en los estados del automata"
        }
    # Leer la cadena símbolo por símbolo
    for simbolo in afd.cadena:
        # Verificar que el símbolo pertenezca al alfabeto
        if simbolo not in afd.alfabeto:
            return {
                "operacion": "AFD",
                "cadena": afd.cadena,
                "aceptada": False,
                "error": f"El simbolo '{simbolo}' no pertenece al alfabeto"
            }
        # Verificar que exista una transición
        if estado_actual not in afd.transiciones:
            return {
                "operacion": "AFD",
                "cadena": afd.cadena,
                "aceptada": False,
                "error": f"No existen transiciones para el estado '{estado_actual}'"
            }
        if simbolo not in afd.transiciones[estado_actual]:
            return {
                "operacion": "AFD",
                "cadena": afd.cadena,
                "aceptada": False,
                "error": f"No existe transicion para {estado_actual} con '{simbolo}'"
            }
        # Cambiar de estado
        estado_actual = afd.transiciones[
            estado_actual
        ][simbolo]
        recorrido.append(
            estado_actual
        )
    # Verificar si terminó en un estado final
    aceptada = estado_actual in afd.finales
    return {
        "operacion": "AFD",
        "cadena": afd.cadena,
        "estado_inicial": afd.inicial,
        "recorrido": recorrido,
        "estado_final": estado_actual,
        "estados_finales": afd.finales,
        "aceptada": aceptada
    }
# =========================================================
# EVALUADOR DE AFN
# =========================================================
@app.post("/afn")

def evaluar_afn(afn: AFN):
    estados_actuales = {afn.inicial}
    recorrido = [
        list(estados_actuales)
    ]
    # Verificar que el estado inicial exista
    if afn.inicial not in afn.estados:
        return {
            "operacion": "AFN",
            "error": "El estado inicial no existe en los estados del automata"
        }
    # Leer la cadena símbolo por símbolo
    for simbolo in afn.cadena:
        # Verificar que el símbolo pertenezca al alfabeto
        if simbolo not in afn.alfabeto:
            return {
                "operacion": "AFN",
                "cadena": afn.cadena,
                "aceptada": False,
                "error": f"El simbolo '{simbolo}' no pertenece al alfabeto"
            }
        nuevos_estados = set()
        # Revisar todas las posibilidades
        for estado in estados_actuales:
            if estado in afn.transiciones:
                if simbolo in afn.transiciones[estado]:
                    destinos = afn.transiciones[
                        estado
                    ][simbolo]
                    for destino in destinos:
                        nuevos_estados.add(destino)
        estados_actuales = nuevos_estados
        recorrido.append(
            list(estados_actuales)
        )
    estados_finales_alcanzados = (
        estados_actuales.intersection(
            set(afn.finales)
        )
    )
    aceptada = len(
        estados_finales_alcanzados
    ) > 0
    return {
        "operacion": "AFN",
        "cadena": afn.cadena,
        "estado_inicial": afn.inicial,
        "recorrido": recorrido,
        "estados_finales": afn.finales,
        "estados_finales_alcanzados": list(
            estados_finales_alcanzados
        ),
        "aceptada": aceptada
    }
class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.complexities = {}
        self.loop_depth = 0
    def visit_For(self, node):
        self.loop_depth += 1
        complexity = self.complexity_from_depth(
            self.loop_depth
        )
        self.complexities[node.lineno] = complexity
        self.generic_visit(node)
        self.loop_depth -= 1
    def visit_While(self, node):
        self.loop_depth += 1
        complexity = self.complexity_from_depth(
            self.loop_depth
        )
        self.complexities[node.lineno] = complexity
        self.generic_visit(node)
        self.loop_depth -= 1
    # -----------------------------------------------------
    # IF
    # -----------------------------------------------------
    def visit_If(self, node):
        self.complexities[node.lineno] = "O(1)"
        self.generic_visit(node)
    # -----------------------------------------------------
    # FUNCIONES
    # -----------------------------------------------------
    def visit_FunctionDef(self, node):
        self.complexities[node.lineno] = "O(1)"
        self.generic_visit(node)
    # -----------------------------------------------------
    # COMPLEJIDAD SEGÚN PROFUNDIDAD
    # -----------------------------------------------------
    def complexity_from_depth(self, depth):
        if depth <= 1:
            return "O(n)"
        return f"O(n^{depth})"
# =========================================================
# UTILIDADES DE COMPLEJIDAD
# =========================================================



def complexity_degree(complexity: str) -> int:
    """
    Obtiene el grado de una complejidad.
    O(1)   -> 0
    O(n)   -> 1
    O(n^2) -> 2
    O(n^3) -> 3
    """
    if complexity == "O(1)":
        return 0
    if complexity == "O(n)":
        return 1
    if "^" in complexity:
        try:
            return int(
                complexity
                .split("^")[1]
                .replace(")", "")
            )
        except ValueError:
            return 1
    return 1





def get_dominant_complexity(
    complexities: List[str]
):
    if not complexities:
        return "O(1)"
    return max(
        complexities,
        key=complexity_degree
    )





def calculate_sum(
    complexities: List[str]
):
    if not complexities:
        return "O(1)"
    return " + ".join(
        complexities
    )





def calculate_big_omega(
    complexities: List[str]
):
    if not complexities:
        return "Ω(1)"
    menor = min(
        complexities,
        key=complexity_degree
    )
    return menor.replace(
        "O(",
        "Ω("
    )
# =========================================================
# ANÁLISIS DEL CÓDIGO
# =========================================================



def analyze_code(source_code: str):
    try:
        tree = ast.parse(
            source_code
        )
    except SyntaxError as error:
        raise HTTPException(
            status_code=400,
            detail=(
                "El archivo contiene un error "
                f"de sintaxis: {error}"
            )
        )
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    lines = source_code.splitlines()
    commented_lines = []
    complexities = []
    # -----------------------------------------------------
    # Analizar cada línea
    # -----------------------------------------------------
    for number, line in enumerate(
        lines,
        start=1
    ):
        complexity = analyzer.complexities.get(
            number
        )
        if complexity is not None:
            commented_lines.append(
                f"{line}  # Complejidad: {complexity}"
            )
            complexities.append(
                complexity
            )
        else:
            commented_lines.append(
                line
            )
    # -----------------------------------------------------
    # Calcular resultados
    # -----------------------------------------------------
    worst_case = get_dominant_complexity(
        complexities
    )
    best_case = calculate_big_omega(
        complexities
    )
    complexity_sum = calculate_sum(
        complexities
    )
    # -----------------------------------------------------
    # Agregar resumen
    # -----------------------------------------------------
    commented_lines.append("")
    commented_lines.append(
        "# =================================================="
    )
    commented_lines.append(
        "# RESUMEN DE COMPLEJIDAD"
    )
    commented_lines.append(
        "# =================================================="
    )
    commented_lines.append(
        "# Suma de complejidades individuales: "
        + complexity_sum
    )
    commented_lines.append(
        "# Complejidad de mayor grado: "
        + worst_case
    )
    commented_lines.append(
        "# Peor caso (Big-O): "
        + worst_case
    )
    commented_lines.append(
        "# Mejor caso (Big-Omega): "
        + best_case
    )
    commented_lines.append(
        "# =================================================="
    )
    return (
        "\n".join(commented_lines),
        worst_case,
        best_case,
        complexity_sum
    )
# =========================================================
# ENDPOINT: ANALIZAR ARCHIVO
# =========================================================
@app.post("/complejidad/analizar")

async def analizar_complejidad(
    archivo: UploadFile = File(...)
):
    # Verificar extensión
    if not archivo.filename.lower().endswith(".py"):
        raise HTTPException(
            status_code=400,
            detail=(
                "Solamente se aceptan "
                "archivos Python (.py)"
            )
        )
    contenido = await archivo.read()
    # Convertir bytes a texto
    try:
        codigo = contenido.decode(
            "utf-8"
        )
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail=(
                "El archivo debe estar "
                "codificado en UTF-8"
            )
        )
    resultado = analyze_code(
        codigo
    )
    codigo_comentado = resultado[0]
    nombre_original = archivo.filename
    nombre_salida = (
        nombre_original[:-3]
        + "_analizado.py"
    )
    return Response(
        content=codigo_comentado,
        media_type="text/plain",
        headers={
            "Content-Disposition":
                f'attachment; filename="{nombre_salida}"'
        }
    )
@app.post("/complejidad/peor-caso")

async def peor_caso(
    archivo: UploadFile = File(...)
):
    if not archivo.filename.lower().endswith(".py"):
        raise HTTPException(
            status_code=400,
            detail=(
                "Solamente se aceptan "
                "archivos Python (.py)"
            )
        )
    contenido = await archivo.read()
    try:
        codigo = contenido.decode(
            "utf-8"
        )
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail=(
                "El archivo debe estar "
                "codificado en UTF-8"
            )
        )
    _, big_o, _, suma = analyze_code(
        codigo
    )
    return {
        "archivo": archivo.filename,
        "tipo": "Peor caso",
        "notacion": "Big-O",
        "complejidad": big_o,
        "suma_complejidades": suma
    }
@app.post("/complejidad/mejor-caso")

async def mejor_caso(
    archivo: UploadFile = File(...)
):
    # Verificar extensión
    if not archivo.filename.lower().endswith(".py"):
        raise HTTPException(
            status_code=400,
            detail=(
                "Solamente se aceptan "
                "archivos Python (.py)"))
    contenido = await archivo.read()
    try:
        codigo = contenido.decode(
            "utf-8"
        )
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail=(
                "El archivo debe estar "
                "codificado en UTF-8"
            )
        )
    _, _, big_omega, suma = analyze_code(
        codigo
    )
    return {
        "archivo": archivo.filename,
        "tipo": "Mejor caso",
        "notacion": "Big-Omega",
        "complejidad": big_omega,
        "suma_complejidades": suma
    }
# =========================================================
# ACTIVIDAD 12: BÚSQUEDAS INFORMADAS
# =========================================================
from schemas import SearchRequest
from greedy_search import greedy_search
from star_search import star_search
@app.post("/search/greedy", tags=["Búsqueda informada"])
def endpoint_greedy(request: SearchRequest):
    """Ejecuta Greedy Best-First Search sobre un grafo dirigido ponderado."""
    try:
        return greedy_search(
            graph=request.grafo,
            origin=request.origen,
            destination=request.destino,
            visit_limit=request.limite_visitas,
            coordinates=request.coordenadas,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
@app.post("/search/star", tags=["Búsqueda informada"])
def endpoint_star(request: SearchRequest):
    """Ejecuta A* sobre un grafo dirigido ponderado."""
    try:
        return star_search(
            graph=request.grafo,
            origin=request.origen,
            destination=request.destino,
            visit_limit=request.limite_visitas,
            coordinates=request.coordenadas,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))