"""
File: trending.py
Author: Rythm Gade
"""



from indexTools import *
from math import *

def cagr(idxlist, periods):
    """
    Determine Compound annual growth given initial HPI and ending HPI and num of periods
    :param idxlist: 2 item list of start/end HPI
    :param periods: number of periods between HPI values
    :return: CAGR
    """
    HPI0 = float(idxlist[0])
    HPI1 = float(idxlist[1])
    n = int(periods)
    cagrExp = (pow((HPI1/HPI0), (1/n))-1)*100
    return float(cagrExp)

def calculate_trends(data, year0, year1):
    """
    Return list of (region, rate) tuples sorted in descending order by CAGR
    :param data: state or zip key HPI
    :param year0: start year
    :param year1: end year
    :return: List
    """
    if year1 < year0:
        raise ValueError('Year1 must be later then Year0')
    else:
        cagrList = []
        periods = int(year1) - int(year0)
        for key, value in data.items():
            HPI0 = 0
            HPI1 = 0
            for d in value:
                if d.year == year0:
                    HPI0 = float(d.index)
                if d.year == year1:
                    HPI1 = float(d.index)
            if HPI0 == 0 or HPI1 == 0:
                pass
            else:
                cagrList.append((key, cagr((HPI0, HPI1), periods)))
        cagrList = sorted(cagrList, key=lambda x: x[1], reverse=True)
        return cagrList



def main():
    """
    Main
    :return: None
    """
    file = "data/" + input("Enter file name: ")
    yr0 = int(input("Enter start year of interest: "))
    yr1 = int(input("Enter ending year of interest: "))
    heading = str(yr0) + '-' + str(yr1) + ' Compound Annual Growth Rate'
    if "ZIP" in file:
        data = read_zip_house_price_data(file)
        c = calculate_trends(data, yr0, yr1)
        if len(c) < 10:
            print(heading)
            i = 1
            print("The Top 10:")
            for value in data[0:len(c)]:
                print(i, ":", (value))
                i += 1
            print("The Bottom 10:")
            j = len(data) - 9
            for val in data[-len(c):]:
                print(j, ":", (val))
                j += 1
        else:
            print_ranking(c, heading)

    else:
        data = read_state_house_price_data(file)
        an = annualize(data)
        c = calculate_trends(an, yr0, yr1)
        if len(c) < 10:
            print(heading)
            i = 1
            print("The Top 10:")
            for value in data[0:len(c)]:
                print(i, ":", (value))
                i += 1
            print("The Bottom 10:")
            j = len(data) - 9
            for val in data[-len(c):]:
                print(j, ":", (val))
                j += 1
        else:
            print_ranking(c, heading)

if __name__ == '__main__':
    main()
