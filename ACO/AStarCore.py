# -*- coding: utf-8 -*-

import collections
import heapq
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import axes

class SquareGrid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.nodeHeight=[]

    def in_bounds(self, id):
        (x, y,z) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        # id高度小于等于实际点的高度，认为不可航行
        (x,y,z)=id
        #print id
        if 0 <= x < (self.width) and 0 <= y < (self.height):
            # print y*self.width +x
            (x1,y1,z1)= self.nodeHeight[x*self.width +y]
            # return (x,y) not in self.walls and z1<=z
            #print z1<=z
            if z1<=z:
                return True
            else:
                return False

        else:
            return False

    def neighbors(self, id):
        (x, y,z) = id
        results = [(x + 1, y,z), (x, y - 1,z),(x , y,z+1), (x - 1, y,z), (x, y + 1,z), (x, y ,z-1)]
        if (x + y+z) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super(GridWithWeights, self).__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(a, b):
    (x1, y1,z1) = a
    (x2, y2,z2) = b
    return math.sqrt(pow((x1 - x2),2)+pow((y1 - y2),2)+pow((z1 - z2),2))

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start) # optional
    path.reverse() # optional
    return path

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def getDistance(width,heigh,graph,start,goal):
    diagram4 = GridWithWeights(width,heigh)
    diagram4.nodeHeight=graph
    came_from, cost_so_far = a_star_search(diagram4, start, goal)
    return cost_so_far[goal]

# ----------- 程序的测试入口处 -----------
if __name__ == '__main__':
    diagram4 = GridWithWeights(4, 4)
    diagram4.nodeHeight=[(0,0,0),(0,1,1),(0,2,2),(0,3,5),
                         (1, 0, 3), (1, 1, 4), (1, 2, 0),(1, 3, 3),
                         (2, 0, 2), (2, 1, 8), (2, 2, 3),(2, 3, 0),
                         (3, 0, 0), (3, 1, 0), (3, 2, 1), (3, 3, 0),
                         ]
    start=(0,0,0)
    goal=(3,3,0)
    came_from, cost_so_far=a_star_search(diagram4,start,goal)
    path=reconstruct_path(came_from,start,goal)
    print path  # 路径值
    print cost_so_far[goal]  # 路径代价
