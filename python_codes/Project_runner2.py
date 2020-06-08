import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Data_analyzer import Analyzer2
import sys

class Project_runner2:

    def __init__(self, path, me_cutoff, tre_cutoff, tp_cutoff):

        self.__directory_path = path
        self.__me_cutoff = me_cutoff
        self.__tre_cutoff = tre_cutoff
        self.__tp_cutoff = tp_cutoff

    def __analyze_linear(self):

        total, valid = [], []

        for i in range(1, 6, 1):
            path = self.__directory_path + "/linear" + str(i) + ".xlsx"
            # print("now: ", path)

            analyzer = Analyzer2(path, self.__me_cutoff, self.__tre_cutoff, self.__tp_cutoff)

            a, b = analyzer.main()
            total.append(a)
            valid.append(b)

        return total, valid

    def __analyze_model(self):

        total, valid = [], []

        for i in range(1, 6, 1):
            path = self.__directory_path + "/model" + str(i) + ".xlsx"
            # print("now: ", path)

            analyzer = Analyzer2(path, self.__me_cutoff, self.__tre_cutoff, self.__tp_cutoff)

            a, b = analyzer.main()
            total.append(a)
            valid.append(b)

        return total, valid

    def plot_trend(self):
        linear_total, linear_valid = self.__analyze_linear()
        model_total, model_valid = self.__analyze_model()

        x = np.arange(1, 6, 1)
        plt.plot(x, linear_valid, '-o', label="linear")
        plt.plot(x, model_valid, '-o', label="model")
        plt.xticks(np.arange(1, 6, 1))
        plt.axhline(15, ls="--", color="k")
        plt.legend()
        plt.ylim(0, 16)
        plt.grid()
        plt.show()

    def show_results(self):
        subjects = ["/Emi", "/Kimika", "/Mai", "/Rei", "/Toshiko"]

        linear_total, linear_valid = 0, 0
        model_total, model_valid = 0, 0
        for p in subjects:
            print("subject: ", p)
            tmp = self.__directory_path
            self.__directory_path += p

            a, b = self.__analyze_linear()
            print("individual result (linear): ", sum(b), "/", sum(a))

            c, d = self.__analyze_model()
            print("individual result (model): ", sum(d), "/", sum(c))

            linear_total += sum(a)
            linear_valid += sum(b)
            model_total += sum(c)
            model_valid += sum(d)

            self.__directory_path = tmp

        print("Linear全体の結果: ", linear_valid, "/", linear_total)
        print("Model全体の結果: ", model_valid, "/", model_total)

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 5:
        raise Exception("not enough arguments")
    file_path = args[1]
    me_cutoff = int(args[2])
    tre_cutoff = int(args[3])
    tp_cutoff = float(args[4])
    runner = Project_runner2(file_path, me_cutoff, tre_cutoff, tp_cutoff)
    runner.plot_trend()
