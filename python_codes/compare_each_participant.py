import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st

base_directory = "/home/soichiro/Desktop/pdev/editing/data/"

linear_1 = pd.read_excel(base_directory + "Emi/linear_result.xlsx")
linear_2 = pd.read_excel(base_directory + "Toshiko/linear_result.xlsx")
linear_3 = pd.read_excel(base_directory + "Mai/linear_result.xlsx")
linear_4 = pd.read_excel(base_directory + "Rei/linear_result.xlsx")
linear_5 = pd.read_excel(base_directory + "Kimika/linear_result.xlsx")

model_1 = pd.read_excel(base_directory + "Emi/model_result.xlsx")
model_2 = pd.read_excel(base_directory + "Toshiko/model_result.xlsx")
model_3 = pd.read_excel(base_directory + "Mai/model_result.xlsx")
model_4 = pd.read_excel(base_directory + "Rei/model_result.xlsx")
model_5 = pd.read_excel(base_directory + "Kimika/model_result.xlsx")

def return_combined_data():

    linear = linear_1
    linear = linear.append(linear_2, ignore_index=True)
    linear = linear.append(linear_3, ignore_index=True)
    linear = linear.append(linear_4, ignore_index=True)
    linear = linear.append(linear_5, ignore_index=True)

    model = model_1
    model = model.append(model_2, ignore_index=True)
    model = model.append(model_3, ignore_index=True)
    model = model.append(model_4, ignore_index=True)
    model = model.append(model_5, ignore_index=True)

    linear = linear[linear.ME <= 150]
    model = model[model.ME <= 150]

    linear = linear[linear.TRE <= 4]
    model = model[model.TRE <= 4]

    return linear, model

def show_by_criteria(index):
    linear_1_ = linear_1[linear_1.ME <= 150]
    linear_indexes = [linear_1_[index], linear_2[index], linear_3[index], linear_4[index], linear_5[index]]
    model_indexes = [model_1[index], model_2[index], model_3[index], model_4[index], model_5[index]]

    label_x = ["Participant 1", "Participant 2", "Participant 3", "Participant 4", "Participant 5"]

    x1 = [1, 2, 3, 4, 5]
    y1 = [linear_indexes[i].mean() for i in range(5)]
    std1 = [linear_indexes[i].std(ddof=1) for i in range(5)]

    x2 = [1.3, 2.3, 3.3, 4.3, 5.3]
    y2 = [model_indexes[i].mean() for i in range(5)]
    std2 = [linear_indexes[i].std(ddof=1) for i in range(5)]

    plt.bar(x1, y1, width=0.3, label="linear", align="center")
    plt.errorbar(x1, y1, yerr=std1, ecolor="black", capsize=4, capthick=0.5, elinewidth=0.5, ls='none')

    plt.bar(x2, y2, width=0.3, label="model", align="center")
    plt.errorbar(x2, y2, yerr=std2, ecolor="black", capsize=4, capthick=0.5, elinewidth=0.5, ls='none')

    plt.legend(loc=2)

    plt.xticks([1.15, 2.15, 3.15, 4.15, 5.15], label_x)

    plt.title(index + ": comparison by participants")

    plt.show()

def show_by_summary(index):

    linear_summary, model_summary = return_combined_data()

    label_x = ["linear", "model"]

    plt.bar([1], linear_summary[index].mean(), label="linear", align="center")
    plt.errorbar([1], linear_summary[index].mean(), yerr=linear_summary[index].std(ddof=1), ecolor="black", capsize=4, capthick=0.5, elinewidth=0.5, ls="none")

    plt.bar([2], model_summary[index].mean(), label="model", align="center")
    plt.errorbar([2], model_summary[index].mean(), yerr=model_summary[index].std(ddof=1), ecolor="black", capsize=4, capthick=0.5, elinewidth=0.5, ls="none")

    plt.title(index)
    plt.xticks([1, 2], label_x)
    plt.legend(loc=2)
    plt.show()

    print("linear follows the normal distribution?: ", st.shapiro(linear_summary[index])[1] >= 0.05)
    print("model follows the normal distribution?: ", st.shapiro(model_summary[index])[1] >= 0.05)

    print("Mann-Whitney's U-test")
    print("Statistically significant difference?: ", st.mannwhitneyu(linear_summary[index], model_summary[index], alternative="two-sided")[1] < 0.05)
    #2群の代表値には差があるといえる.


def show_familiality_trend(index, who):

    results = {1: (linear_1, model_1), 2: (linear_2, model_2), 3: (linear_3, model_3), 4: (linear_4, model_4), 5: (linear_5, model_5)}

    data = results[who]

    linear_trend = data[0][index]
    model_trend = data[1][index]

    x1 = np.arange(0, len(linear_trend), 1)
    x2 = np.arange(0, len(model_trend), 1)

    plt.plot(x1, linear_trend, label="linear")
    plt.plot(x2, model_trend, label="model")

    plt.legend(loc=2)

    plt.ylim(0, 300)
    plt.xlabel("# of attempt")
    plt.ylabel("index: " + index)
    plt.title("subject No." + str(who))

    plt.show()

if __name__ == "__main__":
    import sys

    args = sys.argv

    if len(args) == 1:
        raise ValueError("invalid number of arguments: pass the parameter on the command line")
    elif len(args) == 2:
        # show_by_criteria(args[1])
        show_by_summary(args[1])
    elif len(args) == 3:
        show_familiality_trend(args[1], int(args[2]))
