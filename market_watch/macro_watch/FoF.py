#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Mercer@Zhihu
# Created Date: July 2022
# version ='0.1'
# ---------------------------------------------------------------------------
""" A data loader of Federal Reserve's Flow of Funds data."""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sys
import os
import datetime
import pandas as pd
import numpy as np

import requests as req
from io import StringIO
from pathlib import Path


class GenericFoF:

    def __init__(self, series_id: str):
        """
        :param series_id: identifiers for a particular table, e.g., 8bfa7e966f36b2bfd04b129267d1fe75 for L210.Q
        US Treasury securities (levels).
        """

        self.series_id = series_id
        self.table_url = "https://www.federalreserve.gov/datadownload/Output.aspx?" \
                         f"rel=Z1&series={self.series_id}" \
                         "&lastobs=" \
                         f"&from=03/01/1945&to=12/31/{datetime.datetime.today().year}" \
                         "&filetype=csv&label=include&layout=seriescolumn"
        self.meta = self.get_meta()
        self.data = self.get_table()

    def get_meta(self):
        meta_raw = pd.read_csv(
            StringIO(req.get(self.table_url).content.decode()),
            index_col=0, nrows=5, header=None
        )

        meta = (
            meta_raw
            .rename(lambda x: x.strip().lower().replace(':', '').replace(' ', '_')).T
            .set_index('unique_identifier')
        )

        return meta

    def get_table(self):

        rename_dict = self.meta['series_description'].to_dict()  # from unique identifiers to descriptions

        data = (
            pd.read_csv(StringIO(req.get(self.table_url).content.decode()), skiprows=4)
            .iloc[1:, :]  # skip the row of non-unique identifiers
            .pipe(pd.DataFrame.rename, columns=rename_dict)  # turn identifiers to descriptions
            .pipe(pd.DataFrame.rename, columns={'Unique Identifier: ': 'date'})
            .assign(date=lambda x: pd.to_datetime(x.date.values))
            .pipe(pd.DataFrame.set_index, 'date')
            .pipe(pd.DataFrame.replace, {'ND': np.nan})
            .pipe(pd.DataFrame.astype, float)
            .stack().reset_index().rename(columns={'level_1': 'varname', 0: 'value'}) # a long table
        )

        return data

    def cache_data(self):
        root_dir = Path(os.getcwd())
        if not os.path.exists(root_dir/'cache'):
            os.mkdir(root_dir/'cache')
        if not os.path.exists(root_dir/'cache'/'FoF'):
            os.mkdir(root_dir/'cache'/'FoF')
        self.data.to_csv(root_dir/'cache'/'FoF'/f"{self.series_id}.csv")


class USTreasuries(GenericFoF):

    def __init__(self):

        super().__init__('8bfa7e966f36b2bfd04b129267d1fe75')
        self.clean_data()
        self.cache_data()

    def clean_data(self):
        self.data = (
            self.data
                .assign(participant=lambda x: self.parse_L210Q_desc(x, 'participant'))
                .assign(asset_type=lambda x: self.parse_L210Q_desc(x, 'instrument_type'))
                .assign(asset_or_liability=lambda x: self.parse_L210Q_desc(x, 'asset_or_liability'))
        )

    def get_treasury_holdings(self):

        # these asset types will be kept to calculate the total market value of Treasury holdings by participant group
        asset_types_to_aggregate = [
            'treasury_securities',
            'treasury_securities_held_by_thrift_savings_plan',
            'treasury_securities_including_slgs',
            'treasury_securities_excluding_slgs',
            'total_u.s._government_securities',
            'total_treasury_securities',
            'treasury_securities_including_those_held_by_u.s._residual_market_reinsurers',
            'treasury_securities_(net)'
        ]

        # these participant will be excluded from aggregation due to double counting
        holder_types_to_exclude = [
            'federal_government',
            'federal_government_defined_contribution_retirement_funds',
            'federal_government_defined_benefit_retirement_funds',
            'private_defined_contribution_pension_funds',
            'private_defined_benefit_pension_funds'
        ]

        filter_str_asset = ','.join(["'{}'".format(a) for a in asset_types_to_aggregate])
        filter_str_holder = ','.join(["'{}'".format(h) for h in holder_types_to_exclude])

        level_by_holder = (
            self.data
            .query(f"participant not in ({filter_str_holder})")
            .query(f"asset_type in ({filter_str_asset})")
            .query(f"asset_or_liability in ('asset', 'asset_(market_value)')")
            .groupby(['date', 'participant']).value.sum()
            .apply(lambda x: x / 1e3)  # transform data from Millions to Billions
            .unstack().resample('Q').last()
        )

        filepath = Path(os.getcwd())/'cache'/'FoF'/f'{self.series_id}_treasury_holdings.csv'
        level_by_holder.to_csv(filepath)

        return level_by_holder

    def parse_L210Q_desc(self, x: pd.DataFrame, desc_item):
        """
        Return a list of parsed information specified in desc_item.

        :param x: the long format table of FoF data.
        :param desc_item: chosen from (participant, instrument_type, asset_or_liability)
        :return: a list of parsed information.
        """

        return [self._parse_L210Q_desc(name).get(desc_item) for name in x['varname']]

    @staticmethod
    def _parse_L210Q_desc(x: str):

        """
        :param x: a string of description that can be parsed into participant, asset type, and asset/liability
        :return: a dictionary of parsed data
        """

        varname_list = x.split(';')

        # assign null values if no meaningful data found
        parsed_dict = {
            'participant': np.nan,
            'instrument_type': np.nan,
            'asset_or_liability': np.nan
        }

        # For the current L210.Q table, holdings data follows a format with 3 components
        if len(varname_list) > 2:
            parsed_dict = {
                'participant': varname_list[0].lower().strip().replace(',', '').replace(' ', '_'),
                'instrument_type': varname_list[1].lower().strip().replace(',', '').replace(' ', '_'),
                'asset_or_liability': varname_list[2].lower().strip().replace(',', '').replace(' ', '_')
            }

        return parsed_dict



