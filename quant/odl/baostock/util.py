import concurrent.futures
import datetime

from tqdm import tqdm
from quant.odl.models import BS_Stock_Basic
import time
from quant.util import logger
import pandas as pd
import baostock as bs

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


def crawl_query_history_k_data_plus(
    code, fields, start_date="2015-01-01", end_date=datetime.datetime.now().date(), frequency="d", adjustflag="3"
) -> pd.DataFrame:
    """根据查询条件查询指定K线数据，如果查询错误，重复查询8次

    Args:
        code (str): 证券代码
        fields (str): 查询字段
        start_date (str, optional): 开始时间. Defaults to "2015-01-01".
        end_date ([type], optional): 结束时间. Defaults to datetime.datetime.now().date().
        frequency (str, optional): 数据类型，默认为d.
        adjustflag (str, optional): 复权类型，默认不复权：3；1：后复权；2：前复权。

    Returns:
        [pd.DataFrame]: [查询结果集]
    """
    max_try = 8  # 失败重连的最大次数
    for i in range(max_try):
        k_rs = bs.query_history_k_data_plus(
            code, fields, start_date=start_date, end_date=end_date, frequency=frequency, adjustflag=adjustflag
        )
        if k_rs.error_code == "0":
            data_df = k_rs.get_data()
            return data_df
        elif i < (max_try - 1):
            time.sleep(2)
            continue
        else:
            _logger.error("获取历史A股K线数据失败/query_history_k_data_plus respond error_code:" + k_rs.error_code)
            _logger.error("获取历史A股K线数据失败/query_history_k_data_plus respond  error_msg:" + k_rs.error_msg)
