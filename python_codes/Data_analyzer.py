"""Data_analyzer.pyの機能に関して

    * Author : S.Uchino
    * Data_analyzerクラスは座標データから以下の情報を計算します。
        - TRE(Target Re-Entry): ターゲットの円にカーソルが再進入した回数
        - TAC(Task Axis Crossing): なぞり経路を横切った回数
        - MDC(Movement Direction Change): なぞり経路に垂直な方向に進行方向が変化した回数
        - ODC(Orthogonal Direction Change): なぞり経路に沿った方向に進行方向が変化した回数
        - ME(Movement Error): ズレ絶対値の平均 Σ|y_i|/n
        - MV(Movement Variability):　ズレの標準偏差 √(Σ(y_i-y')/n)
        - MO(Movement Offset): ズレの平均　Σy_i/n
        - Throughput: 各タスクの時間的なパフォーマンス指標

    * TRE,TAC,...など色々指標が出てきますが、全て論文に依拠しています。詳しくは
        "Accuracy Measures for Evaluating Computer Pointing Devices - I.Scott MacKenzie et.al."
        を参考にしてください

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from Data_store import DataFrames
from New_tester import Tester
import pygame
from pygame.locals import *
import sys
import warnings

class Analyzer:
    """
    Data_storeクラスから座標データ・時間データを受け取り、分析するクラスです。。

    Attributes
    ----------
    data : Data_store object
        Data_storeクラスのインスタンス
    cods : dict
        座標データ
    order : list
        円をクリックする順番
    time : list
        時間データ
    tgt_radius : int
        ターゲット円の半径
    """

    def __init__(self, path):
        """
        コンストラクタです。分析するexcelファイルのパスを受け取ります。

        Parameters
        ----------
        path : str
            excelファイルのファイルパスです
        """
        self.__data = DataFrames(path)
        self.__cods = self.__data.get_cods()
        self.__angles = self.__data.get_angles()
        self.__order = self.__data.get_orders()
        self.__time = self.__data.get_time()
        self.__tgt_radius = Tester.getTgtRadius()

        print("Analyzing: " + path)
        print("target circle's radius is set to: ", self.__tgt_radius)

    def _TRE_counter(self):
        """
        TREを計算して、リストとしてreturnします。

        Returns
        -------
        TRE : list
            TREを計15回分の格納したlist型
        """
        TRE = []

        for i in range(15):
            tgt_num = self.__order[i + 1]
            dst_x = 450 + 200 * np.cos(np.pi * tgt_num / 8)
            dst_y = 450 + 200 * np.sin(np.pi * tgt_num / 8)

            x_cods = self.__cods['x'][i]
            y_cods = self.__cods['y'][i]

            distance = [np.sqrt((x - dst_x) ** 2 + (y - dst_y) ** 2) for x, y in zip(x_cods, y_cods)]

            outer_evac = 0
            inner_entry = 0

            for count in range(len(distance) - 1):
                if distance[count] >= 30 and distance[count + 1] <= 30:
                    inner_entry += 1

                if distance[count] <= 30 and distance[count + 1] >= 30:
                    outer_evac += 1

            TRE.append((outer_evac + inner_entry)//2)

        return TRE



    def __ideal_route(self, i):
        """
        task axisを表すような直線をax + by + c = 0として計算して、各係数a,b,cをreturn

        Parameters
        ----------
        i : int
            今何回目のクリックについて見ているか

        Returns
        -------
        a, b, c : int
            ax + by + c = 0の係数
        """
        x_prev = int(450 + 200 * np.cos(np.pi * self.__order[i] / 8))
        y_prev = int(450 + 200 * np.sin(np.pi * self.__order[i] / 8))

        x_tgt = int(450 + 200 * np.cos(np.pi * self.__order[i+1] / 8))
        y_tgt = int(450 + 200 * np.sin(np.pi * self.__order[i+1] / 8))

        # print(x_prev, y_prev, " -> ", x_tgt, y_tgt)

        a = -(y_tgt - y_prev)
        b = (x_tgt - x_prev)
        c = -x_tgt * y_prev + y_tgt * x_prev

        return a, b, c

    def __show_route_initialize(self):
        pygame.init()

    def __show_route(self, count):
        """
        取得した座標データを利用して軌跡を表示する関数です。見る必要が無い場合はこの関数を
        コメントアウトしてください。
        """
        screen_size = (900, 900)
        screen = pygame.display.set_mode(screen_size)
        screen.fill((255, 255, 255))

        x_prev = int(450 + 200 * np.cos(np.pi * self.__order[count] / 8))
        y_prev = int(450 + 200 * np.sin(np.pi * self.__order[count] / 8))

        x_tgt = int(450 + 200 * np.cos(np.pi * self.__order[count + 1] / 8))
        y_tgt = int(450 + 200 * np.sin(np.pi * self.__order[count + 1] / 8))

        pygame.draw.circle(screen, (255, 0, 0), (x_prev, y_prev), self.__tgt_radius)
        pygame.draw.circle(screen, (255, 0, 0), (x_tgt, y_tgt), self.__tgt_radius)
        pygame.draw.line(screen, (20, 128, 20), (x_prev, y_prev), (x_tgt, y_tgt), 5)

        x_route = self.__cods['x'][count]
        y_route = self.__cods['y'][count]

        for x, y in zip(x_route, y_route):
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1)


        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pygame.quit()
                    return



    def _TAC_counter(self):
        """
        TACを計算してリストとして格納してreturnします。

        Returns
        -------
        TAC : list
            計15回分のTACをlist型にしてreturn
        """
        TAC = []

        for i in range(15):
            a, b, c = self.__ideal_route(i)
            x_cods = self.__cods['x'][i]
            y_cods = self.__cods['y'][i]

            sgn = [np.sign(a*x + b*y + c) for x, y in zip(x_cods, y_cods)]

            count = 0
            for j in range(1, len(sgn)-2):
                if (sgn[j-1] == sgn[j]) and (sgn[j] != sgn[j+1]) and (sgn[j+1] == sgn[j+2]):
                    count += 1

            TAC.append(count)

        return TAC

    def _MV_ME_MO_counter(self):
        """
        MV, ME, MOを計算してそれぞれlist型としてreturnします

        Returns
        -------
        MV, ME, MO : list
            各15回分のMV，ME, MOをlistとしてreturn
        """
        MV = []
        ME = []
        MO = []

        for i in range(15):
            a, b, c = self.__ideal_route(i)

            x_cods = self.__cods['x'][i]
            y_cods = self.__cods['y'][i]

            distance = np.array([abs(a * x + b * y + c) / np.sqrt(a ** 2 + b ** 2) for x, y in zip(x_cods, y_cods)])
            x = np.arange(0, len(distance))
            # plt.plot(x, distance)
            # plt.show()
            sgn = ([np.sign(a*x + b*y + c) for x, y in zip(x_cods, y_cods)])
            signed_distance = distance*sgn

            # print("distance:")
            # print(distance)
            mv = np.sqrt(np.var(distance))
            me = np.mean(distance)
            mo = np.mean(signed_distance)

            MV.append(mv)
            ME.append(me)
            MO.append(mo)

        return MV, ME, MO

    def _MDC_counter(self):
        """
        MDCを計算してlistとしてreturn

        Returns
        -------
        MDC : list
            MDCの各15回分を含むlist型
        """

        MDC = []

        for i in range(15):
            # self.__show_route(i)
            a, b, c = self.__ideal_route(i)

            x_cods = self.__cods['x'][i]
            y_cods = self.__cods['y'][i]

            distance = np.array([abs(a * x + b * y + c) / np.sqrt(a ** 2 + b ** 2) for x, y in zip(x_cods, y_cods)])
            len_distance = np.arange(0, len(distance), 1)

            # plt.plot(len_distance, distance)
            # plt.show()
            d_distance = [distance[k + 1] - distance[k] for k in range(len(distance)-1)]

            mdc = 0
            for j in range(len(d_distance) - 1):
                if np.sign(d_distance[j+1]) != np.sign(d_distance[j]):
                    mdc += 1

            MDC.append(mdc)

        return MDC

    def _ODC_counter(self):
        """
        ODCを計算してlistとしてreturn

        Returns
        -------
        ODC : list
            MDCの各15回分を含むlist型
        """
        ODC = []

        for i in range(15):
            a, b, c = self.__ideal_route(i)

            a, b, c = b, -a, (-b*450 + a*450)

            x_cods = self.__cods['x'][i]
            y_cods = self.__cods['y'][i]

            distance = np.array([abs(a*x + b*y + c) / np.sqrt(a** 2 + b** 2) for x, y in zip(x_cods, y_cods)])

            d_distance = [distance[k + 1] - distance[k] for k in range(len(distance) - 1)]

            odc = 0
            for j in range(len(d_distance) - 1):
                if np.sign(d_distance[j + 1]) != np.sign(d_distance[j]):
                    odc += 1

            ODC.append(odc)

        return ODC

    def _TP_counter(self):
        """
        Throughput(TP)を各15回分計算してlist型としてreturn

        Throughput : list
            Throughputの各15回分を計算したlist
        """
        Throughput = []

        for i in range(15):
            MT = self.__time[i]

            x_prev = int(450 + 200 * np.cos(np.pi * self.__order[i] / 8))
            y_prev = int(450 + 200 * np.sin(np.pi * self.__order[i] / 8))

            x_tgt = int(450 + 200 * np.cos(np.pi * self.__order[i + 1] / 8))
            y_tgt = int(450 + 200 * np.sin(np.pi * self.__order[i + 1] / 8))

            dist = np.sqrt((x_tgt-x_prev)**2 + (y_tgt-y_prev)**2)

            ID = np.log2(dist/60 + 1)

            tp = ID/MT

            Throughput.append(tp)

        return Throughput

    def _max_angle_counter(self):
        roll_max_angles = []
        pitch_max_angles = []

        for i in range(15):
            roll_max = max((abs(min(self.__angles["roll"][i])), max(self.__angles["roll"][i])))
            pitch_max = max((abs(min(self.__angles["pitch"][i])), max(self.__angles["pitch"][i])))

            roll_max_angles.append(roll_max)
            pitch_max_angles.append(pitch_max)

        return roll_max_angles, pitch_max_angles

    def _mean_angle_counter(self):
        roll_mean = []
        pitch_mean = []
        for i in range(15):
            # print(np.mean(self.__angles["roll"][i]))
            roll = np.mean(self.__angles["roll"][i])
            pitch = np.mean(self.__angles["pitch"][i])

            roll_mean.append(roll)
            pitch_mean.append(pitch)

        return roll_mean, pitch_mean

    def check_route(self):
        """
        計15回分の軌跡を表示できるmethodです。publicにしてあります。
        """
        for i in range(15):
            self.__show_route(i)


    def getDataFrame(self):
        """
        TRE, TAC,...を計算してpandasのデータフレームに格納します。

        Returns
        -------
        df : pandas DataFrame object
            TRE, TAC等を表っぽいデータとしてreturnします。
        """
        TRE = self._TRE_counter()
        TAC = self._TAC_counter()
        MV, ME, MO = self._MV_ME_MO_counter()
        TP = self._TP_counter()
        MDC = self._MDC_counter()
        ODC = self._ODC_counter()
        roll_max, pitch_max = self._max_angle_counter()
        roll_mean, pitch_mean = self._mean_angle_counter()

        df = pd.DataFrame({
            'click': np.arange(1, 16),
            'TRE': TRE,
            'TAC': TAC,
            'MV': MV,
            'ME': ME,
            'MO': MO,
            'MDC': MDC,
            'ODC': ODC,
            'Throughput': TP,
            'max_roll': roll_max,
            'max_pitch': pitch_max,
            'mean_roll': roll_mean,
            'mean_pitch': pitch_mean
        })

        return df


class Analyzer2(Analyzer):

    def __init__(self, path, ME_cutoff, TRE_cutoff, TP_cutoff):
        super().__init__(path)
        self.ME_cutoff = ME_cutoff
        self.TRE_cutoff = TRE_cutoff
        self.TP_cutoff = TP_cutoff


    def main(self):
        TRE = self._TRE_counter()
        TAC = self._TAC_counter()
        MV, ME, MO = self._MV_ME_MO_counter()
        TP = self._TP_counter()
        MDC = self._MDC_counter()
        ODC = self._ODC_counter()

        df = pd.DataFrame({
            'click': np.arange(1, 16),
            'TRE': TRE,
            'TAC': TAC,
            'MV': MV,
            'ME': ME,
            'MO': MO,
            'MDC': MDC,
            'ODC': ODC,
            'Throughput': TP
        })

        countAll = len(df)

        df = df[df.ME <= self.ME_cutoff]
        df = df[df.TRE <= self.TRE_cutoff]
        df = df[df.Throughput >= self.TP_cutoff]

        countValid = len(df)

        return countAll, countValid


if __name__ == "__main__":

    def unit_test():
        path = "./test.xlsx"
        # 例：New_tester.pyによってデスクトップにtest.xlsxが作成されたなら
        #    C:Users/FUFITSU/Desktop/test.xlsxに変更してください
        test = Analyzer(path)
        df = test.main()

        print(df)  #データを分析した結果がコンソールに表示されます。

    unit_test()
