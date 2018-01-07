"""
File: volatility.py
Author: Rythm Gade
"""



from indexTools import *
from math import *

def average(nums):
    """
    Returns average of given dataset
    :param nums: list of float values
    :return: average
    """
    sum = 0
    for i in nums:
        sum += i
    avg = sum/len(nums)
    return float(avg)

def deviation_squared(nums, avg):
    """
    Returns dev^2 for list of values and given avg
    :param nums: list of vals
    :param avg: avg of nums
    :return: dev^2
    """
    devAr = []
    for i in nums:
        devsq = pow((avg - i), 2)
        devAr.append(float(devsq))
    return devAr

def measure_volatility(data):
    """
    Return volatility for dataset
    :param data: state or zip key data
    :return: volatility
    """
    volList = []
    for key, value in data.items():
        numlst = []
        for d in value:
            numlst.append(d.index)
        avg = average(numlst)
        obvs = len(numlst)
        devsqlst = deviation_squared(numlst, avg)
        sumdevsq = 0
        for i in devsqlst:
            sumdevsq += i
        stdev = sqrt(sumdevsq/obvs)
        volList.append((key, stdev))
    sortdata = sorted(volList, key=lambda x: x[1], reverse=True)
    return sortdata

def main():
    """
    Main
    :return: None
    """
    file = "data/" + input("Enter file name: ")
    roi = input("Enter region of interest: ")
    heading = "Annualized Price Standard Deviation, High to Low"
    if "ZIP" in file:
        data = read_zip_house_price_data(file)
        meData = measure_volatility(data)
        print_ranking(meData, heading)
        s = [item for item in meData if item[0] == roi]
        if s == None:
            print(roi, " not found")
        else:
            print("Standard deviation for ", roi, " is", s)
    else:
        data = read_state_house_price_data(file)
        an = annualize(data)
        meData = measure_volatility(an)
        print_ranking(meData, heading)
        s = [item for item in meData if item[0] == roi]
        if s == None:
            print(roi, " not found")
        else:
            print("Standard deviation for ", roi, " is", s[0][1])

if __name__ == '__main__':
    main()