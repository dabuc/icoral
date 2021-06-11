# -*- coding: utf-8 -*-
"""A股K线数据"""
import concurrent.futures
import datetime

import pandas as pd
from quant.odl.baostock.util import crawl_query_history_k_data_plus
from quant.odl.models import (
    BS_Daily,
    BS_Daily_hfq,
    BS_m30_hfq,
    BS_m60_hfq,
    BS_Stock_Basic,
    BS_Trade_Dates,
    BS_Weekly_hfq,
)
from quant.util import logger
from quant.util.database import engine
from sqlalchemy import func, select
from tqdm import tqdm

import baostock as bs

_logger = logger.Logger(__name__).get_log()


def __get_fields(frequency="d") -> str:
    """
    获取历史A股K线数据的字段列
    """
    d_fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,\
    tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
    w_m_fields = "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"
    min_fields = "date,time,code,open,high,low,close,volume,amount,adjustflag"

    frequency_fields = {
        "d": d_fields,
        "w": w_m_fields,
        "m": w_m_fields,
        "5": min_fields,
        "15": min_fields,
        "30": min_fields,
        "60": min_fields,
    }

    return frequency_fields[frequency]


def __get_params(frequency="d", adjustflag="3"):
    """
    获取参数：code，起止时间
    """

    s1 = select(BS_Stock_Basic.code, BS_Stock_Basic.ipoDate)
    if adjustflag == "1" or frequency == "60" or frequency == "30":  # 后复权
        s1 = s1.where(BS_Stock_Basic.type == "1")  # 只有股票有复权数据，指数没有
    df1 = pd.read_sql(s1, engine)

    table_model = BS_Daily
    if frequency == "d" and adjustflag == "1":
        table_model = BS_Daily_hfq
    elif frequency == "w" and adjustflag == "1":
        table_model = BS_Weekly_hfq
    elif frequency == "60" and adjustflag == "1":
        table_model = BS_m60_hfq
    elif frequency == "30" and adjustflag == "1":
        table_model = BS_m30_hfq

    s2 = select(table_model.code, func.max(table_model.date).label("mx_date")).group_by(table_model.code)
    df2 = pd.read_sql(s2, engine)

    df3 = df1.merge(df2, "left", on="code")

    # 获取最新交易日期
    t = BS_Trade_Dates.get_lastest_trade_date()
    df3["end_date"] = t if t is not None else datetime.datetime.now().date()

    condition1 = df3["mx_date"].isnull()
    df3.loc[condition1, "start_date"] = df3.loc[condition1, "ipoDate"]
    code1 = df3[condition1]
    code1 = code1[["code", "start_date", "end_date"]]
    # print(code1)

    condition2 = df3["mx_date"] < datetime.datetime.now().date()
    df3.loc[condition2, "start_date"] = df3.loc[condition2, "mx_date"] + datetime.timedelta(days=1)
    code2 = df3[condition2]
    code2 = code2[["code", "start_date", "end_date"]]
    # print(code2)

    t = pd.concat([code1, code2])
    result = t.to_dict(orient="records")
    return result


def get_history_k_data(frequency="d", adjustflag="3"):
    """
    获取历史A股K线数据
    """

    # 获取指定日期的指数、股票数据
    data_df = pd.DataFrame()
    params = __get_params(frequency, adjustflag)
    fields = __get_fields(frequency)
    load_to_DB = _load_to_DB[frequency]
    bs.login()
    codes_num = len(params)
    with tqdm(total=codes_num) as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for task in params:
                start_date = datetime.datetime.strftime(task["start_date"], "%Y-%m-%d")
                end_date = datetime.datetime.strftime(task["end_date"], "%Y-%m-%d")

                k_rs_data = crawl_query_history_k_data_plus(
                    task["code"],
                    fields,
                    start_date=start_date,
                    end_date=end_date,
                    frequency=frequency,
                    adjustflag=adjustflag,
                )
                data_df = data_df.append(k_rs_data)
                if len(data_df) > 6000:
                    tmp = data_df
                    executor.submit(load_to_DB, tmp, frequency, adjustflag)
                    data_df = pd.DataFrame()

                pbar.update(1)
        load_to_DB(data_df, frequency, adjustflag)

    bs.logout()


