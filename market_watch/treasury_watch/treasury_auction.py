#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mercer@Zhihu
# Created Date: July 2022
# version ='0.1'
# ---------------------------------------------------------------------------
""" Parse auction announcements and results of U.S. Treasury securities"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
import sys
from pathlib import Path
import datetime
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
from tqdm import tqdm


def parse_data(url):
    page = req.get(url)
    soup = bs(page.content, "xml")
    auction_data = soup.contents[0]

    # parse information of auction results
    results = auction_data.find('AuctionResults')
    results_data_dict = {tag.name: tag.text for tag in results.find_all()}

    # parse information of auction announcement/meta
    announcement = auction_data.find('AuctionAnnouncement')
    ann_data_dict = {tag.name: tag.text for tag in announcement.find_all()}

    cusip = ann_data_dict['CUSIP']

    results_df = pd.DataFrame(data=results_data_dict, index=[cusip])
    announcement_df = pd.DataFrame(data=ann_data_dict, index=[cusip])

    return results_df, announcement_df


def get_result_url(date, num):
    return f'https://www.treasurydirect.gov/xml/R_{date}_{num}.xml'


def _get_data(cache_dates):

    """A helper function that returns the auction results and announcement for a given range of cache dates."""

    df_result_list = []
    df_ann_list = []
    for dt in tqdm(cache_dates, desc='Caching Treasury auctions data'):
        ran_out = False
        n = 1
        while not ran_out:
            try:
                df_result, df_ann = parse_data(get_result_url(dt, n))
                df_result['Date'] = dt
                df_result_list.append(df_result)
                df_ann_list.append(df_ann)
                n += 1
            except:
                ran_out = True

    result_cache_df = pd.concat(df_result_list)
    ann_cache_df = pd.concat(df_ann_list)

    return result_cache_df, ann_cache_df


def get_data(cache_dir, start_date='2008-01-01'):

    """
    A wrapper of _get_data, with additional routines to identify the non-cached dates and only download necesary data.

    :param cache_dir: the directory of cache data
    :param start_date: the starting date of cache.
    :return: two dataframes of auction results and announcements.
    """

    start_date = pd.to_datetime(start_date).strftime("%Y-%m-%d") # enforce the format of start_date
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    cache_dates = [dt.strftime('%Y%m%d') for dt in pd.date_range(start_date, end_date, freq='B')]

    # the file names used to save cache files
    result_filename = f"auction_results_{start_date.replace('-','')}_{end_date.replace('-','')}.csv"
    ann_filename = f"auction_announcements_{start_date.replace('-', '')}_{end_date.replace('-', '')}.csv"

    # if there is no existing cache, directly move to download new cache, otherwise, append to existing cache
    has_cache = False
    for f in os.listdir(cache_dir):
        if 'auction_results' in f:

            # we will use the existing cache dates to determine the starting date of appending cache file
            first_cache_dt = pd.to_datetime(f.replace('.csv', '').split('_')[2], format='%Y%m%d').strftime('%Y-%m-%d')
            last_cache_dt = pd.to_datetime(f.replace('.csv', '').split('_')[3], format='%Y%m%d').strftime('%Y-%m-%d')
            first_cache_dtstr = first_cache_dt.replace('-','')
            last_cache_dtstr = last_cache_dt.replace('-','')

            # the cache dates are updated to the residual dates
            cache_dates = [dt.strftime('%Y%m%d') for dt in pd.date_range(last_cache_dt, end_date, freq='B')]

            # existing cache names
            result_cache_name = cache_dir / f"auction_results_{first_cache_dtstr}_{last_cache_dtstr}.csv"
            ann_cache_name = cache_dir / f"auction_results_{first_cache_dtstr}_{last_cache_dtstr}.csv"
            has_cache = True

    if not has_cache:
        result_cache_df, ann_cache_df = _get_data(cache_dates)
    else:
        # read cache
        result_cache_old = pd.read_csv(cache_dir / result_cache_name)
        ann_cache_old = pd.read_csv(cache_dir / ann_cache_name)

        # append new data
        result_cache_new, ann_cache_new = _get_data(cache_dates)
        result_cache_df = pd.concat([result_cache_old, result_cache_new]).drop_duplicates()
        ann_cache_df = pd.concat([ann_cache_old, ann_cache_new]).drop_duplicates()

        # remove cache files
        os.remove(cache_dir / result_cache_name)
        os.remove(cache_dir / ann_cache_name)

    result_cache_df.to_csv(cache_dir / result_filename, index=False)
    ann_cache_df.to_csv(cache_dir / ann_filename, index=False)

    return result_cache_df, ann_cache_df


if __name__ == "__main__":

    root_dir = Path(os.getcwd())
    if not os.path.exists(root_dir/'cache'):
        os.mkdir(root_dir/'cache')

    result_data, announcement_data = get_data(root_dir/'cache')


