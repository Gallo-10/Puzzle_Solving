import itertools
import networkx as nx
from tqdm import tqdm


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

                barra_de_carregamento.update(1)

    return False




print("Início do grafo! ")
# Gerar o grafo
grafo = puzzle_grafo()
print("Término do grafo! ")


# Convertendo o grafo para um dicionário de listas
grafo_dict = grafo_to_dict(grafo)

# Escolher dois vértices aleatoriamente como origem e objetivo
origem = (8, 5, 4, 2, 7, 1, 3, 6, 0)
objetivo = (1,2,3,4,5,6,7,8,0)

# Executar busca em extensão
print("Início da busca!")
barra_de_carregamento = tqdm(total=len(grafo_dict), ncols=80, desc="Buscando", bar_format='{l_bar}{bar}| {n:.0f}/{total_fmt} {postfix}')

if busca_em_extensao(grafo_dict, origem, objetivo) == False:
    print("Caminho não encontrado!")
else:
    print("Caminho: ", busca_em_extensao(grafo_dict, origem, objetivo))
    barra_de_carregamento.close()
#Printa data e hora de término
print("Término da busca! ")
