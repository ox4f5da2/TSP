import random
import math
from itertools import groupby

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from prettytable import PrettyTable

###########################################################################
# 随机产生城市坐标和城市间距离

def randomCityCoordinate(cityNum):
  """
  随机产生城市坐标
  :param cityNum: 城市数量 int
  :return: 指定数量的城市坐标 list
  """
  coordinate = []
  while len(coordinate) < cityNum:
    temp = (random.randint(0, cityNum * 2), random.randint(0, cityNum * 2))
    if(coordinate.count(temp) == 0):
      coordinate.append(temp)
  return coordinate

def calculateDistance(coordinate, cityNum, inf):
  """
  计算城市两两间的距离
  :param coordinate: 城市坐标 list
  :param cityNum: 城市数量 int
  :param inf: 无穷大值 double 注: 如果两城市间无路径则用无穷大值来代替
  :return: 指定数量的城市坐标 list
  """
  point = np.zeros((cityNum, cityNum))
  for i in range(len(coordinate)):
    for j in range(i, len(coordinate)):
      # if(i + 1 < j  and random.random() <= 0.3):
      #   point[i][j] = point[j][i] = inf
      #   continue
      point[i][j] = point[j][i] = round(((coordinate[i][0] - coordinate[j][0]) ** 2 + (coordinate[i][1] - coordinate[j][1]) ** 2) ** 0.5, 2)
  return point

def cityInit(ifInput, cityInput, *txtPath):
  """
  随机产生城市矩阵
  :param ifInput: 是否输入城市数量 bool
  :param cityInput: 如果第一个参数为True, 填任意值, 否则填城市数量 int
  :param txtPath: (可选)如果第一个参数为False, 也可以选择文件输入, 文件有三列, 第一列是序号, 第二列是横坐标, 第三列是纵坐标 string
  :return: 城市数量 int, 城市坐标 list, 城市之间的距离矩阵 ndarray

  city.txt示例:
    1   9860  14152
    2   9396  14616
    3  11252  14848
    4  11020  13456
    5   9512  15776
    6  10788  13804
    7  10208  14384
    8  11600  13456
    9  11252  14036
  """ 
  if ifInput == True: cityNum = int(input("请输入城市数量:")) # 城市数量
  else: cityNum = cityInput
  if len(txtPath) == 0:
    coordinate = randomCityCoordinate(cityNum) # 城市坐标
  else:
    coordinate = np.loadtxt(txtPath[0], dtype=np.float32)[:, 1:]
    cityNum = coordinate.shape[0]
  point = calculateDistance(coordinate, cityNum, 10e7) # 城市距离
  return cityNum, coordinate, point

###########################################################################

###########################################################################
# 打印旅行商问题的运行结果表格

def createTable(table_obj):
  """
  打印数据表格
  :param table_obj: 表格对象 obj
  :return: none
  参数示例:
  result_obj = {
    "header": ["TSP参数", "运行结果"],
    "body": [
      ["城市数量", cityNum],
      ["最短路程", distance], 
      ["运行时间", time_str], 
      ["最小路径", path_str] 
    ],
    # name的值要和header一致, l: 左对齐 c: 居中 r: 右对齐
    "align": [
      { "name": "TSP参数", "method": "l" },
      { "name": "运行结果", "method": "l" }
    ],
    "setting": {
      "border": True, # 默认True
      "header": True, # 默认True
      "padding_width": 5 # 空白宽度
    }
  }
  """
  pt = PrettyTable()
  for key in table_obj:
    # 打印表头
    if key == "header": pt.field_names = table_obj[key]
    # 打印表格数据
    elif key == "body": 
      for i in range(len(table_obj[key])): 
        pt.add_row(table_obj[key][i])
    # 表格参数的对齐方式
    elif key == "align": 
      for i in range(len(table_obj[key])): pt.align[table_obj[key][i]["name"]] = table_obj[key][i]["method"]
    # 表格其他设置
    elif key == "setting":
      for key1 in table_obj[key]:
        if key1 == "border": pt.border = table_obj[key][key1]
        elif key1 == "hearder": pt.header = table_obj[key][key1]
        elif key1 == "padding_width": pt.padding_width = table_obj[key][key1]
      # for key1 in table_obj[key]: pt[key1] = table_obj[key][key1]
  print(pt)

