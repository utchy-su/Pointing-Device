import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from Data_store import DataFrames

class Analyzer:
    TGT_RADIUS = 30  # radius of the target

    def __init__(self, path):
        self.__data = DataFrames(path)
        self.__cods = self.__data.get_cods()
        self.__order = self.__data.get_orders()
        self.__time = self.__data.get_time()

    def __TRE_counter(self):
        TRE = []

        for i in range(1, 15):
            tgt_num = self.__order[i]
            dst_x = 450 + 200 * np.cos(np.pi * tgt_num / 8)
            dst_y = 450 + 200 * np.sin(np.pi * tgt_num / 8)

            x_cods = self.__cods['x'][i-1]
            y_cods = self.__cods['y'][i-1]

            distance = [np.sqrt((x - dst_x) ** 2 + (y - dst_y) ** 2) for x, y in zip(x_cods, y_cods)]

            outer_evac = 0
            inner_entry = 0

            for count in range(len(distance) - 1):
                if distance[count] >= 30 and distance[count + 1] <= 30:
                    inner_entry += 1

                if distance[count] <= 30 and distance[count + 1] >= 30:
                    outer_evac += 1

            TRE.append((outer_evac + inner_entry - 1)/2)

        return TRE



    def __ideal_route(self, i):
        """
        a helper method to
        """
        x_prev = int(450 + 200 * np.cos(np.pi * self.__order[i-1] / 8))
        y_prev = int(450 + 200 * np.sin(np.pi * self.__order[i-1] / 8))

        x_tgt = int(450 + 200 * np.pi * self.__order[i] / 8)
        y_tgt = int(450 + 200 * np.pi * self.__order[i] / 8)

        a = -(y_tgt - y_prev)
        b = (x_tgt - x_prev)
        c = -x_tgt * y_prev + y_tgt * x_prev

        return a, b, c



    def __TAC_counter(self):
        TAC = []

        for i in range(1, 15):
            a, b, c = self.__ideal_route(i)
            x_cods = self.__cods['x'][i-1]
            y_cods = self.__cods['y'][i-1]

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

        for i in range(1, 15):
            a, b, c = self.__ideal_route(i)

            x_cods = self.__cods['x'][i-1]
            y_cods = self.__cods['y'][i-1]

            distance = np.array([abs(a * x + b * y + c) / np.sqrt(a ** 2 + b ** 2) for x, y in zip(x_cods, y_cods)])
            sgn = ([np.sign(a*x + b*y + c) for x, y in zip(x_cods, y_cods)])
            signed_distance = distance*sgn

            mv = np.var(distance)
            me = np.mean(distance)
            mo = np.mean(signed_distance)

            MV.append(mv)
            ME.append(me)
            MO.append(mo)

        return MV, ME, MO

    def __MDC_counter(self):

        MDC = []

        for i in range(1, 15):
            a, b, c = self.__ideal_route(i)

            x_cods = self.__cods['x'][i - 1]
            y_cods = self.__cods['y'][i - 1]

            distance = np.array([abs(a * x + b * y + c) / np.sqrt(a ** 2 + b ** 2) for x, y in zip(x_cods, y_cods)])

            d_distance = [distance[k + 1] - distance[k] for k in range(len(distance)-1)]

            mdc = 0
            for j in range(len(d_distance) - 1):
                if np.sign(d_distance[j+1]) != np.sign(d_distance[j]):
                    mdc += 1

            MDC.append(mdc)

        return MDC

    def __ODC_counter(self):
        ODC = []

        for i in range(1, 15):
            a, b, c = self.__ideal_route(i)

            a, b, c = b, -a, (-b*450 + a*450)

            x_cods = self.__cods['x'][i - 1]
            y_cods = self.__cods['y'][i - 1]

            distance = np.array([abs(a*x + b*y + c) / np.sqrt(a** 2 + b** 2) for x, y in zip(x_cods, y_cods)])

            d_distance = [distance[cnt + 1] - distance[cnt] for cnt in range(len(distance) - 1)]

            odc = 0
            for j in range(len(d_distance) - 1):
                if np.sign(d_distance[j + 1]) != np.sign(d_distance[j]):
                    odc += 1

            ODC.append(odc)

        return ODC

    def __TP_counter(self):
        Throughput = []

        for i in range(1, 15):
            MT = self.__time[i-1]

            x_prev = int(450 + 200 * np.cos(np.pi * self.__order[i - 1] / 8))
            y_prev = int(450 + 200 * np.sin(np.pi * self.__order[i - 1] / 8))

            x_tgt = int(450 + 200 * np.cos(np.pi * self.__order[i] / 8))
            y_tgt = int(450 + 200 * np.sin(np.pi * self.__order[i] / 8))

            dist = np.sqrt((x_tgt-x_prev)**2 + (y_tgt-y_prev)**2)

            ID = np.log2(dist/60 + 1)

            tp = ID/MT

            Throughput.append(tp)

        return Throughput

    def main(self):
        TRE = self.__TRE_counter()
        TAC = self.__TAC_counter()
        MV, ME, MO = self.__MV_ME_MO_counter()
        TP = self.__TP_counter()
        MDC = self.__MDC_counter()
        ODC = self.__ODC_counter()

        df = pd.DataFrame({
            'click': np.arange(1, 15, 1),
            'TRE': TRE,
            'TAC': TAC,
            'MV': MV,
            'ME': ME,
            'MO': MO,
            'MDC': MDC,
            'ODC': ODC,
            'Throughput': TP
        })

        return df


if __name__ == "__main__":
    test = Analyzer('./linear1.xlsx')
    df = test.main()
    df.to_excel("./this_is_test.xlsx")
    print(df)
