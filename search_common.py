from collections import deque
from math import hypot, ceil, inf
from typing import Dict, List, Tuple, Optional, Any
import heapq

Graph = Dict[str, List[Tuple[str, float]]]


def all_nodes(graph: Graph) -> set[str]:
    nodes = set(graph)
    for edges in graph.values():
        nodes.update(neighbor for neighbor, _ in edges)
    return nodes


def effective_limit(graph: Graph, limit: Optional[int]) -> int:
    total = len(all_nodes(graph))
    return limit if limit is not None else max(1, ceil(total * 0.8))


def euclidean(a: str, b: str, coordinates: Optional[Dict[str, Tuple[float, float]]]) -> Optional[float]:
    if not coordinates or a not in coordinates or b not in coordinates:
        return None
    ax, ay = coordinates[a]
    bx, by = coordinates[b]
    return hypot(ax - bx, ay - by)


def reverse_hop_heuristic(graph: Graph, destination: str) -> Dict[str, float]:
    """Distancia mínima en número de aristas al destino, respetando direcciones."""
    reverse: Dict[str, List[str]] = {node: [] for node in all_nodes(graph)}
    for node, edges in graph.items():
        for neighbor, _ in edges:
            reverse.setdefault(neighbor, []).append(node)
    distances = {destination: 0}
    queue = deque([destination])
    while queue:
        current = queue.popleft()
        for predecessor in reverse.get(current, []):
            if predecessor not in distances:
                distances[predecessor] = distances[current] + 1
                queue.append(predecessor)
    return {node: float(distances.get(node, 10**9)) for node in all_nodes(graph)}


def reconstruct_path(came_from: Dict[str, str], destination: str) -> List[str]:
    path = [destination]
    while path[-1] in came_from:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def response(found: bool, path: List[str], visited: List[str], limit: int,
             operations: int, peak_frontier: int, algorithm: str, heuristic: str,
             cost: Optional[float] = None, stopped_by_limit: bool = False) -> dict[str, Any]:
    if algorithm == "greedy":
        time_complexity = "O((V + E) log V)"
    else:
        time_complexity = "O((V + E) log V)"  # A* con cola de prioridad; depende de la heurística.
    return {
        "algoritmo": "Greedy Best-First Search" if algorithm == "greedy" else "A*",
        "nodos_visitados": len(visited),
        "visitados": visited,
        "solucion": found,
        "ruta": path if found else [],
        "costo_ruta": cost if found else None,
        "limite_visitas": limit,
        "limite_alcanzado": stopped_by_limit,
        "T(n)": time_complexity,
        "S(n)": "O(V + E)",
        "operaciones_estimadas": operations,
        "maximo_elementos_frontera": peak_frontier,
        "heuristica_utilizada": heuristic,
    }


def path_cost(graph: Graph, path: List[str]) -> float:
    total = 0.0
    for a, b in zip(path, path[1:]):
        matches = [weight for neighbor, weight in graph.get(a, []) if neighbor == b]
        if not matches:
            return inf
        total += min(matches)
    return total
