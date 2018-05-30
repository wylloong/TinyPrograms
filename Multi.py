# -*- coding: utf-8 -*-
# JOE论文仿真

import collections
import math
from shapely.geometry import Polygon  # 比较多边形交叉
import matplotlib.pyplot as plt
import matplotlib
import json
import os
import time
import RiskSubjection
import GeoCommonBase
import OABase
import SQLiteRW
import Multi_AStar
import time
# import winsound
import os
import sys

# <editor-fold desc="变量定义">
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf',size=20)
Point = collections.namedtuple("Point", ["x", "y"])
TimeGrid=collections.namedtuple("TimeGrid",["x","y","z","unitlength","unitwidth","unitheight","isNavigonal"])
VesselInfo=collections.namedtuple("ObstacleInfo",["start_x","start_y","velocity","heading","isObstacle","multiPoints","curr_x","curr_y","hasAvoided"])
Point3D=collections.namedtuple("Point3D", ["x", "y","z"])
TDPoint = collections.namedtuple("TDPoint", ["x", "y","z"])
AABB=collections.namedtuple("AABB",["max","min"])
plannedPathFile = "E:\\localPath.txt"
SquareProperty = collections.namedtuple("SquareProperty",["x", "y", "lu_x", "lu_y", "rl_x", "rl_y", "isNavigonal"])
# </editor-fold>

# <editor-fold desc="障碍物运动区域化为多边形">
def motionZonetoPolygon(velocity,criticalValue,evaluTime,impactFactor,safeDis=200,vesselSize=100):
    angleProbeValues=[10,45,90,135,170,190,225,270,315,350]
    evaluDistance=velocity*evaluTime+safeDis+vesselSize
    realtivePnts=[]
    for angle in angleProbeValues:
        orienFactor=RiskSubjection.velocityDirectionFactor(angle,impactFactor)
        distance=(1-criticalValue)*orienFactor*evaluDistance
        pnt=Point(distance*math.sin(angle/180*math.pi),distance*math.cos(angle/180*math.pi))
        realtivePnts.append(pnt)
    print(realtivePnts)
    return realtivePnts
# </editor-fold>

# if __name__=="__main__":
#     motionZonetoPolygon(10,0.1,20,0.7)

# 比较平面重叠属性

# 根据当前位置和速度方向确定运动方位多边形区域

def motionZonePolygon(heading,realtivePnts):
    realPnts=[]
    # 以原点为轴，顺时针旋转heading角度
    for pnt in realtivePnts:
        newPnt=GeoCommonBase.RotationWayPnt(0,0,pnt.x,pnt.y,360-heading)
        realPnts.append(newPnt)
    return realPnts
    print(realPnts)

# <editor-fold desc="根据碰撞类型，在运动区域中加入人为不可航行区域">
def addVirtualUnnavigableArea(realtivePnts,heading,collisionType,virLength):
    if collisionType==OABase.CollisionEnum.crossLeft or collisionType==OABase.CollisionEnum.crossRight:
        # 左交叉，在船头加虚拟距离
        y=realtivePnts[0].y+virLength
        realtivePnts[0]=Point(realtivePnts[0].x,y)
        y=realtivePnts[len(realtivePnts)-1].y+virLength
        realtivePnts[len(realtivePnts)-1] = Point(realtivePnts[len(realtivePnts)-1].x, y)
        return motionZonePolygon(heading,realtivePnts)
    elif collisionType==OABase.CollisionEnum.encounter or collisionType==OABase.CollisionEnum.followLeft:
        # 左交叉，在船右侧加上虚拟宽度
        upCenter=(realtivePnts[0].x+realtivePnts[len(realtivePnts)-1].x)/2
        downCenter=(realtivePnts[round(len(realtivePnts)/2)].x+realtivePnts[round(len(realtivePnts)/2)-1].x)/2  # round() 四舍五入
        upCenter+=virLength
        downCenter+=virLength
        pntCount=len(realtivePnts)
        realtivePnts[0]=Point(upCenter,realtivePnts[0].y)
        realtivePnts[round(len(realtivePnts)/2)-1] = Point(downCenter, realtivePnts[round(len(realtivePnts)/2)-1].y)
        while len(realtivePnts)>round(pntCount/2)+2:
            del realtivePnts[1]
        return motionZonePolygon(heading, realtivePnts)
    elif collisionType==OABase.CollisionEnum.followRight:
        # 从右侧超越，在船左侧加上虚拟宽度
        upCenter = (realtivePnts[0].x + realtivePnts[len(realtivePnts) - 1].x) / 2
        downCenter = (realtivePnts[round(len(realtivePnts) / 2)].x + realtivePnts[round(len(realtivePnts) / 2) - 1].x) / 2
        upCenter -= virLength
        downCenter -= virLength
        pntCount = len(realtivePnts)
        realtivePnts[len(realtivePnts)-1] = Point(upCenter, realtivePnts[len(realtivePnts)-1].y)
        realtivePnts[round(len(realtivePnts) / 2)] = Point(downCenter,realtivePnts[round(len(realtivePnts) / 2)].y)
        while len(realtivePnts) > round(pntCount / 2) + 2:
            del realtivePnts[len(realtivePnts)-2]
        return motionZonePolygon(heading, realtivePnts)
    else:
        return None
