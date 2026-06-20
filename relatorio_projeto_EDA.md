**UNIVERSIDADE DE BRASILIA**

Estruturas de Dados e Algoritmos

**Sistema de Classificacao Textual**\
Baseado em Representacoes Relacionais em Grafos

*Aplicacao: Classificacao de Relatos de Falhas em Drones*

|                 |                                        |
|-----------------|----------------------------------------|
| **Disciplina**  | Estruturas de Dados e Algoritmos (EDA) |
| **Professor**   | Glauco                                 |
| **Semestre**    | 2026.1                                 |
| **Integrantes** | A definir pelo grupo                   |
| **Data**        | 10/06/2026                             |

**1. Introducao**

O presente documento descreve o planejamento completo do projeto final da disciplina de Estruturas de Dados e Algoritmos (EDA). O trabalho consiste no desenvolvimento de um sistema de classificacao automatica de relatos de falhas operacionais em drones, utilizando representacoes relacionais em grafos como estrutura central de modelagem e inferencia.

A escolha do dominio de aplicacao decorre da crescente utilizacao de Veiculos Aereos Nao Tripulados (VANTs/drones) em operacoes de inspeção, logistica e pesquisa, onde o registro e a categorizacao precisa de falhas e critica para a seguranca e manutencao dos sistemas.

**1.1 Motivacao**

Atualmente, quando um operador registra uma ocorrencia durante um voo ou teste, esse relato e produzido em linguagem natural e precisa ser manualmente categorizado por um tecnico especializado. Esse processo e lento, sujeito a inconsistencias e nao escala bem para grandes volumes de dados. O sistema proposto automatiza essa classificacao com base na estrutura semantica e estatistica do vocabulario tecnico presente nos relatos.

**1.2 Objetivo Geral**

Desenvolver um sistema que, dado um relato textual descrevendo uma ocorrencia em drone, infira automaticamente sua categoria de falha por meio de algoritmos sobre grafos, sem recorrer a modelos de aprendizado supervisionado tradicionais.

**2. Definicao do Problema**

**2.1 Entrada do Sistema**

A entrada e um texto livre em portugues descrevendo uma ocorrencia de falha em drone. Exemplos:

|  |  |
|----|----|
| **Relato de Falha** | **Categoria Esperada** |
| *O GPS perdeu sinal durante o voo e o drone entrou em modo failsafe.* | **Navegacao** |
| *Falha na comunicacao entre a estacao de solo e o veiculo.* | **Comunicacao** |
| *O motor traseiro apresentou vibracao excessiva.* | **Propulsao** |
| *A bateria descarregou rapidamente e o drone pousou de emergencia.* | **Energia** |
| *O acelerometro retornou valores inconsistentes durante a decolagem.* | **Sensores** |
| *O firmware travou ao processar o plano de voo automatizado.* | **Software Embarcado** |

**2.2 Saida do Sistema**

A saida e a categoria inferida pelo grafo, acompanhada de um score de confianca por categoria, permitindo auditoria do resultado.

**2.3 Categorias de Falha**

|  |  |  |
|:--:|----|----|
| **Categoria** | **Descricao** | **Palavras-chave Tipicas** |
| **Navegacao** | Falhas em GPS, localização e desvios de rota | GPS, sinal, rota, failsafe, posicao, trajetoria |
| **Sensores** | Leituras incorretas de sensores de bordo | acelerometro, giroscopio, barometro, calibracao |
| **Comunicacao** | Perda de link entre drone e estacao solo | link, telemetria, estacao, sinal, RC, latencia |
| **Propulsao** | Falhas em motores, helices e ESCs | motor, vibracao, ESC, rotacao, helice, empuxo |
| **Energia** | Problemas com bateria e consumo eletrico | bateria, tensao, corrente, carga, descarga |
| **Software** | Bugs de firmware e erros de processamento | firmware, travamento, boot, loop, excecao |

**3. Modelagem do Grafo**

**3.1 Tipo de Grafo**

O sistema utiliza um grafo heterogeneo ponderado nao direcionado, com tres tipos distintos de nos e dois tipos de arestas. Essa heterogeneidade e essencial para capturar as diferentes naturezas das relacoes entre documentos, vocabulario e categorias.

**3.2 Nos do Grafo**

