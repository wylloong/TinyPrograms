&emsp;&emsp;最近在解决三维问题时，需要判断线段是否与立方体交叉，这个问题可以引申为：射线是否穿过立方体AABB。  
&emsp;&emsp;在3D游戏开发中碰撞检测普遍采用的算法是轴对齐矩形边界框(Axially Aligned Bounding Box, AABB)包装盒方法,其基本思想是用一个立方体或者球体完全包裹住3D物体对象，然后根据包装盒的距离、位置等相关信息来计算是否发生碰撞。 
# slab的碰撞检测算法
&emsp;&emsp;<font size=5>本文接下来主要讨论射线与AABB的关系，主要对box2d碰撞检测使用的slab的碰撞检测算法(==Slabs method==)进行介绍，然后使用python语言实现slab碰撞检测方法，该方法可以用于3D物体拾取等应用场景。</font>  
&emsp;&emsp;Slab英文翻译是“平板”，本文是指两个平行平面/直线之间的空间。在2D空间中slab可以理解为平行于坐标轴的两条直线间的区域，3D空间中为平行于xy平面（或者yz面，xz面）的两个平面之间的区域。由此，我们可以把3D空间中的AABB盒子看做是由AABB的3组平行面形成的3个方向的slab的交集。  
&emsp;&emsp;另外，引入候选面的概念：在3D空间中，我们先确定正对着射线的三个面，也就是说，我们可以通过某种方式将AABB相对于射线Ray的背面给忽略掉，从而确定三个候选的面。这三个候选的面，就是有可能和射线Ray发生交叉的最近的面。  

---
&emsp;&emsp;根据这个定义，我们可以得到以下三个结论：
1. 性质一：如果一个点在AABB中，那么这个点必定同时在这3个slab中。
2. 性质二：如果一条射线和AABB相交，那么这条射线和3个slab的相交部分必定有重合部分。
3. 性质三：当射线与这三个候选面中的一个发生交叉之后，射线Ray的原点到这个面的距离要比到其他几个面的距离要长。  
---
&emsp;&emsp;性质一和性质二比较容易理解，如果射线和3个slab的相交线段没有重合，那么这些线段就不可能同时存在于3个slab中，也就不可能在AABB盒子中。  
&emsp;&emsp;为了方便理解性质三，使用2D图形来讲解：

<div align=center><img src="http://p05tunu6e.bkt.clouddn.com/18-1-22/14739430.jpg" width = "400" height = "300" alt="图片名称" align=center/></div>

&emsp;&emsp;在上图中，我们的射线在右下角，向左上角发射，射线经过一个A点，其中候选面是y1面和x2面。  
&emsp;&emsp;根据上述性质，可以看到A点同时在2D空间中的2个slab中；此外，根据性质二，因为射线与平面相交，那么这条射线与slab的相交部分必有重合部分，因为A点在射线上，且在平面中，那么可以得到max(t1,t2)<=tA<=min(t3,t4);根据性质三：当交叉后，可以看出t2>t1。  
&emsp;&emsp;同理，我们可以把上述的验证过程推广到三维中。在三维空间中，假设射线到3个候选面的距离分别是t1、t2、t3，到候选面对应的面的距离分别为t4、t5、t6，那么根据性质二，射线与AABB碰撞的条件是max(t1,t2,t3)<=min(t4,t5,t6);如果发生交叉，那么根据性质三，射线到最近的交叉面的距离是是max(t1,t2,t3)。  

---
&emsp;&emsp;在上述性质基础上，确定射线与AABB是否交叉需要三步骤：
1. 如何确定候选面：只要将平面方程带入射线Ray的方程，求出这两个平面的t值，然后t值较小的那个自然先与射线交叉，那么就表示它是一个候选面。射线可以用参数方程表示为R(t) = P0 + t·d, (其中P0为射线起点，d为射线的方向向量)
2. 如何确定候选面的方程。平面由隐式定义方程X·n=D， (其中X为平面上的点，n为平面法向量，D为原点到平面的距离)给出。由于AABB的slab平面都分别和两个坐标轴平行，它的面的法线总是有两个分量是0，而另外一个分量总是为1，所以我们一致使用某个轴分量为1的法线。如果上面的方程表示的是AABB盒的左面的面，那么公式中的n表示的就是(1,0,0)，但上面的公式表示的是AABB盒的右边的面的时候，n表示的值依然是(1,0,0)。  
3. 如何对交叉点是否在AABB盒上进行判断。根据性质二判断，即射线与AABB碰撞的条件是max(t1,t2,t3)<=min(t4,t5,t6)。
---
# 碰撞检测算法公式推导

&emsp;&emsp;求取t值的公式推导如下： 

<div align=center><img src="http://p05tunu6e.bkt.clouddn.com/18-1-22/97654879.jpg" width = "350" height = "500" alt="图片名称" align=center/></div>

---

# 碰撞检测算法Python源代码

最后，附上我的Python代码片段。
```python
# Ray-AABB方法 相交返回True，否则返回False
# TDPoint = collections.namedtuple("TDPoint", ["x", "y","z"])
# AABB有最大和最小点组成，数据结构为｛max=TDPoint,min=TDPoint｝
# Ray由原点和方向组成，其中方向矢量为1，数据结构为｛TDPoint，TDPoint｝
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
```

from [3D空间中射线与轴向包围盒AABB的交叉检测算法](http://blog.csdn.net/i_dovelemon/article/details/38342739)  
from [Box2D 射线和AABB的碰撞检测](http://blog.csdn.net/ring0hx/article/details/7677418)
