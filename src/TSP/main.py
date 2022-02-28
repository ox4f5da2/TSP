import numpy as np

import ACO
import DP
import GA
import utils

algorithmList = ["动态规划算法", "蚁群算法", "遗传算法", "蚁群算法优化测试", "数据集测试", "自动化算法测试"]

def functionChoose(choice):
  print("现在使用的是{}".format(algorithmList[int(choice) - 1]))
  if int(choice) < len(algorithmList) - 1:
    cityNum, coordinate, point = utils.cityInit(True, 0)
  if choice == "1": DP.dynamicProgramming(cityNum, coordinate, point, True)
  elif choice == "2": 
    ACO.antColonyOptimization(cityNum, coordinate, point, True, setting={
        "iter_max": 300,
        "ifOptimanation": True,
        "threshold": 6,
        "skipNum": 20
      })
  elif choice == "3": GA.geneticAlgorithm(cityNum, coordinate, point, True)
  elif choice == "4": 
    print("蚁群算法优化测试")
    cityNumList = np.array(input("输入城市规模:").split(",")).astype(int)
    skipNumList = np.array(input("输入跳过次数:").split(",")).astype(int)
    marks = input("输入线条样式:").split(",")
    iter = int(input("输入每轮测试次数:"))
    ACO.optimazationTest(cityNumList, skipNumList, marks, iter)
  elif choice == '5':
    txt = input("请输入导入的坐标文件路径:")
    num = int(input("请输入每种算法运行次数:"))
    ACO_all = GA_all = 0
    for i in range(num):
      cityNum, coordinate, point = utils.cityInit(False, 0, txt)
      ACO_dis, ACO_time, iterNum = ACO.antColonyOptimization(cityNum, coordinate, point, False, setting={
                                      "iter_max": 300,
                                      "ifOptimanation": True,
                                      "threshold": 6,
                                      "skipNum": 20
                                    })
      ACO_all += ACO_dis
      print("已完成第{}次蚁群算法, 用时{}".format(i + 1, utils.calcTime(ACO_time)))
      GA_dis, GA_time = GA.geneticAlgorithm(cityNum, coordinate, point, False)
      GA_all += GA_dis
      print("已完成第{}次遗传算法, 用时{}".format(i + 1, utils.calcTime(GA_time)))
    utils.createTable({
      "header": ["算法名称", "运行结果"],
      "body": [
        ["{}次蚁群算法最优解平均值".format(num), ACO_all / num], 
        ["{}次遗传算法最优解平均值".format(num), GA_all / num],
      ],
      "align": [
        { "name": "参数", "method": "c" }, { "name": "运行结果", "method": "l" }
      ],
      "setting": {
        "border": True, # 默认True
        "header": True, # 默认True
        "padding_width": 5 # 空白宽度
      }
    })                          
  elif choice == str(len(algorithmList)):
    x = np.array(input("输入想要测试的城市规模:").split(",")).astype(int)
    iteration = int(input("请输入每轮测试的次数:"))
    dp_dis_list = []
    aco_dis_list = []
    ga_dis_list = []
    dp_time_list = []
    aco_time_list = []
    ga_time_list = []
    for i in range(len(x)):
      cityNum, coordinate, point = utils.cityInit(False, x[i])
      dp_dis_all = aco_dis_all = ga_dis_all = 0
      dp_time_all = aco_time_all = ga_time_all = 0
      for j in range(iteration):
        if x[i] <= 20: 
          dp_dis, dp_time = DP.dynamicProgramming(cityNum, coordinate, point, False)
          dp_dis_all += dp_dis
          dp_time_all += dp_time
        setting = {
          "iter_max": 300,
          "ifOptimanation": True,
          "threshold": 6,
          "skipNum": 20
        }
        aco_dis, aco_time, iterNum = ACO.antColonyOptimization(cityNum, coordinate, point, False, setting)
        aco_dis_all += aco_dis
        aco_time_all += aco_time
        ga_dis, ga_time = GA.geneticAlgorithm(cityNum, coordinate, point, False)
        ga_dis_all += ga_dis
        ga_time_all += ga_time
      if x[i] <= 20:
        dp_dis_list.append(dp_dis_all / iteration)
        dp_time_list.append(dp_time_all / iteration)
      else:
        dp_dis_list.append(0)
        dp_time_list.append(0)
      aco_dis_list.append(aco_dis_all / iteration)
      aco_time_list.append(aco_time_all / iteration)
      ga_dis_list.append(ga_dis_all / iteration)
      ga_time_list.append(ga_time_all / iteration)
      print("tip: 目前已经完成第{}轮算法测试".format(i + 1))
    print("所有测试已经完成")
    dataList = [[
      [
        { "x-data":x, "y-data": dp_dis_list, "title": "Algorithm Performance Test", "x-label": "number of cities", "y-label":"value of distance", "marks": '-o', "ifShowLabel": True, "label": "DP" },
        { "x-data":x, "y-data": aco_dis_list, "title": "Algorithm Performance Test", "x-label": "number of cities", "y-label":"value of distance", "marks": '-s', "ifShowLabel": True, "label": "ACO" },
        { "x-data":x, "y-data": ga_dis_list,"title": "Algorithm Performance Test", "x-label": "number of cities", "y-label":"value of distance", "marks": '-^', "ifShowLabel": True, "label": "GA" }
      ],[ 
        { "x-data":x, "y-data": dp_time_list, "title": "Algorithm Performance Test", "x-label": "number of cities", "y-label":"value of time", "marks": '-o', "ifShowLabel": True, "label": "DP" },
        { "x-data":x, "y-data": aco_time_list, "title": "Algorithm Performance Test", "x-label": "number of cities", "y-label":"value of time", "marks": '-s', "ifShowLabel": True, "label": "ACO" },
        { "x-data":x, "y-data": ga_time_list,"title": "Algorithm Performance Test", "x-label": "number of cities", "y-label":"value of time", "marks": '-^', "ifShowLabel": True, "label": "GA" }
      ]
    ]]
    utils.drawPlots(dataList, 2)

def init():
  body = []
  allChoice = []
  for i in range(len(algorithmList)): 
    body.append([i + 1, algorithmList[i]])
    allChoice.append(str(i + 1))
  return body, allChoice

def main():
  print("旅行商问题求解")
  body, allChoice = init()
  start_gui = {
    "header": ["算法序号", "算法名称"],
    "body": body,
    "align": [
      { "name": "算法名称", "method": "l" }
    ],
  }
  utils.createTable(start_gui) # 打印开始界面
  while True:
    exitFlag = False
    utils.showTip({
      "notice": "请输入想要使用的算法的序号:",
      "warning": "请正确输入算法序号"
    }, allChoice, allChoice, functionChoose) # 显示网络图的提示
    while True:
      ifExit = input("是否退出(Y/N)")
      if ifExit == "Y" or ifExit == 'y' or ifExit == "N" or ifExit == "n":
        if ifExit == "Y" or ifExit == 'y': exitFlag = True
        elif ifExit == "N" or ifExit == "n": exitFlag = False
        break
      else: print("非法输入")
    if exitFlag == True: break

if __name__ == "__main__":
  main()
