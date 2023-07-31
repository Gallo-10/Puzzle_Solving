import itertools
import networkx as nx
import random


def puzzle_grafo():
    # Gerar todas as permutações possíveis dos números de 0 a 8 sem repetição
    permutacoes = list(itertools.permutations(list(range(9))))

    # Criar um grafo usando networkx
    grafo = nx.MultiGraph()

    # Adicionar os vértices (permutações) ao grafo
    for perm in permutacoes:
        grafo.add_node(perm)

    # Adicionar as arestas entre vértices que representam movimentos válidos
    for perm in permutacoes:
        a, b, c, d, e, f, g, h, i = perm

        # movimentos de A
        if b == 0:
            grafo.add_edge(perm, (b, a, c, d, e, f, g, h, i))
        if d == 0:
            grafo.add_edge(perm, (d, b, c, a, e, f, g, h, i))

        # movimentos de B
        if a == 0:
            grafo.add_edge(perm, (b, a, c, d, e, f, g, h, i))
        if c == 0:
            grafo.add_edge(perm, (a, c, b, d, e, f, g, h, i))
        if e == 0:
            grafo.add_edge(perm, (a, e, c, d, b, f, g, h, i))

        # movimentos de C
        if b == 0:
            grafo.add_edge(perm, (a, c, b, d, e, f, g, h, i))
        if f == 0:
            grafo.add_edge(perm, (a, b, f, d, e, c, g, h, i))

        # movimentos de D
        if a == 0:
            grafo.add_edge(perm, (d, b, c, a, e, f, g, h, i))
        if e == 0:
            grafo.add_edge(perm, (a, b, c, e, d, f, g, h, i))
        if g == 0:
            grafo.add_edge(perm, (a, b, c, g, e, f, d, h, i))

        # movimentos de E
        if b == 0:
            grafo.add_edge(perm, (a, e, c, d, b, f, g, h, i))
        if d == 0:
            grafo.add_edge(perm, (a, b, c, e, d, f, g, h, i))
        if f == 0:
            grafo.add_edge(perm, (a, b, c, d, f, e, g, h, i))
        if h == 0:
            grafo.add_edge(perm, (a, b, c, d, h, f, g, e, i))

        # movimentos de F
        if c == 0:
            grafo.add_edge(perm, (a, b, f, d, e, c, g, h, i))
        if e == 0:
            grafo.add_edge(perm, (a, b, c, d, f, e, g, h, i))
        if i == 0:
            grafo.add_edge(perm, (a, b, c, d, e, i, g, h, f))

        # movimentos de G
        if d == 0:
            grafo.add_edge(perm, (a, b, c, g, e, f, d, h, i))
        if h == 0:
            grafo.add_edge(perm, (a, b, c, d, e, f, h, g, i))

        # movimentos de H
        if e == 0:
            grafo.add_edge(perm, (a, b, c, d, h, f, g, e, i))
        if g == 0:
            grafo.add_edge(perm, (a, b, c, d, e, f, h, g, i))
        if i == 0:
            grafo.add_edge(perm, (a, b, c, d, e, f, g, i, h))

        # movimentos de I
        if f == 0:
            grafo.add_edge(perm, (a, b, c, d, e, i, g, h, f))
        if h == 0:
            grafo.add_edge(perm, (a, b, c, d, e, f, g, i, h))

    return grafo


def contraction(grafo, vertice1, vertice2):
    # Unir vertice2 em vertice1 (realizar a contração)
    for vizinho in grafo[vertice2]:
        if vizinho != vertice1:
            grafo.add_edge(vertice1, vizinho)

    # Remover vertice2 do grafo
    grafo.remove_node(vertice2)


def random_contraction(grafo):
    # Fazer uma cópia do grafo para evitar modificar o original
    grafo_copia = grafo.copy()

    # Realizar a contração na cópia até restarem apenas 2 vértices
    while len(grafo_copia) > (len(grafo)/2):
        vertice1 = random.choice(list(grafo_copia.nodes()))
        vizinhos_vertice1 = list(grafo_copia[vertice1])
        while len(vizinhos_vertice1) == 0:
            vertice1 = random.choice(list(grafo_copia.nodes()))
            vizinhos_vertice1 = list(grafo_copia[vertice1])
        vertice2 = random.choice(vizinhos_vertice1)
        contraction(grafo_copia, vertice1, vertice2)

    return grafo_copia


def grafo_to_dict(grafo):
    grafo_dict = {}
    for node in grafo.nodes():
        vizinhos = list(grafo[node])
        grafo_dict[node] = vizinhos
    return grafo_dict


def busca_em_extensao(grafo, inicio, objetivo):
    # Define a fila de busca
    fila = [inicio]

    # Define os nós visitados
    visitados = [inicio]

    # Define o caminho a percorrer
    parentes = {}

    # Enquanto a fila não estiver vazia
    while fila:
        no = fila.pop(0)

        if no == objetivo:
            caminho = [objetivo]

            while objetivo != inicio:
                caminho.insert(0, parentes[objetivo])
                objetivo = parentes[objetivo]
            return caminho

        # Para cada vizinho do nó
        for vizinho in grafo[no]:
            if vizinho not in visitados:
                # Adiciona o nó como visitado
                visitados.append(vizinho)

                # Adiciona na fila
                fila.append(vizinho)

                # Adiciona o pai do vizinho sendo o nó
                parentes[vizinho] = no

    return False

print("Início do grafo: ")
# Gerar o grafo
grafo = puzzle_grafo()
print("Término do grafo: ")

print("Inicio da contração do grafo: ")
# Executar a contração
resultado = random_contraction(grafo)

# Convertendo o grafo para um dicionário de listas
grafo_dict = grafo_to_dict(resultado)

# Escolher dois vértices aleatoriamente como origem e objetivo
origem = (8, 5, 4, 2, 7, 1, 3, 6, 0)
objetivo = (1,2,3,4,5,6,7,8,0)

# Executar busca em extensão
print("Início da busca: ",)
if busca_em_extensao(grafo_dict, origem, objetivo) == False:
    print("Caminho não encontrado!")
else:
    print("Caminho: ", busca_em_extensao(grafo_dict, origem, objetivo))
#Printa data e hora de término
print("Término da busca: ", )
