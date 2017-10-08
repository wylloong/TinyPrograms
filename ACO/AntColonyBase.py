# -*- coding: utf-8 -*-

import random
import copy
import sys
import Tkinter
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import AntColonyCore
import math

# 随机生成点
#RandomNodes=True
RandomNodes=False

# 演示情形
#  Demo=1  # 纯粹蚁群算法
Demo=2  # 不回起始点的蚁群算法

# 距离表示
DistanceType=1 # 欧式距离
# DistanceType=2 # 曼哈顿距离

# 城市数，蚁群
(city_num, ant_num,iter_max) = (50,100,1500)

# 随机产生孔数目
if RandomNodes:
    distance_x=[]
    distance_x.append(10)
    for x in range(city_num-1):
        distance_x.append(int((random.random()*700+50)//1))
    distance_y=[]
    distance_y.append(10)
    for x in range(city_num-1):
        distance_y.append(int((random.random()*500+50)//1))
    distance_z=[]
    distance_z.append(0)
    for x in range(city_num - 1):
        distance_z.append(0)
else:
    distance_x = [
        10, 272, 176, 171, 650, 499, 267, 703, 408, 437, 491, 74, 532,
        416, 626, 42, 271, 359, 163, 508, 229, 576, 147, 560, 35, 714,
        757, 517, 64, 314, 675, 690, 391, 628, 87, 240, 705, 699, 258,
        428, 614, 36, 360, 482, 666, 597, 209, 201, 492, 294]
    distance_y = [
        10, 395, 198, 151, 242, 556, 57, 401, 305, 421, 267, 105, 525,
        381, 244, 330, 395, 169, 141, 380, 153, 442, 528, 329, 232, 48,
        498, 265, 343, 120, 165, 50, 433, 63, 491, 275, 348, 222, 288,
        490, 213, 524, 244, 114, 104, 552, 70, 425, 227, 331]
    distance_z = []
    distance_z.append(0)
    for x in range(city_num - 1):
        distance_z.append(0)

# 城市距离和信息素
distance_graph = [[0.0 for col in xrange(city_num)] for raw in xrange(city_num)]  # 距离矩阵，默认为0
pheromone_graph = [[1.0 for col in xrange(city_num)] for raw in xrange(city_num)] #信息素矩阵，默认为1

iterDistance=[]  # 缓存距离数值，用于最后的性能分析

# ----------- TSP问题 -----------
class TSP(object):
    def __init__(self, root, width=800, height=600, n=city_num):
        # 创建画布
        self.root = root
        self.width = width
        self.height = height
        # 城市数目初始化为city_num
        self.n = n
        # Tkinter.Canvas
        self.canvas = Tkinter.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#EBEBEB",  # 背景白色
            xscrollincrement=1,
            yscrollincrement=1
        )
        self.canvas.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
        self.title("ABB-路径规划算法实现 (n:初始化 e:开始搜索 s:停止搜索 q:退出程序)" )
        self.__r = 3
        self.__lock = threading.RLock()  # 线程锁
        self.__bindEvents()
        self.new()

        # 计算城市之间的距离
        #self.globalPathPlan = GlobalPathPlanwithHex.GlobalPathPlan_Hexagonal()
        for i in xrange(city_num):  #xrange用法与range相同，所不同的是生成的不是一个数组，而是一个生成器。
            for j in xrange(city_num):
                if (DistanceType==1):  # 欧式距离
                    distance_graph[i][j]=DistancebyEuclidean(distance_x[i],distance_y[i],distance_z[i],distance_x[j],distance_y[j],distance_z[j])
                elif (DistanceType==2):  # 曼哈顿距离
                    distance_graph[i][j] =DistancebyManhattan(distance_x[i],distance_y[i],distance_z[i],distance_x[j],distance_y[j],distance_z[j])
                #起始点和目标点距离设置为1
                # if j<i:
                #     distance_graph[i][j] = distance_graph[j][i]
                #     PlanedPath.append(PlanedPath[j*city_num+i])  # 保存规划的路径
                #     PlanedPathwithCurve.append(PlanedPathwithCurve[j*city_num+i])  # 优化的曲线
                #     print("%d -> %d 未优化距离： %f 优化后的距离： %f  ACO权衡距离： %f" % (i, j, 0, 0, distance_graph[i][j]))
                # else:
                #     if (i==0 and j==city_num-1) or (j==0 and i==city_num-1):
                #         distance_graph[i][j] = 1
                #         PlanedPath.append(None)
                #         PlanedPathwithCurve.append(None)
                #         continue
                #     if(abs(Rdistance_x[i]-Rdistance_x[j])>0.0001):
                #         planeddistanceall, pathFinderPoints, distanceall, curvelist=self.globalPathPlan.getDistanceofTwoPoints(Rdistance_x[i],Rdistance_y[i],Rdistance_x[j],Rdistance_y[j])
                #         #temp_distance = pow(distanceall, 0.2)
                #         temp_distance = distanceall/1852 #转换为海里
                #         print("%d -> %d 未优化距离： %f 优化后的距离： %f  ACO权衡距离： %f"%(i,j,planeddistanceall,distanceall,temp_distance))
                #         distance_graph[i][j] = (temp_distance + 0.5)
                #         PlanedPath.append(pathFinderPoints)  #保存规划的路径
                #         PlanedPathwithCurve.append(curvelist)  #优化的曲线
                #     else:
                #         #distance_graph[i][j] =pow(Distancelist[i*8+j],1)
                #         distance_graph[i][j]=1
                #         PlanedPath.append(None)
                #         PlanedPathwithCurve.append(None)
                # #distance_graph[i][j] = pow(Distancelist[i * 8 + j], 1)
        if(Demo==2):
            # 不回起始点
            for x in range(city_num):
                distance_graph[x][0]=1
                #distance_graph[0][x] = 0.1
        print distance_graph

    # 按键响应程序
    def __bindEvents(self):
        self.root.bind("q", self.quite)  # 退出程序
        self.root.bind("n", self.new)  # 初始化
        self.root.bind("e", self.search_path)  # 开始搜索
        self.root.bind("s", self.stop)  # 停止搜索

    # 更改标题
    def title(self, s):
        self.root.title(s)

    # 初始化TSP问题
    def new(self, evt=None):
        # 停止线程
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()  # 释放线程锁
        self.clear()  # 清除信息
        self.nodes = []  # 节点坐标
        self.nodes2 = []  # 节点对象
        # 初始化城市节点
        for i in range(len(distance_x)):
            # 在画布上随机初始坐标
            x = distance_x[i]
            y = distance_y[i]
            z = distance_z[i]
            self.nodes.append((x, y))
            # 生成节点椭圆，半径为self.__r
            node = self.canvas.create_oval(x - self.__r,
                                           y - self.__r, x + self.__r, y + self.__r,
                                           fill="#ff0000",  # 填充红色
                                           outline="#000000",  # 轮廓白色
                                           tags="node",
                                           )
            self.nodes2.append(node)
            # 显示坐标
            self.canvas.create_text(x, y - 10,
                                    text='(' + str(x) + ',' + str(y) + ',' + str(z) + ')',  # 所绘制文字的内容
                                    fill='black'  # 所绘制文字的颜色为灰色
                                    )

        # 顺序连接城市
        # self.line(range(city_num))

        # 初始城市之间的距离和信息素
        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone_graph[i][j] = 1.0

        self.ants = [AntColonyCore.Ant(ID,city_num,distance_graph,pheromone_graph) for ID in xrange(ant_num)]  # 初始蚁群
        self.best_ant = AntColonyCore.Ant(-1,city_num,distance_graph,pheromone_graph)  # 初始最优解
        self.best_ant.total_distance = 1 << 31  # 初始最大距离
        self.iter = 1  # 初始化迭代次数

    # 将节点按order顺序连线
    def line(self, order):
        # 删除原线
        self.canvas.delete("line")

        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill="#000000", tags="line")
            return i2

        # # 删除某个坐标点
        # if Demo==2: # 不显示返回起始点
        #     if 0 in self.best_ant.path:
        #         index=self.best_ant.path.index(0)
        #         if index==0:  #在0位，则从末尾开始
        #             index=city_num
        #         self.best_ant.path.pop(index-1)  # 删除 n->0的路径
        #         self.line(self.best_ant.path)
        #
        # order[-1]为初始值
        reduce(line2, order, order[-1])  # 反复调用函数line2

    # 清除画布
    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    # 退出程序
    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.root.destroy()
        print u"\n程序已退出..."
        sys.exit()

    # 停止搜索
    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

    # 开始搜索
    def search_path(self, evt=None):

        # 开启线程
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        #minimundistance=[]
        #while self.__running:
        for i in xrange(iter_max):  #迭代次数
            # 遍历每一只蚂蚁
            for ant in self.ants:
                # 搜索一条路径
                ant.search_path()
                #ant.__update_pheromone_gragh()
                # 与当前最优蚂蚁比较
                if ant.total_distance < self.best_ant.total_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
            #记录此次迭代最短距离
            iterDistance.append(self.best_ant.total_distance)
            # 更新信息素
            # 所有蚂蚁完成对城市的遍历后，更新信息素
            self.__update_pheromone_gragh()

            print u"迭代次数：", self.iter, u"最佳路径总距离：", int(self.best_ant.total_distance)
            #minimundistance.append(int(self.best_ant.total_distance))
            # 连线
            self.line(self.best_ant.path)
            # 设置标题
            self.title("ABB-路径规划算法实现  当前迭代次数: %d" % self.iter)
            # 更新画布
            self.canvas.update()
            self.iter += 1

        print("路径规划完成")
        # 绘制数据显示
        x = range(0, len(iterDistance))
        plt.figure(figsize=(10,6))
        plt.plot(x,iterDistance,'k')
        # plt.xticks((0, 20, 40, 60, 80, 100, 120), ('200504', '200912', '201108', '201306', '201502', '201610', ''))
        plt.xlabel('Iterations')
        plt.ylabel('Distance of Path')
        plt.title('Convergence Curves')
        plt.show()

        #绘制航路
        #print(self.best_ant.path)
        #pathsequence=self.best_ant.path
        '''
        pathlist=[]
        pathlistwithCurvelist = []  #优化的曲线路径
        pathIndex=0
        pathsequence.append(pathsequence[0]) #首尾相连
        while pathIndex<len(pathsequence)-1:
            first=pathsequence[pathIndex]
            second=pathsequence[pathIndex+1]
            pathIndex=pathIndex+1
            if first==city_num-1 and second==0:
                continue
            if first==0 and second==city_num-1:
                continue
            planedPath=PlanedPath[first*city_num+second]
            pathwithCurve=PlanedPathwithCurve[first*city_num+second]
            if planedPath!= None: #有航路
                print(11)
                #pathlist.append(planedPath)
            if pathwithCurve!=None:
                pathlistwithCurvelist.append(pathwithCurve)
        #print(pathlist)
        print(minimundistance)
        self.globalPathPlan.show2plt(pathlist,pathlistwithCurvelist)
        '''


    # 更新信息素
    def __update_pheromone_gragh(self):

        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = [[0.0 for col in xrange(city_num)] for raw in xrange(city_num)]
        for ant in self.ants:
            for i in xrange(1, city_num):
                start, end = ant.path[i - 1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                temp_pheromone[start][end] += AntColonyCore.Q / ant.total_distance  # 信息素
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in xrange(city_num):
            for j in xrange(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * AntColonyCore.RHO + temp_pheromone[i][j]  # 上一次的信息素*衰减因子+此次的信息素

    # 主循环
    def mainloop(self):
        self.root.mainloop()

# 距离定义
# 欧式距离
def DistancebyEuclidean(x1, y1,z1,x2, y2,z2):
    temp_distance = pow((x1 - x2), 2) + pow((y1 - y2), 2)+ pow((z1 - z2), 2)
    return math.sqrt(temp_distance)

# 曼哈顿距离
def DistancebyManhattan(x1, y1,z1,x2, y2,z2):
    return abs(x1 - x2) + abs(y1 - y2)+abs(z1-z2)

# ----------- 程序的入口处 -----------

if __name__ == '__main__':
    print u""" 
--------------------------------------------------------
    程序：机械臂打孔路径规划的算法设计
    作者：王彦龙 
    日期：2017-09-25
    语言：Python 2.7 
-------------------------------------------------------- 
    """
    TSP(Tkinter.Tk()).mainloop()