import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from cliffs_delta import cliffs_delta
import pymannkendall as mk

new_data = pd.read_excel("new_version_perf.xlsx")
old_data = pd.read_excel("original_version_perf.xlsx")

def histograms(old_data, new_data):
    count_old, bins_old = np.histogram(old_data["TOTAL_CPU"], bins=30)
    count_new, bins_new = np.histogram(new_data["TOTAL_CPU"], bins=30)

    fig, axs = plt.subplots(
        2, 1, sharex=True, sharey=True, layout='constrained')

    axs[1].stairs(count_new, bins_new)
    axs[1].set_title("New data histogram")
    axs[1].set_ylabel("number of request")
    axs[1].set_xlabel("cpu times")

    axs[0].stairs(count_old, bins_old)
    axs[0].set_title("Old data histogram")
    axs[0].set_ylabel("number of request")


def two_relative(old_data, new_data):
    res = stats.ttest_rel(old_data["TOTAL_CPU"], new_data["TOTAL_CPU"])
    res2 = stats.wilcoxon(old_data["TOTAL_CPU"], new_data["TOTAL_CPU"])
    print("the pvalue of the paired T test is " + str(res.pvalue))
    print("the pvalue of the wilcoxon test is " + str(res2.pvalue))
    pass


def cohen_d(x, y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.std(x, ddof=1) ** 2 + (ny-1)*np.std(y, ddof=1) ** 2) / dof)

def magnitude(old_data, new_data):
    d = cohen_d(old_data["TOTAL_CPU"], new_data["TOTAL_CPU"])
    cliff = cliffs_delta(old_data["TOTAL_CPU"], new_data["TOTAL_CPU"])
    print("cohen's d is " + str(d))
    print("Cliff's delta is " + str(cliff))

def trendAnalysis(old_data, new_data):
    # trend.cox_stuart(old_data["TOTAL_CPU"])
    old_cox = mk.original_test(old_data["TOTAL_CPU"])
    # trend.cox_stuart(new_data["TOTAL_CPU"])
    new_cox = mk.original_test(new_data["TOTAL_CPU"])

    print(str(old_cox))
    print(str(new_cox))
    pass
    
histograms(old_data, new_data)

two_relative(old_data, new_data)

magnitude(old_data, new_data)

trendAnalysis(old_data, new_data)

plt.show()
