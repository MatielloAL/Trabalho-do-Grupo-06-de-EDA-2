# Trabalho do Grupo 06 — EDA 2

Classificador de falhas de drones usando grafo de similaridade textual e BFS.

## Instalação

```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

## Como rodar

```bash
python src/main.py
```

### Comandos disponíveis

- Digite um relato → exibe a categoria predita
- `avaliar` → roda os casos de teste e exibe acurácia
- `sair` → encerra o sistema

## Estrutura

```
src/
  preprocessamento.py   # NLP: tokenização, lematização, Jaccard
  grafo.py              # Estrutura de dados: lista de adjacência
  construcao.py         # Constrói o grafo a partir do dataset
  bfs.py                # BFS implementado do zero
  classificador.py      # Lógica de classificação por similaridade
  main.py               # Interface interativa
dados/
  dataset.json          # 240 relatos de treinamento (80%)
  test_cases.json       # 60 casos de teste (20%)
```

## Análise dos Resultados

*(a ser preenchido após rodar o sistema — Issue 5)*