# </editor-fold>

# if __name__=="__main__":
#     fig=plt.figure(1)
#     ax = fig.add_subplot(1, 1, 1)
#     plt.axis("equal")  # 设置图像显示的时候XY轴比例
#     realtivePnts=motionZonetoPolygon(10,0.2,20,0.7)
#     Pnts=addVirtualUnnavigableArea(realtivePnts,45,OABase.CollisionEnum.followLeft,300)
#     xList=[]
#     yList=[]
#     for pnt in Pnts:
#         xList.append(pnt.x)
#         yList.append(pnt.y)
#     print(Pnts)
#     xList.append(xList[0])
#     yList.append(yList[0])
#     plt.plot(xList,yList)
#     plt.show()

def getOBSPolygon(ini_x,ini_y,heading,velocity,criticalValue,evaluTime,impactFactor,collisionType,virLength,safeDis=200,vesselSize=100):
    realtivePnts=motionZonetoPolygon(velocity,criticalValue,evaluTime,impactFactor,safeDis,vesselSize)
    Pnts=addVirtualUnnavigableArea(realtivePnts,heading,collisionType,virLength)
    transPnts=[]
    for pnt in Pnts:
        pnt=Point(pnt.x+ini_x,pnt.y+ini_y)
        transPnts.append(pnt)
    return transPnts

# if __name__=="__main__":
#     fig=plt.figure(1)
#     ax = fig.add_subplot(1, 1, 1)
#     plt.axis("equal")  # 设置图像显示的时候XY轴比例
#     # realtivePnts=motionZonetoPolygon(10,0.2,20,0.7)
#     Pnts=getOBSPolygon(1230,850,90, 2* 1852 / 3600, 0.7, 30, 0.8, OABase.CollisionEnum.followRight, 150,safeDis=150,vesselSize=20)
#     xList=[]
#     yList=[]
#     for pnt in Pnts:
#         xList.append(pnt.x)
#         yList.append(pnt.y)
#     print(Pnts)
#     xList.append(xList[0])
#     yList.append(yList[0])
#     plt.plot(xList,yList)
#     plt.show()

# <editor-fold desc="根据AABB概念，得到多边形的最大值和最小值">
def envelopePolygon(polygon):
    minx=miny=1000000
    maxx=maxy=-1000000
    for pnt in polygon:
        if pnt.x < minx:
            minx=pnt.x
        if pnt.x>maxx:
            maxx=pnt.x
        if pnt.y < miny:
            miny=pnt.y
        if pnt.y>maxy:
            maxy=pnt.y
    return minx,maxx,miny,maxy
# </editor-fold>

# <editor-fold desc="投影判断法">
def gridNavigation(TDlength,TDwidth,z,unitlength,unitwidth,ObsPolygon):
    unNavigation=[]
    minx,maxx,miny,maxy=envelopePolygon(ObsPolygon)
    for x in range(int(TDlength/unitlength)):
        for y in range(int(TDwidth/unitwidth)):
            if (maxx-unitlength*x)*(unitlength * (x+1)-minx)>=0 and (maxy-unitlength*y)*(unitlength * (y+1)-miny)>=0:
                # 根据AABB概念，缩小比较范围，非暴力比较
                polygon=[]
                point1=Point(unitlength*x,unitwidth*y)
                point2 = Point(unitlength * x, unitwidth * (y+1))
                point3 = Point(unitlength * (x+1), unitwidth * (y+1))
                point4 = Point(unitlength * (x+1), unitwidth * y)
                polygon.append(point1)
                polygon.append(point2)
                polygon.append(point3)
                polygon.append(point4)
                isNavigation=_2DPolygonsCross(polygon,ObsPolygon) # 是否可以航行判断
                if isNavigation==True:
                    # 不可航行
                    unNavigation.append(Point3D(x,y,z))
    return unNavigation
