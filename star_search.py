"""Implementación propia de A* (búsqueda estrella)."""
import heapq
from typing import Optional, Dict, Tuple, List
from search_common import Graph, all_nodes, effective_limit, euclidean, reconstruct_path, response, path_cost


def star_search(graph: Graph, origin: str, destination: str,
                visit_limit: Optional[int] = None,
                coordinates: Optional[Dict[str, Tuple[float, float]]] = None) -> dict:
    nodes = all_nodes(graph)
    limit = effective_limit(graph, visit_limit)
    if origin not in nodes or destination not in nodes:
        raise ValueError("El origen y el destino deben existir en el grafo.")
    if origin == destination:
        return response(True, [origin], [origin], limit, 1, 1, "astar", "h(n)=0 (origen igual a destino)", 0.0)

    has_coordinates = bool(coordinates) and all(node in coordinates for node in nodes)
    def heuristic(node: str) -> float:
        value = euclidean(node, destination, coordinates) if has_coordinates else None
        return value if value is not None else 0.0
    heuristic_name = "distancia euclidiana" if has_coordinates else "h(n)=0 (sin coordenadas; equivale a Dijkstra y conserva optimalidad)"

    frontier = [(heuristic(origin), 0.0, 0, origin)]
    counter = 1
    came_from: Dict[str, str] = {}
    g_score = {origin: 0.0}
    closed = set()
    visited: List[str] = []
    operations = 0
    peak_frontier = 1
    found = False
    stopped = False

    while frontier:
        _f, queued_g, _, current = heapq.heappop(frontier)
        operations += 1
        if current in closed or queued_g > g_score.get(current, float("inf")):
            continue
        if len(visited) >= limit:
            stopped = True
            break
        visited.append(current)
        if current == destination:
            found = True
            break
        closed.add(current)
        for neighbor, weight in graph.get(current, []):
            operations += 1
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                if neighbor in closed:
                    closed.remove(neighbor)
                heapq.heappush(frontier, (tentative_g + heuristic(neighbor), tentative_g, counter, neighbor))
                counter += 1
        peak_frontier = max(peak_frontier, len(frontier))

    path = reconstruct_path(came_from, destination) if found else []
    return response(found, path, visited, limit, operations, peak_frontier, "astar", heuristic_name,
                    path_cost(graph, path) if found else None, stopped)
