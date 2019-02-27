import os
import pandas as pd
from datetime import datetime, timedelta

wd = os.getcwd()

polldata = "apprate.xlsx"
djdata = "djdata.csv"
rudata = "rudata.csv"
xlpolldata = pd.ExcelFile(polldata)
dfdjdata = pd.read_csv(djdata)
dfrudata = pd.read_csv(rudata)

print(xlpolldata.sheet_names)

dfpolldata = xlpolldata.parse('Approval Rating Spreadsheet')

mutdata = dfpolldata
mutdata.insert(0, "djavg", 0)


def string_to_date(instring):
    return pd.to_datetime(instring)


dfdjdata["Date"] = dfdjdata.apply(lambda row: string_to_date(row["Date"]), axis=1)
dfrudata["Date"] = dfrudata.apply(lambda row: string_to_date(row["Date"]), axis=1)

print(dfdjdata)

print(dfdjdata["Date"][1])

"""Averages the DJIA valuations at the beginning and end of each polling period, looking ahead or behind three days
if the market was closed on one of the end dates"""


def get_avg_valuation(indf, date1, date2):
    quote1 = indf.loc[indf["Date"] == date1]["Close"]
    quote2 = indf.loc[indf["Date"] == date2]["Close"]
    if quote1.size > 0 and quote2.size > 0:
        return (quote1.values[0] + quote2.values[0]) / 2
    else:
        if quote1.size == 0:
            pydate1 = date1.to_pydatetime()
            pynewdate1 = pydate1 - timedelta(days=1)
            if indf.loc[indf["Date"] == pd.to_datetime(pynewdate1)]["Close"].size == 0:
                pynewdate1 = pydate1 + timedelta(days=1)
                if indf.loc[indf["Date"] == pd.to_datetime(pynewdate1)]["Close"].size == 0:
                    pynewdate1 = pydate1 + timedelta(days=2)
                    if indf.loc[indf["Date"] == pd.to_datetime(pynewdate1)]["Close"].size == 0:
                        pynewdate1 = pydate1 - timedelta(days=2)
                        if indf.loc[indf["Date"] == pd.to_datetime(pynewdate1)]["Close"].size == 0:
                            pynewdate1 = pydate1 + timedelta(days=3)
                            if indf.loc[indf["Date"] == pd.to_datetime(pynewdate1)]["Close"].size == 0:
                                pynewdate1 = pydate1 - timedelta(days=3)
        else:
            pynewdate1 = date1.to_pydatetime()
        if quote2.size == 0:
            pydate2 = date2.to_pydatetime()
            pynewdate2 = pydate2 - timedelta(days=1)
            if indf.loc[indf["Date"] == pd.to_datetime(pynewdate2)]["Close"].size == 0:
                pynewdate2 = pydate2 + timedelta(days=1)
                if indf.loc[indf["Date"] == pd.to_datetime(pynewdate2)]["Close"].size == 0:
                    pynewdate2 = pydate2 + timedelta(days=2)
                    if indf.loc[indf["Date"] == pd.to_datetime(pynewdate2)]["Close"].size == 0:
                        pynewdate2 = pydate2 - timedelta(days=2)
                        if indf.loc[indf["Date"] == pd.to_datetime(pynewdate2)]["Close"].size == 0:
                            pynewdate2 = pydate2 + timedelta(days=3)
                            if indf.loc[indf["Date"] == pd.to_datetime(pynewdate2)]["Close"].size == 0:
                                pynewdate2 = pydate2 - timedelta(days=3)
        else:
            pynewdate2 = date2.to_pydatetime()
    return (indf.loc[indf["Date"] == pd.to_datetime(pynewdate1)]["Close"].values[0]
            + indf.loc[indf["Date"] == pd.to_datetime(pynewdate2)]["Close"].values[0]) / 2


mutdata["djavg"] = mutdata.apply(lambda row: get_avg_valuation(dfdjdata, row["startdate"], row["enddate"]), axis=1)
mutdata["ruavg"] = mutdata.apply(lambda row: get_avg_valuation(dfrudata, row["startdate"], row["enddate"]), axis=1)


# Old, bad way of doing it
# for index, row in dfpolldata.iterrows():
#     mutdata.at["djavg", index] = 0
#     print(index)
#
# for index, row in dfdjdata.iterrows():
#     print(index, row["Date"])
#
# print(type(dfpolldata["startdate"][1]))
# print(dfpolldata["startdate"][1].year)
# print(pd.to_datetime(dfdjdata["Date"][1]))
# print(type(dfdjdata["Date"][1]))

# print(mutdata)
# print(mutdata["djavg"])
# print(mutdata["ruavg"])

mutdata.to_excel("poll_and_avg.xlsx")