|  |  |  |
|----|----|----|
| **Tipo de No** | **Descricao** | **Exemplo** |
| **Documento (D)** | Cada relato de falha no conjunto de dados | *\"O GPS perdeu sinal\...\"* |
| **Termo (T)** | Palavras relevantes apos pre-processamento (stopwords removidas, stemming aplicado) | *\"GPS\", \"sinal\", \"falha\"* |
| **Categoria (C)** | Os 6 rotulos de classificacao --- nos fixos com peso de ancoragem 1.0 | *\"Navegacao\", \"Propulsao\"\...* |

**3.3 Arestas do Grafo**

|  |  |  |
|----|----|----|
| **Tipo de Aresta** | **Nos Conectados** | **Peso / Calculo** |
| **Documento-Termo** | D \<-\> T | TF-IDF do termo no relato. Reflete importancia estatistica do token dentro do documento. |
| **Termo-Categoria** | T \<-\> C | Frequencia de coocorrencia nos dados de treino: quantas vezes o termo aparece em relatos ja rotulados com cada categoria. |
| **Documento-Documento (opcional)** | D \<-\> D | Similaridade cosseno entre vetores TF-IDF dos relatos. Utilizado como refinamento na propagacao. |

**4. Algoritmo de Classificacao**

**4.1 Visao Geral do Fluxo**

Dado um novo relato sem classe, o sistema executa as seguintes etapas:

1.  Pre-processamento textual: tokenizacao, remocao de stopwords e stemming/normalizacao.

2.  Conexao ao grafo: para cada termo extraido, busca-se os nos de Termo ja presentes no grafo.

3.  Propagacao de scores: cada no Termo conectado propaga seu peso para os nos de Categoria atraves das arestas Termo-Categoria.

4.  Agregacao: os scores de cada categoria sao somados, ponderados pelos pesos das arestas.

5.  Decisao: a categoria com maior score agregado e atribuida ao novo documento.

**4.2 Formula de Propagacao**

**score(C) = SUM \[ peso(D, t) \* peso(t, C) \] para todo t em Termos(D)**

Onde peso(D, t) e o TF-IDF do termo t no documento novo, e peso(t, C) e a coocorrencia normalizada do termo com a categoria C nos dados de treino.

**4.3 Exemplo Numerico**

Relato novo: \"A bateria descarregou rapidamente durante o voo e o drone pousou de emergencia.\"

Termos extraidos: bateria, descarregou, voo, drone, pousou, emergencia

|  |  |  |  |  |  |
|:--:|:--:|:--:|:--:|:--:|:--:|
| **Termo** | **Energia** | **Navegacao** | **Propulsao** | **Comunicacao** | **Sensores** |
| **bateria** | 0.90 | 0.10 | 0.20 | 0.00 | 0.00 |
| **voo** | 0.30 | 0.40 | 0.20 | 0.10 | 0.05 |
| **emergencia** | 0.40 | 0.50 | 0.10 | 0.05 | 0.00 |
| **pousou** | 0.20 | 0.60 | 0.10 | 0.00 | 0.00 |
| **TOTAL** | **1.80** | **1.60** | **0.60** | **0.15** | **0.05** |

Resultado: argmax(scores) = Energia (1.80) -\> classe atribuida: ENERGIA.

**5. Estruturas de Dados Utilizadas**

Alem do grafo como estrutura central, o sistema emprega as seguintes estruturas auxiliares:

|  |  |  |
|----|----|----|
| **Estrutura** | **Papel no Sistema** | **Justificativa** |
| **Dicionario / HashMap** | Indice invertido: termo -\> lista de documentos. Base da construcao do grafo. | Acesso O(1) por chave; estrutura natural para mapeamento vocabulario-documentos. |
| **Matriz Esparsa** | Representacao interna das arestas do grafo com seus pesos. | Eficiencia de espaco para grafos com baixa densidade de conexoes. |
| **Fila de Prioridade (Heap)** | Ranqueamento de categorias por score durante a propagacao. | Permite extrair o maximo em O(log n), essencial para escalabilidade. |
| **Vetor TF-IDF** | Representacao numerica de cada documento para calculo de similaridade. | Fundacao matematica para a construcao dos pesos das arestas D-T. |
| **Lista de Adjacencia** | Representacao do grafo em memoria para percurso eficiente. | O(V+E) de espaco, ideal para grafos esparsos como o deste problema. |

**6. Dados de Entrada**

**6.1 Natureza dos Dados**

Os dados de entrada serao sinteticos, gerados pelo proprio grupo, com revisao tecnica para garantir consistencia terminologica com o vocabulario real de operacoes com VANTs. Cada relato simulara uma ocorrencia plausivel durante voo ou teste em campo.

