class Graph:
    def __init__(self, name_file, chromatic_number):
        self.nro_vertices = 0
        self.nro_arestas = 0
        self.matriz = []
        self.open_graph(name_file)
        self.nro_colors = chromatic_number
                
    def open_graph(self, name_file):
        arquivo = open(name_file, 'r')
        linha1 = arquivo.readline()
        (p, edge, self.nro_vertices, self.nro_arestas) = linha1.strip().split(' ')
        self.nro_vertices = int(self.nro_vertices)
        self.matriz = [ [ 0 for __ in range(int(self.nro_vertices))] for __ in range(int(self.nro_vertices))]

        for line in arquivo:
            edge, v1,v2 = line.strip().split(' ')
            self.matriz[int(v1)-1][int(v2)-1] = 1
            self.matriz[int(v2)-1][int(v1)-1] = 1

        # print("Matriz de aresta: ", self.matriz)
        print("Número de vértices: ", self.nro_vertices)
        print("Número de arestas: ", self.nro_arestas)
        arquivo.close()
        
    def existsEdge(self, v1, v2):
        if self.matriz[v1][v2] == 1 or self.matriz[v2][v1] == 1:
            return True
        return False    

    def get_total_colors(self, particle):
        return len(list(set(particle)))

    def conflict_edges(self, particle):
        result = []
        for index1, color1 in enumerate(particle):
            for index2, color2 in enumerate(particle):
                if self.existsEdge(index1, index2) and color1 == color2 and index1 != index2:
                    if ((index1, index2) not in result) and ((index2,index1) not in result):
                        result.append((index1,index2))

        return result
