import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Compare:

    def __init__(self, subject):
        self.linear = pd.read_excel("./data_with_questionaire/{}/linear/summary.xlsx".format(subject))
        self.sqrt = pd.read_excel("./data_with_questionaire/{}/sqrt/summary.xlsx".format(subject))
        self.quad = pd.read_excel("./data_with_questionaire/{}/quad/summary.xlsx".format(subject))

        self.data = [self.linear, self.sqrt, self.quad]

    def compare_performances(self, param):
        if not isinstance(param, str):
            raise TypeError("param should be str type")

        # plt.plot(np.arange(0, len(self.lin10[param]), 1), self.lin10[param], 'o')
        # plt.plot(np.arange(0, len(self.lin20[param]), 1), self.lin20[param], 'o')

        lin_mean = self.linear[param].mean()
        sqrt_mean = self.sqrt[param].mean()
        quad_mean = self.quad[param].mean()

        lin_std = self.linear[param].std()
        sqrt_std = self.sqrt[param].std()
        quad_std = self.quad[param].std()

        x = [1, 2, 3]
        plt.xticks(x, ["linear", "sqrt", "quad"])
        plt.legend()
        plt.bar(x, [lin_mean, sqrt_mean, quad_mean])
        plt.errorbar(x, [lin_mean, sqrt_mean, quad_mean], yerr=[lin_std, sqrt_std, quad_std], ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

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
    subject = input("subject?: ")
    param = input("param?: ")

    test = Compare(subject)
    test.compare_performances(param)
