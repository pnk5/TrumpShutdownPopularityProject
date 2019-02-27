# TrumpShutdownPopularityProject
An econometrics exercise in examining the impact of the government shutdown on Trump's popularity.
## Project Layout (In order of Execution)
#### 1. Gathered data
Secured poll data from fivethirtyeight in appdata.xlsx, then historical Dow Jones Industrial and Russell 2000 data from Yahoo Finance in djdata.csv and rudata.csv respectively.
#### 2. Merge market data and polling data
Averaged the market indicators at the beginning and end of each polling period, and the nearest day if the market was closed on that particular day, script found in mergepolldji.py
#### 3. Perform regressions
Perform linear regressions on approval rating vs government state (shutdown/open) and multivariate linear regressions on approval rating vs government state with the addition of dow jones industrial data and russell 2000 data, script found in Script.R.
