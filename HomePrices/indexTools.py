"""
File: indexTools.py
Author: Rythm Gade
"""



from rit_lib import *

class QuarterHPI(struct):
    """
    QuarterHPI class
    """
    _slots = ((int, 'year'),(int, 'qtr'),(float, 'index'))

class AnnualHPI(struct):
    """
    AnnualHPI class
    """
    _slots = ((int, 'year'),(float, 'index'))

def read_state_house_price_data(filepath):
    """
    Reads in filedata for state data
    :param filepath: filename
    :return: dictionary of state keyed quarterHPI objects
    """
    data = {}
    fd = open(filepath)
    for line in fd:
        if line.startswith("state"):
            pass
        else:
            fields = line.split("\t")
            key = fields [0]
            yr = fields[1]
            qtr = fields[2]
            idx = fields[3]
            if idx != '.':
                if key in data:
                    data[key].append(QuarterHPI(int(yr), int(qtr), float(idx)))
                else:
                    data[key] = [QuarterHPI(int(yr), int(qtr), float(idx))]
            else:
                print(line, end='')
                print('warning: data unavailable in original source.')
    return data

def read_zip_house_price_data(filepath):
    """
    Reads in filedata for ZIP data
    :param filepath: filename
    :return: dictionary of ZIP keyed annualHPI objects
    """
    data = {}
    fd = open(filepath)
    counted = 0
    uncounted = 0
    for line in fd:
        if line.startswith("Five-Digit ZIP Code"):
            pass
        else:
            fields = line.split("\t")
            key = fields[0]
            yr = fields[1]
            idx = fields[3]
            if idx != '.':
                if key in data:
                    data[key].append(AnnualHPI(int(yr), float(idx)))
                else:
                    data[key] = [AnnualHPI(int(yr), float(idx))]
                counted += 1
            else:
                uncounted += 1
    print("count: ", counted, " uncounted: ", uncounted)
    return data

def index_range(data, region):
    """
    Takes in data(region keyed objects) and region and returns lowest and highest HPI for the region
    :param data: state or zip keyed HPI object
    :param region: region of interest
    :return: low and high HPI object
    """
    minHPI = 100000
    maxHPI = 0
    minHPIobj = None
    maxHPIobj = None
    for value in data[region]:
        if value.index < minHPI:
            minHPI = value.index
            minHPIobj = value
        elif value.index > maxHPI:
            maxHPI = value.index
            maxHPIobj = value
    return minHPIobj, maxHPIobj

def print_range(data, region):
    """
    Prints index range
    :param data: state or zip keyed HPI object
    :param region: region of interest
    :return: none
    """
    minHPIobj, maxHPIobj = index_range(data, region)
    if isinstance(minHPIobj, QuarterHPI) == True:
        print("Region: ", region)
        print("Low: year/quarter/index:", minHPIobj.year, "/", minHPIobj.qtr, "/", minHPIobj.index)
        print("High: year/quarter/index:", maxHPIobj.year, "/", maxHPIobj.qtr, "/", maxHPIobj.index)
    else:
        print("Region: ", region)
        print("Low: year/quarter/index:", minHPIobj.year, "/", minHPIobj.index)
        print("High: year/quarter/index:", maxHPIobj.year, "/", maxHPIobj.index)


def print_ranking(data, heading = "Ranking"):
    """
    Prints top and bottom 10 HPI objects
    :param data: state or zip keyed HPI object
    :param heading: heading
    :return: None
    """
    print(heading)
    i = 1
    print("The Top 10:")
    for value in data[0:10]:
        print(i, ":", (value))
        i += 1
    print("The Bottom 10:")
    j = len(data) - 9
    for val in data[-10:]:
        print(j, ":", (val))
        j += 1

def annualize(data):
    """
    Annualize quarterHPI
    :param data: quarterHPI objects (state keyed)
    :return: annualized data
    """
    anDict = {}
    for key, value in data.items():
        currKey = key
        i = 0
        while currKey == key:
            currYear = value[i].year
            nextYear = value[i+1].year
            yrCount = 0
            total = 0
            while value[i].year == nextYear:
                total += float(value[i].index)
                yrCount += 1
                i += 1
            if value[i].year != nextYear:
                if key in anDict:
                    anDict[key].append(AnnualHPI(int(currYear), float(total/yrCount)))
                else:
                    anDict[key] = [AnnualHPI(int(currYear), float(total/yrCount))]
            if i == len(value)-1:
                if key in anDict:
                    anDict[key].append(AnnualHPI((int(nextYear)+1), float(value[i].index)))
                    break
                else:
                    anDict[key] = [AnnualHPI((int(nextYear)+1), float(value[i].index))]
                    break
    return anDict

def main():
    """
    Main
    :return:
    """
    roi = "hi"
    file = "data/" + input("Enter file name: ")
    if "ZIP" in file:
        data = read_zip_house_price_data(file)
    else:
        data = read_state_house_price_data(file)
    while roi != '':
        roi = input("Enter region name: ")
        if roi == '':
            break
        else:
            print("=============================================")
            print("Region: ", roi)
            if len(roi) > 2:
                for value in data[roi]:
                    print(value)
            else:
                andata = annualize(data)
                print_range(data, roi)
                print_range(andata, roi)
                print("Annualized Index Values for ", roi)
                for value in andata[roi]:
                    print(value)


if __name__ == '__main__':
    main()



