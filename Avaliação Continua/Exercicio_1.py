# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } 
        self.num = 0
        self.seq = "" #guardar sequencia original
    
    def print_tree(self): 
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1):#posicao de origem o simbolo e caso a posicao n seja uma folha e -1
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p, sufnum):
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():
                if pos == len(p)-1:
                    self.add_node(node,p[pos],sufnum)
                else:
                    self.add_node(node,p[pos])
            node = self.nodes[node][1][p[pos]] 
            pos +=1
    
    def suffix_tree_from_seq(self, text):
        self.seq = text 
        t = text+"$"
        for i in range(len(t)):
            self.add_suffix(t[i:],i) 
            
    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
                pos+=1
            else:
                return None
        return self.get_leafes_below(node)
        

    def get_leafes_below(self, node):
        res = []
        if self.nodes[node][0] >=0: 
            res.append(self.nodes[node][0])        
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res
    def nodes_below (self, node):
        """
        Exercicio 1 a)
        
        """
        if node >= len(self.nodes):
            return None
        else:
            nodesID = list(self.nodes[node][1].values())
            for a in nodesID:
                nodesID.extend(list(self.nodes[a][1].values()))
            return nodesID
        
    def match_prefix (self, prefix):
        """
        Exercicio 1 b)
        
        """
        ns = SuffixTree.find_pattern(self, prefix)
        if ns == None or ns == []: 
            return None
        else:
            m =[]
            for i in ns:
                m.append(self.seq[i:])
            m = sorted(m, key = len, reverse = True)
            matchf = []
            for i in m:
                matchf.append(i)
            for i in range(len(m)): 
                mm = len(m[i])
                f = 1
                while mm > len(prefix)  : 
                    matchf.append(m[i][:-f])
                    mm = mm - 1
                    f = f+1
            return (list(dict.fromkeys(matchf)))

def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    #print(st.repeats(2,2))

def test3():
    seq = "TACTAAC"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    print(st.match_prefix("TA"))

#test()
print()
#test2()
test3()
        
            
    
    
