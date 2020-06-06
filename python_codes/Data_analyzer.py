import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from Data_store import DataFrames
from new_tester import TaskAxis
import pygame
from pygame.locals import *
import sys

class Analyzer:
    TGT_RADIUS = 30  # radius of the target

    def __init__(self, path):
        self.__data = DataFrames(path)
        self.__cods = self.__data.get_cods()
        self.__order = self.__data.get_orders()
        self.__time = self.__data.get_time()

    def __TRE_counter(self):
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
        a helper method to
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
        screen_size = (900, 900)
        screen = pygame.display.set_mode(screen_size)
        screen.fill((255, 255, 255))

        x_prev = int(450 + 200 * np.cos(np.pi * self.__order[count] / 8))
        y_prev = int(450 + 200 * np.sin(np.pi * self.__order[count] / 8))

        x_tgt = int(450 + 200 * np.cos(np.pi * self.__order[count + 1] / 8))
        y_tgt = int(450 + 200 * np.sin(np.pi * self.__order[count + 1] / 8))

        pygame.draw.circle(screen, (255, 0, 0), (x_prev, y_prev), TaskAxis.TGT_RADIUS)
        pygame.draw.circle(screen, (255, 0, 0), (x_tgt, y_tgt), TaskAxis.TGT_RADIUS)
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



    def __TAC_counter(self):
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

    def __MV_ME_MO_counter(self):
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

    def __MDC_counter(self):

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

    def __ODC_counter(self):
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

    def __TP_counter(self):
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

    def check_route(self):

        for i in range(15):
            self.__show_route(i)

    def __remove_outliers(self, df):

        df = df[df.ME <= 50]

        return df

    def main(self):
        TRE = self.__TRE_counter()
        TAC = self.__TAC_counter()
        MV, ME, MO = self.__MV_ME_MO_counter()
        TP = self.__TP_counter()
        MDC = self.__MDC_counter()
        ODC = self.__ODC_counter()

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

        df = self.__remove_outliers(df)
        # print(df)

        return df


if __name__ == "__main__":
    def data_generate():
        path = "/home/soichiro/Desktop/pdev/editing/data/Kimika/model"
        attempts = [path + str(i) + ".xlsx" for i in range(1, 6)]
        df = pd.DataFrame(columns=["click", "TRE", "TAC", "MV", "ME", "MO", "MDC", "ODC", "Throughput"])

        for data in attempts:
            test = Analyzer(data)
            data_frame = test.main()
            df = df.append(data_frame, ignore_index=True)

        # print(df)

        save_path = "/home/soichiro/Desktop/pdev/editing/data/Kimika/model_outlier_removed.xlsx"
        # df.to_excel(save_path)

    def unit_test():
        path = "/home/soichiro/Desktop/pdev/editing/data/Emi/linear1.xlsx"

        test = Analyzer(path)
        df = test.main()
        print(df)

    def check_route():
        path = "/home/soichiro/Desktop/pdev/editing/data/Emi/linear"
        attempts = [path + str(i) + ".xlsx" for i in range(1, 6)]

        for data in attempts:
            test = Analyzer(data)
            test.check_route()

    data_generate()
