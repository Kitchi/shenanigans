#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Pool

fname = 'headlines.txt'
base_url = 'https://indianexpress.com/section/india/'
beg = 0
if os.path.exists('page_no'):
    with open('page_no', 'r') as fptr:
        line = fptr.readlines()
        beg = int(line[0])

    print(f"Starting from page {beg} since the 'page_no' file exists.")


# They have 25117 pages of archives on the IE website at the time of writing
for pp in range(beg, 11525):
    titles = []
    print(f"Processing page {pp}/25118", end="\r")
    if pp > 0:
        page_url = base_url + f'page/{pp}/'
    else:
        page_url = base_url

    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for h2 in soup.findAll('h2', attrs={'class':'title'}):
        heading = h2.find('a').contents
        if len(heading) > 0:
            heading = heading[0]
        date = h2.findNextSibling('div').contents[0].strip()
        date = date.split()

        if len(date) == 0:
            continue

        with open(fname, 'a') as fptr:
            fptr.write(f"{str(date[0]):<9s} {str(date[1]).strip(','):<2s} "
                       f"{str(date[2]):<4s} {str(heading):<s}\n")

        np.savetxt('page_no', [pp,], fmt='%d')

#print(np.count_nonzero(titles))
