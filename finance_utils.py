#-------------------------------------------------------------------------------
# Name:        finance_utils
# Purpose:
#
# Author:      temp
#
# Created:     18-03-2017
# Copyright:   (c) temp 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import glob
import urllib
import datetime
import time

# Scientific computing package
import numpy as np
#from matplotlib.finance import parse_yahoo_historical
# Data Analysis library
import pandas as pd

def filenameToSymbol(filename):
    return os.path.basename(filename).replace('.csv', '')

def symbolToFilename(symbol, basedir):
    return os.path.join(basedir, symbol.upper()) + '.csv'

def getAllSymbolsAvailable(basedir):
    return map(filenameToSymbol, glob.glob(os.path.join(basedir, '*.csv')))

def getSymbolsFromFile(tickerFile):
    tickerList = []
    try:
        f = open(tickerFile, 'r')
        for tickerRow in f.readlines():
            tickerRow = tickerRow.strip() # remove leading and trailing whitespace
            if not tickerRow or tickerRow[0] == "#":  # skip comment line starting with #
                continue
            ticker = tickerRow.split()[0] # split on whitespace
            tickerList.append(ticker)
        f.close()
    except:
        print "Error: ticker file %s not found" % tickerFile
    return tickerList

def downloadUrl(url):
    tryAgain = True
    count = 0
    s = ""
    while tryAgain and count < 5:
        try:
            s = urllib.urlopen(url).read()
            tryAgain = False
        except:
            print "Error, will try again"
            count += 1
    return s

#-------------------------------------------------------------------------------
# http://www.quantshare.com/sa-43-10-ways-to-download-historical-stock-quotes-data-for-free
def downloadData(symbol, basedir, startDate, endDate):
    print "Downloading:%s" % symbol
    ticker = symbol.upper()
    # Date 1
    d1 = (startDate.month-1, startDate.day, startDate.year)
    # Date 2
    d2 = (endDate.month-1, endDate.day, endDate.year)

    dividends = False # not supported for now
    if dividends:
        g='v'
    else:
        g='d'

    #   or:  'http://ichart.finance.yahoo.com/table.csv?'
    urlFmt = 'http://table.finance.yahoo.com/table.csv?a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&s=%s&y=0&g=%s&ignore=.csv'

    url =  urlFmt % (d1[0], d1[1], d1[2], d2[0], d2[1], d2[2], ticker, g)

    cachename = symbolToFilename(symbol, basedir)

    fh = open(cachename, 'w')
    fh.write(downloadUrl(url))
    fh.close()

#-------------------------------------------------------------------------------
def updateAllSymbols(basedir, startDate, endDate):
    for s in getAllSymbolsAvailable(basedir):
        downloadData(s, basedir, startDate, endDate)

def getPortfolioSnapshot(dataTransactions, dateParam):
    snapshotDate = time.strptime(dateParam, "%d/%m/%Y")

    # Create an empty snapshot table
    snapshotTable = pd.DataFrame(columns = ['Mean cost', 'Number', 'Price'])

    # Fill the snapshot table with all tickers up to the asking date
    for index, tickerRow in dataTransactions.iterrows():
        date = str(index).split(' ')[0]
        ticker = tickerRow['Ticker']
        buyNb = tickerRow['Buy']
        sellNb = tickerRow['Sell']
        cost = tickerRow['Cost']
        transationDate = time.strptime(date, "%Y-%m-%d")

        # For transactions before or equal to the asking date
        if  transationDate <= snapshotDate:
            # Look at all index if the ticker is already there
            if ticker in snapshotTable.index:
                # Adjust stocks for the specified ticker
                if buyNb != 'NaN':
                    totalNumber =  snapshotTable.loc[ticker]['Number'] + buyNb
                    meanCost = snapshotTable.loc[ticker]['Mean cost'] * snapshotTable.loc[ticker]['Number'] / totalNumber + cost * buyNb / totalNumber
                    snapshotTable.at[ticker, 'Number'] = totalNumber
                    snapshotTable.at[ticker, 'Mean cost'] = meanCost

                if sellNb != 'NaN':
                    totalNumber = snapshotTable.loc[ticker]['Number'] - sellNb
                    snapshotTable.at[ticker, 'Number'] = totalNumber

            else:
                if buyNb != 'NaN':
                    # Add ticker in the snapshot table
                    newTicker = pd.DataFrame({'Mean cost':cost, 'Number':buyNb, 'Price':'Nan'}, index = [ticker])
                    snapshotTable  = snapshotTable.append(newTicker)
                else:
                    # Error
                     print "Error: It is not normal to sell if you do not own"

    # Remove all lines with a share number below one
    for ticker, tickerRow in snapshotTable.iterrows():
        if tickerRow['Number'] <= 0:
            snapshotTable = snapshotTable.drop(ticker)

    return snapshotTable

#def getAnnualReturn(dataTransactions, year):
    # Create a table
    # One line contains Ticker name, Mean cost, Price

    # Initialize the table with January 1st  portofolio

    # Update the table with the transactions during the year
    # Add a line for every sell transaction
    #for tickerRow in dataTransactions:
        #if tickerRow[0:1].split("/")[2:3] == year:

    # Get the December 31 price for every line excepted for the Sell transaction
    # Update the price with the December 31 price list

    # Calculate the annual return for the total of lines


def main():
    _defBaseDir = './stock_db/test'

    startDate = datetime.date(1900, 1, 1)
    endDate = datetime.date.today()

    s = 'SPY'

    f = symbolToFilename(s, _defBaseDir)
    print f
    print filenameToSymbol(f)

    print getAllSymbolsAvailable(_defBaseDir)
    downloadData(s, _defBaseDir, startDate, endDate)
    updateAllSymbols(_defBaseDir, startDate, endDate)
    print getSymbolsFromFile('stock_db/dj.txt')


if __name__ == '__main__':
    main()
