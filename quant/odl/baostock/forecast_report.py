# -*- coding: utf-8 -*-
"""季频业绩预告"""


from quant.odl.models import BS_Stock_Basic, BS_forecast_report
from quant.util.database import engine
from quant.util import logger
from quant.settings import QtConfig
import baostock as bs
import pandas as pd
import time
from tqdm import tqdm
import concurrent.futures
from datetime import datetime

_logger = logger.Logger(__name__).get_log()


def load_to_DB(data_df, param, pbar):
    """
    加载数据到数据库
    """

    data_df["profitForcastExpPubDate"] = pd.to_datetime(
        data_df["profitForcastExpPubDate"], format="%Y-%m-%d"
    )
    data_df["profitForcastExpStatDate"] = pd.to_datetime(
        data_df["profitForcastExpStatDate"], format="%Y-%m-%d"
    )

    data_df["profitForcastChgPctUp"] = pd.to_numeric(
        data_df["profitForcastChgPctUp"], errors="coerce"
    )
    data_df["profitForcastChgPctDwn"] = pd.to_numeric(
        data_df["profitForcastChgPctDwn"], errors="coerce"
    )

    try:
        data_df.to_sql(
            BS_forecast_report.__tablename__,
            engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:  # traceback.format_exc(1)
        _logger.error(
            "{}:{}至{}保存出错/{}".format(
                param["code"], param["start_date"], param["end_date"], repr(e)
            )
        )
    finally:
        pbar.update(1)


def get_forecast_report():

    codes = BS_Stock_Basic.get_stock_codes()

    #### 登陆系统 ####
    lg = bs.login()  # noqa

    codes_num = len(codes)
    with tqdm(total=codes_num) as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for code in codes:
                data_df = pd.DataFrame()
                max_try = 8  # 失败重连的最大次数
                for i in range(max_try):
                    param = {
                        "code": code,
                        "start_date": "2003-01-01",
                        "end_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                    rs = bs.query_forecast_report(**param)
                    if rs.error_code == "0":
                        data_df = data_df.append(rs.get_data())
                        break
                    elif i < (max_try - 1):
                        time.sleep(2)
                        continue
                    else:
                        _logger.error("respond error_code:" + rs.error_code)
                        _logger.error("respond  error_msg:" + rs.error_msg)
                        _logger.error("{}下载失败".format(code))

                if data_df.empty:
                    pbar.update(1)
                else:
                    executor.submit(load_to_DB, data_df, param, pbar)

    _logger.info("【季频盈利能力】数据全部下载完成")

    #### 登出系统 ####
    bs.logout()
