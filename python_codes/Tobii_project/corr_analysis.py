import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Data_store import DataFrames


class CorrAnalysis:

    def __init__(self, path):
        self.df = DataFrames(path)

    def y_corr(self):
        y = []
        gaze_y = []

        y_list = self.df.get_cods()['y']
        gaze_y_list = self.df.get_gaze_cods()['y']

        for i in range(15):
            y += y_list[i]
            gaze_y += gaze_y_list[i]

        y = pd.Series(y)
        gaze_y = pd.Series(gaze_y)

        print("y-gaze_y corr: ", y.corr(gaze_y))

        plt.plot(y, gaze_y, "o")
        plt.xlabel("x (cursor position)")
        plt.ylabel("y (gaze position)")
        plt.title("correlation between mouse-eye positions")
        plt.show()

    def x_corr(self):
        x = []
        gaze_x = []

        x_list = self.df.get_cods()['x']
        gaze_x_list = self.df.get_gaze_cods()['x']

        for i in range(15):
            x += x_list[i]
            gaze_x += gaze_x_list[i]

        x = pd.Series(x)
        gaze_x = pd.Series(gaze_x)

        a, b = np.polyfit(x, gaze_x, 1)

        print("x-gaze_x corr: ", x.corr(gaze_x))
        plt.plot(x, gaze_x, "o")
        plt.plot(x, [a*x_i +b for x_i in x], label="y="+f"{a:3}"+"x+"+f"{b:3}")
        plt.xlabel("gaze position x")
        plt.ylabel("cursor position x")
        plt.title("correlation between mouse-eye positions")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    path = ".\\data\\Nishigaichi\\mouse\\test9.xlsx"
    test = CorrAnalysis(path)
    test.x_corr()
    test.y_corr()
