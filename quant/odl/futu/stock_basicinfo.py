from quant.odl.models import Ft_stock_basicinfo
from quant.util.database import engine
from futu import *



def query_stock_basicinfo():
    """
    获取静态数据
    """
    quote_ctx = OpenQuoteContext(host="127.0.0.1", port=11111)

    market_list =[Market.HK,Market.US,Market.SH,Market.SZ]
    stock_type_list = [SecurityType.STOCK,SecurityType.IDX,SecurityType.PLATE,SecurityType.PLATESET]

    for market in market_list:
        for stock_type in stock_type_list:
            ret, data = quote_ctx.get_stock_basicinfo(market, stock_type)
            if ret == RET_OK:

                data["market"] = market
                data["strike_price"] = pd.to_numeric(data["strike_price"], errors="coerce")
                data["suspension"] = pd.to_numeric(data["suspension"], errors="coerce").astype(bool)
                data["delisting"] = pd.to_numeric(data["delisting"], errors="coerce").astype(bool)
                data["main_contract"] = pd.to_numeric(data["main_contract"], errors="coerce").astype(bool)

                data["strike_time"] = pd.to_datetime(data["strike_time"])
                data["listing_date"] = pd.to_datetime(data["listing_date"], format="%Y-%m-%d")  
                data["last_trade_time"] = pd.to_datetime(data["last_trade_time"])

                data.to_sql(
                    Ft_stock_basicinfo.__tablename__,
                    engine,
                    if_exists="append",
                    index=False,
                )
            else:
                print("error:", data)


    quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽



if __name__ == "__main__":
    query_stock_basicinfo()

