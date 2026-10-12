"""Implementación propia de Greedy Best-First Search."""
import heapq
from typing import Optional, Dict, Tuple, List
from search_common import Graph, all_nodes, effective_limit, euclidean, reverse_hop_heuristic, reconstruct_path, response, path_cost


def greedy_search(graph: Graph, origin: str, destination: str,
                  visit_limit: Optional[int] = None,
                  coordinates: Optional[Dict[str, Tuple[float, float]]] = None) -> dict:
    nodes = all_nodes(graph)
    limit = effective_limit(graph, visit_limit)
    if origin not in nodes or destination not in nodes:
        raise ValueError("El origen y el destino deben existir en el grafo.")
    if origin == destination:
        return response(True, [origin], [origin], limit, 1, 1, "greedy", "h(n)=0 (origen igual a destino)", 0.0)

    hop_h = reverse_hop_heuristic(graph, destination)
    has_coordinates = bool(coordinates) and all(node in coordinates for node in nodes)
    def heuristic(node: str) -> float:
        if has_coordinates:
            return euclidean(node, destination, coordinates) or 0.0
        return hop_h.get(node, float("inf"))
    heuristic_name = "distancia euclidiana" if has_coordinates else "mínimo número de aristas hasta el destino (BFS inversa)"

    frontier = [(heuristic(origin), 0, origin)]
    counter = 1
    came_from: Dict[str, str] = {}
    discovered = {origin}
    visited: List[str] = []
    operations = 0
    peak_frontier = 1
    found = False
    stopped = False

    while frontier:
        _, _, current = heapq.heappop(frontier)
        operations += 1
        if current in visited:
            continue
        if len(visited) >= limit:
            stopped = True
            break
        visited.append(current)
        if current == destination:
            found = True
            break
        for neighbor, _weight in graph.get(current, []):
            operations += 1
            if neighbor not in discovered and neighbor not in visited:
                discovered.add(neighbor)
                came_from[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor), counter, neighbor))
                counter += 1
        peak_frontier = max(peak_frontier, len(frontier))

    path = reconstruct_path(came_from, destination) if found else []
    return response(found, path, visited, limit, operations, peak_frontier, "greedy", heuristic_name,
                    path_cost(graph, path) if found else None, stopped)
