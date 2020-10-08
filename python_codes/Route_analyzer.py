import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Data_store import DataFrames
from Data_analyzer import Analyzer
from New_tester import Tester, Base
import pygame
from pygame.locals import *

class Route_analyzer:
    """
    ルートごとにThroughput,TRE,MEなどの指標を評価するプログラムです。

    Attributes:
    TREs : list
        TREを各ルートに関して算出したものを格納します。
    MEs : list
        MEを各ルートに関して算出したものを格納します。
    TPs : list
        Throughputを各ルートに関して算出したものを格納します。
    meanRolls : list
        各ルートについて、クリック動作時のロール角の最大値を格納します。
    meanPitchs : list
        各ルートについて、クリック動作時のピッチ角の最大値を格納します。

    """

    def __init__(self, path):
        """
        コンストラクタです。pathには各動作則・ゲインを解析したあとのsummary.xlsxを指定
        """
        self.__df = pd.read_excel(path)
        self.__meanEachRoute = { "TRE":[], "ME":[], "Throughput":[], "meanRolls":[], "meanPitchs":[]}
        self.__stdEachRoute = { "TRE":[], "ME":[], "Throughput":[], "meanRolls":[], "meanPitchs":[]}
        self.__calculateMeanForEachRoute()

    def getMeanEachRoute(self, param):
        return self.__meanEachRoute[param]

    def getStdEachRoute(self, param):
        return self.__stdEachRoute[param]


    def __calculateMeanForEachRoute(self):
        """
        クリック==iのデータだけ抽出して平均を取る関数。
        self.__dfが各クリックに関しての総データを保持しているので、その中から特定のクリック(i.e.ルート)
        に関する情報だけ抽出します
        """
        for i in range(1, 16, 1):
            self.__meanEachRoute["TRE"].append(self.__df[self.__df.click == i].TRE.mean())
            self.__meanEachRoute["ME"].append(self.__df[self.__df.click == i].ME.mean())
            self.__meanEachRoute["Throughput"].append(self.__df[self.__df.click == i].Throughput.mean())
            self.__meanEachRoute["meanRolls"].append(self.__df[self.__df.click == i].mean_roll.mean())
            self.__meanEachRoute["meanPitchs"].append(self.__df[self.__df.click == i].mean_pitch.mean())

            self.__stdEachRoute["TRE"].append(self.__df[self.__df.click == i].TRE.std())
            self.__stdEachRoute["ME"].append(self.__df[self.__df.click == i].ME.std())
            self.__stdEachRoute["Throughput"].append(self.__df[self.__df.click == i].Throughput.std())
            self.__stdEachRoute["meanRolls"].append(self.__df[self.__df.click == i].mean_roll.std())
            self.__stdEachRoute["meanPitchs"].append(self.__df[self.__df.click == i].mean_pitch.std())

    def plotCorr(self, param1, param2):
        # x1 = pd.Series(self.__meanEachRoute[param1])
        # x2 = pd.Series(self.__meanEachRoute[param2])

        x1 = pd.Series(self.__df[param1])
        x2 = pd.Series(self.__df[param2])

        print(x1.corr(x2))

        plt.plot(x1, x2, "o", color="black")
        # plt.xlim(0, max(x1)*1.2)
        # plt.ylim(0, max(x2)*1.2)
        plt.title("corr = " + str(x1.corr(x2)))
        plt.show()

    def plotHist(self, param):
        """
        各パラメータの結果のヒストグラム
        """
        x = self.__df[param]

        # plt.xlim(0, 40)
        plt.hist(x, bins=20)
        plt.show()

    def plotMeans(self, param):
        criterion = self.__meanEachRoute[param]
        std = self.__stdEachRoute[param]
        x = np.arange(1, len(criterion)+1, 1)

        plt.plot(x, criterion, '-o', label=param, color="black")
        plt.errorbar(x, criterion, yerr=std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5 ,ls="none")
        plt.legend()
        # plt.ylim(0,  * 1.2)
        # plt.grid()
        plt.show()

    def showRoutes(self):
        pygame.init()

        screen_size = (900, 900)
        screen = pygame.display.set_mode(screen_size)
        screen.fill((255, 255, 255))
        Base(screen, screen_size, Tester.getTgtRadius(), Tester.getLayoutRadius())

        order = Tester.getOrders()

        for count in range(15):
            x_prev = int(450 + 200 * np.cos(np.pi * order[count] / 8))
            y_prev = int(450 + 200 * np.sin(np.pi * order[count] / 8))

            x_tgt = int(450 + 200 * np.cos(np.pi * order[count + 1] / 8))
            y_tgt = int(450 + 200 * np.sin(np.pi * order[count + 1] / 8))

            Throughput = int(self.__df[self.__df.click == count+1].Throughput.mean() * 10)

            # pygame.draw.circle(screen, (255, 0, 0), (x_prev, y_prev), Tester.getTgtRadius())
            # pygame.draw.circle(screen, (255, 0, 0), (x_tgt, y_tgt), Tester.getTgtRadius())
            pygame.draw.line(screen, (20, 128, 20), (x_prev, y_prev), (x_tgt, y_tgt), Throughput)

            pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pygame.quit()
                    return


