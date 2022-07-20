import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from market_watch.fed_watch.fred import FREDSeries, FRED
from market_watch.utils.brush import Brush


def load_fred(cache_path, series_dict, units='Trillions'):
    cache_data = FRED(cache_path)
    cache_data.cache_fred_series(list(series_dict.keys()), update=True)  # cache time series data
    cache_data.print_series()  # show the series cached for this run
    cache_data.align_units(units)  # align the units of level variables

    # combine all the time series data into one pandas dataframe
    dflist = []
    for s, da in cache_data.aligned_series_data.items():
        dflist.append(da.to_dataframe(name=s))
    plot_data = pd.concat(dflist, axis=1).rename(columns=series_dict)

    return cache_data, plot_data


if __name__ == "__main__":

    root_dir = Path(os.getcwd())
    if not os.path.exists(root_dir / 'fred_cache'):
        os.mkdir(root_dir / 'fred_cache')

    if not os.path.exists(root_dir / 'figures'):
        os.mkdir(root_dir / 'figures')

    series_dict = {
        'WDTGAL': 'TGA',
        'RRPONTTLD': 'ON RRP',
        'MVMTD027MNFRBDAL': 'Treasury Debt',
        'M2NS': 'M2',
        'WTFSRFL': 'QE'
    }

    fred_data, plot_data = load_fred(root_dir/'fred_cache', series_dict, 'Trillions')

    # resample and define new variables
    plot_data = plot_data.resample('M').mean().copy()
    plot_data['TGA+M2'] = plot_data['TGA'] + plot_data['M2']

    # plot data
    vars_to_plot = ['TGA', 'ON RRP', 'Treasury Debt', 'M2', 'TGA+M2', 'QE']
    Brush.quick_line_plot(plot_data[vars_to_plot],
                          title='MMT Tracker',
                          figsize=(8,5),
                          ref_date='2019-12-31',  # set the end of 2019 as the reference date
                          marker='o')

    plt.savefig(root_dir/'figures'/'mmt.jpg', bbox_inches='tight', dpi=200)