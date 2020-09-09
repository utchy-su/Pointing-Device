import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Data_store import DataFrames
from Data_analyzer import Analyzer

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
    maxRolls : list
        各ルートについて、クリック動作時のロール角の最大値を格納します。
    maxPitchs : list
        各ルートについて、クリック動作時のピッチ角の最大値を格納します。

    """

    def __init__(self, path):
        """
        コンストラクタです。pathには各動作則・ゲインを解析したあとのsummary.xlsxを指定
        """
        self.__df = pd.read_excel(path)
        print(self.__df.columns)
        self.__meanEachRoute = { "TRE":[], "ME":[], "Throughput":[], "maxRolls":[], "maxPitchs":[]}
        self.__stdEachRoute = { "TRE":[], "ME":[], "Throughput":[], "maxRolls":[], "maxPitchs":[]}
        self.__calculateMeanForEachRoute()

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
            self.__meanEachRoute["maxRolls"].append(self.__df[self.__df.click == i].max_roll.mean())
            self.__meanEachRoute["maxPitchs"].append(self.__df[self.__df.click == i].max_pitch.mean())

            self.__stdEachRoute["TRE"].append(self.__df[self.__df.click == i].TRE.std())
            self.__stdEachRoute["ME"].append(self.__df[self.__df.click == i].ME.std())
            self.__stdEachRoute["Throughput"].append(self.__df[self.__df.click == i].Throughput.std())
            self.__stdEachRoute["maxRolls"].append(self.__df[self.__df.click == i].max_roll.std())
            self.__stdEachRoute["maxPitchs"].append(self.__df[self.__df.click == i].max_pitch.std())

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
        x = self.__df[param]

        # plt.xlim(0, 40)
        plt.hist(x, bins=20)
        plt.show()

    def plotMeans(self, param):
        criterion = self.__meanEachRoute[param]
        std = self.__stdEachRoute[param]
        x = np.arange(0, len(criterion), 1)

        plt.plot(x, criterion, '-o', label=param, color="black")
        plt.errorbar(x, criterion, yerr=std, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5 ,ls="none")
        plt.legend()
        # plt.ylim(0,  * 1.2)
        # plt.grid()
        plt.show()

    def showRoutes(self):
        


if __name__ == "__main__":
    import sys
    param = sys.argv[1]
    test = Route_analyzer("./Nishigaichi/Linear/gain_10/summary.xlsx")
    test.plotHist(param)
    test.plotMeans(param)
    test.plotCorr("max_pitch", "max_roll")
