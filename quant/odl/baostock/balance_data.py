# -*- coding: utf-8 -*-
"""季频偿债能力"""

import pandas as pd
from quant.odl.baostock.util import crawl_finance_data
from quant.odl.models import BS_Balance_Data
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
    data_df["currentRatio"] = pd.to_numeric(data_df["currentRatio"], errors="coerce")
    data_df["quickRatio"] = pd.to_numeric(data_df["quickRatio"], errors="coerce")
    data_df["cashRatio"] = pd.to_numeric(data_df["cashRatio"], errors="coerce")
    data_df["YOYLiability"] = pd.to_numeric(data_df["YOYLiability"], errors="coerce")
    data_df["liabilityToAsset"] = pd.to_numeric(data_df["liabilityToAsset"], errors="coerce")
    data_df["assetToEquity"] = pd.to_numeric(data_df["assetToEquity"], errors="coerce")

    try:
        data_df.to_sql(
            BS_Balance_Data.__tablename__,
            engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:  # traceback.format_exc(1)
        _logger.error("{}:{}-{}保存出错/{}".format(param["code"], param["year"], param["quarter"], repr(e)))


def get_balance_data():

    #### 登陆系统 ####
    bs.login()  # noqa

    crawl_finance_data(bs.query_balance_data, load_to_DB, BS_Balance_Data)
    #### 登出系统 ####
    bs.logout()
