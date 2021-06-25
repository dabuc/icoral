from quant.odl.models import Ft_plate_stock
from quant.util.database import engine

from futu import *


def query_plate_stock():
    """获取全部美股, 全部 A 股（沪深）,所有港股 的基本信息"""
    Ft_plate_stock.clear_table()

    quote_ctx = OpenQuoteContext(host="127.0.0.1", port=11111)
    plate_code_list = ["US.USAALL", "SH.3000005", "SH.3000002", "HK.BK1910"]  # 全部美股, 全部 A 股（沪深）,沪深指数,所有港股

    for plate_code in plate_code_list:
        ret, data = quote_ctx.get_plate_stock(plate_code)
        if ret == RET_OK:
            data["plate_code"] = plate_code
            data["updated_on"] = datetime.now()
            df = data[
                [
                    "plate_code",
                    "code",
                    "lot_size",
                    "stock_name",
                    "stock_type",
                    "list_time",
                    "stock_id",
                    "main_contract",
                    "last_trade_time",
                    "updated_on",
                ]
            ]
            df.to_sql(
                Ft_plate_stock.__tablename__,
                engine,
                if_exists="append",
                index=False,
            )
        else:
            print("error:", data)
    quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
