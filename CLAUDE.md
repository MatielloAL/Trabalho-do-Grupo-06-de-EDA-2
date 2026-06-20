# CLAUDE.md — Projeto EDA: Classificador de Falhas de Drones

> Este arquivo é lido pelo Claude Code no início de cada sessão neste repositório.
> Ele define o contexto do projeto, as regras inegociáveis do professor e as instruções de trabalho para a tarefa atual (Issue 1). Atualize a seção "Tarefa Atual" conforme avançarmos para as próximas issues.

---

## 1. Contexto do Projeto (não inventar, não expandir)

- **Disciplina:** Estruturas de Dados e Algoritmos (EDA) — UnB, 2026.1, Prof. Glauco.
- **Tema do grupo (Grupo E / Grupo 06):** Sistema de classificação textual baseado em
  representações relacionais em grafos.
- **Domínio de aplicação escolhido:** Classificação de relatos de falhas operacionais em
  drones, em português, em 6 categorias: `Navegação`, `Sensores`, `Comunicação`,
  `Propulsão`, `Energia`, `Software Embarcado`.
- **Dataset:** `dados/dataset.json` (240 relatos, treino), `dados/test_cases.json`
  (60 relatos, teste). Também existe `dados/relatos_falhas_drones.csv` com os mesmos
  dados em formato CSV — usar o que já está sendo usado pelo restante do código; não
  duplicar fonte de dados sem necessidade.
- **Linguagem obrigatória:** Python (permitida pelo edital, junto com C/C++).

### Fonte da verdade técnica

Existe um documento de planejamento (`relatorio_projeto_EDA.md`) entregue ao professor
em 10/06/2026 com uma proposta inicial (stemming, TF-IDF, propagação de scores). **Essa
proposta foi superada.** A decisão técnica atual e vigente do grupo é a que está
implementada nos artefatos do repositório:

- **Pré-processamento:** lematização com **spaCy** (não stemming).
- **Similaridade:** índice de **Jaccard** sobre conjuntos de lemas (não TF-IDF/cosseno).
- **Algoritmo principal sobre o grafo:** **BFS implementado do zero** (`src/bfs.py`),
  não "propagação de score por arestas ponderadas".
- **Grafo:** lista de adjacência (`src/grafo.py`).

➡️ **Regra para o Claude Code:** sempre que houver conflito entre o `relatorio_projeto_EDA.md`
e os arquivos reais do repositório (README, Issues, `requirements.txt`, código já
existente), **o repositório vence**. O relatório só deve ser consultado para contexto de
negócio (significado das categorias, motivação, vocabulário típico de cada categoria),
nunca para decidir algoritmo, estrutura de dados ou biblioteca.

---

## 2. Regras do Edital (inegociáveis — penalizam a nota do grupo inteiro)

Estas regras valem para **todo o projeto**, não só para a Issue 1. O Claude Code deve
ter isso em mente mesmo em issues futuras de grafo/BFS/classificador:

1. **Uso de grafo é obrigatório.** Sem grafo = nota zero.
2. **Pelo menos uma estrutura de dados além do grafo é obrigatória.** Sem isso = -5,0.
   (No nosso caso: lista de adjacência é o grafo; outras estruturas auxiliares — ex.
   listas, sets, dicionários de índice invertido — contam como a estrutura adicional,
   desde que justificadas.)
3. **Os algoritmos principais de grafo (ex. BFS) devem ser implementados pelo próprio
   grupo, sem bibliotecas prontas** (proibido usar `networkx` ou similar para BFS/
   percurso/ranqueamento). Usar biblioteca pronta para algoritmo principal de grafo =
   **-5,0**.
4. **Bibliotecas externas de PLN são permitidas** (regra 7 do edital), **desde que a
   modelagem em grafos e os algoritmos principais sejam implementados pelo grupo.**
   Isso é exatamente o papel do spaCy aqui: ele só pode ser usado para tokenização/
   lematização/stopwords (etapa de PLN), **nunca** para grafo, BFS, ranqueamento ou
   classificação.
5. **Código deve estar no GitHub, atualizado até 22/06/2026.** Atraso = -2,0/dia.
6. **Código que não executa ou tem falhas graves = nota zero.**

➡️ **Implicação direta para a Issue 1:** `spacy` é a única biblioteca autorizada nesta
issue, e seu uso deve ficar restrito ao módulo `src/preprocessamento.py`, apenas para
tokenização, remoção de stopwords e lematização. A função `jaccard()` deve ser
implementada manualmente com operações de conjunto nativas do Python
(`set.intersection`, `set.union` ou operadores `&` / `|`), sem bibliotecas de similaridade
prontas (ex. não usar `sklearn`, `scipy.spatial.distance`, etc. para isso).

---

## 3. Ambiente de Desenvolvimento

- **SO:** Windows com WSL2 (Ubuntu).
- **Editor:** VS Code (com extensão Remote - WSL).
- **Status:** Issue 0 (setup do projeto) já está concluída — venv, estrutura de pastas
  e Git já existem. **Não recriar nada disso.** Antes de codar, o Claude Code deve
  apenas verificar:
  - Se o venv está ativo (`which python` deve apontar para dentro do venv, não para
    `/usr/bin/python3`).
  - Se `spacy` está instalado (`pip show spacy`).
  - Se o modelo `pt_core_news_sm` está instalado (`python -m spacy validate` ou
    tentar `spacy.load("pt_core_news_sm")`).
  - Se algo estiver faltando, **perguntar antes de instalar**, mostrando o comando
    exato que será executado.

