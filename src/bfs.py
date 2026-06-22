"""Busca em largura (BFS) implementada do zero sobre a classe Grafo.

Usa collections.deque apenas como fila FIFO — toda a lógica de percurso
(visitados, expansão de vizinhos, controle de profundidade) é própria.
"""

from collections import deque

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from grafo import Grafo


def bfs(grafo: Grafo, vertice_inicial: int, profundidade_max: int) -> list[tuple[int, float]]:
    """Executa BFS a partir de vertice_inicial, respeitando profundidade_max.

    Entrada:
        grafo            — instância de Grafo (lista de adjacência ponderada).
        vertice_inicial  — id do vértice de partida.
        profundidade_max — número máximo de níveis a explorar (1 ou 2).

    Saída:
        Lista de (id_vertice, peso_da_aresta) de todos os vértices alcançados.
        O peso é o da aresta que alcançou o vértice na árvore BFS.
        O vértice inicial NÃO aparece na lista de retorno.

    Casos de borda:
        - profundidade_max <= 0          → []
        - vertice_inicial inexistente    → []
        - grafo sem vértices             → []
    """
    if profundidade_max <= 0:
        return []

    if grafo.get_vertice(vertice_inicial) is None:
        return []

    visitados: set[int] = set()
    visitados.add(vertice_inicial)

    # Fila: cada elemento é (id_vertice, profundidade_atual, peso_aresta)
    fila: deque[tuple[int, int, float]] = deque()

    # Enfileira os vizinhos diretos do vértice inicial (profundidade 1)
    for vizinho_id, peso in grafo.get_vizinhos(vertice_inicial):
        if vizinho_id not in visitados:
            visitados.add(vizinho_id)
            fila.append((vizinho_id, 1, peso))

    resultado: list[tuple[int, float]] = []

    while fila:
        vertice_atual, profundidade, peso_aresta = fila.popleft()
        resultado.append((vertice_atual, peso_aresta))

        # Só expande vizinhos se ainda não atingiu a profundidade máxima
        if profundidade < profundidade_max:
            for vizinho_id, peso in grafo.get_vizinhos(vertice_atual):
                if vizinho_id not in visitados:
                    visitados.add(vizinho_id)
                    fila.append((vizinho_id, profundidade + 1, peso))

    return resultado


# ---------------------------------------------------------------------------
# TESTE MANUAL — mini-grafo de 4 vértices (mesmo de grafo.py)
#
#     0 --0.5-- 1
#     |         |
#    0.3       0.4
#     |         |
#     2 --0.2-- 3
#
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    g = Grafo()

    g.adicionar_vertice(0, "O GPS perdeu sinal", "Navegação", ["gps", "perder", "sinal"])
    g.adicionar_vertice(1, "Falha na comunicação", "Comunicação", ["falha", "comunicação"])
    g.adicionar_vertice(2, "Motor com vibração", "Propulsão", ["motor", "vibração"])
    g.adicionar_vertice(3, "Bateria descarregou", "Energia", ["bateria", "descarregar"])

    g.adicionar_aresta(0, 1, 0.5)
    g.adicionar_aresta(0, 2, 0.3)
    g.adicionar_aresta(1, 3, 0.4)
    g.adicionar_aresta(2, 3, 0.2)

    # --- Profundidade 1 a partir do vértice 0 ---
    r1 = bfs(g, 0, 1)
    print("BFS(0, prof=1):", r1)
    # Deve retornar vizinhos diretos de 0: vértices 1 (peso 0.5) e 2 (peso 0.3)
    assert set(r1) == {(1, 0.5), (2, 0.3)}, f"Falhou prof=1: {r1}"

    # --- Profundidade 2 a partir do vértice 0 ---
    r2 = bfs(g, 0, 2)
    print("BFS(0, prof=2):", r2)
    # Nível 1: vértices 1 e 2. Nível 2: vértice 3 (alcançado via 1 com peso 0.4
    # OU via 2 com peso 0.2 — depende da ordem, mas só aparece uma vez).
    ids_r2 = {v for v, _ in r2}
    assert ids_r2 == {1, 2, 3}, f"Falhou prof=2 ids: {ids_r2}"
    assert len(r2) == 3, f"Falhou prof=2 tamanho: {len(r2)}"

    # --- Profundidade 1 a partir do vértice 3 ---
    r3 = bfs(g, 3, 1)
    print("BFS(3, prof=1):", r3)
    assert set(r3) == {(1, 0.4), (2, 0.2)}, f"Falhou BFS(3,1): {r3}"

    # --- Casos de borda ---
    assert bfs(g, 0, 0) == [], "Falhou: profundidade 0 deveria retornar []"
    assert bfs(g, 0, -1) == [], "Falhou: profundidade negativa deveria retornar []"
    assert bfs(g, 99, 2) == [], "Falhou: vértice inexistente deveria retornar []"

    g_vazio = Grafo()
    assert bfs(g_vazio, 0, 1) == [], "Falhou: grafo vazio deveria retornar []"

    print("\nOK: todos os asserts de bfs.py passaram")
