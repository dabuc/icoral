# -*- coding: utf-8 -*-
"""板块列表"""
from quant.odl.models import Ft_plate_list, Ft_plate_stock
from quant.util import logger as qt_logger
from quant.util.database import engine
from tqdm import tqdm

from futu import *

_logger = qt_logger.Logger(__name__).get_log()


def query_plate_stock(plate_code_list: list):

    Ft_plate_stock.clear_table()

    quote_ctx = OpenQuoteContext(host="127.0.0.1", port=11111)

    try:
        with tqdm(total=len(plate_code_list)) as pbar:
            max_try = 8  # 失败重连的最大次数
            for plate_code in plate_code_list:
                for i in range(max_try):

                    start = time.time()
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
                        df.to_csv("aa.csv")
                        df.to_sql(
                            Ft_plate_stock.__tablename__,
                            engine,
                            if_exists="append",
                            index=False,
                        )

                        end = time.time()
                        jg = 3 - (end - start)
                        if jg > 0:
                            time.sleep(jg)
                        
                        pbar.update(1)
                        break
                    elif i < (max_try - 1):
                        time.sleep(3)
                        continue
                    else:
                        _logger.error("获取板块内股票列表失败/get_plate_stock respond {}_error:{}".format(plate_code, data))

    except:
        raise
    finally:
        quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽


def query_plate_stock_A():
    """
    查询A股各个板块的成分股
    """
    plate_list = Ft_plate_list.get_hs_plate_list()  # 获取沪深板块列表

    plate_list.append('SH.3000000') #上海主板
    plate_list.append('SZ.3000001') #深证主板
    plate_list.append('SZ.3000004') #创业板（深）
    plate_list.append('SH.BK0992') #科创板
    plate_list.append('SH.BK0600') #热度榜（沪深）
    plate_list.append('SH.BK0921') #已上市新股-A 股

    plate_set = set(plate_list)
    
    query_plate_stock(plate_set)
