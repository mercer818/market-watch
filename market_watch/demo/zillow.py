import os
from pathlib import Path
from market_watch.housing_watch.zillow import ZillowData

if __name__ == "__main__":

    root_dir = Path(os.getcwd())
    cache_dir = root_dir / 'zillow_cache'

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    zd = ZillowData(cache_dir)
    zd.build_urls()

    # Cache Zillow Home Value Index for Bedroom 5+ with ZIP-level granularity
    zd.cache_ZHVI_ZIP(zd.ZHVI_BR5_zip_url, 'ZHVI_BR5', 'ZHVI_BR5_zip', read_cache = False)

    # A wrapper of pre-defined caching routines
    zd.cache_all_data(read_cache=False)

    # Get access to cached data
    zd.data_dict['ZORI_ZIP']
