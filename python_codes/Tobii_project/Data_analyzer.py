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

    TODO:
    1. 視線とポインタの距離を計算してみる -> MEとの相関が計算できそう

"""

import pandas as pd
import numpy as np
from Data_store import DataFrames
from New_tester import Tester
import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
from stdlib import MyLibrary as lib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import concurrent.futures
from multiprocessing import Pool


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

    def __init__(self, path, center):
        """
        コンストラクタです。分析するexcelファイルのパスを受け取ります。

        Parameters
        ----------
        path : str
            excelファイルのファイルパスです
        """
        self.__data = DataFrames(path, flattening_range=5)
        self.path = path
        self.__cods = self.__data.get_cods()
        self.__angles = self.__data.get_angles()
        self.__gaze_cods = self.__data.get_gaze_cods()
        self.__order = self.__data.get_orders()
        self.__dist = self.__data.get_dist_gaze_pointer()
        self.__time = self.__data.get_time()
        self.__timestamp = self.__data.get_timestamp()
        self.__tgt_radius = Tester.getTgtRadius()
        self.__outliers = self.__data.get_outlier_index()
        self.__cx = center[0]
        self.__cy = center[1]

    def _MD_counter(self):
        """
        Mean Distance := 視線交点とポインタ座標の距離の平均
        :return: MDを計15回分計算したlist型
        """

        MD = []
        for i in range(15):
            tmp = np.mean(self.__dist[i])
            MD.append(tmp)

        return MD

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
            dst_x = self.__cx + 200 * np.cos(np.pi * tgt_num / 8)
            dst_y = self.__cy + 200 * np.sin(np.pi * tgt_num / 8)

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
        x_prev = int(self.__cx + 200 * np.cos(np.pi * self.__order[i] / 8))
        y_prev = int(self.__cy + 200 * np.sin(np.pi * self.__order[i] / 8))

        x_tgt = int(self.__cx + 200 * np.cos(np.pi * self.__order[i+1] / 8))
        y_tgt = int(self.__cy + 200 * np.sin(np.pi * self.__order[i+1] / 8))

        # print(x_prev, y_prev, " -> ", x_tgt, y_tgt)

        a = -(y_tgt - y_prev)
        b = (x_tgt - x_prev)
        c = -x_tgt * y_prev + y_tgt * x_prev

        return a, b, c

    def __show_route_initialize(self):
        pygame.init()
        screen_size = (1920, 1080)
        screen = pygame.display.set_mode(screen_size)
        screen.fill((255, 255, 255))

        return screen

    def __show_route(self, count, screen):
        """
        取得した座標データを利用して軌跡を表示する関数です。見る必要が無い場合はこの関数を
        コメントアウトしてください。
        """

        x_prev = int(self.__cx + 200 * np.cos(np.pi * self.__order[count] / 8))
        y_prev = int(self.__cy + 200 * np.sin(np.pi * self.__order[count] / 8))

        x_tgt = int(self.__cx + 200 * np.cos(np.pi * self.__order[count + 1] / 8))
        y_tgt = int(self.__cy + 200 * np.sin(np.pi * self.__order[count + 1] / 8))

        pygame.draw.circle(screen, (0, 0, 0), (x_prev, y_prev), self.__tgt_radius, width=2)
        pygame.draw.circle(screen, (0, 0, 0), (x_tgt, y_tgt), self.__tgt_radius, width=2)
        pygame.draw.line(screen, (0, 0, 0), (x_prev, y_prev), (x_tgt, y_tgt), width=2)

        x_route = self.__cods['x'][count]
        y_route = self.__cods['y'][count]

        gaze_x_route = self.__gaze_cods['x'][count]
        gaze_y_route = self.__gaze_cods['y'][count]

        for px, py, gx, gy in zip(x_route, y_route, gaze_x_route, gaze_y_route):
            px, py, gx, gy = int(px), int(py), int(gx), int(gy)
            pygame.draw.circle(screen, (242, 132, 52), (int(px), int(py)), 5)
            gx1, gy1 = gx - 5, gy - 5
            gx2, gy2 = gx + 5, gy - 5
            gx3, gy3 = gx - 5, gy + 5
            gx4, gy4 = gx + 5, gy + 5
            pygame.draw.line(screen, color=(122, 25, 255), start_pos=(gx1, gy1), end_pos=(gx4, gy4), width=5)
            pygame.draw.line(screen, color=(122, 25, 255), start_pos=(gx2, gy2), end_pos=(gx3, gy3), width=5)

            pygame.time.delay(10)
            pygame.display.update()
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    screen.fill((255, 255, 255))
                    return

                if event.type == QUIT:
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

    def _gaze_MV_ME_MO_counter(self):
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

            x_cods = self.__gaze_cods['x'][i]
            y_cods = self.__gaze_cods['y'][i]

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

            x_prev = int(self.__cx + 200 * np.cos(np.pi * self.__order[i] / 8))
            y_prev = int(self.__cy + 200 * np.sin(np.pi * self.__order[i] / 8))

            x_tgt = int(self.__cx + 200 * np.cos(np.pi * self.__order[i + 1] / 8))
            y_tgt = int(self.__cy + 200 * np.sin(np.pi * self.__order[i + 1] / 8))

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

    def _mean_tlead_counter(self):
        mt = []
        for i in range(15):
            tlead = self.__data.get_tlead()[i]
            mean_tlead = np.nanmean(tlead)
            mt.append(mean_tlead)

        return mt

    def _corr_counter(self):
        x_corr = []
        y_corr = []

        for i in range(15):
            px, py = self.__cods['x'][i], self.__cods['y'][i]
            gx, gy = self.__gaze_cods['x'][i], self.__gaze_cods['y'][i]

            px = pd.Series(px)
            py = pd.Series(py)
            gx = pd.Series(gx)
            gy = pd.Series(gy)

            cx, cy = px.corr(gx), py.corr(gy)

            x_corr.append(cx)
            y_corr.append(cy)

        return x_corr, y_corr

    def param_tlead_corr(self):
        x, y = [], []
        sampling_range = 1
        for i in range(15):
            a, b, c = self.__ideal_route(i)

            x_cods = self.__cods['x'][i]
            y_cods = self.__cods['y'][i]
            t = self.__timestamp[i]

            dist = np.array([abs(a * x + b * y + c) / np.sqrt(a ** 2 + b ** 2) for x, y in zip(x_cods, y_cods)])

            dist_dt = [(dist[j+1] - dist[j])/(t[j+1] - t[j]) for j in range(len(dist)-1)]

            tlead = self.__data.get_tlead()[i]
            tlead = [0 if t < 0 else 1 for t in tlead]  # 0:視線追従, 1:視線先行

            # md = self.__data.get_dist_gaze_pointer()[i][1:]

            print(tlead.count(0), tlead.count(1))

            x.append(dist_dt)
            y.append(tlead)
        x = np.hstack(x)
        plt.hist(x)
        plt.show()
        y = np.hstack(y)
        x_test = x.reshape(-1, 1)
        y_test = y
        # x, y = np.hstack(x), np.hstack(y)

        lr = LogisticRegression()
        lr.fit(x_test, y_test)

        w0 = lr.intercept_[0]
        w1 = lr.coef_[0][0]

        p = lambda v: 1/(1 + np.exp(-(w0+w1*v)))

        x_range = np.arange(min(x), max(x), 0.01)
        prediction = np.array([p(x_) for x_ in x_range])
        plt.plot(x, y, "o")
        plt.plot(x_range, prediction)
        plt.xlabel("tracking error $|y_i|$")
        plt.ylabel("$t_lead$")
        plt.show()

    def check_route(self):
        """
        計15回分の軌跡を表示できるmethodです。publicにしてあります。
        """
        screen = self.__show_route_initialize()
        for i in range(15):
            self.__show_route(i, screen)

    def __data_cleansing(self, df):
        pd.set_option('display.max_rows', 500)
        # print(df)
        # print("outliers:", self.__outliers)
        df = df.dropna(how="any")
        df = df[df.gaze_MV > 0]
        df = df[df.x_corr > 0]
        df = df[df.y_corr > 0]
        df = df.drop(self.__outliers)
        # print("|\n|\n\\/")
        # print(df)
        # print("--------------")
        return df

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
        gaze_MV, gaze_ME, gaze_MO = self._gaze_MV_ME_MO_counter()
        TP = self._TP_counter()
        MDC = self._MDC_counter()
        ODC = self._ODC_counter()
        roll_max, pitch_max = self._max_angle_counter()
        roll_mean, pitch_mean = self._mean_angle_counter()
        MD = self._MD_counter()
        mean_tlead = self._mean_tlead_counter()
        x_corr, y_corr = self._corr_counter()

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
            'mean_pitch': pitch_mean,
            'MD': MD,
            'gaze_MV': gaze_MV,
            'gaze_ME': gaze_ME,
            'gaze_MO': gaze_MO,
            'mean_tlead': mean_tlead,
            'x_corr': x_corr,
            'y_corr': y_corr
        })
        df = self.__data_cleansing(df)
        return df


class ExecuteAnalysis:

    def __init__(self):
        pass

    def data_cleansing(self, df):
        df = df.dropna()
        df = df[df.gaze_MV > 0]
        df = df[df.x_corr > 0]
        df = df[df.y_corr > 0]
        return df

    def test(self, subject, param):
        center = (1920 // 2, 1080 // 2)
        test = Analyzer(".\\data\\" + subject + "\\" + param + "\\test1.xlsx", center)
        df = test.getDataFrame()
        for i in range(2, 21):
            path = ".\\data\\" + subject + "\\" + param + "\\test" + str(i) + ".xlsx"
            t = Analyzer(path, center)
            df = df.append(t.getDataFrame(), ignore_index=True)
        print(df)
        df.to_excel(".\\data\\" + subject + "\\" + param + "\\summary.xlsx")

    def get_params(self):
        args = []
        subject = ["Nishigaichi"]
        param = ["linear_10", "mouse"]

        for s in subject:
            for p in param:
                args.append((s, p))

        return args

    def test_wrapper(self, a):
        self.test(*a)


if __name__ == "__main__":
    t = ExecuteAnalysis()
    args = t.get_params()

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executer:
        executer.map(t.test_wrapper, args)

    def corr_check():
        center = (1920//2, 1080//2)
        path = ".\\data\\Murakami\\linear_10\\test15.xlsx"
        test = Analyzer(path, center)

        test.param_tlead_corr()
    # corr_check()

    def analyze(param_x, param_y):
        modes = ["linear", "sqrt"]
        for mode in modes:
            df = pd.read_excel(".\\data\\Uchino\\" + mode + "_10\\summary.xlsx")
            print(df)
            x = df[param_x]
            xLQ, xHQ = lib.get_valid_range(x)
            y = df[param_y]
            yLQ, yHQ = lib.get_valid_range(y)
            x, y = x[(xLQ < x) & (x < xHQ)], y[(xLQ < x) & (x < xHQ)]
            x, y = x[(yLQ < y) & (y < yHQ)], y[(yLQ < y) & (y < yHQ)]
            plt.plot(x, y, "o", alpha=0.3, label=mode)

        # a, b = np.polyfit(x, y, 1)
        # l = [a*x_ + b for x_ in x]
        # plt.plot(x2, y2, "o", alpha=0.5)
        # plt.plot(x, z, "o")
        # plt.plot(x, l, "-", label="$y=$" + str(a)[0:6] + "$x+$" + str(b)[0:6])
        # plt.title("corr= " + str(x.corr(y)))
        plt.xlim(0, 150)
        # plt.ylim(0, 1.5)
        plt.xlabel("Mean Distance Between Gaze and Position[px]")
        # plt.ylabel("Throughput[bits/sec]")
        plt.legend()
        plt.show()

    # analyze("MD", "ME")

    def route_checker():
        path = ".\\data\\Murakami\\linear_10\\test15.xlsx"
        center = (1920//2, 1080//2)
        test = Analyzer(path, center)

        test.check_route()

    # route_checker()
    # analyze()
