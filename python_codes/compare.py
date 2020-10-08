import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Compare:

    def __init__(self):
        self.lin10 = pd.read_excel("./Nishigaichi/Linear/gain_10/summary.xlsx")
        self.lin20 = pd.read_excel("./Nishigaichi/Linear/gain_20/summary.xlsx")

        self.sqrt10 = pd.read_excel("./Nishigaichi/sqrt/gain_10/summary.xlsx")
        self.sqrt20 = pd.read_excel("./Nishigaichi/sqrt/gain_20/summary.xlsx")

        self.quad10 = pd.read_excel("./Nishigaichi/quad/gain_10/summary.xlsx")
        self.quad20 = pd.read_excel("./Nishigaichi/quad/gain_20/summary.xlsx")

        self.data = {"linear":[self.lin10, self.lin20],
                    "sqrt": [self.sqrt10, self.sqrt20],
                    "quad": [self.quad10, self.quad20]}

    def compare_performances(self, param):
        if not isinstance(param, str):
            raise TypeError("param should be str type")

        # plt.plot(np.arange(0, len(self.lin10[param]), 1), self.lin10[param], 'o')
        # plt.plot(np.arange(0, len(self.lin20[param]), 1), self.lin20[param], 'o')

        lin10_mean = self.lin10[param].mean()
        lin20_mean = self.lin20[param].mean()

        sqrt10_mean = self.sqrt10[param].mean()
        sqrt20_mean = self.sqrt20[param].mean()

        quad10_mean = self.quad10[param].mean()
        quad20_mean = self.quad20[param].mean()

        lin10_std = self.lin10[param].std()
        lin20_std = self.lin20[param].std()

        sqrt10_std = self.sqrt10[param].std()
        sqrt20_std = self.sqrt20[param].std()

        quad10_std = self.quad10[param].std()
        quad20_std = self.quad20[param].std()

        x1 = [1, 2, 3]
        x2 = [1.3, 2.3, 3.3]

        gain10_result = (lin10_mean, sqrt10_mean, quad10_mean)
        gain10_err = (lin10_std, sqrt10_std, quad10_std)
        gain20_result = (lin20_mean, sqrt20_mean, quad20_mean)
        gain20_err = (lin20_std, sqrt20_std, quad20_std)

        plt.bar(x1, gain10_result, width=0.3, label="gain = 10", align="center")
        plt.errorbar(x1, gain10_result, yerr=gain10_err, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

        plt.bar(x2, gain20_result, width=0.3, label="gain = 20", align="center")
        plt.errorbar(x2, gain20_result, yerr=gain20_err, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

        plt.icks([1.15, 2.15, 3.15], ["linear", "sqrt", "quadratic"])

        plt.title(param + ": by each criterion")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def compare_angles(self, mode="linear", gain=10):

        if not isinstance(gain, int):
            raise TypeError("param must be int type")

        pitch = self.data[mode][gain//10-1]["mean_pitch"]
        roll = self.data[mode][gain//10-1]["mean_roll"]


        x = np.arange(0, len(pitch), 1)

        plt.plot(x, pitch, 'o', label="mean pitch")
        plt.plot(x, roll, 'o', label="mean roll")
        plt.ylim(-20, 20)

        plt.title("gain = " + str(gain))
        # plt.axhline(max(pitch), ls="--", color="black", label="max")
        plt.axhline(np.mean(pitch), ls="-.", color="black", label="mean")
        # plt.axhline(max(roll), ls="--", color="black")
        plt.axhline(np.mean(roll), ls="-.", color="black")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def show_familiality_trend(self, param):
        # roll = [np.mean(roll[j:j+self.__flattening_range]) for j in range(0, len(roll)-self.__flattening_range, self.__flattening_range)]

        lin10 = [np.mean(self.lin10[param][j:j+75]) for j in range(0, len(self.lin10[param])-75, 75)]
        lin20 = [np.mean(self.lin20[param][j:j+75]) for j in range(0, len(self.lin20[param])-75, 75)]

        sqrt10 = [np.mean(self.sqrt10[param][j:j+75]) for j in range(0, len(self.sqrt10[param])-75, 75)]
        sqrt20 = [np.mean(self.sqrt20[param][j:j+75]) for j in range(0, len(self.sqrt10[param])-75, 75)]

        quad10 = [np.mean(self.quad10[param][j:j+75]) for j in range(0, len(self.quad10[param])-75, 75)]
        quad20 = [np.mean(self.quad20[param][j:j+75]) for j in range(0, len(self.quad20[param])-75, 75)]

        x = np.arange(0, len(lin20), 1)
        print(len(x))

        plt.plot(x, lin10, '-o', label="linear k=10", color="blue")
        plt.plot(x, lin20, '--o', label="linear k=20", color="blue")
        plt.plot(x, sqrt10, '-o', label="sqrt k=10", color="green")
        plt.plot(x, sqrt20, '--o', label="sqrt k=20", color="green")
        plt.plot(x, quad10, '-o', label="quad k=10", color="red")
        plt.plot(x, quad20, '--o', label="quad k=20", color="red")

        plt.legend()
        plt.xlabel("# of attempt")
        plt.ylabel("index: " + param)
        # plt.ylim(0, 1)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    test = Compare()
    type = None
    while type != -1:
        type = int(input("0:performance comparison, 1:trend, 2:angles 3:quit  -->"))
        if type == 0:
            param = input("param?: ")
            test.compare_performances(param)
        elif type == 1:
            param = input("param?: ")
            test.show_familiality_trend(param)
        elif type == 2:
            param = input("param?: ")
            gain = input("gain?: ")
            test.compare_angles(param, int(gain))
