# -*- coding: utf-8 -*-
import random
import sys

# ----------- 蚂蚁算法 -----------

# 参数
(ALPHA, BETA, RHO, Q) = (1.0, 1.0, 0.6, 30.0)

class Ant(object):
    # 初始化
    def __init__(self, ID,cityNum,distance_graph,pheromone_graph):
        self.ID = ID  # ID
        self.city_num=cityNum  # 城市数目
        self.distance_graph=distance_graph
        self.pheromone_graph=pheromone_graph
        self.__clean_data()  # 随机初始化出生点

    # 初始数据
    def __clean_data(self):
        self.path = []  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = -1  # 当前停留的城市
        self.open_table_city = [True for i in xrange(self.city_num)]  # 探索城市的状态
        city_index = random.randint(0, self.city_num - 1)  # 随机初始出生点
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    # 选择下一个城市
    def __choice_next_city(self):
        next_city = -1
        select_citys_prob = [0.0 for i in xrange(self.city_num)]
        total_prob = 0.0

        # 获取去下一个城市的概率
        for i in xrange(self.city_num):
            if self.open_table_city[i]: # 城市尚未去
                try:
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow( self.pheromone_graph[self.current_city][i], ALPHA) * pow(
                        (1.0/self.distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError, e:
                    print 'Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID=self.ID,
                                                                                                current=self.current_city,
                                                                                                target=i)
                    sys.exit(1)

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率
            temp_prob = random.uniform(0.0, total_prob) # Get a random number in the range [a, b)
            for i in xrange(self.city_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        # 未从概率产生，顺序选择一个未访问城市
        if next_city == -1:
            for i in xrange(self.city_num):
                if self.open_table_city[i]:
                    next_city = i
                    break

        # 返回下一个城市序号
        return next_city

    # 计算路径总距离
    def __cal_total_distance(self):
        temp_distance = 0.0
        for i in xrange(1, self.city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += self.distance_graph[start][end]

        # 回路
        end = self.path[0]
        temp_distance +=  self.distance_graph[start][end]
        self.total_distance = temp_distance

    # 移动操作
    def __move(self, next_city):
        self.path.append(next_city)
        self.open_table_city[next_city] = False  # 放入禁忌表
        self.total_distance +=  self.distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    # 搜索路径，外部接口
    def search_path(self):
        # 初始化数据
        self.__clean_data()
        # 搜素路径，遍历完所有城市为止
        while self.move_count < self.city_num:
            # 移动到下一个城市
            next_city = self.__choice_next_city()  #根据蚁群算法转移概率，计算下一步选择的城市
            self.__move(next_city)
        # 计算路径总长度
        self.__cal_total_distance()



