import matplotlib.pyplot as plt
from market_watch.utils.data_formatter import bar_plot_index_formatter


class ColorBox:
    def __init__(self):
        self.lightbluegrey = '#b7c9e2'
        self.vermillionred = '#f4320c'
        self.sunyellow = '#ffdf22'
        self.tealish = '#24bca8'
        self.azure = '#069af3'
        self.prussian = '#004577'
        self.vividblue = '#152eff'
        self.violet = '#5d06e9'


def remove_spines(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(True)
    return ax


def add_watermark(ax, source_label):
    ax.set_xlabel(f'Source: {source_label}, Compiled by Mercer@Zhihu', loc='left', color='gray')
    return ax


class Brush:

    @staticmethod
    def quick_bar_plot_month(data, ax=None, ylabel=None,
                             concise_xticks=False,
                             horizontal_xticks=False, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        year_index, month_index = bar_plot_index_formatter(data, 'M')
        ax = data.plot(kind='bar', ax=ax, **kwargs)

        # formatting xticks
        orig_ticks = ax.get_xticks()
        if not concise_xticks:
            _ = ax.set_xticks(orig_ticks, [x + y for x, y in zip(year_index, month_index)])
        else:
            _ = ax.set_xticks(orig_ticks, [x[-2:] + y for x, y in zip(year_index, month_index)])

        # other adjustments
        ax.set_ylabel(ylabel)
        ax.set_xlabel(None)
        ax.grid(axis='y', linestyle=':', color='lightgray')
        ax = remove_spines(ax)

        if horizontal_xticks:
            for label in ax.get_xticklabels(which='major'):
                label.set(rotation=0, horizontalalignment='center')

        return ax

    @staticmethod
    def quick_bar_plot_quarter(data, ax=None, ylabel=None, concise_xticks=False, horizontal_xticks=False, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        year_index, quarter_index = bar_plot_index_formatter(data, 'Q')
        ax = data.plot(kind='bar', ax=ax, **kwargs)

        # formatting xticks
        orig_ticks = ax.get_xticks()
        if not concise_xticks:
            _ = ax.set_xticks(orig_ticks, [x + y for x, y in zip(year_index, quarter_index)])
        else:
            _ = ax.set_xticks(orig_ticks, [x[-2:] + y for x, y in zip(year_index, quarter_index)])

        # other adjustments
        ax.set_ylabel(ylabel)
        ax.set_xlabel(None)
        ax.grid(axis='y', linestyle=':', color='lightgray')
        ax = remove_spines(ax)

        if horizontal_xticks:
            for label in ax.get_xticklabels(which='major'):
                label.set(rotation=0, horizontalalignment='center')

        return ax

    @staticmethod
    def quick_bar_plot_year(data, ax=None, ylabel=None, concise_xticks=False, horizontal_xticks=False, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        year_index = bar_plot_index_formatter(data, 'A')
        ax = data.plot(kind='bar', ax=ax, **kwargs)

        # formatting xticks
        orig_ticks = ax.get_xticks()
        if not concise_xticks:
            _ = ax.set_xticks(orig_ticks, year_index)
        else:
            _ = ax.set_xticks(orig_ticks, [y[-2:] for y in year_index])

        # other adjustments
        ax.set_ylabel(ylabel)
        ax.set_xlabel(None)
        ax.grid(axis='y', linestyle=':', color='lightgray')
        ax = remove_spines(ax)

        if horizontal_xticks:
            for label in ax.get_xticklabels(which='major'):
                label.set(rotation=0, horizontalalignment='center')

        return ax

    @staticmethod
    def quick_line_plot(data, ax=None, ref_date=None, ylabel=None, title=None, **kwargs):

        if ref_date is not None:
            data = data - data.loc[ref_date:].iloc[0, :]
            data = data.loc[ref_date:]

        if ax is None:
            fig, ax = plt.subplots()

        ax = data.plot(kind='line', ax=ax, **kwargs)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(None)
        if title is not None:
            ax.set_title(title, fontsize=14, fontweight='bold', loc='left', color='#939a90')
        ax.grid(axis='y', linestyle=':', color='lightgray')
        ax = remove_spines(ax)

        return ax

    @staticmethod
    def quick_area_plot(data, ax=None, ylabel=None, title=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        ax = data.plot(kind='area', ax=ax, **kwargs)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(None)
        if title is not None:
            ax.set_title(title, fontsize=14, fontweight='bold', loc='left', color='#939a90')
        ax.grid(axis='y', linestyle=':', color='lightgray')
        ax = remove_spines(ax)

        return ax

    @staticmethod
    def quick_hist(data, ax=None, ylabel=None, title=None, **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        ax = data.plot.hist(ax=ax, **kwargs)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(None)
        if title is not None:
            ax.set_title(title, fontsize=14, fontweight='bold', loc='left', color='#939a90')
        ax.grid(axis='x', linestyle=':', color='lightgray')
        ax = remove_spines(ax)

        return ax