# </editor-fold>

# 射线与立方体
def intersectWithAABB(AABB,Ray):
    tmin=0
    tmax=10000

    # <editor-fold desc="平行于x轴">
    if(math.fabs(Ray[1].x)<0.000001):
        if (Ray[0].x<AABB.min.x) or (Ray[0].x>AABB.max.x):
            return  False
    else:
        ood=1.0/Ray[1].x
        t1=(AABB.min.x-Ray[0].x)*ood
        t2=(AABB.max.x-Ray[0].x)*ood
        # t1做候选平面，t2做远平面
        if (t1>t2):
            temp=t1
            t1=t2
            t2=temp
        if t1>tmin:
            tmin=t1
        if t2<tmax:
            tmax=t2
        if tmin>tmax:
            return False
    # </editor-fold>

    # <editor-fold desc="平行于y轴">
    if(math.fabs(Ray[1].y)<0.000001):
        if (Ray[0].y<AABB.min.y) or (Ray[0].y>AABB.max.y):
            return  False
    else:
        ood=1.0/Ray[1].y
        t1=(AABB.min.y-Ray[0].y)*ood
        t2=(AABB.max.y-Ray[0].y)*ood
        # t1做候选平面，t2做远平面
        if (t1>t2):
            temp=t1
            t1=t2
            t2=temp
        if t1>tmin:
            tmin=t1
        if t2<tmax:
            tmax=t2
        if tmin>tmax:
            return False
    # </editor-fold>

    # <editor-fold desc="平行于z轴">
    if(math.fabs(Ray[1].z)<0.000001):
        if (Ray[0].z<AABB.min.z) or (Ray[0].z>AABB.max.z):
            return  False
    else:
        ood=1.0/Ray[1].z
        t1=(AABB.min.z-Ray[0].z)*ood
        t2=(AABB.max.z-Ray[0].z)*ood
        # t1做候选平面，t2做远平面
        if (t1>t2):
            temp=t1
            t1=t2
            t2=temp
        if t1>tmin:
            tmin=t1
        if t2<tmax:
            tmax=t2
        if tmin>tmax:
            return False
    # </editor-fold>

    return True

# 判断线段与立方体网格是否相交，返回交叉的网格list
def rayAABBInter(startPnt,endPnt):
    diff_x = endPnt.x - startPnt.x
    diff_y = endPnt.y - startPnt.y
    diff_z = endPnt.z - startPnt.z
    # 射线方向
    Sum=math.sqrt(diff_x**2+diff_y**2+diff_z**2)
    dirdiff_x=diff_x/Sum
    dirdiff_y = diff_y / Sum
    dirdiff_z = diff_z / Sum
    # 射线原点
    origin_x=startPnt.x-3*diff_x
    origin_y = startPnt.y - 3*diff_y
    origin_z = startPnt.z - 3*diff_z
    origin=TDPoint(origin_x,origin_y,origin_z)
    dir=TDPoint(dirdiff_x,dirdiff_y,dirdiff_z)
    Ray=[]
    Ray.append(origin)
    Ray.append(dir)

    interPntList=[]
    # 判断长度
    for xCube in range(int(diff_x)+1):
        for yCube in range(int(diff_y) + 1):
            for zCube in range(int(diff_z)+1):
                xAdd=xCube
                yAdd=yCube
                zAdd=zCube
                if(diff_x<0):
                    xAdd=-xCube
                if (diff_y < 0):
                    yAdd = -yCube
                if (diff_z < 0):
                    zAdd = -zCube
                centerX=startPnt.x+xAdd
                centerY = startPnt.y + yAdd
                centerZ = startPnt.z + zAdd
                aabb=AABB(TDPoint(centerX+0.5,centerY+0.5,centerZ+0.5),TDPoint(centerX-0.5,centerY-0.5,centerZ-0.5))
                inter=intersectWithAABB(aabb,Ray) # 判断是否相交
                if inter==True:
                    interPntList.append(TDPoint(centerX,centerY,centerZ))
    return interPntList  # 返回相交的网格

