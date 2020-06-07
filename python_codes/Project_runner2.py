import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Data_analyzer import Analyzer2
import sys

class Project_runner2:

    def __init__(self, path, me_cutoff, tre_cutoff):

        self.__directory_path = path
        self.__me_cutoff = me_cutoff
        self.__tre_cutoff = tre_cutoff

    def __analyze_linear(self):

        total, valid = 0, 0

        for i in range(1, 6, 1):
            path = self.__directory_path + "/linear" + str(i) + ".xlsx"
            print("now: ", path)

            analyzer = Analyzer2(path, self.__me_cutoff, self.__tre_cutoff)

            a, b = analyzer.main()
            total += a
            valid += b

        return total, valid

    def __analyze_model(self):

        total, valid = 0, 0

        for i in range(1, 6, 1):
            path = self.__directory_path + "/model" + str(i) + ".xlsx"
            print("now: ", path)

            analyzer = Analyzer2(path, self.__me_cutoff, self.__tre_cutoff)

            a, b = analyzer.main()
            total += a
            valid += b

        return total, valid

    def main(self):
        linear_total, linear_valid = self.__analyze_linear()
        model_total, model_valid = self.__analyze_model()

        print("Result of linear control rule: ")
        print("Valid/Total = ", linear_valid, " / ", linear_total)
        print("\n")
        print("Result of model control rule: ")
        print("Valid/Total = ", model_valid, " / ", model_total)


if __name__ == "__main__":
    args = sys.argv
    file_path = args[1]
    runner = Project_runner2(file_path, 50, 3)
    runner.main()
