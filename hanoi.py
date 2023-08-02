import networkx as nx
import itertools

grafo = nx.Graph()


# Essa função recebe como entrada o número de discos n_discos e gera um grafo contendo todas as transições possiveis na torre
def grafo_hanoi(n_discos):
    # Cria grafo vazio usando a bibilioteca networkx
    grafo = nx.DiGraph()

    # gerar todas as permutações com repetição dos números de 1 a 3 para n_discos vezes para representar todas as combinações possíveis de discos nas colunas
    permutations = list(itertools.product(list(range(1, 4)), repeat=n_discos))

    # Percorre todas as permutações geradas anteriormente, representadas pelas variáveis i, j, k, l e m.
    for perm in permutations:
        i, j, k, l, m = perm
        aux = 1  # Usada para representar uma coluna diferente da coluna atual
        while aux < 4:
            # Adiciona uma aresta no grafo para representar uma transição
            # Se o valor de aux for diferente de i, podemos mover um disco da coluna i para a coluna aux.
            if aux != i:
                grafo.add_edge((i, j, k, l, m), (aux, j, k, l, m))
            if aux != j:
                if j != i:
                    grafo.add_edge((i, j, k, l, m), (i, aux, k, l, m))
            if aux != k:
                if k != i and k != j:
                    grafo.add_edge((i, j, k, l, m), (i, j, aux, l, m))
            if aux != l:
                if l != i and l != j and l != k:
                    grafo.add_edge((i, j, k, l, m), (i, j, k, aux, m))
            if aux != m:
                if m != i and m != j and m != k and m != l:
                    grafo.add_edge((i, j, k, l, m), (i, j, k, l, aux))
            aux += 1 #Incrementa aux para mover para a proxima coluna

    return grafo


def busca_em_extensão(grafo, inicio, objetivo):
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


def busca_em_profundidade(grafo, origem, destino, visitado=None, parentes=None):
    if visitado == None:
        visitado = [origem]
    if parentes == None:
        parentes = {}

    for vizinho in grafo[origem]:
        if vizinho not in visitado:
            visitado.append(vizinho)
            parentes[vizinho] = origem
            if vizinho == destino:
                return parentes
            resultado = busca_em_profundidade(grafo, vizinho, destino, visitado, parentes)
            if resultado != False:
                return resultado
    return False


def grafo_to_dict(grafo):
    grafo_dict = {}
    for node in grafo.nodes():
        vizinhos = list(grafo[node])
        grafo_dict[node] = vizinhos
    return grafo_dict


a = grafo_hanoi(5)

dic = grafo_to_dict(a)
origem = (1, 1, 1, 1, 1)
objetivo = (3, 3, 3, 3, 3)

# # Busca em extensão
print("Busca em Extensão: ", busca_em_extensão(dic, origem, objetivo))

# Busca em profundidade

solucao = busca_em_profundidade(dic, origem, objetivo)
if solucao != False:
    caminho = [objetivo]
    while origem != objetivo:
        caminho.insert(0, solucao[objetivo])
        objetivo = solucao[objetivo]
    print("\n\nBusca em Profundidade: ", caminho)
else:
    print("\n\nBusca em Profundidade: Não foi encontrado solução")