# 曲线平滑处理，去除多余的航点
def pathSmoothing(originalPath,unwalkCells):
    CmpPnt = 0
    if(len(originalPath)<2): # 原始航路数量太少，无法路径优化
        return originalPath
    # 路径平滑处理
    editPntList = originalPath
    while (len(editPntList) > CmpPnt + 2):
        first = editPntList[CmpPnt]
        third = editPntList[CmpPnt + 2]
        interPntList = rayAABBInter(first, third)
        safeFlag = True
        for pnt in interPntList:
            if pnt in unwalkCells:
                safeFlag = False
                break
        if safeFlag:
            # 可以删除该点
            editPntList.remove(editPntList[CmpPnt + 1])
        else:
            # 不可以删除
            CmpPnt += 1
    return editPntList

# 判断二维平面上，多边形与网格的交集
def _2DPolygonsCross(polygon1,polygon2):
    polygonlist1 = []
    for point in polygon1:
        t = (point.x, point.y)
        polygonlist1.append(t)
    p1 = Polygon(polygonlist1)
    polygonlist2 = []
    for point in polygon2:
        t = (point.x, point.y)
        polygonlist2.append(t)
    p2 = Polygon(polygonlist2)
    return p1.intersects(p2)

# point绕固定点旋转
def pointRotation(x,y,rotationHeading,fixedPoint_x,fixedPoint_y):
    Rotaradian =rotationHeading/180 * math.pi
    newX = x*math.cos(Rotaradian) - y*math.sin(Rotaradian)
    newY = x*math.sin(Rotaradian) + y*math.cos(Rotaradian)
    return newX,newY

# 多边形旋转后，取x轴上的极大极小值
def maxminPoint(multiPoints,heading):
    # 计算障碍物的多边形在航行方向的轮廓，旋转后的x最大最小值
    xList = []
    yList = []
    for point in multiPoints:
        x, y = pointRotation(point.x, point.y, heading, 0, 0)
        xList.append(x)
        yList.append(y)
    # 求x方向的极值
    maxXValue = xList[0]
    minXValue = xList[0]
    maxXIndex = 0
    minXIndex = 0
    index = 0
    for point in xList:
        if (point > maxXValue):
            maxXValue = point
            maxXIndex = index
        elif (point < minXValue):
            minXValue = point
            minXIndex = index
        index += 1
    return maxXIndex,minXIndex

# <editor-fold desc="单位时间投影：根据不同时间段的多边形位置，组合成轨迹，其中返回点顺时针组合">
def _3DProject2Polygon(obstacle,time,maxIndex,minIndex,unitTime):
    # 上一次(time)障碍物的位置
    # 每一个点的移动
    lastpoints = []
    for point in obstacle.multiPoints:
        x = point.x + obstacle.velocity * time * unitTime * math.sin(obstacle.heading / 180 * math.pi)
        y = point.y + obstacle.velocity * time * unitTime * math.cos(obstacle.heading / 180 * math.pi)
        pnt = Point(x, y)
        lastpoints.append(pnt)
    # 下一刻(time+1)障碍物的位置
    # 每一个点的移动
    newpoints = []
    for point in obstacle.multiPoints:
        x = point.x + obstacle.velocity * (time+1) * unitTime * math.sin(obstacle.heading / 180 * math.pi)
        y = point.y + obstacle.velocity * (time+1) * unitTime * math.cos(obstacle.heading / 180 * math.pi)
        pnt = Point(x, y)
        newpoints.append(pnt)

    constructPolygon=[]
    # 上一时刻最小值->下一时刻最小值->顺时针->下一时刻最大值->上一时刻最大值->顺时针->上一时刻最小值
    count=minIndex
    pointNum=len(newpoints) # 点的总数
    # 上一时刻最小值
    constructPolygon.append(lastpoints[minIndex])
    # 下一时刻最小值->顺时针->下一时刻最大值
    while (count % pointNum) != maxIndex:
        count=count % pointNum
        constructPolygon.append(newpoints[count])
        count+=1
    # 下一时刻最大值
    constructPolygon.append(newpoints[maxIndex])
    # 上一时刻最大值->顺时针
    count=maxIndex
    while (count % pointNum)!= minIndex:
        count = count % pointNum
        constructPolygon.append(lastpoints[count])
        count += 1

    return constructPolygon
