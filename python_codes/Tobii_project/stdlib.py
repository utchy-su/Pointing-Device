import pandas as pd
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