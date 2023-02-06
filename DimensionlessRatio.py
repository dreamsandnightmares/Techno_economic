import math
import matplotlib.pyplot as plt
import numpy as np

class Ratio(object):
    def __init__(self):
        self.E =None
        self.h = None

        pass

    def Revenue(self,time,Price,X_gen,X_dc,X_ch,n,):
        r_tot = 0
        for i in range (8760):
            r_tot +=max(Price(time)*(X_gen(time)+X_dc(time) -X_ch(time)/n))








if __name__ == '__main__':
    ###### 数据X，Y，Z
    x = np.arange(-10, 10, 0.01)  # 步长为0.01，即每隔0.01取一个点
    y = np.arange(-10, 10, 0.01)  # 步长为0.01，即每隔0.01取一个点
    X, Y = np.meshgrid(x, y)  # 将原始数据变成网格数据形式
    Z = X ** 2 + Y ** 2  # 我们假设Z为关于X，Y的函数，以Z=X^2+Y^2为例


    ctf = plt.contourf(X, Y, Z, 15,cmap=plt.cm.hot)

    ct = plt.contour(X, Y, Z, 15, colors='k')  # 等高线设置成黑色
    plt.clabel(ct, inline=True, fontsize=10)  # 添加标签
    # plt.pcolormesh(X, Y, Z)     # 绘制分类背景图
    plt.colorbar(ctf)  # 添加cbar
    # plt.xticks(())  # 去掉x标签
    # plt.yticks(())  # 去掉y标签

    plt.show()






