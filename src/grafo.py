# Estrutura de dados do grafo usada em todo o sistema de classificação
# de relatos de falhas em drones.
#
# Representação: LISTA DE ADJACÊNCIA. O grafo é esparso (cada frase só
# compartilha palavras com poucas outras), então a lista gasta O(V + E) de
# memória.

class Grafo:
    def __init__(self):
        self._vertices = {}
        self._adjacencia = {}
        self._num_arestas = 0

    def adicionar_vertice(self, id: int, texto: str, categoria: str, lemas: list) -> None:
        """Adiciona um vértice ao grafo. Se o id já existir, atualiza os dados."""
        self._vertices[id] = {
            "id": id,
            "texto": texto,
            "categoria": categoria,
            "lemas": lemas,
        }
        if id not in self._adjacencia:
            self._adjacencia[id] = []

    def adicionar_aresta(self, id_a: int, id_b: int, peso: float) -> None:
        """Cria uma aresta não-direcionada entre id_a e id_b com o peso dado.

        Como o grafo é não-direcionado, a aresta é registrada nas duas
        listas de adjacência. Laços (id_a == id_b) são ignorados, assim como
        arestas para vértices inexistentes.
        """
        if id_a == id_b:
            return
        if id_a not in self._vertices or id_b not in self._vertices:
            return

        for vizinho, _ in self._adjacencia[id_a]:
            if vizinho == id_b:
                return

        self._adjacencia[id_a].append((id_b, peso))
        self._adjacencia[id_b].append((id_a, peso))
        self._num_arestas += 1

    def get_vizinhos(self, id: int) -> list:
        """Retorna a lista de (id_vizinho, peso) do vértice id."""
        return self._adjacencia.get(id, [])

    def get_vertice(self, id: int) -> dict:
        """Retorna o dicionário de dados do vértice id (ou None se não existir)."""
        return self._vertices.get(id)

    def get_todos_vertices(self) -> list:
        """Retorna a lista de ids de todos os vértices do grafo."""
        return list(self._vertices.keys())

    def total_vertices(self) -> int:
        """Retorna a quantidade de vértices."""
        return len(self._vertices)

    def total_arestas(self) -> int:
        """Retorna a quantidade de arestas (cada aresta contada uma vez)."""
        return self._num_arestas


# ----------------------------------------------------------------------------
# TESTE MANUAL — mini-grafo de 4 vértices
#
# Grafo de teste:
#
#     0 --0.5-- 1
#     |         |
#    0.3       0.4
#     |         |
#     2 --0.2-- 3
#
# ----------------------------------------------------------------------------
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

    print("total_vertices:", g.total_vertices())          
    print("total_arestas:", g.total_arestas())            
    print("todos_vertices:", g.get_todos_vertices())      
    print("vizinhos de 0:", g.get_vizinhos(0))            
    print("vizinhos de 3:", g.get_vizinhos(3))           
    print("vertice 2:", g.get_vertice(2))                

    g.adicionar_aresta(0, 1, 0.9)  
    g.adicionar_aresta(0, 0, 1.0) 
    g.adicionar_aresta(0, 99, 0.5) 
    print("total_arestas apos invalidas:", g.total_arestas())  
    print("vizinho inexistente:", g.get_vizinhos(99))         

    print("\n--- rodando asserts ---")

    # estado básico do grafo
    assert g.total_vertices() == 4
    assert g.total_arestas() == 4
    assert g.get_todos_vertices() == [0, 1, 2, 3]

    # vizinhos e pesos (set() pra não depender da ordem de inserção)
    assert set(g.get_vizinhos(0)) == {(1, 0.5), (2, 0.3)}
    assert set(g.get_vizinhos(3)) == {(1, 0.4), (2, 0.2)}

    # dados do vértice
    assert g.get_vertice(2)["categoria"] == "Propulsão"
    assert g.get_vertice(2)["lemas"] == ["motor", "vibração"]
    assert g.get_vertice(99) is None          # vértice inexistente -> None

    # robustez: duplicada, laço e vértice inexistente não criaram aresta
    assert g.total_arestas() == 4
    assert g.get_vizinhos(99) == []           # id inexistente -> lista vazia

    print("OK: todos os asserts passaram")