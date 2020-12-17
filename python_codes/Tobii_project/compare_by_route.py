import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class CompareRoute:

    def __init__(self, param):
        self.subject = ("Iwata", "Uchino", "Murakami", "Nishigaichi")
        self.param = param
        self.N = len(self.subject)

    def compare_route(self):
        x1 = np.arange(1, self.N+1, 1)
        x2 = np.arange(1.3, self.N+1.3, 1)
        y1 = []
        y2 = []
        std1 = []
        std2 = []
        for i in range(self.N):
            path = ".\\data\\" + self.subject[i] + "\\" + self.param + "\\summary.xlsx"
            df = pd.read_excel(path)
            horizontal = df.MD[(df.click == 1) | (df.click == 2) | (df.click == 3)]
            vertical = df.MD[(df.click == 8) | (df.click == 9) | (df.click == 10)]
            y1.append(horizontal.mean())
            y2.append(vertical.mean())
            std1.append(horizontal.std())
            std2.append(vertical.std())
            # 縦方向のMDの方が大きい->縦方向の方がカバーされている領域が大きい？

        plt.bar(x1, y1, width=0.3, align="center", label="horizontal")
        plt.errorbar(x1, y1, yerr=std1, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

        plt.bar(x2, y2, width=0.3, align="center", label="vertical")
        plt.errorbar(x2, y2, yerr=std2, ecolor="black", capsize=3, capthick=0.5, elinewidth=0.5, ls="none")

        plt.xticks(np.arange(1.15, self.N+1.15, 1), self.subject)
        plt.tight_layout()
        plt.legend()
        plt.show()


if __name__ == "__main__":
    path = ".\\data\\Iwata\\linear_10\\summary.xlsx"
    test = CompareRoute("linear_10")
    test.compare_route()