import pandas as pd
import time
import graph
import HybridPSO

arr_arquivos = [
  ('myciel3.txt', 4),
  ('myciel4.txt', 5),
  ('myciel5.txt', 6),
  ('queen5_5.txt', 5),    
  ('queen6_6.txt', 7),
  ('huck.txt', 11),
  ('jean.txt', 10),
  ('david.txt', 11),
  ('games120.txt', 9)
]

results = []
for (filename, chromatic_number) in arr_arquivos:  
  print('\n\n', filename, chromatic_number)
  g = Graph(filename, chromatic_number)
  begin = time.time()
  result = Hybrid_PSO(g)
  [fitness, k, interacoes] = result.run(20000)
  end = time.time()
  print('Tempo de execução: ', str(end-begin), ' segundos')
  results.append([filename, g.nro_vertices, g.nro_arestas, chromatic_number, k, interacoes, "{:.3f}".format(end-begin), fitness])
df = pd.DataFrame(columns=['File', '|V|', '|E|', 'Número Cromático', 'K encontrado',  'Interações', 'Tempo', 'Conflitos'], data=results)
df.head(16)
