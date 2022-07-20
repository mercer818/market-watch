import pandas as pd


def month2quarter(m: str):
    if m in ['01', '02', '03']:
        return 'Q1'
    elif m in ['04', '05', '06']:
        return 'Q2'
    elif m in ['07', '08', '09']:
        return 'Q3'
    elif m in ['10', '11', '12']:
        return 'Q4'


def bar_plot_index_formatter(df, freq='Q'):
    """
    Turn the time index into desired format for plotting.
    """

    orig_index = df.index.tolist()
    if freq == 'Q':
        year_index = [dt.strftime('%Y') for dt in orig_index]
        quarter_index = [month2quarter(dt.strftime('%m')) for dt in orig_index]
        return year_index, quarter_index

    elif freq == 'M':
        year_index = [dt.strftime('%Y') for dt in orig_index]
        month_index = ['-' + dt.strftime('%b') for dt in orig_index]
        return year_index, month_index

    elif freq == 'A':
        year_index = [dt.strftime('%Y') for dt in orig_index]
        return year_index
