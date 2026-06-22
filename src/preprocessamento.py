"""Módulo de pré-processamento de texto e similaridade textual."""

import spacy

nlp = spacy.load("pt_core_news_sm")


def preprocessar(texto: str) -> list[str]:
    """Transforma texto bruto em lista de lemas filtrados.

    Entrada: string com texto em português.
    Saída: lista de lemas em minúsculas, sem stopwords, pontuação ou caracteres especiais.
    Caso de borda: string vazia ou só pontuação retorna lista vazia.
    """
    doc = nlp(texto)
    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]


def jaccard(set_a: set[str], set_b: set[str]) -> float:
    """Calcula a similaridade de Jaccard entre dois conjuntos.

    Entrada: dois conjuntos de strings (ex: lemas).
    Saída: float entre 0.0 e 1.0 — razão |A ∩ B| / |A ∪ B|.
    Caso de borda: retorna 0.0 se a união for vazia.
    """
    uniao = set_a | set_b
    if not uniao:
        return 0.0
    return len(set_a & set_b) / len(uniao)


# ===========================================================================
# Testes manuais com exemplos reais de dados/dataset.json
# ===========================================================================
#
# --- preprocessar() — 6 exemplos (um por categoria) ---
#
# id=0 | Navegação
#   Entrada: "A trajetória calculada pelo sistema de navegação resultou em voo
#             sobre área restrita."
#   Saída:   ['trajetória', 'calcular', 'navegação', 'resultar', 'voo',
#             'restritar']
#
# id=40 | Sensores
#   Entrada: "O giroscópio em eixo de guinada apresentou drift de 5°/min
#             causando rotação lenta não comandada."
#   Saída:   ['giroscópio', 'eixo', 'guinada', 'apresentar', 'drift',
#             'causar', 'rotação', 'lento', 'comandar']
#
# id=80 | Comunicação
#   Entrada: "O receptor RC entrou em modo de failsafe por interferência de
#             curta duração, mas não restaurou controle após."
#   Saída:   ['receptor', 'rc', 'entrar', 'modo', 'failsafe',
#             'interferência', 'curto', 'duração', 'restaurar', 'controle']
#
# id=120 | Propulsão
#   Entrada: "O empuxo assimétrico entre motores do lado esquerdo e direito
#             causou deriva lateral constante."
#   Saída:   ['empuxo', 'assimétrico', 'motor', 'esquerdo', 'direito',
#             'causar', 'deriva', 'lateral', 'constante']
#
# id=160 | Energia
#   Entrada: "A bateria de íon de lítio vazou eletrólito após impacto durante
#             pouso brusco, danificando eletrônica adjacente."
#   Saída:   ['bateria', 'íon', 'lítio', 'vazar', 'eletrólito', 'impacto',
#             'durante', 'pouso', 'brusco', 'danificar', 'eletrônica',
#             'adjacente']
#
# id=200 | Software Embarcado
#   Entrada: "O sistema de controle adaptativo divergiu ao tentar compensar
#             falha de motor sem limite de adaptação."
#   Saída:   ['controle', 'adaptativo', 'divergir', 'compensar', 'falha',
#             'motor', 'limite', 'adaptação']
#
# --- jaccard() ---
#
# jaccard({'motor', 'falhar'}, {'motor', 'falhar'})           → 1.0
# jaccard({'motor', 'falhar'}, {'sensor', 'calibrar'})        → 0.0
# jaccard({'motor', 'falhar'}, {'motor', 'sensor'})           → 0.3333
# jaccard(set(), set())                                       → 0.0
# jaccard(lemas id=0, lemas id=1)                             → 0.0
#   lemas id=0: {'restritar', 'trajetória', 'calcular', 'voo', 'navegação',
#                'resultar'}
#   lemas id=1: {'manobra', 'retornar', 'precisão', 'distância', 'sensor',
#                'pouso', 'solo', 'incorreto', 'durante'}