from futu import *

from quant.odl.models import Ft_history_kline
from quant.util.database import engine


def load_to_db(ktype, autype, data: pd.DataFrame):
    data["ktype"] = ktype
    data["autype"] = autype
    data["time_key"] = pd.to_datetime(data["time_key"])  # str	K 线时间（港股和 A 股市场默认是北京时间，美股市场默认是美东时间）

    data["open"] = pd.to_numeric(data["open"], errors="coerce")  # float	开盘价
    data["close"] = pd.to_numeric(data["close"], errors="coerce")  # float	收盘价
    data["high"] = pd.to_numeric(data["high"], errors="coerce")  # float	最高价
    data["low"] = pd.to_numeric(data["low"], errors="coerce")  # float	最低价
    data["pe_ratio"] = pd.to_numeric(data["pe_ratio"], errors="coerce")  # float	市盈率（该字段为比例字段，默认不展示 %）
    data["turnover_rate"] = pd.to_numeric(data["turnover_rate"], errors="coerce")  # float	换手率
    data["volume"] = pd.to_numeric(data["volume"], errors="coerce")  # int	成交量
    data["turnover"] = pd.to_numeric(data["turnover"], errors="coerce")  # float	成交额

    data["change_rate"] = pd.to_numeric(data["change_rate"], errors="coerce")  # float	涨跌幅
    data["last_close"] = pd.to_numeric(data["last_close"], errors="coerce")  # float	昨收价

    data.to_sql(
        Ft_history_kline.__tablename__,
        engine,
        if_exists="append",
        index=False,
    )



def query_history_kline(ktype, code, start_date, end_date, max_count, autype):
    quote_ctx = OpenQuoteContext(host="127.0.0.1", port=11111)
    ret, data, page_req_key = quote_ctx.request_history_kline(
        code, start=start_date, end=end_date, ktype=ktype, autype=autype, max_count=max_count
    )  # 每页5个，请求第一页
    if ret == RET_OK:
        load_to_db(ktype, autype, data)

    else:
        print("error:", data)
    while page_req_key != None:  # 请求后面的所有结果
        print("*************************************")
        ret, data, page_req_key = quote_ctx.request_history_kline(
            code,
            start=start_date,
            end=end_date,
            ktype=ktype,
            autype=autype,
            max_count=max_count,
            page_req_key=page_req_key,
        )  # 请求翻页后的数据
        if ret == RET_OK:
            load_to_db(ktype, autype, data)
        else:
            print("error:", data)
    print("All pages are finished!")
    quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽



# if __name__ == "__main__":
#     ktype = KLType.K_DAY
#     code = "HK.01810"
#     start_date = "2011-06-16"
#     end_date = "2021-06-16"
#     max_count = 100
#     autype = AuType.NONE

#     query_history_kline(ktype,code,start_date,end_date,max_count,autype)  # 结束后记得关闭当条连接，防止连接条数用尽
