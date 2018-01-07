"""
File: periodRanking.py
Author: Rythm Gade
"""


from indexTools import *

def quarter_data(data, year, qtr):
    """
    Returns list of sorted (high to low) (region, HPI) tuples
    :param data: data
    :param year: year of interest
    :param qtr: qtr of interest
    :return: list
    """
    qList = []
    for key, value in data.items():
        for d in value:
            if d.year == int(year) and d.qtr == int(qtr):
                qList.append((key, float(d.index)))
    qList = sorted(qList, key = lambda x: x[1], reverse= True)
    return qList

def annual_data(data, year):
    """
    Returns list of sorted (high to low) (region, HPI) tuples
    :param data: data
    :param year: year of interest
    :return: list
    """
    aList = []
    for key, value in data.items():
        for d in value:
            if d.year == int(year):
                aList.append((key, float(d.index)))
    aList = sorted(aList, key=lambda x: x[1], reverse=True)
    return aList

def main():
    """
    Main
    :return: None
    """
    file = "data/" + input("Enter file name: ")
    year = input("Enter year of interest for prices: ")
    if "ZIP" in file:
        data = read_zip_house_price_data(file)
        print_ranking(annual_data(data, year))
    else:
        data = read_state_house_price_data(file)
        an = annualize(data)
        print_ranking(annual_data(an, year))

if __name__ == '__main__':
    main()