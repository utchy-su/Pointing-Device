"""Data_store.pyの機能に関して

    * Author: S.Uchino
    * Data_storeクラスはData_analyzerクラスに呼ばれます。
    * 運用する上でこのクラスのコードを理解する必要はありません

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from New_tester import Tester

class DataFrames:
    """
    保存されたexcelデータから座標データ等を読み込み、データフレームとして返します。

    Attributes
    ----------
    path : str
        読み込むexcelデータの存在場所
    data : pandas DataFrame object
        excelデータをpandasのデータフレームとして読み込む
    orders : list
        円をクリックする順番
    cods : dict
        カーソル座標データを保存するdict型
    time : list
        カーソルのi個目の座標データを取得したときの経過時間
    flattening_range : int
        何個のデータごとに平均を取ってノイズを取るか。無視でもOK
    """

    def __init__(self, path, flattening_range=20):
        """
        コンストラクタです。インスタンス化した時点でcodsとtimeにデータを格納します。

        Parameters
        ----------
        path : str
            読み込むexcelデータの存在場所
        flattening_range : int
            平均を取るデータ点の個数を指定します。
        """
        self.__path = path
        self.__data = pd.read_excel(self.__path)
        self.__orders = Tester.getOrders()
        self.__cods = {'x':[], 'y':[]}
        self.__angles = {'roll':[], 'pitch':[]}
        self.__time = []
        self.__flattening_range = flattening_range
        self.__cods_calculator()  # 座標データをcodsに格納
        self.__time_calculator()  # 各タスクにかかった時間をtimeに格納
        self.__angles_calculator()


    def __cods_calculator(self) -> None:
        """
        エクセルデータから(x, y)座標を読み取り、self.__codsに格納します
        """

        for i in range(15):
            tgt_num = self.__orders[i]
            x_destination = 450 * 200 * np.cos(np.pi * tgt_num / 8)
            y_destination = 450 * 200 * np.sin(np.pi * tgt_num / 8)

            x_index = 'x from ' + str(i) + ' to ' + str(i+1)
            y_index = 'y from ' + str(i) + ' to ' + str(i+1)

            x_cods = self.__data[x_index].dropna(how='all')
            y_cods = self.__data[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+self.__flattening_range]) for j in range(0, len(x_cods)-self.__flattening_range, self.__flattening_range)]
            y_cods = [np.mean(y_cods[j:j+self.__flattening_range]) for j in range(0, len(y_cods)-self.__flattening_range, self.__flattening_range)]

            self.__cods['x'].append(x_cods)
            self.__cods['y'].append(y_cods)

    def __time_calculator(self) -> None:
        """
        エクセルデータから各座標が取得された時点での経過時間を読み取り、self.__timeに格納
        """
        for i in range(15):
            time_index = 'time from ' + str(i) + ' to ' + str(i+1)

            time = self.__data[time_index].dropna(how="all")
            MT = (time.iloc[-1] - time.iloc[0])/1000

            self.__time.append(MT)

    def __angles_calculator(self) -> None:
        """
        エクセルデータから角度(roll, pitch)を読み取り、self.__anglesに格納します
        """
        for i in range(15):
            tgt_num = self.__orders[i]
            x_destination = 450 * 200 * np.cos(np.pi * tgt_num / 8)
            y_destination = 450 * 200 * np.sin(np.pi * tgt_num / 8)

            roll_index = 'roll from ' + str(i) + ' to ' + str(i+1)
            pitch_index = 'pitch from ' + str(i) + ' to ' + str(i+1)

            roll = self.__data[roll_index].dropna(how='all')
            pitch = self.__data[pitch_index].dropna(how='all')

            roll = [np.mean(roll[j:j+self.__flattening_range]) for j in range(0, len(roll)-self.__flattening_range, self.__flattening_range)]
            pitch = [np.mean(pitch[j:j+self.__flattening_range]) for j in range(0, len(pitch)-self.__flattening_range, self.__flattening_range)]

            self.__angles['roll'].append(roll)
            self.__angles['pitch'].append(pitch)


    def get_cods(self) -> dict:
        """
        座標データのgetterです
        """
        return self.__cods

    def get_time(self):
        """
        時間データのgetterです
        """
        return self.__time

    def get_orders(self):
        return self.__orders

    def get_angles(self):
        return self.__angles


if __name__ == "__main__":
    test_data = DataFrames("./test.xlsx")
    print(test_data.get_angles())
