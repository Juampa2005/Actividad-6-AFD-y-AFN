from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, model_validator

class SearchRequest(BaseModel):
    """Entrada común para búsqueda voraz y A*."""
    grafo: Dict[str, List[Tuple[str, float]]] = Field(
        ..., description="Lista de adyacencia dirigida: nodo -> [[vecino, peso], ...]"
    )
    origen: str
    destino: str
    limite_visitas: Optional[int] = Field(
        default=None, ge=1,
        description="Máximo de nodos a visitar. Si se omite, se usa el 80% del total (redondeado hacia arriba)."
    )
    coordenadas: Optional[Dict[str, Tuple[float, float]]] = Field(
        default=None,
        description="Coordenadas opcionales por nodo para calcular la heurística euclidiana."
    )

    @model_validator(mode="after")
    def validar_grafo(self):
        nodos = set(self.grafo)
        for vecinos in self.grafo.values():
            for vecino, peso in vecinos:
                nodos.add(vecino)
                if peso < 0:
                    raise ValueError("Los pesos de las aristas deben ser mayores o iguales a cero.")
        if self.origen not in nodos:
            raise ValueError(f"El origen '{self.origen}' no pertenece al grafo.")
        if self.destino not in nodos:
            raise ValueError(f"El destino '{self.destino}' no pertenece al grafo.")
        if self.coordenadas:
            faltantes = nodos.intersection(self.coordenadas.keys())
            # Las coordenadas son opcionales por nodo; la heurística euclidiana se usa
            # solo cuando origen/destino y nodo evaluado tienen coordenadas disponibles.
        return self
