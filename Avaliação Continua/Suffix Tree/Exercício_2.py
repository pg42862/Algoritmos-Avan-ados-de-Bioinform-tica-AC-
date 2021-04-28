# -*- coding: utf-8 -*-

class SuffixTree:

    def __init__(self):
        self.nodes = {0: (-1, {})} 
        self.num = 0
        self.seq1 = ''
        self.seq2 = ''

    def unpack(self, k): #unpack do tupulo -> basicamente tira os parenteses do tuplo
        if self.nodes[k][0] == -1:
            z = self.nodes[k][0]
            y = ''
        else:
            z, y = self.nodes[k][0]
        return z, y


    def print_tree(self):
        for k in self.nodes.keys():
            z, y = self.unpack(k) 

            if z < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", z, y)

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1 
        self.nodes[origin][1][
            symbol] = self.num  
        self.nodes[self.num] = (leafnum, {}) 

    def add_suffix(self, p, sufnum): 
        pos = 0
        node = 0
        while pos < len(p): 
            if p[pos] not in self.nodes[node][1].keys(): 
                if pos == len(p) - 1:  
                    self.add_node(node, p[pos], sufnum)  
                else:
                    self.add_node(node, p[pos])  
            node = self.nodes[node][1][p[pos]] 
            pos += 1  

    def suffix_tree_from_seq(self, seq1, seq2):
        seq1 = seq1 + "$"
        seq2 = seq2 + "#"
        self.seq1 = seq1 
        self.seq2 = seq2
        for i in range(len(seq1)): 
            self.add_suffix(seq1[i:], (0, i)) 
        for i in range(len(seq2)):  
            self.add_suffix(seq2[i:], (1, i))


    def find_pattern(self, pattern):
        node = 0
        for pos in range(len(pattern)):  
            if pattern[pos] in self.nodes[node][1].keys(): 
                node = self.nodes[node][1][
                    pattern[pos]]  
            else:
                return None
        return self.get_leafes_below(node)  

    def get_leafes_below(self, node):
        f_0 = []
        f_1 = []  
        z, y = self.unpack(node)
        if z >= 0:  
            if z == 0:
                f_0.append(y)
            else:
                f_1.append(y)
        else:  
            for k in self.nodes[node][1].keys(): 
                newnode = self.nodes[node][1][k]  
                p, s = self.get_leafes_below(newnode) 
                f_0.extend(p)
                f_1.extend(s) 
        return(f_0, f_1)

    def largestCommonSubstring(self): #corre duas sequencias-> match maior nas duas sequencias
        f_match = ''
        f_cont = 0
        for i in range(len(self.seq1)):
            cont = 0
            match = ''
            for t in self.seq2:
                if self.seq1[i] == t:
                    match+=self.seq1[i]
                    cont+=1
                    i+=1
                else:
                    if cont > f_cont:
                        f_match = match
                        f_cont = cont
                    match = ''
                    cont = 0
        print(f_match)


def test():
    seq1 = "TACTA"
    seq2 = "TAAGGTACTAC"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print(st.find_pattern("TA"))
    print(st.find_pattern("ACG"))


def test2():
    seq1 = "TTTACAVSGHHHSJAKKKKKK"
    seq2 = "TAAGADGGFGGGGGGGGGHLDHOFOIGJKCTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    print(st.find_pattern("TA"))
    st.largestCommonSubstring()


#test()
print()
test2()
