import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
# from stdlib import MyLibrary as lib
from Data_store import DataFrames
import seaborn as sns
from statsmodels.stats.multicomp import tukeyhsd, pairwise_tukeyhsd

def angle_md_correlation(subject, mode):
    x = []
    y = []
    for i in range(1, 21):
        data = DataFrames("data/{}/{}_10/test{}.xlsx".format(subject, mode, i))

        d = data.get_dist_gaze_pointer()
        theta_x, theta_y = data.get_angles()["roll"], data.get_angles()["pitch"]

        x = x + theta_x
        y = y + d
    x = np.hstack(x)
    y = np.hstack(y)

    plt.plot(x, y, "o")
    plt.show()

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

def subjects_comparison(param):
    inoue = pd.read_excel("./data/Inoue/linear_10/summary.xlsx")[param]
    iwata = pd.read_excel("./data/Iwata/linear_10/summary.xlsx")[param]
    murakami = pd.read_excel("./data/Murakami/linear_10/summary.xlsx")[param]
    nishi = pd.read_excel("./data/Nishigaichi/linear_10/summary.xlsx")[param]
    uchino = pd.read_excel("./data/Uchino/linear_10/summary.xlsx")[param]

    beginner = pd.concat([inoue, iwata])
    intermediate = murakami
    expert = pd.concat([nishi, uchino])
    data = [beginner, intermediate, expert]
    names = ["beginner", "intermediate", "expert"]
    x_ticks = [i for i in range(1, 4)]
    means = []
    errs = []

    for subject in data:
        means.append(subject.mean())
        errs.append(subject.std())

    plt.bar(x_ticks, means, align="center")
    plt.errorbar(x_ticks, means, yerr=errs, ecolor="black", capsize=3, capthick=0.5, ls="none")
    plt.xticks(x_ticks, names)
    plt.show()

    data = np.hstack(data)
    group = ["beginner"]*len(beginner) + ["intermediate"]*len(intermediate) + ["expert"]*len(expert)
    res = pairwise_tukeyhsd(data, group)
    print(res)

def subjects_comparison_scatter(param1, param2):
    x, y = [], []
    mode = ["linear_10"]

    x_max, y_max = -1, -1

    for m in mode:
        inoue = pd.read_excel("./data/Inoue/{}/summary.xlsx".format(m))
        iwata = pd.read_excel("./data/Iwata/{}/summary.xlsx".format(m))
        murakami = pd.read_excel("./data/Murakami/{}/summary.xlsx".format(m))
        # nishi = pd.read_excel("./data/Nishigaichi/linear_10/summary.xlsx")
        uchino = pd.read_excel("./data/Uchino/{}/summary.xlsx".format(m))

        data = [inoue, iwata, murakami, uchino]
        names = ["Inoue", "Iwata", "Murakami", "Uchino"]

        for subject in data:
            # x.append(subject[param1].mean())
            # y.append(subject[param2].mean())

            x = x + list(subject[param1])
            y = y + list(subject[param2])

            x_max = max(x_max, x[-1])
            y_max = max(y_max, y[-1])

    nishi = pd.read_excel("./data/Nishigaichi/linear_10/summary.xlsx")
    x.append(nishi[param1].mean())
    y.append(nishi[param2].mean())

    plt.plot(x, y, "o")
    # plt.xlim(0, x_max*1.1)
    # plt.ylim(0, y_max*1.1)
    plt.show()

    x = pd.Series(x)
    y = pd.Series(y)
    print(x.corr(y))

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
    subjects_comparison("ME")
