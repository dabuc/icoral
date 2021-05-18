import concurrent.futures
import time
import copy
import baostock as bs
from quant.util import logger


_logger = logger.Logger(__name__).get_log()


def crawl_data(
    bs_query_func,
    load_data_func,
    bs_query_params_func,
    load_data_func_params: dict = None,
):
    """爬取数据"""

    # ### 登陆系统 ####
    lg = bs.login()  # noqa

    query_params = bs_query_params_func()
    data_df = pd.DataFrame()

    for query_param in query_params:

        max_try = 8  # 失败重连的最大次数
        for i in range(max_try):
            rs = bs_query_func(**query_param)
            if rs.error_code == "0":
                while (rs.error_code == "0") & rs.next():
                    # 获取一条记录，将记录合并在一起
                    data_df.append(rs.get_data())

                if load_data_func_params:
                    params = copy.deepcopy(load_data_func_params)
                else:
                    params = {}
                params["result"] = result
                #params["code"] = query_param['code']
                

                break
            elif i < (max_try - 1):
                time.sleep(2)
                continue
            else:
                _logger.error("respond error_code:" + rs.error_code)
                _logger.error("respond  error_msg:" + rs.error_msg)

    # ### 登出系统 ####
    bs.logout()