# </editor-fold>

# <editor-fold desc="三维环境模型的可航行判断">
def _3DEnvironmentConstruct(TDlength,TDwidth,TDheight,unitlength,unitwidth,unitheight,DynamicObjects,currTime):
    # <editor-fold desc="分解出USV和障碍物">
    ObstacleList=[]
    for object in DynamicObjects:
        if (object.isObstacle==False):  # 水面无人艇
            USVInfo=object
        elif (object.isObstacle==True):  # 障碍物
            ObstacleList.append(object)
    # </editor-fold>

    unNavigationPoints=[]
    # 以障碍物为单位，依次计算
    for obstacle in ObstacleList:
        maxIndex,minIndex=maxminPoint(obstacle.multiPoints,obstacle.heading) # 横轴最大最小值
        # 以层为单位计算
        for time in range(int(TDheight/unitheight)):
            if time < int(currTime/unitheight):
                # 过去的时间
                continue
            else:
                # 构建这一时间层的平面投影，返回多边形的坐标
                constructPolygon=_3DProject2Polygon(obstacle, time,maxIndex,minIndex,unitheight)
                # 比较平面重叠属性 unNavigation--不可航行
                unNavigation=gridNavigation(TDlength, TDwidth, time, unitlength, unitwidth, constructPolygon)
                unNavigationPoints.extend(unNavigation) # list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
    # 不可航行区域输出
    return unNavigationPoints
# </editor-fold>

# <editor-fold desc="仿真数据写入到SQLIte数据库中">
def recordNaviInformation(dbPath,ID,Curr_x,Curr_y,Curr_z,Curr_time):
    # cmd="INSERT INTO JOECA (id,x,y,z,time)" \
    #     "VALUES (%d,%f,%f,%f,%d)"\
    #     %(ID,Curr_x,Curr_y,Curr_z,Curr_time)
    # SQLiteRW.write2SQLite(dbPath,cmd)
    pass
# </editor-fold>

# <editor-fold desc="规划路径数据写入到SQLIte数据库中">
def recordPlannedPathInformation(dbPath,ID,planned_x,planned_y,planned_z,planned_time,smoothed=1):
    # smoothed=1 未优化 smoothed=2 已优化
    pass
    # cmd="INSERT INTO PlannedPath (ID,x,y,z,plannedTime,smoothed)" \
    #     "VALUES (%d,%f,%f,%f,%d,%d)"\
    #     %(ID,planned_x,planned_y,planned_z,planned_time,smoothed)
    # SQLiteRW.write2SQLite(dbPath,cmd)
# </editor-fold>

def A_Star_Search_OA_Path(startPoint,targetPoint,maxDim,unNavigationList,originalStart):
    start = time.clock()
    came_from, cost_so_far, current = Multi_AStar.a_star_search(unNavigationList, maxDim, startPoint, targetPoint,originalStart)
    print("A*搜索路径完成")
    pathFinderPoints = []
    # 回溯父节点
    pathFinderPoints.append(current)
    fatherNode = came_from[current]
    while fatherNode != startPoint:
        pathFinderPoints.append(fatherNode)
        fatherNode = came_from[fatherNode]
    pathFinderPoints.append(startPoint)
    end = time.clock()
    print("A*运行时间 %f seconds" %(end - start))
    reversePath=pathFinderPoints[::-1]
    return reversePath
    # return pathFinderPoints

