#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mercer@Zhihu
# Created Date: July 2022
# version ='0.1'
# ---------------------------------------------------------------------------

"""
Build a data collector of Zillow's relevant data, include:

1. ZHVI: Zillow Home Value Index
2. ZORI: Zillow Obeserved Rent Index
3. Inventory, Liast and Sales Prices, Sales Count and Price Cuts

"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
import pandas as pd


class ZillowData:

    def __init__(self, cache_dir):

        self.cache_dir = cache_dir
        self.data_dict = {}

    def build_urls(self):

        self.rental_url = "https://files.zillowstatic.com/research" \
                          "/public_csvs/zori/Zip_ZORI_AllHomesPlusMultifamily_Smoothed.csv?t=1658459810"

        self.ZHVI_BR1_ngh_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Neighborhood_zhvi_bdrmcnt_1_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR2_ngh_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Neighborhood_zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR3_ngh_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Neighborhood_zhvi_bdrmcnt_3_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR4_ngh_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Neighborhood_zhvi_bdrmcnt_4_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR5_ngh_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Neighborhood_zhvi_bdrmcnt_5_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR1_zip_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Zip_zhvi_bdrmcnt_1_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR2_zip_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Zip_zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR3_zip_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Zip_zhvi_bdrmcnt_3_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR4_zip_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Zip_zhvi_bdrmcnt_4_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

        self.ZHVI_BR5_zip_url = "https://files.zillowstatic.com/research/public_csvs/zhvi/"\
                                "Zip_zhvi_bdrmcnt_5_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv?t=1658459810"

    def cache_ZHVI_neighborhood(self, ZHVI_url, series_name, cache_name, read_cache=True):

        filename = self.cache_dir / f'{cache_name}_neighborhood.parquet'

        if not read_cache:

            ZHVI_data = (
                pd.read_csv(ZHVI_url)
                    .set_index(['RegionID', 'SizeRank', 'RegionName', 'RegionType',
                                'StateName', 'State', 'City', 'Metro', 'CountyName']).stack()
                    .reset_index().rename(columns={'level_9': 'Date', 0: series_name})
            )

            ZHVI_data.to_parquet(filename)
            self.data_dict[series_name] = ZHVI_data

        else:
            if os.path.exists(filename):
                ZHVI_data = pd.read_parquet(filename)
                self.data_dict[series_name] = ZHVI_data
            else:
                self.cache_ZHVI_neighborhood(ZHVI_url, series_name, cache_name, False)

    def cache_ZHVI_ZIP(self, ZHVI_url, series_name, cache_name, read_cache=True):

        filename = self.cache_dir / f'{cache_name}_ZIP.parquet'

        if not read_cache:

            ZHVI_data = (
                pd.read_csv(ZHVI_url)
                    .set_index(['RegionID', 'SizeRank', 'RegionName', 'RegionType',
                                'StateName', 'State', 'City', 'Metro', 'CountyName'])
                    .stack().reset_index().rename(columns={'level_9': 'Date', 0: series_name})
            )

            ZHVI_data.to_parquet(filename)
            self.data_dict[series_name] = ZHVI_data

        else:
            if os.path.exists(filename):
                ZHVI_data = pd.read_parquet(filename)
                self.data_dict[series_name] = ZHVI_data
            else:
                self.cache_ZHVI_neighborhood(ZHVI_url, series_name, cache_name, False)

    def cache_ZORI_ZIP(self, read_cache=True):

        filename = self.cache_dir / 'ZORI_ZIP.parquet'

        if not read_cache:

            ZORI_data = (
                pd.read_csv(self.rental_url)
                    .set_index(['RegionID', 'RegionName', 'SizeRank', 'MsaName']).stack()
                    .reset_index().rename(columns={'level_4': 'Date', 0: 'RENTAL'})
            )

            ZORI_data.to_parquet(self.cache_dir / 'ZORI_ZIP.parquet')
            self.data_dict['ZORI_ZIP'] = ZORI_data

        else:
            if os.path.exists(filename):
                ZORI_data = pd.read_parquet(filename)
                self.data_dict['ZORI'] = ZORI_data
            else:
                self.cache_ZORI_ZIP(False)

    def cache_all_data(self, read_cache=True):

        self.cache_ZHVI_neighborhood(self.ZHVI_BR1_ngh_url, 'ZHVI_BR1', 'ZHVI_BR1', read_cache)
        self.cache_ZHVI_neighborhood(self.ZHVI_BR2_ngh_url, 'ZHVI_BR2', 'ZHVI_BR2', read_cache)
        self.cache_ZHVI_neighborhood(self.ZHVI_BR3_ngh_url, 'ZHVI_BR3', 'ZHVI_BR3', read_cache)
        self.cache_ZHVI_neighborhood(self.ZHVI_BR4_ngh_url, 'ZHVI_BR4', 'ZHVI_BR4', read_cache)
        self.cache_ZHVI_neighborhood(self.ZHVI_BR5_ngh_url, 'ZHVI_BR5', 'ZHVI_BR5', read_cache)

        self.cache_ZHVI_ZIP(self.ZHVI_BR1_zip_url, 'ZHVI_BR1', 'ZHVI_BR1', read_cache)
        self.cache_ZHVI_ZIP(self.ZHVI_BR2_zip_url, 'ZHVI_BR2', 'ZHVI_BR2', read_cache)
        self.cache_ZHVI_ZIP(self.ZHVI_BR3_zip_url, 'ZHVI_BR3', 'ZHVI_BR3', read_cache)
        self.cache_ZHVI_ZIP(self.ZHVI_BR4_zip_url, 'ZHVI_BR4', 'ZHVI_BR4', read_cache)
        self.cache_ZHVI_ZIP(self.ZHVI_BR5_zip_url, 'ZHVI_BR5', 'ZHVI_BR5', read_cache)

        self.cache_ZORI_ZIP()

