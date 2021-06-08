import calendar
import decimal
from datetime import datetime


def get_decimal_from_str(str):
    """
    字符串转Decimal
    """
    r = 0 if str == "" else decimal.Decimal(str)
    return r


def get_int_from_str(str):
    """
    字符串转int
    """
    r = 0 if str == "" else int(str)
    return r


def get_float_from_str(str):
    """
    字符串转float
    """
    r = 0 if str == "" else float(str)
    return r


def convert_to_date(date: str, format: str):
    """
    把字符串转化成日期，如果date为空，则返回空
    """
    result = None

    if date:
        result = datetime.strptime(date, format).date()

    return result


def convert_to_bscode(ts_code):
    """
    ts_code 转换成 bs_code
    """
    b = ts_code.split(".")
    bs_code = "{}.{}".format(b[1].lower(), b[0])
    return bs_code


def convert_to_tscode(bs_code: str):
    """
    bs_code 转换成 ts_code

    bs_code:sh.601398
    ts_code:600230.SH
    """
    b = bs_code.split(".")
    bs_code = "{}.{}".format(b[1], b[0].upper())
    return bs_code


def get_data_part(x: datetime, p):
    """
    获取时间成分[Y,M,W,WD,Q]
    """
    if p == "Y":
        return x.year
    elif p == "M":
        return x.month
    elif p == "W":
        return x.strftime("%W")
    elif p == "WD":
        return x.weekday()
    elif p == "Q":
        r= (x.month-1)//3 + 1
        return r

        # if x.month <= 3:
        #     return 1
        # elif 3 < x.month <= 6:
        #     return 2
        # elif 6 < x.month <= 9:
        #     return 3
        # else:
        #     return 4


def get_q_last_day(year: int, q: int):
    """获取指定年份指定季度的最后日期

    Args:
        year ([int]): 指定年份
        q ([int]): 指定季度

    Returns:
        [int]: 指定年份季度的最后一天
    """
    if q == 1:
        days = calendar.monthrange(year, 3)[1]
        t = datetime(year, 3, days).date()
        return t
    elif q == 2:
        days = calendar.monthrange(year, 6)[1]
        t = datetime(year, 6, days).date()
        return t
    elif q == 3:
        days = calendar.monthrange(year, 9)[1]
        t = datetime(year, 9, days).date()
        return t
    else:
        days = calendar.monthrange(year, 12)[1]
        t = datetime(year, 12, days).date()
        return t