def compareEachRoute(param):
    lin10 = Route_analyzer("./Nishigaichi/Linear/gain_10/summary.xlsx")
    lin20 = Route_analyzer("./Nishigaichi/Linear/gain_20/summary.xlsx")
    sqrt10 = Route_analyzer("./Nishigaichi/sqrt/gain_10/summary.xlsx")
    # sqrt10.plotAngleEachRoute()
    sqrt20 = Route_analyzer("./Nishigaichi/sqrt/gain_20/summary.xlsx")
    quad10 = Route_analyzer("./Nishigaichi/quad/gain_10/summary.xlsx")
    quad20 = Route_analyzer("./Nishigaichi/quad/gain_20/summary.xlsx")

    lin10mean = lin10.getMeanEachRoute(param)
    lin10std = lin10.getStdEachRoute(param)

    lin20mean = lin20.getMeanEachRoute(param)
    lin20std = lin20.getStdEachRoute(param)

    sqrt10mean = sqrt10.getMeanEachRoute(param)
    sqrt10std = sqrt10.getStdEachRoute(param)

    sqrt20mean = sqrt20.getStdEachRoute(param)
    sqrt20std = sqrt20.getStdEachRoute(param)

    quad10mean = quad10.getMeanEachRoute(param)
    quad10std = quad10.getStdEachRoute(param)

    quad20mean = quad20.getMeanEachRoute(param)
    quad20std = quad20.getStdEachRoute(param)

    means = [lin10mean, lin20mean, sqrt10mean, sqrt20mean, quad10mean, quad20mean]

    means = list(map(max, means))
    maxMean = max(means)

    x = np.arange(1, len(lin10mean)+1, 1)

    plt.plot(x, lin10mean, "-o", label="linear k=10", color="black")
    # plt.errorbar(x, lin10mean, yerr=lin10std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

    plt.plot(x, lin20mean, "-^", label="linear k=20", color="black")
    # plt.errorbar(x, lin20mean, yerr=lin20std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

    plt.plot(x, sqrt10mean, "-o", label="sqrt k=10", color="red")
    # plt.errorbar(x, sqrt10mean, yerr=sqrt10std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

    plt.plot(x, sqrt20mean, "-^", label="sqrt k=20", color="red")
    # plt.errorbar(x, sqrt20mean, yerr=sqrt20std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

    plt.plot(x, quad10mean, "-o", label="quad k=10", color="blue")
    # plt.errorbar(x, quad10mean, yerr=quad10std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

    plt.plot(x, quad20mean, "-^", label="quad k=20", color="blue")
    # plt.errorbar(x, quad20mean, yerr=quad20std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

    plt.xticks(x)
    # plt.ylim(0, maxMean*1.2)
    plt.grid()
    plt.ylabel(param)
    plt.xlabel("# of clicks")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    import sys
    param = sys.argv[1]
    compareEachRoute(param)
