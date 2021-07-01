# -*- coding: utf-8 -*-
"""每周的涨跌统计"""
import pandas as pd
from sqlalchemy.sql.expression import column
from quant.odl.models import BS_Daily, BS_Trade_Dates
from quant.util.database import engine as qt_engine
from sqlalchemy import select
from dateutil.parser import parse

pd.set_option("display.unicode.ambiguous_as_wide", True)
pd.set_option("display.unicode.east_asian_width", True)


def __calc_up(values: pd.Series):

    total = values.count()

    up = values[values > 0].count()

    return round(up / total, 4) * 100


def __calc_down(values: pd.Series):

    total = values.count()

    down = values[values < 0].count()

    return round(down / total, 4) * 100


def statistics(code="sh.000001",start:str='2005-01-01'):
    """
    统计
    """

    start_date = parse(start)

    s1 = (
        select(BS_Daily.date, BS_Daily.code, BS_Daily.open, BS_Daily.close, BS_Daily.preclose, BS_Daily.pctChg)
        .where(BS_Daily.code == code,BS_Daily.date >= start_date)
        .order_by(BS_Daily.date)
    )
    df1 = pd.read_sql(s1, qt_engine)

    s2 = select(BS_Trade_Dates.calendar_date, BS_Trade_Dates.weekday)
    df2 = pd.read_sql(s2, qt_engine)

    df3 = df1.merge(df2, "left", left_on="date", right_on="calendar_date")

    df3["cur_day_pctChg"] = (df3["close"] - df3["open"]) / df3["open"]

    # df3["UD"] = 0

    # condition1 = df3["pctChg"] > 0
    # df3.loc[condition1, "UD"] = 1

    t1 = (
        df3.groupby("weekday")["pctChg"]
        .agg([__calc_up, __calc_down])
        .rename(columns={"__calc_up": "上涨概率", "__calc_down": "下跌概率"})
        .reset_index()
    )
    print(t1)

    t2 = (
        df3.groupby("weekday")["cur_day_pctChg"]
        .agg([__calc_up, __calc_down])
        .rename(columns={"__calc_up": "当日上涨概率", "__calc_down": "当日下跌概率"})
        .reset_index()
    )
    print(t2)


if __name__ == "__main__":
    pass
