#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Mercer@Zhihu
# Created Date: July 2022
# version ='0.1'
# ---------------------------------------------------------------------------
""" Data Loader for FRED time series data."""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
import xarray as xr

from fredapi import Fred

api_key = '9a9dc2c044a03d2b8a7ffc62316ec01f'
fred = Fred(api_key)


class FREDSeries:

    def __init__(self, series_id: str):

        self.series_xr = None
        self.data_raw = None

        # first, get meta info
        _meta = fred.search(series_id)
        try:
            # multiple relevant results could be returned for the series_id, select the row with the exact id
            meta = _meta.loc[series_id]
        except:
            # if no results returned for the series_id, raise error
            raise KeyError('No results found for series_id: {}.'.format(series_id))

        self.id = series_id
        self.title = meta.title
        self.observation_start = meta.observation_start
        self.observation_end = meta.observation_end
        self.frequency = meta.frequency
        self.frequency_short = meta.frequency_short
        self.units = meta.units
        self.units_short = meta.units_short
        self.seasonal_adjustment = meta.seasonal_adjustment
        self.seasonal_adjustment_short = meta.seasonal_adjustment_short
        # self.last_update = meta.last_update
        self.notes = meta.notes
        self.attrs = {'id': self.id, 'title': self.title,
                      'start_date': self.observation_start.strftime('%Y-%m-%d'),
                      'end_date': self.observation_end.strftime('%Y-%m-%d'),
                      'frequency': self.frequency, 'units': self.units,
                      'units_short': self.units.split('of')[0].strip(),
                      'seasonal_adj': self.seasonal_adjustment,
                      'seasonal_adj_short': self.seasonal_adjustment_short,
                      }

    def get_raw_data(self):

        self.data_raw = fred.get_series(self.id)
        self.series_xr = xr.DataArray(
            data=self.data_raw.values,
            coords={'as_of_date': self.data_raw.index},
            name=self.id,
            attrs=self.attrs
        )


class FRED:

    def __init__(self, cache_path):

        self.raw_series_data = None
        self.aligned_series_data = None
        self.cache_path = cache_path
        self.id2name = {}
        self.unit_mapper = {'Thousands': 1e3, 'Millions': 1e6, 'Billions': 1e9, 'Trillions': 1e12}

        if not os.path.exists(self.cache_path / 'raw_series'):
            os.mkdir(self.cache_path / 'raw_series')

    def cache_fred_series(self, series_list, update=True):

        print("======================================")
        print("Caching time series data from FRED ...")
        print("======================================")

        raw_series_data = {}
        for s in series_list:
            file_path = self.cache_path / 'raw_series' / f"{s}.cdf"
            s_obj = FREDSeries(s)
            if not update:
                if os.path.exists(file_path):
                    raw_series_data[s] = xr.open_dataarray(file_path)
                    print(f'Loaded cached data for {s}...')
                else:
                    s_obj.get_raw_data()
                    raw_series_data[s] = s_obj.series_xr
                    s_obj.series_xr.to_netcdf(file_path)
                    print(f"{s} is not cached, downloaded the latest data.")
            else:
                s_obj.get_raw_data()
                raw_series_data[s] = s_obj.series_xr
                s_obj.series_xr.to_netcdf(file_path)
                print(f"Data for {s} is cached.")

        self.raw_series_data = raw_series_data

    def print_series(self):

        print("======================================")
        print("Cached time series data details:")
        print("======================================")

        for s, da in self.raw_series_data.items():
            self.id2name[s] = da.attrs['title']
            print(s, '|', self.id2name[s])

    def align_units(self, target_units='Billions'):

        print("===============================================")
        print(f"Align units of all time series to {target_units} ...")
        print("===============================================")

        self.aligned_series_data = {}

        for s, da in self.raw_series_data.copy().items():
            org_units = da.attrs['units_short']
            unit_scaling_ratio = self.unit_mapper[org_units] / self.unit_mapper[target_units]
            self.aligned_series_data[s] = da * unit_scaling_ratio
            self.aligned_series_data[s].attrs = da.attrs
            self.aligned_series_data[s].attrs['units_short'] = target_units
            self.aligned_series_data[s].attrs['units'] = da.attrs['units'].replace(org_units, target_units)
            print(f"{s}: original units is {org_units}, transformed to {target_units}.")