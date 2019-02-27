import os
import pandas as pd

wd = os.getcwd()

polldata = "apprate.xlsx"
djdata = "djdata.csv"
xlpolldata = pd.ExcelFile(polldata)
dfdjdata = pd.read_csv(djdata)

print(xlpolldata.sheet_names)

dfpolldata = xlpolldata.parse('Approval Rating Spreadsheet')

mutdata = dfpolldata
mutdata.insert(0, "djavg", 0)


def string_to_date(instring):
    return pd.to_datetime(instring)


dfdjdata["Date"] = dfdjdata.apply(lambda row: string_to_date(row["Date"]), axis=1)

print(dfdjdata)

print(dfdjdata["Date"][1])
def get_avg_valuation(indf, date1, date2):
    return (indf.loc[indf["Date"] == date1]["Close"] + indf.loc[indf["Date"] == date2]["Close"]) / 2.0


mutdata["djavg"] = mutdata.apply(lambda row: get_avg_valuation(dfdjdata, row["startdate"], row["enddate"]), axis=1)


#
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

print(mutdata)