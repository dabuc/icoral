import concurrent.futures

from tqdm import tqdm
from quant.odl.models import BS_Stock_Basic
import time
from quant.util import logger
import pandas as pd


_logger = logger.Logger(__name__).get_log()


def crawl_finance_data(bs_query_func, load_data_func):
    """爬取季频财务数据"""

    codes = BS_Stock_Basic.get_stock_codes()

    codes_num = len(codes)
    with tqdm(total=codes_num) as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for code in codes:
                data_df = pd.DataFrame()
                for year in range(2007, 2021):
                    for quarter in range(1, 5):
                        max_try = 8  # 失败重连的最大次数
                        for i in range(max_try):
                            param = {"code": code, "year": year, "quarter": quarter}
                            rs = bs_query_func(**param)
                            if rs.error_code == "0":
                                tmp = rs.get_data()
                                tmp["quarter"] = quarter
                                tmp["year"] = year
                                data_df = data_df.append(tmp)
                                break
                            elif i < (max_try - 1):
                                time.sleep(2)
                                continue
                            else:
                                _logger.error("respond error_code:" + rs.error_code)
                                _logger.error("respond  error_msg:" + rs.error_msg)
                                _logger.error(
                                    "{}:{}-{}下载失败".format(code, year, quarter)
                                )

                if data_df.empty:
                    pbar.update(1)
                else:
                    executor.submit(load_data_func, data_df, param, pbar)

    _logger.info("数据全部下载完成")
