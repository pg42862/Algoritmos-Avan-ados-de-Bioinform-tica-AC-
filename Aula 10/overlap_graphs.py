# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class OverlapGraph(MyGraph):
    
    def __init__(self, frags):
        MyGraph.__init__(self, {})
        self.create_overlap_graph(frags)

    def __init__(self, frags, reps = True):
        MyGraph.__init__(self, {})
        if reps: 
            self.create_overlap_graph_with_reps(frags)
        else: 
            self.create_overlap_graph(frags)
        self.reps = reps
        
    
    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags):
        ## add vertices
        for seq in frags:
            self.add_vertex(seq)
        ## add edges
        for seq in frags:#ir buscar um fragmento para comparar com os outros todos e assim sucessivamente
            suf = suffix(seq)#ver o sufixo do fragmento
            for seq2 in frags:#ir buscar outro fragmento
                pref = prefix(seq2)#ver o seu prefixo
                if suf == pref:#se o sufixo do primeiro for igual ao prefixo do segundo
                    self.add_edge(seq,seq2)#adicio um vertice -> seq:seq2 (EXEMPLO: TAC:ACG)
        
    def create_overlap_graph_with_reps(self, frags):  # caso de replicas de fragmentos
        ## add vertices
        idnum = 1 #contagem de frags
        for seq in frags:
            self.add_vertex(seq + '-' + str(idnum))
            idnum = idnum + 1
        ## add edges
        idnum = 1#contagem de frags
        for seq in frags:#ir buscar um fragmento para comparar com os outros todos e assim sucessivamente
            suf = suffix(seq)#ver o sufixo do fragmento
            for seq2 in frags:#ir buscar outro fragmento
                pref=prefix(seq2)#ver o seu prefixo
                if suf == pref:#se o sufixo do primeiro for igual ao prefixo do segundo
                    for x in self.get_instances(seq2):
                        self.add_edge(seq + '-' + str(idnum), x)
            idnum = idnum + 1

        #NOTA ADD VERTEX FUNCTION:
            #def add_vertex(self, v):
            #''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
            #if v not in self.graph.keys():
                #self.graph[v] = []
    
    def get_instances(self, seq):
        res = []#lista com repeticoes de fragmentos
        for k in self.graph.keys():#ver as keys do grafo, ou seja, fragmentos
            if seq in k:#se a seq(fragmento) for igual ao fragmento
                res.append(k)#adicionar a lista
        return res

        #EXEMPLO:
            #res = {'TAA':'AAC'}
            #seq = 'TAA'
            #res2 = []
            #for k in res.keys():
                #if seq in k:
                    #res2.append(k)
            #res2 = ['TAA']
    
    def get_seq(self, node):
        if node not in self.graph.keys(): #se o no n estiver nas keys
            return None#nao existe seq
        if self.reps: #sel.reps = reps, reps = True ou False
            return node.split("-")[0]#separar pelo '-' e ficar com o [0] -> TAC-1, ou seja, ficamos com TAC
        else:#se reps = False
            return node #retornar o no
    
    def seq_from_path(self, path):
        '''Função para dar a sequência reconstruída dado um caminho no grafo '''
        if not self.check_if_hamiltonian_path(path):
            return None
        seq= self.get_seq(path[0])#vai ser a sequencia toda
            #vai buscar o fragmento sem a contagem -> TAC-1, vai buscar TAC
        for i in range(1,len(path)):#vai percorrer a partir do segundo fragmento porque o primeiro ja esta na seq
            nxt = self.get_seq(path[i])#vai buscar so o fragmento sem contagem
            seq += nxt[-1]#adiciona o ultimo elemento do fragmento -> TAC, adiciona C
        return seq#retornar a sequencia completa
   
                    
# auxiliary
def composition(k, seq):
    res = []#abrir lista para guardar fragmentos
    for i in range(len(seq)-k+1):#percorrer a sequencia ??
        # seq = CAATCATGATG -> en(seq)-k+1 -> 'CAATCATGA' - 'TG' -> -k +1 porque fazemos menos o tamanho do segmento que queremos e temos de fazer +1 para incluir a ultima sequencia
        res.append(seq[i:i+k])
        #[i:i+k] -> [0:0+3] nao inclui o 3 entao fica de 0 a 2, ficando 3 elementos da seq
    res.sort()#pôr por ordem
    return res#retornar lista
    
def suffix (seq):#retorna o sufixo do fragmento da seq
    #EXEMPLO: TAC -> Sufixo = AC
    return seq[1:]# de um ate ao fim T=0, A=1 e C=2
    
def prefix(seq):# retorna o prefixo do fragmento da seq
    #EXEMPLO: TAC -> Prefixo = TA
    return seq[:-1]# todos menos o ultimo, T=0, A=1 e C=2

  
# testing / mains
def test1():
    seq = "CAATCATGATG"
    k = 3
    print (composition(k, seq))
   
def test2():
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags,False)#False
    ovgr.print_graph()

def test3():
     frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
     ovgr = OverlapGraph(frags,True)#True
     ovgr.print_graph()

def test4():
    frags = ["ATA",  "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA" , "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    path = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3']
    print (ovgr.check_if_valid_path(path))
    print (ovgr.check_if_hamiltonian_path(path))
    path2 = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3', 'TGG−13', 'GGC−10', 'GCA−9', 'CAT−6', 'ATT−4', 'TTT−15', 'TTC−14', 'TCA−12', 'CAT−7', 'ATA−1', 'TAA−11']
    print (ovgr.check_if_valid_path(path2))
    print (ovgr.check_if_hamiltonian_path(path2))
    print (ovgr.seq_from_path(path2))

def test5():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)

    path = ovgr.search_hamiltonian_path()
    print(path)
    print (ovgr.check_if_hamiltonian_path(path))
    print (ovgr.seq_from_path(path))

def test6():
    orig_sequence = "CAATCATGATGATGATC"
    frags = composition(3, orig_sequence)
    print (frags)
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    print (path)
    print (ovgr.seq_from_path(path))
   
#test1()
print()
#test2()
print()
#test3()
#print()
#test4()
#print()
#test5()
#print()
test6()
