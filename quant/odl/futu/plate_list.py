# -*- coding: utf-8 -*-
"""板块列表"""
from quant.odl.models import Ft_plate_list
from quant.util import logger as qt_logger
from quant.util.database import engine

from futu import *

_logger = qt_logger.Logger(__name__).get_log()


def query_plate_list():
    """
    获取板块列表
    """

    Ft_plate_list.clear_table()

    quote_ctx = OpenQuoteContext(host="127.0.0.1", port=11111)

    market_list = [Market.HK, Market.SH]

    plate_list = ["INDUSTRY", "REGION", "CONCEPT"]  # 行业板块,地域板块,概念板块

    try:
        for m in market_list:
            for plate in plate_list:
                start = time.time()
                ret, data = quote_ctx.get_plate_list(m, plate)
                if ret == RET_OK:
                    # print(data)

                    data["market"] = m
                    data["plate_class"] = plate
                    data["updated_on"] = datetime.now()

                    data.to_sql(
                        Ft_plate_list.__tablename__,
                        engine,
                        if_exists="append",
                        index=False,
                    )
                else:
                    _logger.error("获取板块列表报错/error:{}".format(data))
                    # print("error:", data)

                end = time.time()
                jg = 3 - (end - start)
                if jg > 0:
                    time.sleep(jg)

    finally:
        quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
