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


class TreasuryAuction:

    def __init__(self, cache_dir, start_date = "2008-1-1"):

        self.cache_dir = cache_dir
        self.update_cache = False
        self.has_cache = False
        self.start_date = pd.to_datetime(start_date)  # enforce the format of start_date
        self.end_date = pd.to_datetime(datetime.date.today())
        self.dates = [dt.strftime('%Y%m%d') for dt in pd.date_range(self.start_date, self.end_date, freq='B')]

        # the file names used to save cache files
        self.filename_result = f"auction_results_{self.dates[0]}_{self.dates[-1]}.csv"
        self.filename_ann = f"auction_announcements_{self.dates[0]}_{self.dates[-1]}.csv"

        # cache information placeholders
        self.cache_start_date = None
        self.cache_end_date = None
        self.cache_start_date_str = None
        self.cache_end_date_str = None
        self.residual_cache_dates = None
        self.residual_cache_dates_str = None
        self.result_old_cache_path = None
        self.ann_old_cache_path = None

        self.get_cache_meta()

    def get_cache_meta(self):

        """
        Search for any existing cache file and use the filename to determine the start and end dates of cache.
        """

        # if there is no existing cache, directly move to download new cache, otherwise, append to existing cache
        for f in os.listdir(self.cache_dir):
            if 'auction_results' in f:

                self.has_cache = True

                # existing cache names
                self.result_old_cache_path = self.cache_dir / f
                self.ann_old_cache_path = self.cache_dir / f.replace("auction_results", "auction_announcements")

                cache_start_date_str = f.replace('.csv', '').split('_')[2]
                cache_end_date_str = f.replace('.csv', '').split('_')[3]

                self.cache_start_date = pd.to_datetime(cache_start_date_str, format='%Y%m%d')
                self.cache_end_date = pd.to_datetime(cache_end_date_str, format='%Y%m%d')

                # the cache dates are updated to the residual dates
                if self.end_date > self.cache_end_date:
                    self.residual_cache_dates = pd.date_range(self.cache_end_date, self.end_date, freq='B')
                    self.residual_cache_dates_str = [dt.strftime('%Y%m%d') for dt in self.residual_cache_dates]
                    self.update_cache = True

    def get_auction_data(self, cache_dates):

        """A helper function that returns the auction results and announcement for a given range of cache dates."""

        df_result_list = []
        df_ann_list = []
        for dt in tqdm(cache_dates, desc='Caching Treasury auctions data'):
            ran_out = False
            n = 1
            while not ran_out:
                try:
                    df_result, df_ann = self._parse_data(self._get_result_url(dt, n))
                    df_result['Date'] = dt
                    df_result_list.append(df_result)
                    df_ann_list.append(df_ann)
                    n += 1
                except:
                    ran_out = True

        result_cache_df = pd.concat(df_result_list)
        ann_cache_df = pd.concat(df_ann_list)

        return result_cache_df, ann_cache_df

    def cache_auction_data(self):

        """
        A wrapper of get_auction_data, with additional routines to hdndle cache.
        """

        if not self.has_cache:
            self.result_cache_df, self.ann_cache_df = self.get_auction_data(self.dates)
        else:
            if self.update_cache:
                # read cache
                result_cache_old = pd.read_csv(self.result_old_cache_path)
                ann_cache_old = pd.read_csv(self.ann_old_cache_path)

                # append new data
                result_cache_new, ann_cache_new = self.get_auction_data(self.residual_cache_dates_str)
                self.result_cache_df = pd.concat([result_cache_old, result_cache_new]).drop_duplicates()
                self.ann_cache_df = pd.concat([ann_cache_old, ann_cache_new]).drop_duplicates()

                self.result_cache_df.to_csv(self.cache_dir / self.filename_result, index=False)
                self.ann_cache_df.to_csv(self.cache_dir / self.filename_ann, index=False)

                self._clean_cache()
            else:
                self.result_cache_df = pd.read_csv(self.result_old_cache_path)
                self.ann_cache_df = pd.read_csv(self.ann_old_cache_path)

    def _parse_data(self, url):

        """
        The primary method for parsing treasury auction information from XML files.

        :param url: the link of the auction result/announcement XML file.
        :return:
        """

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

    def _get_result_url(self, date, num):
        return f'https://www.treasurydirect.gov/xml/R_{date}_{num}.xml'

    def _clean_cache(self):
        os.remove(self.result_old_cache_path)
        os.remove(self.ann_old_cache_path)


if __name__ == "__main__":

    root_dir = Path(os.getcwd())
    if not os.path.exists(root_dir/'cache'):
        os.mkdir(root_dir/'cache')

    auction_loader = TreasuryAuction(root_dir/'cache', '2008-1-1')
    auction_loader.cache_auction_data()


