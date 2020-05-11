import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

class DataFrames:
    """
    Get the data from given path. This holds the data as private fields
    Use getter method to pass the data to the other object.
    """

    def __init__(self, path):
        self.__path = path
        self.__data = pd.read_excel(self.__path)
        self.__orders = self.__data['orders']
        self.__cods = {'x':[], 'y':[]}
        self.__time = []
        self.__cods_calculator()  # 座標データをcodsに格納
        self.__time_calculator()  # 各タスクにかかった時間をtimeに格納

    def __cods_calculator(self) -> None:
        """
        get the coordinates from the data
        @return : a list of a list containining coordinates
        """

        for i in range(1, 15):
            tgt_num = self.__orders[i]
            x_destination = 450 * 200 * np.cos(np.pi * tgt_num / 8)
            y_destination = 450 * 200 * np.sin(np.pi * tgt_num / 8)

            x_index = 'x from ' + str(i) + ' to ' + str(i+1)
            y_index = 'y from ' + str(i) + ' to ' + str(i+1)

            x_cods = self.__data[x_index].dropna(how='all')
            y_cods = self.__data[y_index].dropna(how='all')

            x_cods = [np.mean(x_cods[j:j+5]) for j in range(0, len(x_cods)-5, 5)]
            y_cods = [np.mean(y_cods[j:j+5]) for j in range(0, len(y_cods)-5, 5)]

            self.__cods['x'].append(x_cods)
            self.__cods['y'].append(y_cods)

    def __time_calculator(self) -> None:
        """
        get the time spent for each task
        """
        for i in range(1, 15):
            time_index = 'time from ' + str(i) + ' to ' + str(i+1)

            time = self.__data[time_index].dropna(how="all")
            MT = (time.iloc[-1] - time.iloc[0])/1000

            self.__time.append(MT)


    def get_cods(self) -> dict:
        """
        getter method of the private property of data
        @return : data
        """
        return self.__cods

    def get_orders(self):
        """
        getter method of orders for
        """
        return self.__orders

    def get_time(self):
        """
        getter method of time spent for each task
        """

        return self.__time


if __name__ == "__main__":
    file_path = ""
    test_data = DataFrames("./linear1.xlsx")
    print(test_data.get_cods())
    print(len(test_data.get_cods()['x']))
    print(test_data.get_time())
