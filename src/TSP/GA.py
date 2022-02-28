import time

import numpy as np

import utils


class TSP_GA(object):
  citys = np.array([])
  citys_name = np.array([])
  pop_size = 50
  c_rate = 0.7
  m_rate = 0.05
  pop = np.array([])
  fitness = np.array([])
  city_size = -1
  ga_num = 200
  best_dist = 1
  best_gen = []

  def __init__(self, c_rate, m_rate, pop_size, ga_num, coordinate):
    self.fitness = np.zeros(self.pop_size)
    self.c_rate = c_rate
    self.m_rate = m_rate
    self.pop_size = pop_size
    self.ga_num = ga_num
    self.citys = np.array(coordinate)

  def init(self):
    tsp = self
    tsp.load_Citys()
    tsp.pop = tsp.creat_pop(tsp.pop_size)
    tsp.fitness = tsp.get_fitness(tsp.pop)

  def creat_pop(self, size):
    pop = []
    for i in range(size):
      gene = np.arange(self.citys.shape[0])
      np.random.shuffle(gene)
      pop.append(gene)
    return np.array(pop)

  def get_fitness(self, pop):
    d = np.array([])
    for i in range(pop.shape[0]):
      gen = pop[i]  # 取其中一条染色体，编码解
      dis = self.gen_distance(gen)
      dis = self.best_dist / dis
      d = np.append(d, dis)  # 求路径长
    return d

  def get_local_fitness(self, gen, i):
    '''
    :param gen:城市路径
    :param i:第i城市
    :return:第i城市的局部适应度
    '''
    di = 0
    fi = 0
    if i == 0:
      di = self.ct_distance(self.citys[gen[0]], self.citys[gen[-1]])
    else:
      di = self.ct_distance(self.citys[gen[i]], self.citys[gen[i - 1]])
    od = []
    for j in range(self.city_size):
      if i != j:
        od.append(self.ct_distance(self.citys[gen[i]], self.citys[gen[i - 1]]))
    mind = np.min(od)
    fi = di - mind
    return fi

  def EO(self, gen):
    local_fitness = []
    for g in range(self.city_size):
      f = self.get_local_fitness(gen, g)
      local_fitness.append(f)
    max_city_i = np.argmax(local_fitness)
    maxgen = np.copy(gen)
    if 1 < max_city_i < self.city_size - 1:
      for j in range(max_city_i):
        maxgen = np.copy(gen)
        jj = max_city_i
        while jj < self.city_size:
          gen1 = self.exechange_gen(maxgen, j, jj)
          d = self.gen_distance(maxgen)
          d1 = self.gen_distance(gen1)
          if d > d1:
              maxgen = gen1[:]
          jj += 1
    gen = maxgen
    return gen

  def select_pop(self, pop):
    best_f_index = np.argmax(self.fitness)
    av = np.median(self.fitness, axis=0)
    for i in range(self.pop_size):
      if i != best_f_index and self.fitness[i] < av:
        pi = self.cross(pop[best_f_index], pop[i])
        pi = self.mutate(pi)
        pop[i, :] = pi[:]
    return pop

  def cross(self, parent1, parent2):
    """交叉"""
    if np.random.rand() > self.c_rate:
      return parent1
    index1 = np.random.randint(0, self.city_size - 1)
    index2 = np.random.randint(index1, self.city_size - 1)
    tempGene = parent2[index1:index2]  # 交叉的基因片段
    newGene = []
    p1len = 0
    for g in parent1:
      if p1len == index1:
        newGene.extend(tempGene)  # 插入基因片段
      if g not in tempGene:
        newGene.append(g)
      p1len += 1
    newGene = np.array(newGene)
    if newGene.shape[0] != self.city_size:
      print('c error')
      return self.creat_pop(1)
    return newGene

  def mutate(self, gene):
    """突变"""
    if np.random.rand() > self.m_rate:
      return gene
    index1 = np.random.randint(0, self.city_size - 1)
    index2 = np.random.randint(index1, self.city_size - 1)
    newGene = self.reverse_gen(gene, index1, index2)
    if newGene.shape[0] != self.city_size:
      print('m error')
      return self.creat_pop(1)
    return newGene

  def reverse_gen(self, gen, i, j):
    if i >= j:
      return gen
    if j > self.city_size - 1:
      return gen
    parent1 = np.copy(gen)
    tempGene = parent1[i:j]
    newGene = []
    p1len = 0
    for g in parent1:
      if p1len == i:
        newGene.extend(tempGene[::-1])  # 插入基因片段
      if g not in tempGene:
        newGene.append(g)
      p1len += 1
    return np.array(newGene)

  def exechange_gen(self, gen, i, j):
    c = gen[j]
    gen[j] = gen[i]
    gen[i] = c
    return gen

  def evolution(self):
    """
    获取最优路径解及坐标
    :return: 最小距离 double 最优路径解 list
    """
    tsp = self
    not_improve_time = 0
    for i in range(self.ga_num):
      best_f_index = np.argmax(tsp.fitness)
      worst_f_index = np.argmin(tsp.fitness)
      local_best_gen = tsp.pop[best_f_index]
      local_best_dist = tsp.gen_distance(local_best_gen)
      if i == 0:
        tsp.best_gen = local_best_gen
        tsp.best_dist = tsp.gen_distance(local_best_gen)
      if round(local_best_dist, 2) < round(tsp.best_dist, 2):
        tsp.best_dist = local_best_dist
        tsp.best_gen = local_best_gen
        not_improve_time = 0
      else:
        tsp.pop[worst_f_index] = self.best_gen
        not_improve_time += 1
      # print('gen:%d evo,best dist :%s' % (i, self.best_dist))
      tsp.pop = tsp.select_pop(tsp.pop)
      tsp.fitness = tsp.get_fitness(tsp.pop)
      for j in range(self.pop_size):
        r = np.random.randint(0, self.pop_size - 1)
        if j != r:
          tsp.pop[j] = tsp.cross(tsp.pop[j], tsp.pop[r])
          tsp.pop[j] = tsp.mutate(tsp.pop[j])
      #self.best_gen = self.EO(self.best_gen)
      tsp.best_dist = tsp.gen_distance(self.best_gen)
      if not_improve_time >= 2000:
          break # 连续2000次迭代都没有改变最优路线，结束迭代
    # print('best dist :%s' % (self.best_dist))
    new_path = utils.spiltByElement(self.best_gen, 0)
    if len(new_path) == 1:
      return round(self.best_dist, 2), [0] + new_path[0]
    elif len(new_path) == 2:
      return round(self.best_dist, 2), [0] + new_path[1] + new_path[0]

  def load_Citys(self):
    self.city_size = self.citys.shape[0]
    self.citys_name = np.arange(self.city_size)

  def gen_distance(self, gen):
    distance = 0.0
    for i in range(-1, len(self.citys) - 1):
      index1, index2 = gen[i], gen[i + 1]
      city1, city2 = self.citys[index1], self.citys[index2]
      distance += np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
    return distance

  def ct_distance(self, city1, city2):
    d = np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
    return d

def geneticAlgorithm(cityNum, coordinate, point, ifShowResult):
  """
  遗传算法
  :param cityNum: 城市数量 int
  :param coordinate: 城市坐标 list
  :param point: 城市距离矩阵 ndarray
  :param ifShowResult: 是否展示结果 bool
  :return: 最小距离 double 运行时间 double
  """
  start = time.time()
  tsp = TSP_GA(0.5, 0.1, 100, 10000, coordinate)
  tsp.init()
  min_dis, best_route = tsp.evolution()
  end = time.time()
  if ifShowResult == True:
    utils.printTable(best_route, 7, end - start, cityNum, min_dis) # 打印表格
    utils.showTip({
    "notice": "是否显示城市网络图(Y/N):",
    "warning": "非法输入, 请输入Y/y/N/n"
    },["Y", "y", "N", "n"], ["Y", "y"], utils.drawNetwork, coordinate, point, best_route, 10e7) # 显示网络图的提示
  return min_dis, end - start

# if __name__ == '__main__':
#     cityNum, coordinate, point = utils.cityInit(False, 50)
#     geneticAlgorithm(cityNum, coordinate, point, True)
