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
import pygame
from pygame.locals import *


class DataFrames:
    """データを格納するクラス
    保存されたexcelデータから座標データ等を読み込み、データフレームとして返します。

    Attributes:
        path (str): 読み込むexcelデータの存在場所
        data (pandas DataFrame object): excelデータをpandasのデータフレームとして読み込む
        orders (list):円をクリックする順番
        cods (dict): カーソル座標データを保存するdict型
        time (list): カーソルのi個目の座標データを取得したときの経過時間
        flattening_range (int): 何個のデータごとに平均を取ってノイズを取るか。無視でもOK
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
        self.__cods = {'x': [], 'y': []}
        self.__angles = {'roll': [], 'pitch': []}
        self.__gaze_cods = {'x': [], 'y': []}
        self.__dist = []
        self.__time = []
        self.__timestamp = []
        self.__gaze_velocity = []
        self.__tlead = []
        self.__flattening_range = flattening_range
        self.__timestamp_calculator()
        self.__cods_calculator()  # 座標データをcodsに格納
        self.__time_calculator()  # 各タスクにかかった時間をtimeに格納
        self.__angles_calculator()
        self.__gaze_cods_calculator()
        self.__dist_gaze_pointer()
        self.__gaze_velocity_calculator()
        self.__tlead_calculator()

    def __cods_calculator(self) -> None:
        """
        エクセルデータから(x, y)座標を読み取り、self.__codsに格納します
        """

        for i in range(15):
            tgt_num = self.__orders[i]

            x_index = 'x from ' + str(i) + ' to ' + str(i+1)
            y_index = 'y from ' + str(i) + ' to ' + str(i+1)

            self.__data[x_index] = pd.to_numeric(self.__data[x_index], errors='coerce')
            self.__data[y_index] = pd.to_numeric(self.__data[y_index], errors="coerce")

            x_cods = self.__data[x_index].dropna(how='all')
            y_cods = self.__data[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+self.__flattening_range]) for j in range(0, len(x_cods)-self.__flattening_range, self.__flattening_range)]
            y_cods = [np.mean(y_cods[j:j+self.__flattening_range]) for j in range(0, len(y_cods)-self.__flattening_range, self.__flattening_range)]

            self.__cods['x'].append(x_cods)
            self.__cods['y'].append(y_cods)

    def __timestamp_calculator(self) -> None:
        """

        :return:
        """

        for i in range(15):
            t_index = "time from " + str(i) + " to " + str(i+1)

            self.__data[t_index] = pd.to_numeric(self.__data[t_index], errors="coerce")

            t = self.__data[t_index].dropna(how="all")

            t = [t[i] - t[0] for i in range(len(t))]

            t = [np.mean(t[j:j+self.__flattening_range]) for j in range(0, len(t)-self.__flattening_range, self.__flattening_range)]

            self.__timestamp.append(t)

    def __time_calculator(self) -> None:
        """
        エクセルデータから各座標が取得された時点での経過時間を読み取り、self.__timeに格納
        """
        for i in range(15):
            time_index = 'time from ' + str(i) + ' to ' + str(i+1)

            self.__data[time_index] = pd.to_numeric(self.__data[time_index], errors="coerce")

            time = self.__data[time_index].dropna(how="all")
            MT = (time.iloc[-1] - time.iloc[0])/1000

            self.__time.append(MT)

    def __angles_calculator(self) -> None:
        """
        エクセルデータから角度(roll, pitch)を読み取り、self.__anglesに格納します
        """
        for i in range(15):
            roll_index = 'roll from ' + str(i) + ' to ' + str(i+1)
            pitch_index = 'pitch from ' + str(i) + ' to ' + str(i+1)

            self.__data[roll_index] = pd.to_numeric(self.__data[roll_index], errors="coerce")
            self.__data[pitch_index] = pd.to_numeric(self.__data[pitch_index], errors="coerce")

            roll = self.__data[roll_index].dropna(how='all')
            pitch = self.__data[pitch_index].dropna(how='all')

            roll = [np.mean(roll[j:j+self.__flattening_range]) for j in range(0, len(roll)-self.__flattening_range, self.__flattening_range)]
            pitch = [np.mean(pitch[j:j+self.__flattening_range]) for j in range(0, len(pitch)-self.__flattening_range, self.__flattening_range)]

            self.__angles['roll'].append(roll)
            self.__angles['pitch'].append(pitch)

    def __gaze_cods_calculator(self) -> None:
        """
        Excelデータから視線の座標を読み取り，self.__gaze_codsに格納します

        :return: None
        """

        for i in range(15):
            x_index = "gaze x from " + str(i) + " to " + str(i+1)
            y_index = "gaze y from " + str(i) + " to " + str(i+1)

            self.__data[x_index] = pd.to_numeric(self.__data[x_index], errors="coerce")
            self.__data[y_index] = pd.to_numeric(self.__data[y_index], errors="coerce")

            x = self.__data[x_index].dropna(how="all")
            y = self.__data[y_index].dropna(how="all")

            x = [x[j] for j in range(0, len(x)-self.__flattening_range, self.__flattening_range)]
            y = [y[j] for j in range(0, len(y)-self.__flattening_range, self.__flattening_range)]

            self.__gaze_cods['x'].append(x)
            self.__gaze_cods['y'].append(y)

    def __gaze_velocity_calculator(self):
        """
        Excelデータから視線の座標の差分速度を計算し，self.__gaze_velocityに格納します．
        最初の速度はゼロです．
        :return:
        """
        for i in range(15):
            gx, gy = self.__gaze_cods['x'][i], self.__gaze_cods['y'][i]
            t = self.__timestamp[i]

            N = len(gx)
            gaze_velocity = [0]

            for j in range(1, N):
                d = np.sqrt((gx[j]-gx[j-1])**2 + (gy[j]-gy[j-1])**2)
                v = d / (t[j] - t[j-1])
                gaze_velocity.append(v)

            self.__gaze_velocity.append(gaze_velocity)

    def __tlead_calculator(self):
        """
        論文に準拠してt_leadを計算．tlead = (v_m, d_gm)/||v_m||^2
        :return:
        """
        for count in range(15):
            px = self.__cods['x'][count]
            py = self.__cods['y'][count]
            gx = self.__gaze_cods['x'][count]
            gy = self.__gaze_cods['y'][count]
            t = self.__timestamp[count]
            N = len(px)

            vx = [(px[i+1] - px[i])/(t[i+1]-t[i]) for i in range(N-1)]
            vy = [(py[i+1] - py[i])/(t[i+1]-t[i]) for i in range(N-1)]
            dx = [gx[i] - px[i] for i in range(N-1)]
            dy = [gy[i] - py[i] for i in range(N-1)]

            tlead = []

            for vx_, vy_, dx_, dy_ in zip(vx, vy, dx, dy):
                num = vx_*dx_ + vy_*dy_
                den = vx_*vx_ + vy_*vy_

                if num == 0.0 or den == 0.0:
                    tlead.append(np.nan)
                else:
                    tlead.append(num/den)

            self.__tlead.append(tlead)

    def __dist_gaze_pointer(self) -> None:
        for count in range(15):
            dist_list = []
            px, py = self.__cods['x'][count], self.__cods['y'][count]
            gx, gy = self.__gaze_cods['x'][count], self.__gaze_cods['y'][count]
            # print(px)

            for px_, py_, gx_, gy_ in zip(px, py, gx, gy):
                d = np.sqrt((px_-gx_)**2 + (py_-gy_)**2)
                dist_list.append(d)

            self.__dist.append(dist_list)

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

    def get_timestamp(self):
        return self.__timestamp

    def get_gaze_cods(self):
        return self.__gaze_cods

    def get_dist_gaze_pointer(self):
        return self.__dist

    def get_gaze_velocity(self):
        return self.__gaze_velocity

    def get_tlead(self):
        return self.__tlead

class Angle_Analysis:

    def __init__(self, path):
        self.data = DataFrames(path, flattening_range=20)
        self.angles = self.data.get_angles()

    def show_angle_trend(self):

        for i in range(15):
            roll = self.angles["roll"][i]
            pitch = self.angles["pitch"][i]

            x = np.arange(0, len(roll), 1)

            plt.plot(x, roll, label="roll: " + str(i))
            plt.plot(x, pitch, label="pitch: " + str(i))

        plt.legend()
        plt.ylim(-40, 40)
        plt.show()


if __name__ == "__main__":
    path = ".\\data\\Uchino\\mouse\\test4.xlsx"
    test = DataFrames(path, flattening_range=30)
    tlead = test.get_tlead()

    for i in range(15):
        y = tlead[i][1:]
        x = list(range(len(y)))
        plt.plot(x, y, "-o")
        plt.show()

    def get_valid_range(x):
        """
        外れ値を除外する範囲を計算
        :param x: Pandas Series
        :return: 下限LOWER_Q, 上限HIGHER_Q
        """
        Q1 = x.quantile(0.25)
        Q3 = x.quantile(0.75)
        IQR = Q3 - Q1

        LQ = Q1 - 1.5*IQR
        HQ = Q3 + 1.5*IQR

        return LQ, HQ

    def f():
        # path = ".\\data\\Uchino\\sqrt_10\\test1.xlsx"
        x = []
        y = []
        for i in range(1, 5):
            path = ".\\data\\Uchino\\mouse\\test" + str(i) + ".xlsx"
            test = DataFrames(path)
            md = test.get_dist_gaze_pointer()
            v = test.get_gaze_velocity()
            for j in range(15):
                x += md[j][1:]
                y += v[j][1:]

        x = pd.Series(x)
        y = pd.Series(y)

        xLQ, xHQ = get_valid_range(x)
        yLQ, yHQ = get_valid_range(y)

        x, y = x[(xLQ < x) & (x < xHQ)], y[(xLQ < x) & (x < xHQ)]
        x, y = x[(yLQ < y) & (y < yHQ)], y[(yLQ < y) & (y < yHQ)]

        print(x.corr(y))

        plt.plot(x, y, "o")
        plt.show()

