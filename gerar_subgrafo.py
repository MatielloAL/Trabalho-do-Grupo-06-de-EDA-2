"""
Gera uma visualização de subgrafo de amostra do dataset, usando a MESMA
lematização do sistema (spaCy pt_core_news_sm) e a função jaccard do projeto.

Como rodar (na raiz do projeto, com a venv ativada):
    pip install networkx matplotlib
    python gerar_subgrafo.py

Saída: arquivo subgrafo_modelagem.png na pasta atual.
"""

import json
import itertools
import random
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import networkx as nx

# usa o pré-processamento REAL do projeto (mesma lematização do sistema)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from preprocessamento import preprocessar, jaccard

# -------- configuração --------
N_POR_CATEGORIA = 3          # quantos relatos de cada categoria mostrar
SEED = 7                     # muda esse número se quiser outra amostra
CAMINHO_DATASET = os.path.join("dados", "dataset.json")
# ------------------------------

# permite sobrescrever pela linha de comando:
#   python gerar_subgrafo.py 3        -> usa SEED=3
#   python gerar_subgrafo.py 3 2      -> SEED=3, 2 relatos por categoria
if len(sys.argv) >= 2:
    SEED = int(sys.argv[1])
if len(sys.argv) >= 3:
    N_POR_CATEGORIA = int(sys.argv[2])

random.seed(SEED)

with open(CAMINHO_DATASET, encoding="utf-8") as f:
    dados = json.load(f)

cats = ["Navegação", "Sensores", "Comunicação", "Propulsão", "Energia", "Software Embarcado"]
cores = {
    "Navegação": "#4C72B0", "Sensores": "#55A868", "Comunicação": "#C44E52",
    "Propulsão": "#8172B2", "Energia": "#CCB974", "Software Embarcado": "#64B5CD",
}

# amostra: N relatos por categoria
amostra = []
for c in cats:
    desta = [d for d in dados if d["categoria"] == c]
    amostra += random.sample(desta, N_POR_CATEGORIA)

# lematização real (spaCy) — igual ao sistema
for d in amostra:
    d["_lemas"] = set(preprocessar(d["texto"]))

# monta o grafo com a mesma regra do projeto: aresta se jaccard > 0
G = nx.Graph()
for d in amostra:
    G.add_node(d["id"], categoria=d["categoria"])

for a, b in itertools.combinations(amostra, 2):
    s = jaccard(a["_lemas"], b["_lemas"])
    if s > 0:
        G.add_edge(a["id"], b["id"], weight=s)

print(f"Subgrafo: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")

# desenho
pos = nx.spring_layout(G, k=1.1, seed=SEED, iterations=300)
fig, ax = plt.subplots(figsize=(11, 8))

pesos = [G[u][v]["weight"] for u, v in G.edges()]
nx.draw_networkx_edges(
    G, pos, ax=ax,
    width=[0.5 + 6 * w for w in pesos],
    alpha=0.4, edge_color="#999999",
)

node_cores = [cores[G.nodes[n]["categoria"]] for n in G.nodes()]
nx.draw_networkx_nodes(
    G, pos, ax=ax, node_color=node_cores,
    node_size=950, edgecolors="white", linewidths=2,
)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight="bold", font_color="white")

leg = [Patch(facecolor=cores[c], label=c) for c in cats]
# legenda FORA do desenho (à direita), pra não tapar nenhum nó
ax.legend(
    handles=leg, loc="center left", bbox_to_anchor=(1.0, 0.5),
    fontsize=10, framealpha=0.95, title="Categoria",
)

ax.set_title(
    f"Subgrafo de amostra — {G.number_of_nodes()} relatos ({N_POR_CATEGORIA} por categoria)\n"
    "Vértice = relato · Aresta = similaridade de Jaccard (espessura = peso)",
    fontsize=13, fontweight="bold", pad=14,
)
ax.axis("off")
# margem extra à direita pra caber a legenda
plt.subplots_adjust(right=0.80)
plt.savefig("subgrafo_modelagem.png", dpi=150, bbox_inches="tight")
print("Salvo em subgrafo_modelagem.png")