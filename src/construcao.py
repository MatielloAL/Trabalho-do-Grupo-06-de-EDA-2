

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from grafo import Grafo
from preprocessamento import preprocessar, jaccard


def construir_grafo(dataset: list) -> Grafo:

    g = Grafo()

    for relato in dataset:
        lemas = preprocessar(relato["texto"])
        g.adicionar_vertice(relato["id"], relato["texto"], relato["categoria"], lemas)

    ids = g.get_todos_vertices()

    # cacheia set de lemas uma vez por vértice — evita ~57k recriações de set
    sets_lemas = {id: set(g.get_vertice(id)["lemas"]) for id in ids}

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            id_a, id_b = ids[i], ids[j]
            sim = jaccard(sets_lemas[id_a], sets_lemas[id_b])
            if sim > 0:
                g.adicionar_aresta(id_a, id_b, sim)

    return g


def analisar_grafo(grafo: Grafo) -> dict:
    v = grafo.total_vertices()
    e = grafo.total_arestas()

    densidade = (2 * e) / (v * (v - 1)) if v > 1 else 0.0

    graus = {id: len(grafo.get_vizinhos(id)) for id in grafo.get_todos_vertices()}
    grau_medio = sum(graus.values()) / v if v > 0 else 0.0
    grau_max = max(graus.values()) if graus else 0
    vertices_mais_conectados = [id for id, g in graus.items() if g == grau_max]

    return {
        "vertices": v,
        "arestas": e,
        "densidade": densidade,
        "grau_medio": grau_medio,
        "grau_max": grau_max,
        "vertices_mais_conectados": vertices_mais_conectados,
    }



if __name__ == "__main__":
    caminho = os.path.join(os.path.dirname(__file__), "..", "dados", "dataset.json")
    with open(caminho, encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"Carregando {len(dataset)} relatos e construindo grafo...")
    grafo = construir_grafo(dataset)

    stats = analisar_grafo(grafo)

    print("\n=== ANÁLISE ESTRUTURAL DO GRAFO ===")
    print(f"Vértices : {stats['vertices']}")
    print(f"Arestas  : {stats['arestas']}")
    print(f"Densidade: {stats['densidade']:.6f}")
    print(f"Grau médio       : {stats['grau_medio']:.2f}")
    print(f"Grau máximo      : {stats['grau_max']}")
    print(f"Vértice(s) mais conectado(s): {stats['vertices_mais_conectados']}")

