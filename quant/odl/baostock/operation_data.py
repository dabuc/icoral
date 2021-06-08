# -*- coding: utf-8 -*-
"""季频营运能力"""

import pandas as pd
from quant.odl.baostock.util import crawl_finance_data
from quant.odl.models import BS_Operation_Data
from quant.util.database import engine

import baostock as bs
from quant.util import logger

_logger = logger.Logger(__name__).get_log()


def load_to_DB(data_df, param):
    """
    加载数据到数据库
    """

    data_df["pubDate"] = pd.to_datetime(data_df["pubDate"], format="%Y-%m-%d")
    data_df["statDate"] = pd.to_datetime(data_df["statDate"], format="%Y-%m-%d")
    data_df["NRTurnRatio"] = pd.to_numeric(data_df["NRTurnRatio"], errors="coerce")
    data_df["NRTurnDays"] = pd.to_numeric(data_df["NRTurnDays"], errors="coerce")
    data_df["INVTurnRatio"] = pd.to_numeric(data_df["INVTurnRatio"], errors="coerce")
    data_df["INVTurnDays"] = pd.to_numeric(data_df["INVTurnDays"], errors="coerce")
    data_df["CATurnRatio"] = pd.to_numeric(data_df["CATurnRatio"], errors="coerce")
    data_df["AssetTurnRatio"] = pd.to_numeric(data_df["AssetTurnRatio"], errors="coerce")

    try:
        data_df.to_sql(
            BS_Operation_Data.__tablename__,
            engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:  # traceback.format_exc(1)
        _logger.error("{}:{}-{}保存出错/{}".format(param["code"], param["year"], param["quarter"], repr(e)))


def get_operation_data():

    #### 登陆系统 ####
    bs.login()  # noqa

    crawl_finance_data(bs.query_operation_data, load_to_DB, BS_Operation_Data)
    #### 登出系统 ####
    bs.logout()
