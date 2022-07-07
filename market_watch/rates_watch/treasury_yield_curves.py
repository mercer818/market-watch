#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Mercer@Zhihu
# Created Date: July 2022
# version ='0.1'
# ---------------------------------------------------------------------------
""" Parse yield curve data from U.S. Treasury website"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
import pandas as pd
from tqdm import tqdm
from pathlib import Path


# Fetch data for a particular year
# 先定一个抓取某年数据的函数
def get_yc_per_year(curve_type: str, year: int):
    tsy_rates_url = 'https://home.treasury.gov/resource-center/' \
                    f'data-chart-center/interest-rates/daily-treasury-rates.csv' \
                    f'/{year}/all?type={curve_type}&field_tdr_date_value={year}&page&_format=csv'

    return pd.read_csv(tsy_rates_url)


# Apply the data parser to all years and clean the data
# 将上面这个函数应用到想要抓取数据的年份，并做一些简单的数据清洗
def get_yc_from_treasury(curve_type, years: list):
    """
    Get Treasury yield curves data from US Treasury data API.

    Parameters
    ----------
    curve_type: str
        The name of the yield curve to fetch, chosen from one of the followings:
            - "daily_treasury_bill_rates"
            - "daily_treasury_yield_curve" (since 1990)
            - "daily_treasury_real_yield_curve" (since 2003)
    years: list
        A list of years (integers) to fetch the data from.

    Returns
    -------
    yc_data: pd.DataFrame
        A dataframe of yield curve data with columns being the tenors and index being dates.
    """

    # fetch yield curves data for all years
    dflist = []
    for y in tqdm(years, desc=f"Fetching yield curve data for {curve_type.replace('_',' ')}."):
        try:
            dflist.append(get_yc_per_year(curve_type, y))
        except:
            print(f'Data fetching failed for year {y}.')
            pass
    yc_data = pd.concat(dflist)

    # clean data
    type_map = {c: float for c in yc_data.columns if c != 'Date'}

    yc_data = (
        yc_data
            .assign(Date=lambda x: pd.to_datetime(x['Date'].values))
            .pipe(pd.DataFrame.set_index, 'Date')
            .pipe(pd.DataFrame.sort_index)
            .pipe(pd.DataFrame.astype, type_map)
            .pipe(pd.DataFrame.rename, columns=lambda x: x.replace(' YR', 'Y'))
    )

    return yc_data


if __name__ == "__main__":

    root_dir = Path(os.getcwd())
    if not os.path.exists(root_dir/'cache'):
        os.mkdir(root_dir/'cache')
    if not os.path.exists(root_dir/'cache'/'Rates'):
        os.mkdir(root_dir/'cache'/'Rates')

    us_bill_rates = get_yc_from_treasury('daily_treasury_bill_rates',
                                         [y for y in range(1990, 2023)])
    us_bill_rates.to_csv(root_dir / 'cache' / 'Rates' / "daily_treasury_bill_rates.csv")

    us_nom_yields = get_yc_from_treasury('daily_treasury_yield_curve',
                                         [y for y in range(1990, 2023)])
    us_nom_yields.to_csv(root_dir / 'cache' / 'Rates' / "daily_treasury_yield_curve.csv")

    us_real_yields = get_yc_from_treasury('daily_treasury_real_yield_curve',
                                          [y for y in range(1990, 2023)])
    us_nom_yields.to_csv(root_dir / 'cache' / 'Rates' / "daily_treasury_real_yield_curve.csv")