def _load_daily_to_DB(data_df: pd.DataFrame, frequency, adjustflag):
    if data_df.empty:
        return

    try:
        data_df["date"] = pd.to_datetime(data_df["date"], format="%Y-%m-%d")
        # data_df['code'] =
        data_df["open"] = pd.to_numeric(data_df["open"], errors="coerce")
        data_df["high"] = pd.to_numeric(data_df["high"], errors="coerce")
        data_df["low"] = pd.to_numeric(data_df["low"], errors="coerce")
        data_df["close"] = pd.to_numeric(data_df["close"], errors="coerce")
        data_df["preclose"] = pd.to_numeric(data_df["preclose"], errors="coerce")
        data_df["volume"] = pd.to_numeric(data_df["volume"], errors="coerce")
        data_df["amount"] = pd.to_numeric(data_df["amount"], errors="coerce")
        # data_df['adjustflag'] =
        data_df["turn"] = pd.to_numeric(data_df["turn"], errors="coerce")
        data_df["tradestatus"] = pd.to_numeric(data_df["tradestatus"], errors="coerce").astype(bool)
        data_df["pctChg"] = pd.to_numeric(data_df["pctChg"], errors="coerce")
        data_df["peTTM"] = pd.to_numeric(data_df["peTTM"], errors="coerce")
        data_df["psTTM"] = pd.to_numeric(data_df["psTTM"], errors="coerce")
        data_df["pcfNcfTTM"] = pd.to_numeric(data_df["pcfNcfTTM"], errors="coerce")
        data_df["pbMRQ"] = pd.to_numeric(data_df["pbMRQ"], errors="coerce")
        data_df["isST"] = pd.to_numeric(data_df["isST"], errors="coerce").astype(bool)

        if frequency == "d" and adjustflag == "3":
            data_df.to_sql(BS_Daily.__tablename__, engine, if_exists="append", index=False)
        elif frequency == "d" and adjustflag == "1":
            data_df.to_sql(BS_Daily_hfq.__tablename__, engine, if_exists="append", index=False)

    except Exception as e:  # traceback.format_exc(1)
        codes = data_df["code"].unique()
        _logger.error("K线数据保存出错/出错代码：{}；异常信息：{}".format(codes.tolist(), repr(e)))


def _load_weekly_to_DB(data_df: pd.DataFrame, frequency, adjustflag):
    """
    加载周线数据(后复权)到数据库
    """

    if data_df.empty:
        return

    try:

        data_df["date"] = pd.to_datetime(data_df["date"])
        # data_df['code'] =
        data_df["open"] = pd.to_numeric(data_df["open"], errors="coerce")
        data_df["high"] = pd.to_numeric(data_df["high"], errors="coerce")
        data_df["low"] = pd.to_numeric(data_df["low"], errors="coerce")
        data_df["close"] = pd.to_numeric(data_df["close"], errors="coerce")
        data_df["volume"] = pd.to_numeric(data_df["volume"], errors="coerce")
        data_df["amount"] = pd.to_numeric(data_df["amount"], errors="coerce")
        # data_df['adjustflag'] =
        data_df["turn"] = pd.to_numeric(data_df["turn"], errors="coerce")
        data_df["pctChg"] = pd.to_numeric(data_df["pctChg"], errors="coerce")

        if frequency == "w" and adjustflag == "1":
            data_df.to_sql(BS_Weekly_hfq.__tablename__, engine, if_exists="append", index=False)

    except Exception as e:  # traceback.format_exc(1)
        codes = data_df["code"].unique()
        _logger.error("周线后复权数据保存出错/出错代码：{}；异常信息：{}".format(codes.tolist(), repr(e)))


def _load_min_to_DB(data_df: pd.DataFrame, frequency, adjustflag):
    """
    docstring
    """

    if data_df.empty:
        return

    try:
        data_df["date"] = pd.to_datetime(data_df["date"], format="%Y-%m-%d")
        data_df["time"] = pd.to_datetime(data_df["time"], format="%Y%m%d%H%M%S%f")
        # data_df['code'] =
        data_df["open"] = pd.to_numeric(data_df["open"], errors="coerce")
        data_df["high"] = pd.to_numeric(data_df["high"], errors="coerce")
        data_df["low"] = pd.to_numeric(data_df["low"], errors="coerce")
        data_df["close"] = pd.to_numeric(data_df["close"], errors="coerce")
        data_df["volume"] = pd.to_numeric(data_df["volume"], errors="coerce")
        data_df["amount"] = pd.to_numeric(data_df["amount"], errors="coerce")
        # content['adjustflag'] =

        if frequency == "60" and adjustflag == "1":
            data_df.to_sql(BS_m60_hfq.__tablename__, engine, if_exists="append", index=False)
        elif frequency == "30" and adjustflag == "1":
            data_df.to_sql(BS_m30_hfq.__tablename__, engine, if_exists="append", index=False)

    except Exception as e:  # traceback.format_exc(1)
        codes = data_df["code"].unique()
        _logger.error("{}-{}分钟数据保存出错/出错代码：{}；异常信息：{}".format(frequency, adjustflag, codes.tolist(), repr(e)))


_load_to_DB = {"d": _load_daily_to_DB, "w": _load_weekly_to_DB, "60": _load_min_to_DB, "30": _load_min_to_DB}
