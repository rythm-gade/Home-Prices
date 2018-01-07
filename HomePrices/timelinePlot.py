"""
File: timelinePlot.py
Author: Rythm Gade
"""

import numpy.ma as ma
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy
from indexTools import *

def build_plottable_array(xyears, regiondata):
    """
    Returns plottable masked array given year range and data[region]
    :param xyears: list of years
    :param regiondata: data[region]
    :return: array
    """
    mAry = []
    i = 0
    for value in xyears:
        if value == regiondata[i].year:
            index = float(regiondata[i].index)
            mAry.append(index)
            i += 1
        else:
            mAry.append(ma.masked)
    mAry = ma.array(mAry)
    return mAry

def filter_years(data, year0, year1):
    """
    Returns filtered dataset for start/end year
    :param data: dataste (state, zip keyed)
    :param year0: start year
    :param year1: end year
    :return: new dataset
    """
    if year1 < year0:
        raise ValueError('Year1 must be later then Year0')
    else:
        newD = {}
        yrrange = [k for k in range(year0, year1 + 1)]
        for key, value in data.items():
            i = 0
            x = data[key]
            for val in yrrange:
                curr = data[key][i]
                while curr.year != val:
                    i+=1
                    curr = data[key][i]
                if val == curr.year:
                    if key in newD:
                        newD[key].append(AnnualHPI(curr.year, curr.index))
                        i += 1
                    else:
                        newD[key] = [AnnualHPI(curr.year, curr.index)]
                        i += 1
    return newD


def plot_HPI(data, regionList):
    """
    Plots HPI line graphs
    :param data: dataset
    :param regionList: list of regions to plot
    :return: Plots
    """
    for key in regionList:
        indexlst = []
        yearlst = []
        if key in data:
            for i in data[key]:
                indexlst.append(i.index)
                yearlst.append(i.year)
            yearlst = ma.array(yearlst)
            plt.figure()
            plt.plot(yearlst, indexlst, '*', linestyle="-")
    plt.show()
    print("Close display window to continue")

def plot_whiskers(data, regionList):
    """
    Plots HPI box whisker plots
    :param data: dataset
    :param regionList: list of regions to plot
    :return: Plots
    """
    for key in regionList:
        indexlst = []
        if key in data:
            for i in data[key]:
                indexlst.append(i.index)
            plt.figure()
            plt.boxplot(indexlst)
    plt.show()
    print("Close display window to continue")

def main():
    """
    Main
    :return: None
    """
    roi = "hi"
    file = "data/" + input("Enter file name: ")
    yr0 = int(input("Enter start year of range to plot: "))
    yr1 = int(input("Enter end year of range to plot: "))
    if "ZIP" in file:
        data = read_zip_house_price_data(file)
        regionlst = []
        while roi != '':
            roi = input("Enter next region for plots (<ENTER> to stop): ")
            regionlst.append(roi)
        newdata = filter_years(data, yr0, yr1)
        plot_HPI(newdata, regionlst)
        plot_whiskers(newdata, regionlst)
    else:
        data = read_state_house_price_data(file)
        andata = annualize(data)
        regionlst = []
        while roi != '':
            roi = input("Enter next region for plots (<ENTER> to stop): ")
            regionlst.append(roi)
        for i in regionlst[0:len(regionlst)-1]:
            print_range(data, i)
        newdata = filter_years(andata, yr0, yr1)
        plot_HPI(newdata, regionlst)
        plot_whiskers(newdata, regionlst)



if __name__ == '__main__':
    main()