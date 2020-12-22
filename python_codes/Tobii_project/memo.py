import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from stdlib import MyLibrary as lib
from Data_store import DataFrames
import seaborn as sns


def tlead_param_corr(subject, mode, threshold):
    param = lib.get_large_me_param(subject, mode, threshold)
    x_, y_ = [], []
    for p in param:
        attempt, click = p
        path = "./data/{}/{}/test{}.xlsx".format(subject, mode, attempt)
        df = DataFrames(path)

        x, y = df.get_cods()['x'], df.get_cods()['y']
        x = x[click-1]
        y = y[click-1]
        a, b, c = lib.ideal_route(click-1)

        dist = np.array([abs(a * x + b * y + c) / np.sqrt(a ** 2 + b ** 2) for x, y in zip(x, y)])

        # t_lead = df.get_tlead()[click-1]
        # t_lead = [0 if x < 0 else 1 for x in t_lead] + [0]

        md = df.get_dist_gaze_pointer()[click-1]

        x_.append(md)
        y_.append(list(dist))

    x_ = np.hstack(x_)
    y_ = np.hstack(y_)

    x_, y_ = lib.get_valid_data(x_, y_)

    plt.plot(x_, y_, "o")
    plt.show()


def bar_plot():
    param = "ME"
    gaze_param = "gaze_ME"

    lin10 = pd.read_excel("/dat/Uchino/linear_10/summary.xlsx")
    sqrt10 = pd.read_excel("/dat/Uchino/sqrt_10/summary.xlsx")

    lin_mean = lin10[param].mean()
    sq_mean = sqrt10[param].mean()

    lin_gaze_mean = lin10[gaze_param].mean()
    sq_gaze_mean = sqrt10[gaze_param].mean()

    lin_std = lin10[param].std()
    sq_std = sqrt10[param].std()

    lin_gaze_std = lin10[gaze_param].std()
    sq_gaze_std = sqrt10[gaze_param].std()

    x1 = [1, 2]
    x2 = [1.3, 2.3]
    plt.bar(x1, [lin_mean, sq_mean], width=0.3, align="center")
    plt.bar(x2, [lin_gaze_mean, sq_gaze_mean], width=0.3, align="center")
    plt.errorbar(x1, [lin_mean, sq_mean], yerr=[lin_std, sq_std], ecolor="black", capsize=3, capthick=0.5, ls="none")
    plt.errorbar(x2, [lin_gaze_mean, sq_gaze_mean], yerr=[lin_gaze_std, sq_gaze_std], ecolor="black", capsize=3,
                 capthick=0.5, ls="none")

    plt.xticks([1.15, 2.15], ["linear", "sqrt"])

    plt.show()


def hist_plot():
    param = "mean_tlead"
    lin10 = pd.read_excel("/dat/Iwata/linear_10/summary.xlsx")
    sqrt10 = pd.read_excel("/dat/Iwata/sqrt_10/summary.xlsx")
    mouse = pd.read_excel("/dat/Iwata/mouse/summary.xlsx")

    datas = [lin10, sqrt10, mouse]

    for d in datas:
        plt.hist(d[param], bins=30)
        plt.show()


def logistic_validation():
    # x = np.array([0.87, 1.01, 0.97, 0.93, 0.89, 0.83, 0.91, 0.70, 0.57, 0.75, 1.06, 0.55])
    # y = np.array([1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1])

    iris_df = sns.load_dataset("iris")
    iris_df = iris_df[(iris_df["species"] == "versicolor") | (iris_df["species"] == "virginica")]

    x = iris_df[["petal_length"]]
    y = iris_df["species"].map({"versicolor": 0, "virginica": 1})

    x_test = x
    y_test = y

    lr = LogisticRegression()
    lr.fit(x_test, y_test)

    w0 = lr.intercept_[0]
    w1 = lr.coef_[0][0]
    print(w0, w1)
    p = lambda v: 1/(1 + np.exp(-(w0 + w1*v)))

    x_range = np.arange(2, 8, 0.01)

    prediction = np.array([p(item) for item in x_range])

    # for x_, y_ in zip(x, y):
        # print(x_, y_, p(x_))

    plt.plot(x, y, "o")
    plt.plot(x_range, prediction)
    plt.xlabel("Movement Error")
    plt.ylabel("$t_lead$")
    plt.show()


class SeabornTest:

    def __init__(self):
        pass

    def generate_concatenated_data(self, subject):
        linear = pd.read_excel("./data/" + subject + "/linear_10/summary.xlsx")
        # sqrt = pd.read_excel("./data/" + subject + "/sqrt_10/summary.xlsx")
        mouse = pd.read_excel("./data/" + subject + "/mouse/summary.xlsx")

        label = ["linear"]*len(linear) + ["mouse"]*len(mouse)
        label = pd.Series(label, name="label")

        params = ["MD", "ME", "Throughput", "mean_tlead"]
        linear = linear[params]
        # sqrt = sqrt[params]
        mouse = mouse[params]

        df = pd.concat([linear, mouse], ignore_index=True)
        df = pd.concat([df, label], axis=1)

        print(df)
        return df

    def data_plot(self, subject):
        df = self.generate_concatenated_data(subject)
        obj = sns.pairplot(df, hue="label", palette={"linear":"blue", "sqrt":"orange", "mouse":"green"},plot_kws={"alpha": 0.5})
        plt.yticks(fontsize=25)
        plt.xticks(fontsize=25)
        plt.show()
        obj.savefig("./pictures/{}_scattered_mouse.png".format(subject))


if __name__ == "__main__":
    test = SeabornTest()
    test.data_plot("")
