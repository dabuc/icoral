# -*- coding: utf-8 -*-
"""季频杜邦指数"""


# -*- coding: utf-8 -*-
"""季频现金流量"""

import pandas as pd
from quant.odl.baostock.util import crawl_finance_data
from quant.odl.models import BS_Dupont_Data
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

    data_df["dupontROE"] = pd.to_numeric(data_df["dupontROE"], errors="coerce")
    data_df["dupontAssetStoEquity"] = pd.to_numeric(
        data_df["dupontAssetStoEquity"], errors="coerce"
    )
    data_df["dupontAssetTurn"] = pd.to_numeric(
        data_df["dupontAssetTurn"], errors="coerce"
    )
    data_df["dupontPnitoni"] = pd.to_numeric(data_df["dupontPnitoni"], errors="coerce")
    data_df["dupontNitogr"] = pd.to_numeric(data_df["dupontNitogr"], errors="coerce")
    data_df["dupontTaxBurden"] = pd.to_numeric(
        data_df["dupontTaxBurden"], errors="coerce"
    )
    data_df["dupontIntburden"] = pd.to_numeric(
        data_df["dupontIntburden"], errors="coerce"
    )
    data_df["dupontEbittogr"] = pd.to_numeric(
        data_df["dupontEbittogr"], errors="coerce"
    )

    try:
        data_df.to_sql(
            BS_Dupont_Data.__tablename__,
            engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:  # traceback.format_exc(1)
        _logger.error(
            "{}:{}-{}保存出错/{}".format(
                param["code"], param["year"], param["quarter"], repr(e)
            )
        )


def get_dupont_data():

    #### 登陆系统 ####
    bs.login()  # noqa

    crawl_finance_data(bs.query_dupont_data, load_to_DB,BS_Dupont_Data)
    #### 登出系统 ####
    bs.logout()
