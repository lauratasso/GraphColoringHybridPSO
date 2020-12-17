from graph import *
import random, time
import matplotlib.pyplot as plt 


class Hybrid_PSO_TS:
    def __init__(self, graph, iterations):
        self.graph = graph
        self.betterThanAll = []
        self.iterations = iterations
        self.particles = self.get_init_colors()
        self.best_result_pos = []
        self.best_result_qtd = self.graph.qtd_colors
        

    def get_init_colors(self):
        aux = []
        colors = []
        t = []
        for c in range(self.graph.nodes):
            for i in range(self.graph.nodes):
                cor = random.randint(1,self.graph.qtd_colors)
                aux.append(cor)

            t.append(aux)
            aux = []

        colors = t
        return colors


    def get_Allparticles_fitness(self):
        """
        retorna uma lista com o fitness de cada particula
        """
        fitness = []
        for particle in self.particles:
            aux = self.graph.eval_fitness(particle)
            fitness.append(aux)

        return fitness


    def get_velocity(self, particle, gBest):
        velocity = []
        #recupera uma lista com todas as cores
        list_cores = [i+1 for i in range(self.graph.qtd_colors)]

        confiict_edges = self.graph.conflict_edges(self.particles[particle])
        conflictDim = [i for (i,_) in confiict_edges] #qtd de cores conflitantes
        for i in range(len(self.particles[particle])):
            if (self.particles[particle][i] != self.particles[gBest][i]) and i in conflictDim:
                aux = [k for k in list_cores if k != self.particles[particle][i]] #lista de cores menos a atual
                random1 = random.choice(aux) #atualiza a cor do vertice i para random
                velocity.append((i, random1))

        return velocity


    def update_position(self, particle, velocity):
        new_pos = particle
        for i, new_color in velocity:
            new_pos[i] = new_color

        return new_pos

    # def showsParticles(self):

    #     print('Showing particles...\n')
    #     for particle in self.particles:
    #         print('pbest: %s\t|\tqtd_colors pbest: %d\t|\tcurrent solution: %s\t|\tcolor current solution: %d' \
    #             % (str(particle.getPBest()), (particle.getColorPBest()), str(particle.getCurrentSolution()),
    #                 particle.getColorCurrentSolution()))
    #     print('')
    

    def betterResult(self, best):
        result = self.graph.eval_fitness(self.particles[best])

        if result == 0:
            self.best_result_pos  = self.particles[best]
            self.best_result_qtd = self.graph.get_total_colors(self.particles[best])
            return True
        
        return False

    
    def run(self):
        #inicia tabu
        s_init = self.particles[0]
        sb = self.graph.eval_fitness(s_init)
        tabu = []
        aspiration = dict()
        part = 0

        #para  cada iteração
        for t in range(self.iterations):
            #descobre o menor fitness e atualiza o gbest
            fitness = self.get_Allparticles_fitness()
            gBest = fitness.index(min(fitness))
            for i, particle in enumerate(self.particles):
                if i == gBest:
                    continue

                velocity = self.get_velocity(i, gBest)
                
                new_position = self.update_position(particle, velocity)
                f_new_position = self.graph.eval_fitness(new_position)
                f_old_position = self.graph.eval_fitness(particle)


                if  f_new_position < f_old_position: #nova posicao < pBest
                    for v in velocity:
                        if f_new_position < aspiration.setdefault(f_old_position, f_old_position-1) or (v not in tabu):
                            aspiration[f_old_position] = f_new_position - 1 #atualiza funcao de aspiracao
                            particle = new_position
                        else:
                            if v in tabu:
                                continue

                if f_new_position < self.graph.eval_fitness(self.particles[gBest]): #nova pos < gBest
                    gBest = i
                    part = i
              

            tabu.append((part, particle))
            self.particles[part] = particle

            if self.betterResult(gBest):
                self.betterThanAll.append(self.best_result_qtd)

        self.graph.transform_to_nx_graph() #só para efeitos de desenhar o grafo 
        return min(self.betterThanAll)


if __name__ == "__main__":
    g = Graph('grafo.txt')
    it = 1000
    start = time.time()
    result = Hybrid_PSO_TS(g, it)
    print('Numero de iterações: ', it)
    print('Quantidade minima de cores : ', result.run())
    stop = time.time()
    print('Tempo de execução: ', str(stop-start), ' segundos')
    
