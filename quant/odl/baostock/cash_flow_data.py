# -*- coding: utf-8 -*-
"""季频现金流量"""

import pandas as pd
from quant.odl.baostock.util import crawl_finance_data
from quant.odl.models import BS_Cash_Flow_Data
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
    data_df["CAToAsset"] = pd.to_numeric(data_df["CAToAsset"], errors="coerce")
    data_df["NCAToAsset"] = pd.to_numeric(data_df["NCAToAsset"], errors="coerce")
    data_df["tangibleAssetToAsset"] = pd.to_numeric(data_df["tangibleAssetToAsset"], errors="coerce")
    data_df["ebitToInterest"] = pd.to_numeric(data_df["ebitToInterest"], errors="coerce")
    data_df["CFOToOR"] = pd.to_numeric(data_df["CFOToOR"], errors="coerce")
    data_df["CFOToNP"] = pd.to_numeric(data_df["CFOToNP"], errors="coerce")
    data_df["CFOToGr"] = pd.to_numeric(data_df["CFOToGr"], errors="coerce")

    try:
        data_df.to_sql(
            BS_Cash_Flow_Data.__tablename__,
            engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:  # traceback.format_exc(1)
        _logger.error("{}:{}-{}保存出错/{}".format(param["code"], param["year"], param["quarter"], repr(e)))


def get_cash_flow_data():

    #### 登陆系统 ####
    bs.login()  # noqa

    crawl_finance_data(bs.query_cash_flow_data, load_to_DB, BS_Cash_Flow_Data)
    #### 登出系统 ####
    bs.logout()
