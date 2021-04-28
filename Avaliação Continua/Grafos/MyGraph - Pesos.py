# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g #unico atributo (g = dicionario)   

    def print_graph(self):#imprime o grafo
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():#para cada key no dicionario (vertice)
            print (v, " -> ", self.graph[v])#imprimir a key e o seu valor (vertive a qual se ligou)

    ## get basic info

    def get_nodes(self):#vai buscar os vetices(nos)
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())#devolve uma lista com os vertices
        
    def get_edges(self):#buscar as arestas(pares de vertices, ou seja, uma aresta liga dois vertices)
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():#para cada key v
            for d in self.graph[v]:#para cada value d
                f , p = d #value com destino e custo
                edges.append((v,f))#acrescentar a lista as arestas (vertice v que se ligou ao vertice x)
        return edges #devolver a lista
      
    def size(self):#tamanho do grafo
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())#usa o get_nodes e o get_edges para ter o tamanho do grafo
      
    ## add nodes and edges    
    
    def add_vertex(self, v):#adicionar vertice(no)
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = [ ]#adicionar uma key ao dicitionary
        
    def add_edge(self, o, d, p):#(o,d, p) vertices(o,p) e o peso
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():#confirmar se os vertices o e d nao estao no dicionario
            self.add_vertex(o)#adicionar vertice o
        if d not in self.graph.keys():
            self.add_vertex(d)#adicionar vertice d
        vertice=[]#lista para confirmar se o vertice
        for i in self.graph[o]:#ver todos os values de o
            f,p = i #f = vertice, p = peso
            vertice.append(f)#fazer o append do vertice f, para depois fazer uma verificacao
        if d not in vertice:#confirmar se d esta na lista de vertices(value) de o 
            self.graph[o].append((d,p))#adicionar um tuplo com o value d e o peso

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        vertice=[]#lista de sucessores
        for i in self.graph[v]:#ver todos os values de o
            f,p = i#tuplo com vertice e peso
            vertice.append(f)#adicionar o vertice a lista vertice
        return vertice #retornar lista com os sucessores   # needed to avoid list being overwritten of result of the function is used
             
    def get_predecessors(self, v):
        pre =[]#abrir lista de antecessores
        for i in self.graph.keys():#percorrer as keys do dicionario
            vertice = []#lista de sucessores
            for x in self.graph[i]:#percorrer os values de i
                f , p = x# tuplo com de vertice e peso
                vertice.append(f)#adicionar os vertices a lista vertice
                if v in vertice:#verificar se v se encontra na lista de sucessores de i
                    pre.append(i)#se isto se verificar o i vai ser antecessor de v entao adicionamos a lista
        return pre#retornar a lista com os antecessores                
    
    def get_adjacents(self, v):#da lista de vertices(nos) adjacentes do vertice(no) v ->dois vertices sao adjacentes se um e sucessor do outro
        suc = self.get_successors(v)#buscar os sucessores de v
        pred = self.get_predecessors(v)#buscar os antecessores de v
        res = pred #res e igual a lista de antecessores (podia ser ao contrario)
        for p in suc:#percorrer a lista de sucessores
            if p not in res:#verificar se nao esta na lista
                res.append(p)#adicionar todos os sucessores de v a lista de antecessores se nao estiver na lista
        return res #retornar res
        
    ## degrees    
    
    def out_degree(self, v):#calcula grau de saída do vertice(no) v
        out = self.get_successors(v)#lista de todos os arcos que saiem do vertice v
        return (len(out))
    
    def in_degree(self, v):#calcula grau de entrada do vertice(no) v
        in_degree=self.get_predecessors(v)
        return(len(in_degree))
        
    def degree(self, v):#O grau de um vértice e dado pelo numero de arestas que lhe sao incidentes
        degree = self.get_adjacents(v)#ver os sucessores e os predecessores para dar lsita de arestas
        return (len(degree))#contar as arestas da lista
        
    
    ## BFS and DFS searches (TRAVESSIAS)    
    
    def reachable_bfs(self, v):
        '''Começa pelo nó origem, depois explora todos os seus sucessores, depois os sucessores destes, e assim sucessivamente até todos os nós atingíveis terem sido explorados'''
        l = [v]#comeca pelo no de origem
        res = []#lista de nos visitados
        while len(l) > 0:
            node = l.pop(0)#removes the item at the given index from the list and returns the removed item
            if node != v:
                res.append(node)#se o node for diferente de v adicionar a res
            vertice =[]
            for elem in self.graph[node]:#ver os values de node
                f,p=elem
                vertice.append(f)
            for x in vertice:
                if x not in res and x not in l and x != node:#se esse value nao estiver em res, l e for diferente de node
                    l.append(elem)#adicionar a l os nodulos que ainda nao visitou
        return res
        
    def reachable_dfs(self, v):
        '''Começa pelo nó origem e explora o 1º sucessor, seguido pelo 1º sucessor deste e assim sucessivamente até não haver mais sucessores e ter que se fazer “backtracking”'''
        l = [v]#comeca pelo no de origem
        res = []#lista de nos visitados
        while len(l) > 0:#so percorre uma vez
            node = l.pop(0)#removes the item at the given index from the list and returns the removed item
            if node != v: res.append(node)
            s = 0#contagem
            vertice =[]
            for elem in self.graph[node]:
                f,p=elem
                vertice.append(f)
            for x in vertice:
                if x not in res and x not in l:
                    l.insert(s, x)
                    s += 1
        return res    
    
    def distance(self, s, d):#retorna distancia entre vertices(nos) s e d
        '''Usa queue de nós, juntando valor com a distância (tuplo)'''
        if s == d:
            return 0
        l = [(s,0)]#lista com tuplo onde tem o no e a distancia de origem
        visitado =[s]#vertices visitados para obter o caminho
        while len(l) > 0:
            node, dist = l.pop(0)#removes the item at the given index from the list and returns the removed item
            for elem in self.graph[node]:#percorrer os values do no de origem
                f,p=elem
                if f == d:
                    return dist + p #se o primeiro value for d retornar logo a distancia
                elif f not in visitado: #se o value nao estiver em visitado
                    l.append((f,dist+p))#vamos adicionar a lista l (caminho)
                    visitado.append(f)#adicionar o value (que ja foi visitado)

        return None #retorna None se nao e atingivel
        
    def shortest_path(self, s, d): #retorna caminho mais curto entre s e d (lista de nos por onde passa)
        '''Retorna caminho mais curto entre s e d (lista de nós por onde passa)'''
        if s == d:
            return [s,d]
        else:
            l = [(s,[],0)]#lista de nos por onde passa que comeca na de origem
            visitado = [s]#vertices visitados
            while len(l) > 0:#so percorre uma vez
                node, path, sp = l.pop(0)#removes the item at the given index from the list and returns the removed item
                bp = 999999#maior peso
                for elem in self.graph[node]:#percorrer os values do no de origem
                    f,p=elem
                    if f == d:
                        return (path+[node,f],sp + p)#se o primeiro for logo d retorna o caminho mais curto
                    if p < bp:#vai percorrer o caminho mais curto de todas as opcoes
                        bp = p
                        next_no = f
                if next_no not in visitado:#o no do caminho mais curto e adicionado a lista mais o respetivo p
                    l.append((next_no,[next_no, node],sp + bp))
                    visitado.append(next_no)
            
            return None #retorna None se nao e atingivel o caminho mais curto
        
    def reachable_with_dist(self, s):
        '''Retorna lista de nós atingíveis a partir de s com respetiva distância(lista de pares nó, distância)'''
        res = []
        l = [(s,0)]
        while len(l) > 0:#so percorre uma vez
            node, sp = l.pop(0)#removes the item at the given index from the list and returns the removed item
            if node != s:#se vertice diferente de s ??
                res.append((node,sp))#se o vertice for diferente de s adicionar a res o vertice e a distancia
            for elem in self.graph[node]:#percorrer todos os values da key node
                f,p = elem
                if not is_in_tuple_list(l,f) and not is_in_tuple_list(res,f): #??
                    l.append((f,sp + p))#adicionar o value(vertice) e a distancia
        return res