---

## 4. Tarefa Atual — Issue 1: Módulo de Pré-processamento com spaCy

### Objetivo da issue (copiado fielmente da Issue, sem adições)

Implementar o pipeline que transforma texto bruto em lista de lemas filtrados, e a
função de similaridade de Jaccard usada para comparar textos. É a base de comparação
usada pela construção do grafo e pelo classificador.

- **Depende de:** Issue 0 (✅ já concluída).
- **Pode ser feita em paralelo com:** Issue 2 (não é nosso foco agora).

### Tarefas (escopo exato — não adicionar nada fora disso)

1. Configurar spaCy com modelo em português (`pt_core_news_sm`).
2. Implementar em `src/preprocessamento.py`:
   - `preprocessar(texto: str) -> list[str]` que:
     - Tokeniza o texto.
     - Remove stopwords.
     - Aplica lematização (ex: "motores" → "motor", "perdeu" → "perder").
     - Remove pontuação e caracteres especiais.
     - Retorna lista de lemas em minúsculas.
   - `jaccard(set_a: set, set_b: set) -> float` que calcula `|A ∩ B| / |A ∪ B|`,
     retornando `0.0` se a união for vazia.
3. Testar manualmente com **pelo menos 5 exemplos do dataset** (`dados/dataset.json`),
   mostrando entrada e saída esperada num **bloco de comentário no final do arquivo**
   (não usar pytest nesta issue — é assim que o critério de aceite foi definido pelo
   grupo).

### Critério de aceite (copiado fielmente da Issue)

- Módulo importável pelos outros módulos sem erro.
- `preprocessar` retorna lemas corretos.
- `jaccard` retorna valor entre 0 e 1.

### Restrições explícitas para esta issue

- **Única biblioteca externa permitida:** `spacy` (já listada em `requirements.txt`),
  e apenas dentro de `preprocessamento.py`, apenas para o pipeline de PLN.
- **Não tocar em grafo, BFS ou classificador** — isso é trabalho de outras issues.
- **Não usar bibliotecas de similaridade prontas** para `jaccard()` — implementação
  manual com operações de conjunto.
- **Não inventar dados de teste:** os "pelo menos 5 exemplos" do passo 3 devem vir
  literalmente de `dados/dataset.json` (campo `texto`), não de frases criadas
  artificialmente para a demonstração.
- **Não alterar outros arquivos** do repositório (README, requirements.txt, dataset)
  a menos que seja estritamente necessário e eu autorize explicitamente.

---

## 5. Boas Práticas a Seguir (na medida em que se aplicam ao escopo da issue)

Aplicar com bom senso — **não adicionar complexidade que a issue não pede**. Para um
módulo único como `preprocessamento.py`, isso significa principalmente:

- **Código limpo:** nomes descritivos, funções pequenas e com responsabilidade única,
  type hints (`texto: str`, `-> list[str]`), docstrings curtas explicando contrato de
  cada função (entrada, saída, comportamento de borda como união vazia).
- **Tratamento de borda:** strings vazias, texto só com pontuação, `set()` vazio em
  ambos os lados do Jaccard.
- **Sem efeitos colaterais escondidos:** o carregamento do modelo spaCy (`spacy.load`)
  deve ocorrer uma única vez no nível do módulo (não dentro da função `preprocessar`,
  para não recarregar o modelo a cada chamada — isso é custoso e seria um problema de
  performance real, não só estilo).
- **Compatibilidade com Git/GitFlow:** ao final da issue, sugerir mensagem de commit
  no padrão Conventional Commits (ex.: `feat(preprocessamento): implementa pipeline
  spaCy e similaridade de Jaccard (Issue #1)`), mas a decisão de commitar/dar push é
  sempre minha.
- **Documentação mínima:** o bloco de comentário final com os 5 exemplos manuais
  também serve como documentação viva do comportamento esperado da função.

---

## 6. Forma de Trabalho — Regras de Interação (válidas para toda a sessão)

1. **Passo a passo.** Não pular etapas nem implementar tudo de uma vez. Ordem sugerida
   para esta issue:
   1. Verificar ambiente (venv, spaCy, modelo pt).
   2. Implementar `preprocessar()`.
   3. Testar `preprocessar()` isoladamente com 1-2 frases antes de seguir.
   4. Implementar `jaccard()`.
   5. Testar `jaccard()` isoladamente com casos simples (conjuntos iguais, disjuntos,
      união vazia).
   6. Selecionar 5+ exemplos reais de `dados/dataset.json` e montar o bloco de
      comentário final com entrada/saída esperada.
   7. Revisar contra o critério de aceite antes de considerar a issue concluída.
2. **Explicar antes de agir.** Antes de cada bloco de código ou comando, explicar:
   - O que vai ser feito.
   - Por que essa é a abordagem (qual conceito de PLN/estrutura de dados está em jogo).
   - Que parte da Issue ou do edital isso atende.
3. **Nunca inventar.** Se uma informação não estiver nos arquivos do repositório nem
   tiver sido confirmada por mim, perguntar antes de assumir. Isso inclui: nomes de
   variáveis em outros módulos que ainda não existem, formato de dados não documentado,
   ou requisitos que pareçam razoáveis mas não estão escritos em nenhum lugar.
4. **Escopo restrito.** Resolver apenas a Issue 1. Não adiantar implementação de
   `grafo.py`, `bfs.py`, `construcao.py`, `classificador.py` ou `main.py` nesta sessão,
   mesmo que pareça natural ou eficiente fazer isso agora.
