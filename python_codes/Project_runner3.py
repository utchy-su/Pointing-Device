import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Data_analyzer import Analyzer
import sys

class Project_Runner3:

    def __init__(self, path):
        self.__path = path
        self.__linear_data = pd.DataFrame(columns=['click', 'TRE', 'TAC', 'MV', 'ME', 'MO', 'MDC', 'ODC', 'Throughput', 'max roll', 'max pitch'])

    def __analyze_linear(self):

        for i in range(1, 51, 1):
            path = self.__path + "/Linear/gain_10/attempt" + str(i) + ".xlsx"

            print("now: " + path)

            analyzer = Analyzer(path)

            df = analyzer.main()

            self.__linear_data = self.__linear_data.append(df, ignore_index=True)

        self.__linear_data.to_excel(self.__path + "/Linear/gain_10/summary.xlsx")

    def main(self):
        self.__analyze_linear()


if __name__ == "__main__":
    path = "./Nishigaichi"
    test = Project_Runner3(path)
    test.main()