## cycles
    def node_has_cycle (self, v):
        l = [v]
        res = False
        visitado = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                f,p = elem
                if f == v:
                    return True
                elif f not in visitado:
                    l.append(f)
                    visitado.append(f)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v):
                return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})  # criar o grafo
    gr.print_graph()
    print(gr.get_nodes())
    print(gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)

    gr2.add_edge(1, 2, 2)
    gr2.add_edge(2, 3, 4)
    gr2.add_edge(3, 2, 3)
    gr2.add_edge(3, 4, 2)
    gr2.add_edge(4, 2, 5)

    gr2.print_graph()
  
def test3():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    gr.print_graph()
    print()
    print('Sucessores:',gr.get_successors(2))
    print()
    print('Antecessor:',gr.get_predecessors(2))
    print()
    print('Adjacents:',gr.get_adjacents(2))
    print()
    print('In Degree:',gr.in_degree(2))
    print()
    print('Out Degree:',gr.out_degree(2))
    print()
    print('Degree:',gr.degree(2))

def test4():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print('Distancia:',gr.distance(1, 4))
    print('Distancia:',gr.distance(4, 3))

    print('Caminho mais curto:',gr.shortest_path(1, 4))
    print('Caminho mais curto:',gr.shortest_path(4, 3))

    print('Lista de nós atingíveis a partir de v com respetiva distância:',gr.reachable_with_dist(1))
    print('Lista de nós atingíveis a partir de v com respetiva distância:',gr.reachable_with_dist(3))

    gr2 = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print('Distancia:',gr2.distance(2, 1))
    print('Distancia:',gr2.distance(1, 5))

    print('Caminho mais curto:',gr2.shortest_path(1, 5))
    print('Caminho mais curto:',gr2.shortest_path(2, 1))

    print('Lista de nós atingíveis a partir de v com respetiva distância:',gr2.reachable_with_dist(1))
    print('Lista de nós atingíveis a partir de v com respetiva distância:',gr2.reachable_with_dist(4))

def test5():
    gr = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})

    print(gr.node_has_cycle(2))
    print(gr.node_has_cycle(1))
    print(gr.has_cycle())

    gr2 = MyGraph({1: [(2,2)], 2: [(3,4)], 3: [(2,3), (4,2)], 4: [(2,5)]})
    print(gr2.node_has_cycle(1))
    print(gr2.has_cycle())


if __name__ == "__main__":
    #test1()
    test2()
    #test3()
    #test4()
    #test5()
