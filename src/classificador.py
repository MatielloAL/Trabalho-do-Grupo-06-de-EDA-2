"""Classificador de relatos de falhas em drones por similaridade em grafo.

Classifica um relato novo sem inseri-lo no grafo, usando Jaccard para
encontrar vizinhos de nível 1 e get_vizinhos() para nível 2.
Acumula scores por categoria com dict (HashMap) e desempata em 3 critérios.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from grafo import Grafo
from preprocessamento import preprocessar, jaccard
from construcao import construir_grafo


def classificar(texto: str, grafo: Grafo, profundidade: int = 2) -> str:
    """Classifica um relato novo retornando a categoria inferida pelo grafo.

    Entrada:
        texto         — relato de falha em português (texto bruto).
        grafo         — grafo de similaridade já construído (não será mutado).
        profundidade  — 1 (só vizinhos diretos) ou 2 (vizinhos de vizinhos).

    Saída:
        String com o nome da categoria inferida (ex: "Navegação").
        Retorna "" se não houver vizinhos (texto vazio, sem lemas úteis, etc).

    Comportamento:
        1. Pré-processa o texto → conjunto de lemas.
        2. Nível 1: calcula Jaccard entre o relato novo e cada vértice do grafo;
           vértices com Jaccard > 0 são vizinhos de nível 1 (peso = Jaccard).
        3. Nível 2 (se profundidade == 2): expande vizinhos de nível 1 via
           get_vizinhos(), usando o peso da aresta existente no grafo.
        4. Não visita o mesmo vértice duas vezes.
        5. Acumula score por categoria (soma dos pesos das arestas).
        6. Desempata: (1) maior score → (2) categoria do vizinho de maior peso
           individual → (3) categoria com mais vértices visitados.

    Restrição: NÃO muta o grafo (sem adicionar_vertice/adicionar_aresta).
    """
    # Pré-processar o texto novo
    lemas_novo = preprocessar(texto)
    set_novo = set(lemas_novo)

    # Caso de borda: sem lemas úteis → Jaccard será 0 com todos
    if not set_novo:
        return ""

    todos_vertices = grafo.get_todos_vertices()
    if not todos_vertices:
        return ""

    # --- Nível 1: encontrar vizinhos por Jaccard ---
    visitados: set[int] = set()
    # Lista de (id_vertice, peso_aresta) para todos os vértices alcançados
    vertices_alcancados: list[tuple[int, float]] = []

    for vid in todos_vertices:
        vertice = grafo.get_vertice(vid)
        set_vertice = set(vertice["lemas"])
        sim = jaccard(set_novo, set_vertice)
        if sim > 0:
            visitados.add(vid)
            vertices_alcancados.append((vid, sim))

    # --- Nível 2: expandir vizinhos de nível 1 via grafo ---
    if profundidade >= 2:
        # Copiar lista de nível 1 para iterar sem conflito
        vizinhos_nivel1 = list(vertices_alcancados)
        for vid_n1, _ in vizinhos_nivel1:
            for vizinho_id, peso_aresta in grafo.get_vizinhos(vid_n1):
                if vizinho_id not in visitados:
                    visitados.add(vizinho_id)
                    vertices_alcancados.append((vizinho_id, peso_aresta))

    # Caso de borda: nenhum vizinho encontrado
    if not vertices_alcancados:
        return ""

    # --- Acumulação de score por categoria (dict como HashMap) ---
    scores: dict[str, float] = {}
    # Para desempate: maior peso individual por categoria
    max_peso_por_categoria: dict[str, float] = {}
    # Para desempate: contagem de vértices por categoria
    contagem_por_categoria: dict[str, int] = {}

    for vid, peso in vertices_alcancados:
        vertice = grafo.get_vertice(vid)
        categoria = vertice["categoria"]

        # Acumular score (soma dos pesos)
        scores[categoria] = scores.get(categoria, 0.0) + peso

        # Rastrear maior peso individual por categoria
        if peso > max_peso_por_categoria.get(categoria, 0.0):
            max_peso_por_categoria[categoria] = peso

        # Contar vértices por categoria
        contagem_por_categoria[categoria] = contagem_por_categoria.get(categoria, 0) + 1

    # --- Decisão com desempate em 3 critérios ---
    # Ordena categorias por: (1) score desc, (2) max peso individual desc,
    # (3) contagem de vértices desc
    melhor_categoria = max(
        scores.keys(),
        key=lambda cat: (
            scores[cat],
            max_peso_por_categoria.get(cat, 0.0),
            contagem_por_categoria.get(cat, 0),
        ),
    )

    return melhor_categoria


# ---------------------------------------------------------------------------
# TESTE — classificação contra grafo real (dados/dataset.json)
#         usando exemplos de teste de dados/test_cases.json
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    caminho_dataset = os.path.join(os.path.dirname(__file__), "..", "dados", "dataset.json")
    with open(caminho_dataset, encoding="utf-8") as f:
        dataset = json.load(f)

    caminho_test = os.path.join(os.path.dirname(__file__), "..", "dados", "test_cases.json")
    with open(caminho_test, encoding="utf-8") as f:
        test_cases = json.load(f)

    print(f"Construindo grafo com {len(dataset)} relatos de treino...")
    grafo = construir_grafo(dataset)

    v_antes = grafo.total_vertices()
    e_antes = grafo.total_arestas()

    print(f"Grafo construído: {v_antes} vértices, {e_antes} arestas\n")

    # --- Testar com profundidade 1 e 2 ---
    for prof in [1, 2]:
        print(f"{'='*60}")
        print(f"  CLASSIFICAÇÃO COM PROFUNDIDADE {prof}")
        print(f"{'='*60}")

        acertos = 0
        total = len(test_cases)

        for caso in test_cases:
            texto = caso["texto"]
            esperado = caso["categoria"]
            resultado = classificar(texto, grafo, profundidade=prof)

            if resultado == esperado:
                acertos += 1
            else:
                print(f"  ERRO id={caso['id']} | esperado={esperado} | obtido={resultado}")
                print(f"        \"{texto[:80]}...\"")

        print(f"\n  Acurácia (prof={prof}): {acertos}/{total} = {acertos/total*100:.1f}%\n")

    # --- Verificar que o grafo NÃO foi mutado ---
    v_depois = grafo.total_vertices()
    e_depois = grafo.total_arestas()

    assert v_antes == v_depois, f"Grafo mutado! Vértices: {v_antes} → {v_depois}"
    assert e_antes == e_depois, f"Grafo mutado! Arestas: {e_antes} → {e_depois}"
    print("OK: grafo não foi mutado após classificações")

    # --- Teste de casos de borda ---
    assert classificar("", grafo) == "", "Falhou: texto vazio deveria retornar ''"
    assert classificar("...", grafo) == "", "Falhou: texto só pontuação deveria retornar ''"

    g_vazio = Grafo()
    assert classificar("O GPS perdeu sinal", g_vazio) == "", "Falhou: grafo vazio deveria retornar ''"

    print("OK: todos os testes de borda passaram")
