from collections import Counter
import random
import math
import numpy as np
import graph

tam = 11

class Hybrid_PSO:
    def __init__(self, graph):
        self.graph = graph
        self.nro_vertices = int(self.graph.nro_vertices)
        self.particles = self.create_particles()
        self.personal_best = self.particles
        self.f_personal_best = self.get_all_particles_fitness()
        self.f_global_best = min(self.f_personal_best)
        self.global_best = self.particles[self.f_personal_best.index(self.f_global_best)]
        print('self.particles', self.particles)

    def create_particles(self):
        particles = []
        for i in range(tam):
            aux = []
            for j in range(self.nro_vertices):
                aux.insert(j, random.randint(0,int(self.graph.nro_colors)-1))
            particles.insert(i, aux)
        return particles
  
    def get_all_particles_fitness(self):
        """
        retorna uma lista com o fitness de cada particula
        """
        all_fitness = []
        for particle in self.particles:
            aux = self.fitness_function(particle)
            all_fitness.append(aux)
        return all_fitness

    def fitness_function(self, particle):
        eval = 0
        for i in range(self.nro_vertices - 1):
            for j in range(i + 1, self.nro_vertices):
                if (self.graph.existsEdge(i, j)) and (particle[i] == particle[j]):
                    eval += 1
        return eval

    def get_velocity(self, particle, particle_index, position_index):  
        q1 = (self.personal_best[particle_index][position_index] - particle[position_index]) * (random.uniform(0, 1)) * 2
        q2 = (self.global_best[position_index] - particle[position_index]) * (random.uniform(0, 1)) * 2

        return int(q1 + q2)

    def update_position(self, particle, velocity, particle_index, position_index):
        posicaoNova = int(particle[position_index] + velocity)
        corNova = posicaoNova % self.graph.nro_colors
  
        # particle[position_index] = corNova
        # kInterations=0
        # while (self.fitness_function(particle) > self.fitness_function(self.particles[particle_index]) and kInterations < 5):
        #   print("kInterations:", kInterations)
        while (corNova == particle[position_index]):
            corNova = int((corNova + random.uniform(0, self.graph.nro_colors)) % self.graph.nro_colors)
        #     particle[position_index] = corNova
        #   kInterations+=1
        
        self.particles[particle_index][position_index] = corNova
        return

    def hill_climbing(self, particula):
      #print("Hill climbing antes:", self.fitness_function(particula))
      fitness_anterior = self.fitness_function(particula)
      for idx, cor_anterior in enumerate(particula):
        fitness_anterior = self.fitness_function(particula)
        lista_cores = list(range(self.graph.nro_colors))
        random.shuffle(lista_cores)
        for cor in lista_cores:
          particula[idx] = cor
          fitness_atual = self.fitness_function(particula)
          if (fitness_atual < fitness_anterior):
            break
        if (fitness_atual >= fitness_anterior):
          particula[idx] = cor_anterior
        else:
          fitness_anterior = fitness_atual
      #print("Hill climbing depois:", self.fitness_function(particula))
      return particula 
    
    def torneio(self):
      particulas_disponiveis = list(range(len(self.particles)-1))
      for _ in range(int(len(particulas_disponiveis)/2)):
        idx1 = random.choice(particulas_disponiveis)
        idx2 = random.choice(particulas_disponiveis)
        fit1 = self.fitness_function(self.particles[idx1])
        fit2 = self.fitness_function(self.particles[idx2])
        nova_particula = [random.randint(0,self.graph.nro_colors-1) for _ in range(self.graph.nro_vertices)]
        if (fit1>fit2):
          self.particles[idx1] = nova_particula
        else: 
          self.particles[idx2] = nova_particula

    def run(self, iterations):
        #inicializa particulas

        self.f_global_best = min(self.f_personal_best)
        self.global_best = self.particles[self.f_personal_best.index(self.f_global_best)]

        auxiterations = 0
        #para cada iteração, sem uma solução válida
        while (auxiterations < iterations) and self.f_global_best != 0:
            self.torneio()
            for index, particle in enumerate(self.particles):
                for i in range(self.nro_vertices - 1):
                  for j in range(i + 1, self.nro_vertices):
                      # se tiver conflito, atualiza a posicao
                      if (self.graph.existsEdge(i, j)) and (particle[i] == particle[j]) and (i != j):
                        velocidadeNova = self.get_velocity(particle, index, i)
                        self.update_position(particle, velocidadeNova, index, i)

                #atualiza o fitness e o personal_best
                current_fitness = self.fitness_function(self.particles[index])
                if (current_fitness <= self.f_personal_best[index]):
                    self.f_personal_best[index] = current_fitness
                    self.personal_best[index] = self.particles[index]

            self.f_global_best = min(self.f_personal_best)
            self.global_best = self.hill_climbing(self.particles[self.f_personal_best.index(self.f_global_best)])
            auxiterations += 1
        if auxiterations == iterations:
            print(f"Número de iterações chegou ao limite, o melhor fitness encontrado até o momento foi: { self.f_global_best}")
        else:
            print("Interações: ", auxiterations)
            print("Melhor fitness:", self.f_global_best)

        n_cores = len(Counter(self.global_best).keys())
        print("Numero de cores:", n_cores)
        return [self.f_global_best, n_cores, auxiterations]
