#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mercer@Zhihu
# Created Date: July 2022
# version ='0.1'
# ---------------------------------------------------------------------------
""" Get open market operations data from NY Fed."""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------


import os
from pathlib import Path
import pandas as pd
import datetime
from tqdm import tqdm


class OutRightTsyPurchase:

    def __init__(self, cache_dir):

        self.raw_data = None
        self.cache_dir = Path(cache_dir)
        self.api_root = 'https://markets.newyorkfed.org/api'
        self.api_series = 'tsy/all/results/details'

    def get_data_raw(self, read_cache=True):

        if not read_cache:
            dflist = []
            for year in tqdm(range(2000, datetime.date.today().year + 1)):
                try:
                    df = pd.read_csv(
                        f'{self.api_root}/{self.api_series}/search.csv?startDate=01/01/{year}&endDate=12/31/{year}'
                    )
                    dflist.append(df)
                except:
                    print(f"Loading {year} data failed.")
                    pass
            self.raw_data = pd.concat(dflist)
            self.raw_data.to_pickle(self.cache_dir / 'outrightpurchase.pkl')

        else:
            if not os.path.exists(self.cache_dir / 'outrightpurchase.pkl'):
                self.get_data_raw(read_cache=False)
            else:
                self.raw_data = pd.read_pickle(self.cache_dir / 'outrightpurchase.pkl')

    def post_processing(self):

        self.raw_data['Operation Date'] = pd.to_datetime(self.raw_data['Operation Date'].values.tolist())
        self.raw_data['Settlement Date'] = pd.to_datetime(self.raw_data['Settlement Date'].values.tolist())


if __name__ == "__main__":

    root_dir = Path(os.getcwd())
    if not os.path.exists(root_dir/'cache'):
        os.mkdir(root_dir/'cache')

    fed_tsy_or = OutRightTsyPurchase(root_dir/'cache')
    fed_tsy_or.get_data_raw(read_cache=False)
    fed_tsy_or.post_processing()

