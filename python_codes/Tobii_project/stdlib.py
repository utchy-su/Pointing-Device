import pandas as pd
from New_tester import Tester
from Data_store import DataFrames
import numpy as np


class MyLibrary:

    @staticmethod
    def get_valid_range(x):
        """
        外れ値を除外する範囲を計算
        :param x: Pandas Series
        :return: 下限LOWER_Q, 上限HIGHER_Q
        """
        x = pd.Series(x)

        Q1 = x.quantile(0.25)
        Q3 = x.quantile(0.75)
        IQR = Q3 - Q1

        LQ = Q1 - 1.5*IQR
        HQ = Q3 + 1.5*IQR

        return LQ, HQ

    @staticmethod
    def get_valid_data(x, y):
        """
        2つのデータで，互いの条件に合う様に
        :param x:
        :param y:
        :return:
        """
        x, y = pd.Series(x), pd.Series(y)
        xLQ, xHQ = MyLibrary.get_valid_range(x)
        yLQ, yHQ = MyLibrary.get_valid_range(y)

        x, y = x[(xLQ < x) & (x < xHQ)], y[(xLQ < x) & (x < xHQ)]
        x, y = x[(yLQ < y) & (y < yHQ)], y[(yLQ < y) & (y < yHQ)]

        return x, y

    @staticmethod
    def get_large_me_param(subject, param, threshold):
        path = "./data/{}/{}/summary.xlsx".format(subject, param)
        df = pd.read_excel(path)
        index = df.index[df.ME > threshold]
        index = index.map(lambda x: x+1)
        index = [(x//16+1, x%16) for x in index]
        return index

    @staticmethod
    def ideal_route(i):
        cx, cy = 1920//2, 1080//2
        order = Tester.getOrders()
        x_prev = int(cx + 200*np.cos(np.pi * order[i]/8))
        y_prev = int(cy + 200*np.sin(np.pi * order[i]/8))

        x_tgt = int(cx + 200*np.cos(np.pi * order[i+1]/8))
        y_tgt = int(cx + 200*np.sin(np.pi * order[i+1]/8))

        a = -(y_tgt - y_prev)
        b = (x_tgt - x_prev)
        c = -x_tgt * y_prev + y_tgt * x_prev

        return a, b, c

if __name__ == "__main__":
    pass