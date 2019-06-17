import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st


class Analyzer:

    def __init__(self, path, save_path):
        self.path = path
        self.save_path = save_path

        self.df = pd.read_excel(path)

        self.orders = self.df['orders']
        self.tgt_rad = 30  # pixels

    def __TRE_counter(self):
        TRE = []

        for i in range(1, 15):
            tgt_num = self.orders[i]
            dst_x = 450 + 200 * np.cos(np.pi * tgt_num / 8)
            dst_y = 450 + 200 * np.sin(np.pi * tgt_num / 8)

            x_index = 'x from ' + str(i) + ' to ' + str(i + 1)
            y_index = 'y from ' + str(i) + ' to ' + str(i + 1)

            x_cods = self.df[x_index].dropna(how='all')
            y_cods = self.df[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+5]) for j in range(0, len(x_cods)-5, 5)]
            y_cods = [np.mean(y_cods[j:j+5]) for j in range(0, len(y_cods)-5, 5)]

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

    def __Ideal_route(self, i):
        x_prev = int(450 + 200 * np.cos(np.pi * self.orders[i-1] / 8))
        y_prev = int(450 + 200 * np.sin(np.pi * self.orders[i-1] / 8))

        x_tgt = int(450 + 200 * np.cos(np.pi * self.orders[i] / 8))
        y_tgt = int(450 + 200 * np.sin(np.pi * self.orders[i] / 8))

        a = -(y_tgt - y_prev)
        b = (x_tgt - x_prev)
        c = -x_tgt * y_prev + y_tgt * x_prev

        # (x2 - x1)y - (y2 - y1)x + (-x2y1 + y2x1) = 0
        # ax + by + c = 0
        # implicit expression for the line

        return a, b, c

    def __TAC_counter(self):
        TAC = []

        for i in range(1, 15):
            a, b, c = self.__Ideal_route(i)

            x_index = 'x from ' + str(i) + ' to ' + str(i + 1)
            y_index = 'y from ' + str(i) + ' to ' + str(i + 1)

            x_cods = self.df[x_index].dropna(how='all')
            y_cods = self.df[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+5]) for j in range(0, len(x_cods)-5, 5)]
            y_cods = [np.mean(y_cods[j:j+5]) for j in range(0, len(y_cods)-5, 5)]

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
            a, b, c = self.__Ideal_route(i)

            x_index = 'x from ' + str(i) + ' to ' + str(i + 1)
            y_index = 'y from ' + str(i) + ' to ' + str(i + 1)

            x_cods = self.df[x_index].dropna(how='all')
            y_cods = self.df[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+5]) for j in range(0, len(x_cods)-5, 5)]
            y_cods = [np.mean(y_cods[j:j+5]) for j in range(0, len(y_cods)-5, 5)]

            # plt.plot(x_cods, y_cods)
            # x = np.arange(200, 700, 1)
            # plt.plot(x, -a/b*x + -c/b) if b != 0 else plt.axvline(450)
            # plt.xlim(0, 900)
            # plt.ylim(0, 900)
            # plt.show()
            # visual aid for accuracy validation

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
            a, b, c = self.__Ideal_route(i)

            x_index = 'x from ' + str(i) + ' to ' + str(i + 1)
            y_index = 'y from ' + str(i) + ' to ' + str(i + 1)

            x_cods = self.df[x_index].dropna(how='all')
            y_cods = self.df[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+5]) for j in range(0, len(x_cods)-5, 5)]
            y_cods = [np.mean(y_cods[j:j+5]) for j in range(0, len(y_cods)-5, 5)]

            distance = np.array([abs(a * x + b * y + c) / np.sqrt(a ** 2 + b ** 2) for x, y in zip(x_cods, y_cods)])

            d_distance = [distance[cnt+1] - distance[cnt] for cnt in range(len(distance)-1)]

            # plt.plot(np.arange(0, len(d_distance), 1), np.sign(d_distance), 'o')
            # plt.show()

            mdc = 0
            for j in range(len(d_distance) - 1):
                if np.sign(d_distance[j+1]) != np.sign(d_distance[j]):
                    mdc += 1

            MDC.append(mdc)

        return MDC

    def __ODC_counter(self):
        ODC = []

        for i in range(1, 15):
            a, b, c = self.__Ideal_route(i)
            a, b, c = b, -a, (-b*450+a*450)
            # b(x-xp) - a(y-yp)=0  ->  an orthogonal line

            x_index = 'x from ' + str(i) + ' to ' + str(i + 1)
            y_index = 'y from ' + str(i) + ' to ' + str(i + 1)

            x_cods = self.df[x_index].dropna(how='all')
            y_cods = self.df[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j + 5]) for j in range(0, len(x_cods) - 5, 5)]
            y_cods = [np.mean(y_cods[j:j + 5]) for j in range(0, len(y_cods) - 5, 5)]

            # plt.plot(x_cods, y_cods)
            # x = np.arange(200, 700, 1)
            # plt.plot(x, -a/b*x + -c/b) if b != 0 else plt.axvline(450)
            # plt.xlim(0, 900)
            # plt.ylim(0, 900)
            # plt.show()

            distance = np.array([abs(a*x + b*y + c) / np.sqrt(a** 2 + b** 2) for x, y in zip(x_cods, y_cods)])

            d_distance = [distance[cnt + 1] - distance[cnt] for cnt in range(len(distance) - 1)]

            odc = 0
            for j in range(len(d_distance) - 1):
                if np.sign(d_distance[j + 1]) != np.sign(d_distance[j]):
                    odc += 1

            ODC.append(odc)

        return ODC

    def __TS_counter(self):
        TS = []

        for i in range(1, 15):
            time_index = 'time from ' + str(i) + ' to ' + str(i+1)

            time = self.df[time_index].dropna(how='all')
            ts = (time.iloc[-1] - time.iloc[0])/1000

            TS.append(ts)

        return TS

    def __TIC_counter(self):  # average duration time that the cursor stayed in the circle
        TIC = []

        for i in range(1, 15):
            x_index = 'x from ' + str(i) + ' to ' + str(i + 1)
            y_index = 'y from ' + str(i) + ' to ' + str(i + 1)
            time_index = 'time from ' + str(i) + ' to ' + str(i + 1)

            x_tgt = int(450 + 200 * np.cos(np.pi * self.orders[i] / 8))
            y_tgt = int(450 + 200 * np.sin(np.pi * self.orders[i] / 8))

            x_cods = self.df[x_index].dropna(how='all')
            y_cods = self.df[y_index].dropna(how='all')
            t = self.df[time_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+5]) for j in range(0, len(x_cods)-5, 5)]
            y_cods = [np.mean(y_cods[j:j+5]) for j in range(0, len(y_cods)-5, 5)]
            t = [np.mean(t[j:j+5]) for j in range(0, len(t)-5, 5)]

            # check = pd.DataFrame({'x': x_cods, 'y': y_cods, 't': t})

            distance = [np.sqrt((x - x_tgt)**2 + (y-y_tgt)**2) for x, y in zip(x_cods, y_cods)]

            time_in_circle = []
            for j in range(len(distance) - 1):
                if distance[j] <= 30:
                    time_in_circle.append(t[j])

            tic = (time_in_circle[-1] - time_in_circle[0])/1000
            TIC.append(tic)
        return TIC

    def __ACV_counter(self):  # ACV: average cursor velocity
        ACV = []

        for i in range(1, 15):
            x_index = 'x from ' + str(i) + ' to ' + str(i + 1)
            y_index = 'y from ' + str(i) + ' to ' + str(i + 1)
            time_index = 'time from ' + str(i) + ' to ' + str(i + 1)

            x = self.df[x_index].dropna(how='all')
            y = self.df[y_index].dropna(how='all')
            time = self.df[time_index].dropna(how='all')

            x = [np.mean(x[cnt:cnt+5]) for cnt in range(0, len(x)-5, 5)]
            y = [np.mean(y[cnt:cnt+5]) for cnt in range(0, len(y)-5, 5)]
            time = [np.mean(time[cnt:cnt+5]) for cnt in range(0, len(time)-5, 5)]

            dx = [x[j+1] - x[j] for j in range(len(x) - 1)]
            dy = [y[j+1] - y[j] for j in range(len(y) - 1)]
            dt = [(time[j+1] - time[j])/1000 for j in range(len(time) - 1)]

            v = [np.sqrt(x**2 + y**2)/t for x, y, t in zip(dx, dy, dt)]

            ACV.append(np.mean(v))
        return ACV

    def __TP_counter(self):
        Throughput = []

        for i in range(1, 15):
            time_index = 'time from ' + str(i) + ' to ' + str(i + 1)

            time = self.df[time_index].dropna(how='all')
            MT = (time.iloc[-1] - time.iloc[0]) / 1000

            x_prev = int(450 + 200 * np.cos(np.pi * self.orders[i - 1] / 8))
            y_prev = int(450 + 200 * np.sin(np.pi * self.orders[i - 1] / 8))

            x_tgt = int(450 + 200 * np.cos(np.pi * self.orders[i] / 8))
            y_tgt = int(450 + 200 * np.sin(np.pi * self.orders[i] / 8))

            dist = np.sqrt((x_tgt-x_prev)**2 + (y_tgt-y_prev)**2)

            ID = np.log2(dist/60+1)

            tp = ID/MT

            Throughput.append(tp)

        return Throughput

    def main(self):
        TRE = self.__TRE_counter()
        TAC = self.__TAC_counter()
        MV, ME, MO = self.__MV_ME_MO_counter()
        TS = self.__TS_counter()
        TP = self.__TP_counter()
        AVC = self.__ACV_counter()
        TIC = self.__TIC_counter()
        MDC = self.__MDC_counter()
        ODC = self.__ODC_counter()

        df = pd.DataFrame({
            'click': np.arange(1, 15, 1),
            'TRE': TRE,
            'TAC': TAC,
            'TIC': TIC,
            'MDC': MDC,
            'ODC': ODC,
            'MV': MV,
            'ME': ME,
            'MO': MO,
            'AVC': AVC,
            'Time Spent': TS,
            'Throughput': TP
        })
        return df


if __name__ == '__main__':
    def data_generate():
        path = 'C:/Users/smart/Google ドライブ/Pdev_results/linear vs non-linear result/Kitamura/non-linear/'
        attempts = [path + 'attempt' + str(i) + '.xlsx' for i in np.arange(1, 26, 1)]

        df = pd.DataFrame(columns=['click', 'TRE', 'TAC', 'MV', 'ME', 'MO', 'Time Spent', 'Throughput'])

        for attempt in attempts:
            print(attempt)
            test = Analyzer(attempt, 'NA')
            data = test.main()
            df = df.append(data, ignore_index=True)

        save_path = path + 'test3.xlsx'
        df.to_excel(save_path)
        print(df)

    data_generate()

