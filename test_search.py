"""Pruebas automatizadas mínimas para los algoritmos de búsqueda."""
import json
from pathlib import Path
from greedy_search import greedy_search
from star_search import star_search

GRAPHS = json.loads((Path(__file__).parent / "grafos" / "grafos_profesor.json").read_text(encoding="utf-8"))


def test_all_graphs_have_expected_node_counts():
    assert len(GRAPHS["grafo-10"]) == 10
    assert len(GRAPHS["grafo-25"]) == 25
    assert len(GRAPHS["grafo-50"]) == 50


def test_astar_finds_known_routes():
    cases = [("grafo-10", "A", "D"), ("grafo-25", "A", "I"), ("grafo-50", "A", "K")]
    for name, origin, destination in cases:
        result = star_search(GRAPHS[name], origin, destination)
        assert result["solucion"] is True
        assert result["ruta"][0] == origin
        assert result["ruta"][-1] == destination


def test_greedy_finds_known_routes():
    cases = [("grafo-10", "A", "D"), ("grafo-25", "A", "I"), ("grafo-50", "A", "K")]
    for name, origin, destination in cases:
        result = greedy_search(GRAPHS[name], origin, destination)
        assert result["solucion"] is True
        assert result["ruta"][0] == origin
        assert result["ruta"][-1] == destination


def test_visit_limit_is_respected():
    graph = GRAPHS["grafo-10"]
    result = star_search(graph, "A", "J", visit_limit=2)
    assert result["nodos_visitados"] <= 2


def test_unreachable_destination_returns_no_solution():
    graph = {"A": [["B", 1]], "B": [], "C": []}
    result = star_search(graph, "A", "C")
    assert result["solucion"] is False
    assert result["ruta"] == []
