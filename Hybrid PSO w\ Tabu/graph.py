import networkx as nx

class Graph:
    def __init__(self, name_file):
        self.nodes_items = []
        self.edges = []        
        self.open_graph(name_file)
        self.nodes = len(self.nodes_items)
        self.qtd_colors = self.nodes
        

    def open_graph(self, name_file):
        _file = open(name_file, 'r')
        for index, line in enumerate(_file):
            if index == 0:
                self.nodes_items = line.strip().split(' ')
                self.nodes_items = [int(i) for i in self.nodes_items]
            else:
                edge = line.strip().split(' ')
                self.edges.append((int(edge[0]), int(edge[1])))

        _file.close()

        
    def existsEdge(self, v1, v2):
        if ((v1, v2) in self.edges) or ((v2, v1) in self.edges):
            return True
        
        return False    



    def get_total_colors(self, particle):
        lista = list(set(particle))               

        return len(lista)


    def eval_fitness(self, particle):
        evaluation = 0
        for i, cor1 in enumerate(particle):
            for j, cor2 in enumerate(particle):
                if (self.existsEdge(i,j)) and cor1 == cor2 and i!=j:
                    evaluation += 1
        return evaluation


    def conflict_edges(self, particle):
        result = []
        for i in range(len(particle)):
            for j in range(len(particle)):
                if particle[i] == particle[j] and self.existsEdge(i,j):
                    if (i,j) not in result and (j,i) not in result:
                        result.append((i,j))

        return result


    def transform_to_nx_graph(self):
        grafo = nx.Graph()
        n = len(self.nodes_items)
        grafo.add_nodes_from([0, n])

        for e in self.edges:
            grafo.add_edge(e[0], e[1])