# 代码测试区域
if __name__=="__main__":

    # <editor-fold desc="仿真设置">
    unitheight = 10
    searchheight = 80
    columnNum=60
    rowNum=60
    unitlength = 16.0 * 1852 / 3600 * unitheight  # 网格的单位长度
    unitwidth = 16.0 * 1852 / 3600 * unitheight  # 网格的单位宽度
    TDlength = unitlength*columnNum  # 目标区域的长度
    TDwidth = unitlength*rowNum  # 目标区域的宽度
    maxDim=TDPoint(columnNum,rowNum,searchheight)
    startPoint = TDPoint(45, 44, 0)
    targetPoint = TDPoint(45, 12, 60)
    originalStart=TDPoint(45, 44, 0)
    # </editor-fold>

    # 保留环境中的不可航性网格Cells
    unwalkableCells=[]

    # <editor-fold desc="人机交互显示">
    # ax = plt.subplot(111, projection='3d')
    fig = plt.figure()
    plt.axis("equal")  # 设置图像显示的时候XY轴比例
    # </editor-fold>

    # <editor-fold desc="构建第一个动态障碍物_对遇">
    heading = 8
    start_x = 3650
    start_y = 2150
    velocity = 8 * 1852 / 3600
    Pnts = getOBSPolygon(start_x, start_y, heading, velocity, 0.6, 40, 0.8, OABase.CollisionEnum.encounter, 600,
                         safeDis=200, vesselSize=20)
    dynaObs1 = VesselInfo(start_x, start_y, velocity, heading, True, Pnts, start_x, start_y, False)
    # </editor-fold>

    # <editor-fold desc="构建第二个动态障碍物_右交叉">
    heading=86
    start_x=3190
    start_y=2850
    velocity=10 * 1852 / 3600
    Pnts = getOBSPolygon(start_x,start_y,heading,velocity, 0.6, 30, 0.8, OABase.CollisionEnum.crossRight, 400,safeDis=200,vesselSize=20)
    dynaObs2=VesselInfo(start_x,start_y,velocity,heading,True,Pnts,start_x,start_y,False)
    # </editor-fold>

    # <editor-fold desc="构建第三个障碍物_静态障碍物">
    heading = 0
    start_x = 3540
    start_y = 3086
    velocity = 0
    transPnts = []
    transPnts.append(Point(start_x-10, start_y+10))
    transPnts.append(Point(start_x + 10, start_y + 10))
    transPnts.append(Point(start_x + 10, start_y - 10))
    transPnts.append(Point(start_x - 10, start_y - 10))
    dynaObs3 = VesselInfo(start_x, start_y, velocity, heading, True, transPnts, start_x, start_y, False)
    # </editor-fold>

    # <editor-fold desc="构建第四个动态障碍物">
    heading = 276
    start_x = 5000
    start_y = 1500
    velocity = 7 * 1852 / 3600
    Pnts = getOBSPolygon(start_x, start_y, heading, velocity, 0.6, 30, 0.8, OABase.CollisionEnum.crossLeft, 800,
                         safeDis=200, vesselSize=20)
    dynaObs4 = VesselInfo(start_x, start_y, velocity, heading, True, Pnts, start_x, start_y, False)
    # </editor-fold>

    # <editor-fold desc="构建第五个动态障碍物">
    heading = 276
    start_x = 5000
    start_y = 1500
    velocity = 6 * 1852 / 3600
    Pnts = getOBSPolygon(start_x, start_y, heading, velocity, 0.6, 30, 0.8, OABase.CollisionEnum.crossLeft, 800,
                         safeDis=200, vesselSize=20)
    dynaObs5 = VesselInfo(start_x, start_y, velocity, heading, True, Pnts, start_x, start_y, False)
    # </editor-fold>

    DynamicObjects = []
    DynamicObjects.append(dynaObs1)
    DynamicObjects.append(dynaObs2)
    DynamicObjects.append(dynaObs3)
    DynamicObjects.append(dynaObs4)
    DynamicObjects.append(dynaObs5)

    TDheight=searchheight*unitheight  # 目标区域的高度
    previousPlannedPath = []  # 保存之前的局部规划路径信息

    print("环境建模初始化")
    unNavigationList=_3DEnvironmentConstruct(TDlength,TDwidth,TDheight,unitlength,unitwidth,unitheight,[],0)
    unwalkableCells.extend(unNavigationList)  # unNavigationList的元素复制到unwalkableCells中
    unwalkableCells = list(set(unwalkableCells))  # 去除unwalkableCells中重复的元素

    # <editor-fold desc="读入ENC静态障碍物">
    # 读入电子海图给出的静态障碍物
    time.sleep(2)
    SquareList=[]
    with open("/Users/didi/Downloads/squareEnvi.txt", "r") as r:
        filelist = r.readlines()
        for x in filelist:
            dic = json.loads(x)  # 输出dict类型
            p = SquareProperty(**dic)
            hexpro = SquareProperty(p.x, p.y, p.lu_x, p.lu_y, p.rl_x, p.rl_y,p.isNavigonal)
            SquareList.append(hexpro)
    print("静态障碍物读取成功")
    # 识别障碍物，加入到unwalkableCells
    unNavigation = []
    for pnt in SquareList:
        if pnt.isNavigonal==False:
            for h in range(searchheight):
                unNavigation.append(Point3D(pnt.x, pnt.y, int(h)))
    unwalkableCells.extend(unNavigation)  # unNavigationList的元素复制到unwalkableCells中
    unwalkableCells = list(set(unwalkableCells))  # 去除unwalkableCells中重复的元素
    # </editor-fold>

    # 局部路径规划
    plannedOAPath = A_Star_Search_OA_Path(startPoint, targetPoint, maxDim, unwalkableCells,originalStart)
    print("路径规划成功")

    localPathList = []
    count=0
    timeAlive=0
    temp=[]
    for _3DPnt in plannedOAPath:
        localPathList.append(_3DPnt)
        temp.append(_3DPnt)
    print("新的规划路径：")
    previousPlannedPath.append(temp)
    print(localPathList)

    # 路径平滑处理
    smoohPath = pathSmoothing(temp.copy(), unwalkableCells)
    print("优化后的路径: ")
    print(smoohPath)

    os.system('say "test"')

    # <editor-fold desc="保存障碍物的前段轨迹 初始化">
    USVhasTravedPntList=[]
    hasTravedPntList=[]
    hasTravedPntList.append([])
    hasTravedPntList.append([])
    hasTravedPntList.append([])
    hasTravedPntList.append([])
    hasTravedPntList.append([])
    motionTime = 0  # 路径规划后的运动时间，外部计时
    # </editor-fold>

    timeCount = 0  # 仿真系统的内部计时
    while True and timeCount<30*searchheight:
        # 不断遍历，等待路径规划的结果
        time.sleep(0.2) # 单位：秒
        timeCount+=5
        # <editor-fold desc="模拟USV运动部分">
        if((timeCount)%30==0):
            plt.clf()  # clears the entire current figure with all its axes, but leaves the window opened
            # <editor-fold desc="重新绘制已规划的路径">
            for pathlist in previousPlannedPath:
                # print("绘制已规划的路径")
                xList = []
                yList = []
                for pnt in pathlist:
                    xList.append((pnt.x) * unitlength)
                    yList.append((pnt.y) * unitlength)
                plt.plot(xList, yList, 'b:', marker='o')
            # </editor-fold>

            # <editor-fold desc="绘制障碍物轨迹">
            # 障碍物轨迹
            for obsTrave in hasTravedPntList:
                if len(obsTrave)>0:
                    xList = []
                    yList = []
                    for pnt in obsTrave:
                        xList.append(pnt.x)
                        yList.append(pnt.y)
                    plt.plot(xList, yList, 'b:', marker='o')
            # USV 轨迹
            xList = []
            yList = []
            for pnt in USVhasTravedPntList:
                xList.append((pnt.x-0.1) * unitlength)
                yList.append((pnt.y-0.1) * unitlength)
            plt.plot(xList, yList, 'b:', marker='o')
            # </editor-fold>

            # 可行路径不为空
            if (len(localPathList)>2):
                # 假设单位规划时间
                motionTime += unitheight  # 根据网格的单位高度Z unit 确定
                tp=localPathList.pop(1)
                while(tp==startPoint and len(localPathList)>0):
                    tp = localPathList.pop(1)
                startPoint=tp # 下一个航路点

                # 绘制USV的当前位置
                plt.scatter(startPoint.x*unitlength, startPoint.y*unitlength, c='r', marker='.',linewidths=20)  # 散点图

                # 障碍物
                for k,element in enumerate(DynamicObjects):
                    polygons=[]
                    xPnts=[]
                    yPnts=[]
                    offset_x=element.velocity * math.sin(element.heading / 180 * math.pi)*motionTime
                    offset_y=element.velocity * math.cos(element.heading / 180 * math.pi)*motionTime
                    for pnt in element.multiPoints:
                        x=pnt.x + offset_x
                        y=pnt.y + offset_y
                        xPnts.append(x)
                        yPnts.append(y)
                    xPnts.append(xPnts[0])
                    yPnts.append(yPnts[0])
                    point = Point(element.start_x+offset_x, element.start_y+offset_y)  # 保存OBS轨迹

                    # 替换当前坐标的参数
                    temp = element._replace(curr_x=element.start_x+offset_x,curr_y=element.start_y+offset_y)
                    DynamicObjects[k] = temp
                    hasTravedPntList[k].append(point)
                    plt.plot(xPnts,yPnts,c='b',marker='.')

                plt.pause(0.01)

                # <editor-fold desc="根据危险度确定障碍物,并规划路径">
                currOBSList=[]
                # for k, element in enumerate(DynamicObjects):
                #     # 两船的距离在探测范围内
                #     if(element.hasAvoided==False and GeoCommonBase.DistanceofPoints(startPoint.x*unitlength, startPoint.y*unitlength,element.curr_x,element.curr_y)<3000):
                #         # DCPA触发路径规划,暂时省去，认为障碍物进去探测范围就开始规划
                #         currOBSList.append(element)
                #         temp = element._replace(hasAvoided=True)
                #         DynamicObjects[k] = temp
                #         print(" 系统第一次检测到障碍物，时间： %d "%(motionTime))
                print(motionTime)

                if(motionTime==10):
                    k=0
                    element=DynamicObjects[k]
                    currOBSList.append(element)
                    temp = element._replace(hasAvoided=True)
                    DynamicObjects[k] = temp
                    print(" 系统第一次检测到障碍物，时间： %d "%(motionTime))
                    k = 1
                    element = DynamicObjects[k]
                    currOBSList.append(element)
                    temp = element._replace(hasAvoided=True)
                    DynamicObjects[k] = temp
                    print(" 系统第一次检测到障碍物，时间： %d " % (motionTime))

                if (motionTime == 110):
                    # TDPoint(x=44, y=38, z=11), TDPoint(x=43, y=38, z=12), TDPoint(x=43, y=37, z=13), TDPoint(x=42, y=37,z=14)
                    # 故意设置静态障碍物
                    k = 2
                    element = DynamicObjects[k]
                    currOBSList.append(element)
                    temp = element._replace(hasAvoided=True)
                    DynamicObjects[k] = temp
                    print(" 系统第一次检测到障碍物，时间： %d " % (motionTime))

                if (motionTime == 250):
                    k = 3
                    element = DynamicObjects[k]
                    currOBSList.append(element)
                    temp = element._replace(hasAvoided=True)
                    DynamicObjects[k] = temp
                    print(" 系统第一次检测到障碍物，时间： %d " % (motionTime))

                if (motionTime == 300):
                    k = 4
                    element = DynamicObjects[k]
                    currOBSList.append(element)
                    temp = element._replace(hasAvoided=True)
                    DynamicObjects[k] = temp
                    print(" 系统第一次检测到障碍物，时间： %d " % (motionTime))

                if (len(currOBSList)>0):
                    unNavigationList = _3DEnvironmentConstruct(TDlength, TDwidth, TDheight, unitlength, unitwidth,
                                                               unitheight, currOBSList,motionTime)
                    print(unNavigationList)
                    unwalkableCells.extend(unNavigationList)
                    unwalkableCells=list(set(unwalkableCells)) # 去除unwalkableCells中重复的元素
                    print("添加障碍物成功")

                    # 局部路径规划
                    plannedOAPath = A_Star_Search_OA_Path(startPoint, targetPoint, maxDim, unwalkableCells,originalStart)
                    print("路径规划成功")

                    localPathList = []
                    count = 0
                    timeAlive = 0
                    temp = []
                    for _3DPnt in plannedOAPath:
                        localPathList.append(_3DPnt)
                        temp.append(_3DPnt)
                    print("新的规划路径：")
                    previousPlannedPath.append(temp)
                    print(localPathList)

                    # 路径平滑处理
                    smoohPath = pathSmoothing(temp.copy(), unwalkableCells)
                    print("优化后的路径: ")
                    print(smoohPath)

                    os.system('say "test"')

                # </editor-fold>
        # </editor-fold>
    print("已退出while循环")
    plt.show()
