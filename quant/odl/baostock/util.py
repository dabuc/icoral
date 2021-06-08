from calendar import month
import concurrent.futures
import datetime
from quant.util.dataconvert import get_data_part
import time

import pandas as pd
from dateutil.relativedelta import relativedelta
from quant.odl.models import BS_Profit_Data, BS_Stock_Basic
from quant.util import logger
from quant.util.database import engine
from sqlalchemy import func, select
from tqdm import tqdm

import baostock as bs

_logger = logger.Logger(__name__).get_log()


def __get_finance_params(table_model):
    """
    获取财务相关参数
    --季频盈利能力：BS_Profit_Data
    --季频营运能力：BS_Operation_Data
    --季频成长能力：BS_Growth_Data
    --季频偿债能力：BS_Balance_Data
    --季频现金流量：BS_Cash_Flow_Data
    --季频杜邦指数：BS_Dupont_Data
    """
    s1 = select(BS_Stock_Basic.code, BS_Stock_Basic.ipoDate, BS_Stock_Basic.outDate).where(
        BS_Stock_Basic.type == "1", BS_Stock_Basic.status == "1"
    )
    df1 = pd.read_sql(s1, engine)

    s2 = select(table_model.code, func.max(table_model.statDate).label("max_statDate")).group_by(table_model.code)
    df2 = pd.read_sql(s2, engine)
    df3 = df1.merge(df2, "left", on="code")

    # 新股
    condition1 = df3["max_statDate"].isnull()
    df3.loc[condition1, "start_date"] = df3.loc[condition1, "ipoDate"] - datetime.timedelta(days=365 * 2)
    code1 = df3[condition1]
    code1 = code1[["code", "start_date"]]

    # 已经更新过财报的股票
    # 计算下个财报发布日期（简单计算）
    df3["next_pubDate"] = df3["max_statDate"] + datetime.timedelta(days=30 * 4)
    df3["next_pubDate"] = pd.to_datetime(df3["next_pubDate"], format="%Y-%m-%d")
    condition2 = df3["next_pubDate"] < datetime.datetime.now()
    df3.loc[condition2, "start_date"] = df3.loc[condition2, "max_statDate"] + datetime.timedelta(days=20)
    code2 = df3[condition2]
    code2 = code2[["code", "start_date"]]
    t = pd.concat([code1, code2])
    result = t.to_dict(orient="records")
    return result


def __get_year_q_list(start_date, end_date):
    """
    获取指定时间范围内的年份季度列表
    """
    start_year_q = get_data_part(start_date, "Q")
    end_date_q = get_data_part(end_date, "Q")
    tmp = []
    for item in range(start_date.year, end_date.year + 1):
        if item == start_date.year:
            for q in range(start_year_q, 5):
                t = {"year": item, "Q": q}
                tmp.append(t)
        elif item == end_date.year:
            for q in range(1, end_date_q):
                t = {"year": item, "Q": q}
                tmp.append(t)
        else:
            for q in range(1, 5):
                t = {"year": item, "Q": q}
                tmp.append(t)
    return tmp


def crawl_finance_data(bs_query_func, load_data_func, table_model):
    """爬取季频财务数据"""

    tasks = __get_finance_params(table_model)
    codes_num = len(tasks)
    data_df = pd.DataFrame()
    with tqdm(total=codes_num) as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for task in tasks:
                code = task["code"]
                start_date = task["start_date"]
                end_date = datetime.datetime.now().date()
                year_q_list = __get_year_q_list(start_date, end_date)
                
                for item in year_q_list:
                    year = item["year"]
                    quarter = item["Q"]

                    max_try = 8  # 失败重连的最大次数
                    for i in range(max_try):
                        param = {"code": code, "year": year, "quarter": quarter}
                        rs = bs_query_func(**param)
                        if rs.error_code == "0":
                            tmp = rs.get_data()
                            tmp["quarter"] = quarter
                            tmp["year"] = year
                            data_df = data_df.append(tmp)
                            break
                        elif i < (max_try - 1):
                            time.sleep(2)
                            continue
                        else:
                            _logger.error("respond error_code:" + rs.error_code)
                            _logger.error("respond  error_msg:" + rs.error_msg)
                            _logger.error("{}:{}-{}下载失败".format(code, year, quarter))
                
                pbar.update(1)
                if len(data_df) > 100:
                    tmp = data_df
                    executor.submit(load_data_func, data_df, param)
                    data_df = pd.DataFrame()

            load_data_func(data_df, param)

                    
    _logger.info("数据全部下载完成")


def crawl_query_history_k_data_plus(
    code, fields, start_date="2015-01-01", end_date=datetime.datetime.now().date(), frequency="d", adjustflag="3"
) -> pd.DataFrame:
    """根据查询条件查询指定K线数据，如果查询错误，重复查询8次

    Args:
        code (str): 证券代码
        fields (str): 查询字段
        start_date (str, optional): 开始时间. Defaults to "2015-01-01".
        end_date ([type], optional): 结束时间. Defaults to datetime.datetime.now().date().
        frequency (str, optional): 数据类型，默认为d.
        adjustflag (str, optional): 复权类型，默认不复权：3；1：后复权；2：前复权。

    Returns:
        [pd.DataFrame]: [查询结果集]
    """
    max_try = 8  # 失败重连的最大次数
    for i in range(max_try):
        k_rs = bs.query_history_k_data_plus(
            code, fields, start_date=start_date, end_date=end_date, frequency=frequency, adjustflag=adjustflag
        )
        if k_rs.error_code == "0":
            data_df = k_rs.get_data()
            return data_df
        elif i < (max_try - 1):
            time.sleep(2)
            continue
        else:
            _logger.error("获取历史A股K线数据失败/query_history_k_data_plus respond error_code:" + k_rs.error_code)
            _logger.error("获取历史A股K线数据失败/query_history_k_data_plus respond  error_msg:" + k_rs.error_msg)