def timeFormat(number):
  """
  时间格式保持两位
  :param number: 数字 int
  :return: 两位的数字字符 str
  """
  if number < 10: return "0" + str(number)
  else: return str(number)
 
def calcTime(time):
  """
  将毫秒根据数值大小转为合适的单位
  :param time: 数字 double
  :return: 时间字符串 str
  """
  count = 0
  while time < 1:
    if count == 3: break
    else: count += 1
    time *= 1000
  if count == 0: 
    hour = int(time // 3600)
    minute = int(time % 3600 // 60)
    second = time % 60
    if hour > 0: return timeFormat(hour) + "时" + timeFormat(minute) + "分" + timeFormat(int(second)) + "秒"
    if minute > 0: return timeFormat(minute) + "分" + timeFormat(int(second)) + "秒"
    if second > 0: return str(round(time, 3)) + "秒"
  elif count == 1: return str(round(time, 3)) + "毫秒"
  elif count == 2: return str(round(time, 3)) + "微秒"
  elif count == 3: return str(round(time, 3)) + "纳秒"

def pathToString(path, everyRowNum):
  """
  将最优路径列表转为字符串
  :param path: 最优路径列表 list
  :param: everyRowNum 每行打印的路径数,除去头尾 int
  :return: 路径字符串 str
  """
  min_path_str = ""
  for i in range(len(path)):
    min_path_str += str(path[i]) + ("\n--> " if i != 0 and i % everyRowNum == 0 else " --> ")
  min_path_str += "0" # 单独输出起点编号
  return min_path_str

#打印表格
def printTable(path, everyRowNum, runTime, cityNum, distance):
  """
  将最优路径列表转为字符串
  :param path: 最优路径列表 list
  :param: everyRowNum 每行打印的路径数,除去头尾 int
  :param: runTime 程序运行时间 double
  :param: cityNum 城市数量 int
  :param: distance 最优距离 double
  :return: none
  """
  path_str = pathToString(path, everyRowNum)
  time_str = calcTime(runTime) # 程序耗时
  # 打印的表格对象
  result_obj = {
    "header": ["TSP参数", "运行结果"],
    "body": [
      ["城市数量", cityNum],
      ["最短路程", distance], # 最小值就在第一行最后一个
      ["运行时间", time_str], # 计算程序执行时间
      ["最小路径", path_str] # 输出路径
    ],
    "align": [
      { "name": "参数", "method": "l" },
      { "name": "运行结果", "method": "l" }
    ],
  }
  createTable(result_obj) # 打印结果

###########################################################################

###########################################################################
# 画图函数

def isPath(path, i, j):
  """
  判断边是否为最小路径
  :param path: 最优路径列表 list
  :param: i / j 路径的下标 int
  :return: 布尔值
  """
  idx = path.index(i)
  pre_idx = idx - 1 if idx - 1 >= 0 else len(path) - 1
  next_idx = idx + 1 if idx + 1 < len(path) else 0
  if j == path[pre_idx] or j == path[next_idx]:
    return True
  return False

def drawNetwork(coordinate, point, path, inf, *args):
  """
  画出网络图
  :param coordinate: 城市坐标 list
  :param: point 城市距离矩阵 ndarray
  :param: path 最优路径 list
  :param: inf 无穷大值 double
  :return: none
  """
  G_min = nx.Graph() # 最短路径解
  G = nx.Graph() # 城市路径图
  edges = []
  for i in range(len(coordinate)):
    G_min.add_node(i, pos = coordinate[i]) # 添加节点
    G.add_node(i, pos = coordinate[i])
    for j in range(i + 1, len(coordinate)):
      if point[i][j] != inf:
        if isPath(path, i, j):
          G_min.add_edge(i, j, weight=point[i][j], color='r')
        G.add_edge(i, j, weight=point[i][j])
  tmp_edges = nx.get_edge_attributes(G_min,'color')
  for key in tmp_edges:
    edges.append(tmp_edges[key])
  pos = pos_min = nx.get_node_attributes(G_min,'pos')
  labels = nx.get_edge_attributes(G_min,'weight')
  # 城市所有路径
  plt.subplot(121)
  plt.title("TSP City Network")
  nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='b')
  # 最短路径解
  plt.subplot(122)
  plt.title("Shortest path solution")
  nx.draw(G_min, pos_min, with_labels=True, font_weight='bold',node_color='g', edge_color=edges)
  nx.draw_networkx_edge_labels(G_min, pos_min, edge_labels=labels)
  plt.show()

def drawPlots(dataList, everyRowNum):
  """
  画出多条线
  :param figureID: 图的id值 int | str
  :param dataList: 图的数据 list
  :param everyRowNum: 每行显示图的个数 int
  :return: none

  dataList:
    x-data: 子图横坐标的数据 list
    y-data: 子图纵坐标的数据 list
    title: 子图的标题 str
    x-label: 子图横坐标的文字 str
    y-label: 子图纵坐标的文字 str
    marks: 子图线的样式 str
    ifShowLabel: 子图是否展示标记 str
    label: 标记的文字 str
  注: str没有值写空
  dataList参数示例:
    dataList = [ 
      [# 每张大图
          [# 每张大图内的子图
          {"x-data": x1, "y-data": gdp_rate1, "title":"title1", "x-label": "a", "y-label":"b",
            "marks": '.-',"ifShowLabel": True, "label": "GDP" } # 子图的内容
        ],[
          {"x-data":x2 "y-data": gdp_rate2, "title":"title2", "x-label": "a", "y-label":"b",
            "marks": '.-',"ifShowLabel": False, "label": "GDP" }
        ]
      ],
      [...]
    ]
  """
  for page in range(len(dataList)):
    plt.figure("第{}张图".format(page + 1))
    for i in range(len(dataList[page])):
      item = dataList[page][i]
      if len(dataList[page]) > 1:
        plt.subplot(math.ceil(len(dataList[page]) / everyRowNum) * 100 + everyRowNum * 10 + i + 1)
      for j in range(len(item)):
        plt.plot(item[j]["x-data"], item[j]["y-data"], item[j]["marks"], label=item[j]["label"])
      plt.title(item[j]["title"]) # 设置标题
      plt.xticks(item[j]["x-data"])  # 设置横坐标刻度为给定的数据
      plt.xlabel(item[j]["x-label"]) # 设置横坐标轴标题
      plt.ylabel(item[j]["y-label"]) # 设置横坐标轴标题
      if item[j]["ifShowLabel"] == True:
        plt.legend() # 显示图例，即每条线对应label中的内容
  plt.show() # 显示图形

###########################################################################

###########################################################################
# 是否显示网络图提示

def showTip(tips, allChoice, legal, callback, *args):
  """
  终端内容提示
  :param tips: 提示内容对象 obj
  :param: allChoice 所有合法字符 list
  :param: legal 成功执行的字符 list
  :param: callback 成功执行后的回调函数 function
  :param: *args 剩余参数,传递给回调函数的参数
  :return: none

  tips对象示例:
  {
    "notice": "是否显示城市网络图(Y/N):",
    "warning": "非法输入, 请输入Y/y/N/n"
  }
  """
  while True:
    choice = input(tips["notice"])
    if allChoice.count(choice) > 0:
      if legal.count(choice) > 0: callback(*args, choice)
      break
    else: print(tips["warning"] + "\n")

###########################################################################

###########################################################################
# 其他功能

def spiltByElement(data, element):
  """
  将列表根据某个元素分割
  :param data: 要分割的列表 list
  :param: element 所有合法字符 list
  :return: 分割后的列表 list
  """
  return [list(g) for k, g in groupby(data, lambda x:x==element) if not k]

###########################################################################