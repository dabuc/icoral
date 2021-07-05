# -*- coding: utf-8 -*-
"""季频成长能力"""

import pandas as pd
from quant.odl.baostock.util import crawl_finance_data
from quant.odl.models import BS_Growth_Data
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
    data_df["YOYEquity"] = pd.to_numeric(data_df["YOYEquity"], errors="coerce")
    data_df["YOYAsset"] = pd.to_numeric(data_df["YOYAsset"], errors="coerce")
    data_df["YOYNI"] = pd.to_numeric(data_df["YOYNI"], errors="coerce")
    data_df["YOYEPSBasic"] = pd.to_numeric(data_df["YOYEPSBasic"], errors="coerce")
    data_df["YOYPNI"] = pd.to_numeric(data_df["YOYPNI"], errors="coerce")

    try:
        data_df.to_sql(
            BS_Growth_Data.__tablename__,
            engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:  # traceback.format_exc(1)
        _logger.error("{}:{}-{}保存出错/{}".format(param["code"], param["year"], param["quarter"], repr(e)))


def get_growth_data():

    #### 登陆系统 ####
    bs.login()  # noqa

    crawl_finance_data(bs.query_growth_data, load_to_DB, BS_Growth_Data)
    #### 登出系统 ####
    bs.logout()
