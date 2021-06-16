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
                #data["stock_type"] = SecurityType.PLATE

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

