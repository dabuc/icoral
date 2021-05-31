from quant.odl.models import BS_Trade_Dates
import baostock as bs
import pandas as pd
from quant.util.database import engine, session_scope
from quant.util.dataconvert import get_data_part, get_int_from_str
from sqlalchemy import func
import datetime


def get_start_date():
    """
    获取开始时间
    """
    with session_scope() as sm:
        t = sm.query(func.max(BS_Trade_Dates.calendar_date)).scalar()

        if t:
            return t + datetime.timedelta(days=1)
        else:
            return datetime.datetime.strptime("1990-01-01","%Y-%m-%d").date()


def get_trade_dates():
    """
    获取交易日期
    """

    start_time = get_start_date()
    if start_time > datetime.datetime.now().date():
        return

    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print("login respond error_code:" + lg.error_code)
    print("login respond  error_msg:" + lg.error_msg)

    #### 获取交易日信息 ####
    rs = bs.query_trade_dates(start_date=start_time.strftime("%Y-%m-%d"))
    print("query_trade_dates respond error_code:" + rs.error_code)
    print("query_trade_dates respond  error_msg:" + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == "0") & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    result["calendar_date"] = pd.to_datetime(result.calendar_date, format="%Y-%m-%d")
    result["year"] = result["calendar_date"].apply(get_data_part, p="Y")
    result["month"] = result["calendar_date"].apply(get_data_part, p="M")
    result["week"] = result["calendar_date"].apply(get_data_part, p="W")
    result["weekday"] = result["calendar_date"].apply(get_data_part, p="WD")
    result["quarter"] = result["calendar_date"].apply(get_data_part, p="Q")
    pd.DatetimeIndex
    result["is_trading_day"] = [None if x == "" else bool(get_int_from_str(x)) for x in result["is_trading_day"]]

    # 输出结果集
    result.to_sql(BS_Trade_Dates.__tablename__, engine, if_exists="append", index=False)

    #### 登出系统 ####
    bs.logout()


if __name__ == "__main__":
    get_trade_dates()
