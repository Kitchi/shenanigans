#!/usr/bin/env python3

import numpy as np
import nltk
import pandas as pd
import bottleneck as bn

from scipy.stats import median_abs_deviation
from scipy.interpolate import splrep, splev
from nltk.sentiment import SentimentIntensityAnalyzer
from multiprocessing import Pool
from datetime import datetime

import matplotlib.ticker
import matplotlib.pyplot as plt


# pandas read_csv won't work for headlines.txt so write a custom function
def read_file(fname):
    with open(fname, 'r') as fptr:
        lines = fptr.readlines()
        nlines = len(lines)

    day = np.zeros(nlines, dtype='object')
    month = np.zeros(nlines, dtype='object')
    year = np.zeros(nlines, dtype=int)
    headline = np.zeros(nlines, dtype='object')

    with open(fname, 'r') as fptr:
        for idx, line in enumerate(fptr):
            words = line.split()
            day[idx] = int(words[1])
            month[idx] = words[0]
            year[idx] = int(words[2])
            headline[idx] = " ".join(words[3:])

            #month.append(words[0])
            #year.append(int(words[2]))
            #headline.append(" ".join(words[3:]))

    return day, month, year, headline


sia = SentimentIntensityAnalyzer()

def get_sentiment(line):
    return sia.polarity_scores(line)['compound']

def main():
    '''
    pool = Pool(4)

    day, month, year, headline = read_file('headlines.txt')

    df = pd.DataFrame()
    df['day'] = day
    df['month'] = month
    df['year'] = year
    df['headline'] = headline

    df['my'] = df['month'].astype(str) + " " + df['year'].astype(str)
    stopwords = nltk.corpus.stopwords.words("english")
    stopwords = stopwords + ['says',]



    meanscore = []
    stdscore = []
    for mm in df['my'].unique():
        mdx = np.where(df['my'] == mm)
        tdf = df.iloc[mdx].reset_index(drop=True)

        #scores = np.zeros(tdf['headline'].size)
        scores = pool.map(get_sentiment, tdf['headline'].values)

        #for idx, line in enumerate(tdf['headline'].values):
        #    scores[idx] = sia.polarity_scores(line)['compound']

            #w = [w for w in line.split() if w.isalpha()]
            #w = [w for w in w if w.lower() not in stopwords]
            #words.extend(w)

        print(np.mean(scores), np.std(scores))
        meanscore.append(np.mean(scores))
        stdscore.append(np.std(scores))

    np.save('meanscore.npy', meanscore, allow_pickle=True)
    np.save('dfmyunique.npy', df['my'].unique(), allow_pickle=True)
    '''

    plt.style.use('seaborn-poster')
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')

    fig, ax = plt.subplots(figsize=(40,30))
    fig.autofmt_xdate()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    meanscore = np.load('meanscore.npy', allow_pickle=True)
    dfmy = np.load('dfmyunique.npy', allow_pickle=True)
    dfmy = pd.to_datetime(dfmy)

    #xspl = np.linspace(0, dfmy.size, 1000)
    #splc = splrep(np.arange(dfmy.size), meanscore, k=3)
    #yspl = splev(xspl, splc)
    #xspl = np.arange(dfmy.year.min(), dfmy.year.max())
    yspl = bn.move_mean(meanscore, window=9)

    ax.scatter(dfmy, meanscore)
    ax.plot(dfmy, yspl, c='tab:red', label='Rolling mean')

    ax.tick_params(axis='both', width=4.0, length=15, labelsize=50)
    ax.tick_params(axis='x', rotation=90)

    ax.set_xlabel('Date', fontsize=80)
    ax.set_ylabel('Sentiment', fontsize=80)

    plt.legend(fontsize=50)

    plt.savefig('headlines_sentiment.png', bbox_inches='tight')



if __name__ == '__main__':
    main()
