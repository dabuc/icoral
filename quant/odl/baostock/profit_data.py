# -*- coding: utf-8 -*-
"""季频盈利能力"""

import pandas as pd
from quant.odl.baostock.util import crawl_finance_data
from quant.odl.models import BS_Profit_Data
from quant.util.database import engine

import baostock as bs
from quant.util import logger

_logger = logger.Logger(__name__).get_log()


def load_to_DB(data_df, param):
    """
    加载数据到数据库
    """
    data_df["pubDate"] = pd.to_datetime(data_df["pubDate"])
    data_df["statDate"] = pd.to_datetime(data_df["statDate"])
    data_df["roeAvg"] = pd.to_numeric(data_df["roeAvg"], errors="coerce")
    data_df["npMargin"] = pd.to_numeric(data_df["npMargin"], errors="coerce")
    data_df["gpMargin"] = pd.to_numeric(data_df["gpMargin"], errors="coerce")
    data_df["netProfit"] = pd.to_numeric(data_df["netProfit"], errors="coerce")
    data_df["epsTTM"] = pd.to_numeric(data_df["epsTTM"], errors="coerce")
    data_df["MBRevenue"] = pd.to_numeric(data_df["MBRevenue"], errors="coerce")
    data_df["totalShare"] = pd.to_numeric(data_df["totalShare"], errors="coerce")
    data_df["liqaShare"] = pd.to_numeric(data_df["liqaShare"], errors="coerce")

    try:
        data_df.to_sql(
            BS_Profit_Data.__tablename__,
            engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:  # traceback.format_exc(1)
        _logger.error("{}:{}-{}保存出错/{}".format(param["code"], param["year"], param["quarter"], repr(e)))


def get_profit_data():
    #### 登陆系统 ####
    bs.login()  # noqa

    crawl_finance_data(bs.query_profit_data, load_to_DB, BS_Profit_Data)
    #### 登出系统 ####
    bs.logout()