**6.2 Estrutura do Dataset**

- Volume planejado: 60 a 90 relatos rotulados (10 a 15 por categoria), para a fase de treinamento/construcao do grafo.

- Formato: CSV com colunas \[id, relato, categoria\].

- Balanceamento: distribuicao uniforme entre as 6 categorias.

- Idioma: portugues brasileiro, refletindo o contexto de operadores nacionais.

**6.3 Pre-processamento**

- Conversao para minusculas.

- Remocao de stopwords em portugues (artigos, preposicoes, conjuncoes).

- Stemming ou lematizacao para reduzir variacoes morfologicas (ex: \'falhou\', \'falha\', \'falhando\' -\> \'falh\').

- Calculo de TF-IDF por termo para cada documento.

**6.4 Possibilidade de Dados Reais**

Como complemento opcional, o grupo avaliara o uso da base publica FAA Drone Incident Database (traducao ou adaptacao dos relatos) para validar o sistema em dados do mundo real.

**7. Cronograma de Desenvolvimento**

|  |  |  |  |
|----|----|----|----|
| **Fase** | **Atividade** | **Entregavel** | **Responsavel** |
| **Fase 1** | Geracao e rotulagem do dataset sintetico (60-90 relatos) | Arquivo CSV com dataset | Grupo |
| **Fase 2** | Pre-processamento textual: tokenizacao, stopwords, TF-IDF | Modulo de pre-processamento | Grupo |
| **Fase 3** | Construcao do grafo: nos, arestas e pesos | Classe Grafo com lista de adjacencia | Grupo |
| **Fase 4** | Implementacao do algoritmo de propagacao de scores | Funcao classify(relato) -\> categoria | Grupo |
| **Fase 5** | Avaliacao: acuracia, matriz de confusao, analise de erros | Relatorio de metricas | Grupo |
| **Fase 6** | Interface de demonstracao (terminal ou web simples) | Demo funcional | Grupo |
| **Fase 7** | Documentacao final e preparacao da apresentacao | Relatorio final + slides | Grupo |

**8. Respostas as Perguntas do Professor**

Este capitulo sintetiza as respostas diretas as cinco questoes enviadas pelo Prof. Glauco para a reuniao de acompanhamento.

**1) Qual sera a area de aplicacao?**

Engenharia de sistemas autonomos / aviacao nao tripulada (VANTs/drones). Especificamente, analise e gestao de falhas operacionais, uma area onde a categorizacao precisa de ocorrencias e critica para seguranca e manutencao.

**2) Qual problema voce deseja resolver?**

Automatizar a classificacao de relatos de falha em drones escritos em linguagem natural. O processo manual e lento, sujeito a erro e nao escalavel. O sistema infere a categoria usando a estrutura relacional do grafo, sem modelo supervisionado tradicional.

**3) Qual sera o input? Dados reais ou ficticios?**

Input: texto livre em portugues descrevendo uma ocorrencia. Dados: sinteticos gerados pelo grupo (60-90 relatos), com possibilidade de complementacao por dados reais da FAA Drone Incident Database.

**4) Como voce esta pensando na modelagem do grafo?**

Grafo heterogeneo ponderado com 3 tipos de nos (Documento, Termo, Categoria) e arestas ponderadas por TF-IDF (D-T) e coocorrencia normalizada (T-C). A classificacao ocorre por propagacao de scores dos nos de categoria ate o documento novo, via acumulacao ponderada pelos pesos das arestas.

**5) Qual outra estrutura de dados, alem de grafos, voce utilizara?**

Dicionario/HashMap (indice invertido), Matriz Esparsa (arestas do grafo), Fila de Prioridade/Heap (ranqueamento de categorias), Vetor TF-IDF (pesos das arestas D-T) e Lista de Adjacencia (representacao em memoria do grafo).

**9. Consideracoes Finais**

O projeto proposto oferece uma abordagem elegante e alinhada ao enunciado da disciplina: o grafo nao e apenas uma estrutura de armazenamento, mas o proprio mecanismo de inferencia. A escolha do dominio de drones garante relevancia tecnica e viabilidade pratica na geracao dos dados.

A propagacao de scores pelas arestas ponderadas demonstra concretamente conceitos de grafos vistos na disciplina --- como lista de adjacencia, percurso por vizinhanca e analise estrutural --- aplicados a um problema real de processamento de linguagem natural.

O grupo esta preparado para detalhar e ajustar qualquer aspecto do planejamento conforme orientacao do professor na reuniao de acompanhamento.
