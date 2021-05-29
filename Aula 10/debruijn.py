# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class DeBruijnGraph (MyGraph):
    
    def __init__(self, frags):
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o, d):
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        self.graph[o].append(d)

    def in_degree(self, v):
        res = 0
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res += self.graph[k].count(v)
        return res

    def create_deBruijn_graph(self, frags):
        for seq in frags:
            suf = suffix(seq)
            self.add_vertex(suf)
            pref = prefix(seq)
            self.add_vertex(pref)
            self.add_edge(pref, suf)

    def seq_from_path(self, path):#extrair a seqeuncia do caminho
        seq = path[0]
        for i in range(1,len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq 
    
def suffix (seq):#retorna o sufixo do fragmento da seq
    #EXEMPLO: TAC -> Sufixo = AC
    return seq[1:]# de um ate ao fim T=0, A=1 e C=2
    
def prefix(seq):# retorna o prefixo do fragmento da seq
    #EXEMPLO: TAC -> Prefixo = TA
    return seq[:-1]# todos menos o ultimo, T=0, A=1 e C=2

def composition(k, seq):
    res = []#abrir lista para guardar fragmentos
    for i in range(len(seq)-k+1):#percorrer a sequencia ??
        # seq = CAATCATGATG -> en(seq)-k+1 -> 'CAATCATGA' - 'TG' -> -k +1 porque fazemos menos o tamanho do segmento que queremos e temos de fazer +1 para incluir a ultima sequencia
        res.append(seq[i:i+k])
        #[i:i+k] -> [0:0+3] nao inclui o 3 entao fica de 0 a 2, ficando 3 elementos da seq
    res.sort()#pôr por ordem
    return res#retornar lista



def test1():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    
    
def test2():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    print (dbgr.check_nearly_balanced_graph())
    print (dbgr.eulerian_path())


def test3():
    orig_sequence = "ATGCAATGGTCTG"
    frags = composition(3, orig_sequence)
    # ... completar



test1()
print()
#test2()
#print()
#test3()
    
