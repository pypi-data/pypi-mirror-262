#! env python

import os
import sys
import argparse
import re
import plotly as pltly
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as pdr
import numpy as np
# https://github.com/pydata/pandas-datareader/blob/main/pandas_datareader/fred.py

# settings
pd.options.plotting.backend = "plotly"
pd.set_option('display.max_columns', None)


class PlotObs():

    def __init__(self):
        self.df  = None
        self.fig = None       # plotly figure

    def loadpath(self, fpath):
        """
        broken
        """
        name=None
        try:
            fp = open(fpath, 'r')
            ln = fp.readline()
            la = ln.split()
            name = la[4]
        except Exception as e:
            print('%s: %s' % (fpath, e) )

        self.df = pd.read_csv(fpath,
                     index_col=0,
                     parse_dates=True,
                     header=None,
                     skiprows=1,
                     names=["DATE", name],
                     na_values=".",
                 )
        self.df = pd.read_csv(fpath)
        self.df.columns
        obj = self.df.get([0,4])
        print(type(obj) )
        print(obj)

        print(self.df)

        # self.df = pd.read_csv(fpath,
        #        index_col=4,
        #        usecols=[0,1,4,5],
        #        parse_dates=True,
        #        header=0,
        #        skiprows=1,
        #        names=["date",name],
        #       na_values=".")
        #self.df.bfill(inplace=True)

    def loadts(self, tsa):
        """
        works
        """
        self.df = pdr.DataReader(tsa, data_source="fred")
        self.df.bfill(inplace=True)

    def plot(self):
        fig = self.df.plot()
        fig.show()

def main():
    argp = argparse.ArgumentParser(description='build a glot for FRED observatsion(s)')
    argp.add_argument('--file', help='path to FRED time series observations')
    argp.add_argument('--tslist',
        help='comma separated list of names of FRED timeseries observations')

    args = argp.parse_args()

    po = PlotObs()
    if args.tslist:
        tsa = args.tslist.split(',')
        po.loadts(tsa)
        po.plot()
    elif args.file:
        po.loadpath(args.file)
        po.plot()

if __name__ == '__main__':
    main()
