# -*- coding: utf-8 -*-
"""季频盈利能力"""

from quant.odl.models import BS_Profit_Data, BS_Stock_Basic, Task_Details
from quant.util.database import session_scope, engine
from quant.util import logger
from quant.settings import QtConfig
import baostock as bs
import pandas as pd
import time
from tqdm import tqdm
from quant.util.helper import is_dev_env
import concurrent.futures

_logger = logger.Logger(__name__).get_log()

def get_query_codes():

    with session_scope() as sm:
        query = sm.query(BS_Stock_Basic.code).filter(
            BS_Stock_Basic.type == 1, BS_Stock_Basic.status == 1
        )

        if is_dev_env():
            codes = query.limit(100)
        else:
            codes = query.all()

        

        result = [(x.code) for x in codes]

        return result


def load_to_DB(data_df,pbar):
    """
    加载数据到数据库
    """
    data_df["pubDate"] = pd.to_datetime(data_df["pubDate"], format="%Y-%m-%d")
    data_df["statDate"] = pd.to_datetime(data_df["statDate"], format="%Y-%m-%d")
    data_df["roeAvg"] = pd.to_numeric(data_df["roeAvg"], errors="coerce")
    data_df["npMargin"] = pd.to_numeric(data_df["npMargin"], errors="coerce")
    data_df["gpMargin"] = pd.to_numeric(data_df["gpMargin"], errors="coerce")
    data_df["netProfit"] = pd.to_numeric(data_df["netProfit"], errors="coerce")
    data_df["epsTTM"] = pd.to_numeric(data_df["epsTTM"], errors="coerce")
    data_df["MBRevenue"] = pd.to_numeric(data_df["MBRevenue"], errors="coerce")
    data_df["totalShare"] = pd.to_numeric(
        data_df["totalShare"], errors="coerce"
    )
    data_df["liqaShare"] = pd.to_numeric(data_df["liqaShare"], errors="coerce")

    data_df.to_sql(
        BS_Profit_Data.__tablename__,
        engine,
        if_exists="append",
        index=False,
    )
    # _logger.info("{}【季频盈利能力】数据下载完成".format(code))
    pbar.update(1)


def get_profit_data():

    codes = get_query_codes()

    #### 登陆系统 ####
    lg = bs.login()  # noqa

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
                            rs = bs.query_profit_data(**param)
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
                                _logger.error("{}:{}-{}下载失败".format(code, year, quarter))

                if not data_df.empty:
                    executor.submit(load_to_DB, data_df,pbar)
            

        _logger.info("【季频盈利能力】数据全部下载完成")

    #### 登出系统 ####
    bs.logout()
