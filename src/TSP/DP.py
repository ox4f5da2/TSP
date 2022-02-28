import time

import numpy as np

import utils # 自定义工具函数包

inf = 10e7 # 定义无穷大值

def getMinDistance(point, cityNum, dp):
  """
  得到动态规划后的列表
  :param point: 城市距离矩阵 ndarray
  :param cityNum: 城市数量 int
  :return: dp列表 list
  """
  column = 1 << (cityNum - 1) # dp数组的列数
  # 初始化dp数组第一列
  for i in range(cityNum): 
    dp[i][0] = point[i][0]
  # 更新dp数组，先列再行
  for j in range(1, column): 
    for i in range(0, cityNum):
      dp[i][j] = inf
      if i == 0:
        if (j << 1) & 1 == 1:
          continue
      elif i >= 0:
        if ((j >> (i - 1)) & 1) == 1 :
          continue
      for k in range(1, cityNum):
        if ((j >> (k - 1)) & 1) == 0:
          continue
        if dp[i][j] > point[i][k] + dp[k][j ^ (1 << (k - 1))]:
          dp[i][j] = point[i][k] + dp[k][j ^ (1 << (k - 1))]
  return dp

def isVisited(visited, cityNum):
  """
  判断结点是否都以访问但不包括0号结点
  :param visited: 访问数组 ndarray
  :param cityNum: 城市数量 int
  :return: 布尔值
  """
  for i in range(1, cityNum):
    if visited[i] == False:
      return False
  return True

def getPath(point, cityNum, dp):
  """
  判断结点是否都以访问但不包括0号结点
  :param point: 城市距离矩阵 ndarray
  :param cityNum: 城市数量 int
  :return: 动态规划最优路径 list
  """
  path = [] # 存储最短路径
  column = 1 << (cityNum - 1) # dp数组的列数
  visited = np.zeros(cityNum, dtype=np.bool_) # 标记访问数组
  pioneer = 0 # 前驱节点编号
  min = inf
  S = column - 1
  # 把起点结点编号加入容器
  path.append(0)
  while isVisited(visited, cityNum) == False:
    for i in range(1, cityNum):
      if visited[i] == False and (S & (1 << (i - 1))) != 0:
        if min > point[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]:
          min = point[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]
          temp = i
    pioneer = temp
    path.append(pioneer)
    visited[pioneer] = True
    S = S ^ (1 << (pioneer - 1))
    min = inf
  return path

def dynamicProgramming(cityNum, coordinate, point, ifShowResult):
  """
  动态规划算法
  :param cityNum: 城市数量 int
  :param coordinate: 城市坐标 list
  :param point: 城市距离矩阵 ndarray
  :param ifShowResult: 是否展示结果 bool
  :return: 最小距离 double 运行时间 double
  """
  start = time.perf_counter() # 程序开始时间
  dp = getMinDistance(point, cityNum, np.zeros((cityNum, 1 << (cityNum - 1)))) # 计算dp列表以及最短路径的值
  path = getPath(point, cityNum, dp) # 获取最优路径，保存在path中，根据动态规划公式反向找出最短路径结点列表
  end = time.perf_counter() # 程序结束时间
  if ifShowResult == True:
    utils.printTable(path, 7, end - start, cityNum, round(dp[0][(1 << (cityNum - 1)) - 1], 2)) # 打印表格
    utils.showTip({
      "notice": "是否显示城市网络图(Y/N):",
      "warning": "非法输入, 请输入Y/y/N/n"
    },["Y", "y", "N", "n"], ["Y", "y"], utils.drawNetwork, coordinate, point, path, inf) # 显示网络图的提示
  return round(dp[0][(1 << (cityNum - 1)) - 1], 2), end - start
  
# if __name__ == "__main__":
#   cityNum, coordinate, point = utils.cityInit()
#   dynamicProgramming(cityNum, coordinate, point)