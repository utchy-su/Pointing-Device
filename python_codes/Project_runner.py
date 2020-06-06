import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from Data_analyzer import Analyzer
import sys

class Project_runner:

    def __init__(self, path):

        self.__directory_path = path
        self.__linear_data = pd.DataFrame(columns=['click', 'TRE', 'TAC', 'MV', 'ME', 'MO', 'MDC', 'ODC', 'Throughput'])
        self.__model_data = pd.DataFrame(columns=['click', 'TRE', 'TAC', 'MV', 'ME', 'MO', 'MDC', 'ODC', 'Throughput'])

    def __analyze_linear(self):

        for i in range(1, 6, 1):
            path = self.__directory_path + "/linear" + str(i) + ".xlsx"
            print("now: " + path)

            analyzer = Analyzer(path)

            df = analyzer.main()
            self.__linear_data = self.__linear_data.append(df, ignore_index=True)

            # print(df)

        self.__linear_data.to_excel(self.__directory_path + "/linear_outlier_removed_50.xlsx")

    def __analyze_model(self):
        for i in range(1, 6, 1):
            path = self.__directory_path + "/model" + str(i) + ".xlsx"
            print("now: " + path)

            analyzer = Analyzer(path)

            df = analyzer.main()
            self.__model_data = self.__model_data.append(df, ignore_index=True)

        self.__model_data.to_excel(self.__directory_path + "/model_outlier_removed_50.xlsx")


    def main(self):
        self.__analyze_linear()
        self.__analyze_model()

if __name__ == "__main__":
    directory_path = ""
    args = sys.argv

    if len(args) == 1:
        raise ValueError("file path not given")
    else:
        directory_path = args[1]


    runner = Project_runner(directory_path)
    runner.main()
