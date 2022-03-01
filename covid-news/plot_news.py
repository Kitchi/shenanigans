#!/usr/bin/env python3


import click
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker

# pandas read_csv won't work for headlines.txt so write a custom function
def read_file(fname):
    day = []
    month = []
    year = []
    headline = []
    with open(fname, 'r') as fptr:
        for line in fptr:
            words = line.split()
            day.append(int(words[1].strip(',')))
            month.append(words[0])
            year.append(int(words[2]))
            headline.append(" ".join(words[3:]))

    return day, month, year, headline


@click.command()
def plot_news():
    """
    Reads headlines.txt and ecdc_data.csv and generate histograms
    """

    headlines = 'headlines.txt'
    ecdc = 'ecdc_data.csv'

    day, month, year, headline = read_file(headlines)

    df = pd.DataFrame()
    df['day'] = day
    df['month'] = month
    df['year'] = year
    df['headline'] = headline

    idx = np.where((df['year'] == 2020) | (df['year'] == 2021))
    df = df.iloc[idx]

    idx = np.where(df['headline'].str.contains('covid') | df['headline'].str.contains('corona'))
    df = df.iloc[idx]

    df['covid'] = 1

    df['my'] = df['month'].astype(str) + " " + df['year'].astype(str)

    # This section was to verify that groupby did the correct thing.
    #dates = list(df['my'].unique())
    #counts = np.zeros(len(dates))
    #for my in df['my']:
    #    idx = dates.index(my)
    #    counts[idx] += 1

    edf = pd.read_csv(ecdc, skipinitialspace=True)
    idx = np.where(edf['country'] == 'India')
    edf = edf.iloc[idx]
    edf['year_week'] = edf['year_week'].str.replace('-', '').astype(int)
    edf['lastdayweek'] = pd.to_datetime((edf['year_week']-1).astype(str) + "6", format="%Y%U%w")

    edf['month'] = pd.DatetimeIndex(edf['lastdayweek']).month_name()
    edf['year'] = pd.DatetimeIndex(edf['lastdayweek']).year

    edf['my'] = edf['month'].astype(str) + " " + edf['year'].astype(str)
    gedf = edf.groupby(['my'], sort=False).sum().reset_index(drop=False)
    gdf = df.groupby(['my'], sort=False).sum().reset_index(drop=False)
    gdf = gdf.iloc[::-1]


    plt.style.use('seaborn-poster')
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')
    fig, ax = plt.subplots(figsize=(15,10))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    reports = gdf['covid']/gdf['covid'].sum() * 100.
    cases = gedf['weekly_count']/gedf['weekly_count'].sum() * 100.

    ax.bar(gdf['my'], reports, label='No. of headlines')
    ax.plot(gedf['my'], cases, label='No. of cases', color='tab:orange')
    ax.set_ylabel('Fraction of total (\%)', fontsize=30)


    fmt = matplotlib.ticker.StrMethodFormatter("{x}")
   # ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)

    ax.tick_params(axis='both', width=4.0, length=15, labelsize=25)
    ax.tick_params(axis='x', rotation=60)
    ax.set_title('Coronavirus : Cases vs. Headlines', fontsize=40)

    plt.legend(fontsize=25)

    plt.tight_layout()
    plt.savefig('news_vs_cases.png', bbox_inches='tight')
    #plt.show()



if __name__ == '__main__':
    plot_news()
