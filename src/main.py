import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from construcao import construir_grafo, analisar_grafo
from classificador import classificar


def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def linha():
    print("=" * 60)


def mostrar_cabecalho():
    linha()
    print("CENTRAL DE ANÁLISE DE FALHAS EM DRONES".center(60))
    linha()


def mostrar_menu():
    print("\nComandos disponíveis:")
    print("[1] Classificar relato")
    print("[2] Avaliar sistema")
    print("[3] Ver estatísticas do grafo")
    print("[4] Como funciona")
    print("[0] Sair")


def explicar_sistema():
    linha()
    print("COMO O SISTEMA FUNCIONA".center(60))
    linha()
    print("1. O relato é processado com spaCy.")
    print("2. Stopwords e pontuações são removidas.")
    print("3. As palavras são transformadas em lemas.")
    print("4. A similaridade é calculada com Jaccard.")
    print("5. O grafo é percorrido para encontrar relatos relacionados.")
    print("6. A categoria com maior score é escolhida.")


def mostrar_estatisticas(stats):
    linha()
    print("ESTATÍSTICAS DO GRAFO".center(60))
    linha()
    print(f"Vértices: {stats['vertices']}")
    print(f"Arestas: {stats['arestas']}")
    print(f"Densidade: {stats['densidade']:.6f}")
    print(f"Grau médio: {stats['grau_medio']:.2f}")
    print(f"Grau máximo: {stats['grau_max']}")
    print(f"Vértices mais conectados: {stats['vertices_mais_conectados']}")


def avaliar(test_cases, grafo, profundidade=2):
    total = len(test_cases)
    acertos = 0
    por_categoria = {}
    erros = []

    for caso in test_cases:
        texto = caso["texto"]
        esperado = caso["categoria"]
        predito = classificar(texto, grafo, profundidade)

        if esperado not in por_categoria:
            por_categoria[esperado] = {"total": 0, "acertos": 0}

        por_categoria[esperado]["total"] += 1

        if predito == esperado:
            acertos += 1
            por_categoria[esperado]["acertos"] += 1
        else:
            erros.append((texto, esperado, predito))

    acuracia = (acertos / total) * 100

    print(f"\nAcurácia geral: {acuracia:.2f}%")
    print(f"Acertos: {acertos}/{total}")

    print("\nAcurácia por categoria:")
    for categoria, dados in por_categoria.items():
        acc = (dados["acertos"] / dados["total"]) * 100
        print(f"- {categoria}: {acc:.2f}% ({dados['acertos']}/{dados['total']})")

    print("\nErros:")
    if not erros:
        print("Nenhum erro encontrado.")
    else:
        for texto, esperado, predito in erros:
            print(f"- Esperado: {esperado} | Predito: {predito} | Texto: {texto}")

    return acuracia


def main():
    raiz = os.path.dirname(os.path.dirname(__file__))

    caminho_dataset = os.path.join(raiz, "dados", "dataset.json")
    caminho_testes = os.path.join(raiz, "dados", "test_cases.json")

    mostrar_cabecalho()

    print("Carregando dataset...")
    dataset = carregar_json(caminho_dataset)

    print("Construindo grafo...")
    grafo = construir_grafo(dataset)

    stats = analisar_grafo(grafo)

    print("\nSistema pronto.")
    print(f"Relatos carregados: {stats['vertices']}")
    print(f"Arestas criadas: {stats['arestas']}")

    while True:
        mostrar_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando o sistema...")
            break

        elif opcao == "1":
            relato = input("\nDigite o relato da falha: ").strip()

            if not relato:
                print("Relato vazio. Tente novamente.")
                continue

            inicio = time.perf_counter()
            categoria = classificar(relato, grafo, profundidade=2)
            fim = time.perf_counter()

            linha()
            print("RESULTADO DA ANÁLISE".center(60))
            linha()
            print(f"Relato analisado: {relato}")

            if categoria == "":
                print("Categoria: não foi possível classificar.")
            else:
                print(f"Categoria predita: {categoria}")

            print(f"Tempo de análise: {fim - inicio:.4f} segundos")

        elif opcao == "2":
            test_cases = carregar_json(caminho_testes)

            linha()
            print("AVALIAÇÃO DO SISTEMA".center(60))
            linha()

            print("\n--- Nível de análise 1 ---")
            print("(Somente relatos mais parecidos)")
            acc1 = avaliar(test_cases, grafo, profundidade=1)

            print("\n--- Nível de análise 2 ---")
            print("(Relatos mais parecidos + relatos relacionados)")
            acc2 = avaliar(test_cases, grafo, profundidade=2)

            linha()
            print("COMPARAÇÃO DOS MODOS DE ANÁLISE".center(60))
            linha()

            print("\nNível de análise 1")
            print("(Somente relatos mais parecidos)")
            print(f"Acurácia: {acc1:.2f}%")

            print("\nNível de análise 2")
            print("(Relatos mais parecidos + relatos relacionados)")
            print(f"Acurácia: {acc2:.2f}%")

            print("\nMelhor resultado:")
            if acc2 > acc1:
                print("Nível de análise 2")
            elif acc1 > acc2:
                print("Nível de análise 1")
            else:
                print("Os dois níveis tiveram o mesmo resultado.")

        elif opcao == "3":
            mostrar_estatisticas(stats)

        elif opcao == "4":
            explicar_sistema()

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()