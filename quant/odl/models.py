# -*- coding: utf-8 -*-
"""baostock 数据模型"""
from sqlalchemy import (
    UniqueConstraint,
    Column,
    Integer,
    BigInteger,
    Numeric,
    String,
    Enum,
    Float,
    Boolean,
    Date,
    DateTime,
    JSON,
    Text,
    func,
)
from quant.util.database import Base
from datetime import date, datetime
from quant.util.database import session_scope
from quant.util import logger
from quant.util.helper import is_dev_env
from sqlalchemy.ext.declarative import declared_attr

_logger = logger.Logger(__name__).get_log()


class Task_Details(Base):
    """任务执行细节表"""

    __tablename__ = "odl_task_details"
    id = Column(Integer, primary_key=True)
    task = Column(Integer, nullable=False)  # 任务ID
    code = Column(String(20), nullable=False)  # 证券代码
    content = Column(JSON)  # 任务内容
    finished = Column(Boolean, default=False, nullable=False)  # 是否完成
    remark = Column(String(50))  # 备注信息
    create_on = Column(DateTime, default=datetime.now())

    @staticmethod
    def del_with_task(task):
        """
        按任务ID过滤，删除历史任务列表
        """
        with session_scope() as sm:
            query = sm.query(Task_Details).filter(Task_Details.task == task)
            query.delete()
            sm.commit()
            _logger.info("任务：{}-历史任务已删除".format(task))


class BS_Trade_Dates(Base):
    """
    交易日期
    """

    __tablename__ = "odl_bs_trade_dates"
    calendar_date = Column("calendar_date", Date, primary_key=True)  # 日期
    year = Column("year", Integer, nullable=False)  # 年
    month = Column("month", Integer, nullable=False)  # 月
    week = Column("week", String(2), nullable=False)  # 周
    weekday = Column("weekday", Integer, nullable=False)  # 星期几
    quarter = Column("quarter", Integer, nullable=False)  # 季度
    is_trading_day = Column("is_trading_day", Boolean)  # 是否交易日(0:非交易日;1:交易日)

    @staticmethod
    def get_lastest_trade_date():
        """
        获取最新交易日期
        """
        with session_scope() as sm:
            query = sm.query(func.max(BS_Trade_Dates.calendar_date)).filter(BS_Trade_Dates.is_trading_day == True)
            t = query.scalar()
            return t


class BS_Stock_Basic(Base):
    """
    BS-证券基本资料
    """

    __tablename__ = "odl_bs_stock_basic"
    code = Column(String(10), primary_key=True)  # 证券代码
    code_name = Column(String(100))  # 证券名称
    ipoDate = Column(Date)  # 上市日期
    outDate = Column(Date)  # 退市日期
    type = Column(Enum("1", "2", "3"))  # 证券类型，其中1：股票，2：指数,3：其它
    status = Column(Boolean)  # 上市状态，其中1：上市，0：退市
    ts_code = Column(String(10))  # ts_证券代码
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def get_stock_codes(include_index: bool = False):
        """获取所有上市股票代码列表；测试环境只获取前10个

        Args:
            include_index (bool, optional): 是否包含指数.默认不包含

        Returns:
            [List]: 股票代码列表
        """
        with session_scope() as sm:
            query = sm.query(BS_Stock_Basic.code).filter(BS_Stock_Basic.status == 1)

            if not include_index:
                query = query.filter(BS_Stock_Basic.type == 1)

            if is_dev_env():
                codes = query.limit(10)
            else:
                codes = query.all()

            result = [(x.code) for x in codes]

            return result

    @staticmethod
    def get_ipo_date(code: str):
        """
        获取股票的上市日期
        """
        with session_scope() as sm:
            query = sm.query(BS_Stock_Basic.ipoDate).filter(BS_Stock_Basic.code == code)
            r = query.scalar()
            return r


class BS_Profit_Data(Base):
    """
    季频盈利能力
    """

    __tablename__ = "odl_bs_profit_data"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 统计年份
    year = Column("year", Integer, nullable=False)
    # 统计季度
    quarter = Column("quarter", Integer, nullable=False)
    # 公司发布财报的日期
    pubDate = Column("pubDate", Date, nullable=False)
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", Date, nullable=False)
    # 净资产收益率(平均)(%)
    roeAvg = Column("roeAvg", Numeric(15, 6))
    # 销售净利率(%)
    npMargin = Column("npMargin", Numeric(15, 6))
    # 销售毛利率(%)
    gpMargin = Column("gpMargin", Numeric(15, 6))
    # 净利润(元)
    netProfit = Column("netProfit", Numeric(23, 6))
    # 每股收益
    epsTTM = Column("epsTTM", Numeric(15, 6))
    # 主营营业收入(元)
    MBRevenue = Column("MBRevenue", Numeric(23, 6))
    # 总股本
    totalShare = Column("totalShare", Numeric(23, 2))
    # 流通股本
    liqaShare = Column("liqaShare", Numeric(23, 2))

    __table_args__ = (UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),)


class BS_Operation_Data(Base):
    """
    季频营运能力
    """

    __tablename__ = "odl_bs_operation_data"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 统计年份
    year = Column("year", Integer, nullable=False)
    # 统计季度
    quarter = Column("quarter", Integer, nullable=False)
    # 公司发布财报的日期
    pubDate = Column("pubDate", Date, nullable=False)
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", Date, nullable=False)
    # 应收账款周转率(次)——营业收入/[(期初应收票据及应收账款净额+期末应收票据及应收账款净额)/2]
    NRTurnRatio = Column("NRTurnRatio", Numeric(15, 6))
    # 应收账款周转天数(天)——季报天数/应收账款周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    NRTurnDays = Column("NRTurnDays", Numeric(15, 6))
    # 存货周转率(次)——营业成本/[(期初存货净额+期末存货净额)/2]
    INVTurnRatio = Column("INVTurnRatio", Numeric(15, 6))
    # 存货周转天数(天)——季报天数/存货周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    INVTurnDays = Column("INVTurnDays", Numeric(15, 6))
    # 流动资产周转率(次)——营业总收入/[(期初流动资产+期末流动资产)/2]
    CATurnRatio = Column("CATurnRatio", Numeric(15, 6))
    # 总资产周转率——营业总收入/[(期初资产总额+期末资产总额)/2]
    AssetTurnRatio = Column("AssetTurnRatio", Numeric(15, 6))
    __table_args__ = (UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),)


class BS_Growth_Data(Base):
    """
    季频成长能力
    """

    __tablename__ = "odl_bs_growth_data"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 统计年份
    year = Column("year", Integer, nullable=False)
    # 统计季度
    quarter = Column("quarter", Integer, nullable=False)
    # 公司发布财报的日期
    pubDate = Column("pubDate", Date, nullable=False)
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", Date, nullable=False)
    # 净资产同比增长率	(本期净资产-上年同期净资产)/上年同期净资产的绝对值*100%
    YOYEquity = Column("YOYEquity", Numeric(15, 6))
    # 总资产同比增长率	(本期总资产-上年同期总资产)/上年同期总资产的绝对值*100%
    YOYAsset = Column("YOYAsset", Numeric(15, 6))
    # 净利润同比增长率	(本期净利润-上年同期净利润)/上年同期净利润的绝对值*100%
    YOYNI = Column("YOYNI", Numeric(15, 6))
    # 基本每股收益同比增长率	(本期基本每股收益-上年同期基本每股收益)/上年同期基本每股收益的绝对值*100%
    YOYEPSBasic = Column("YOYEPSBasic", Numeric(15, 6))
    # 归属母公司股东净利润同比增长率	(本期归属母公司股东净利润-上年同期归属母公司股东净利润)/上年同期归属母公司股东净利润的绝对值*100%
    YOYPNI = Column("YOYPNI", Numeric(15, 6))
    __table_args__ = (UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),)


class BS_Balance_Data(Base):
    """
    季频偿债能力
    """

    __tablename__ = "odl_bs_balance_data"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 统计年份
    year = Column("year", Integer, nullable=False)
    # 统计季度
    quarter = Column("quarter", Integer, nullable=False)
    # 公司发布财报的日期
    pubDate = Column("pubDate", Date, nullable=False)
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", Date, nullable=False)
    # 流动比率	流动资产/流动负债
    currentRatio = Column("currentRatio", Numeric(15, 6))
    # 速动比率	(流动资产-存货净额)/流动负债
    quickRatio = Column("quickRatio", Numeric(15, 6))
    # 现金比率	(货币资金+交易性金融资产)/流动负债
    cashRatio = Column("cashRatio", Numeric(15, 6))
    # 总负债同比增长率	(本期总负债-上年同期总负债)/上年同期中负债的绝对值*100%
    YOYLiability = Column("YOYLiability", Numeric(15, 6))
    # 资产负债率	负债总额/资产总额
    liabilityToAsset = Column("liabilityToAsset", Numeric(15, 6))
    # 权益乘数	资产总额/股东权益总额=1/(1-资产负债率)
    assetToEquity = Column("assetToEquity", Numeric(15, 6))
    __table_args__ = (UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),)


class BS_Cash_Flow_Data(Base):
    """
    季频现金流量
    """

    __tablename__ = "odl_bs_cash_flow_data"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 统计年份
    year = Column("year", Integer, nullable=False)
    # 统计季度
    quarter = Column("quarter", Integer, nullable=False)
    # 公司发布财报的日期
    pubDate = Column("pubDate", Date, nullable=False)
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", Date, nullable=False)
    # 流动资产除以总资产
    CAToAsset = Column("CAToAsset", Numeric(15, 6))
    # 非流动资产除以总资产
    NCAToAsset = Column("NCAToAsset", Numeric(15, 6))
    # 有形资产除以总资产
    tangibleAssetToAsset = Column("tangibleAssetToAsset", Numeric(15, 6))
    # 已获利息倍数	息税前利润/利息费用
    ebitToInterest = Column("ebitToInterest", Numeric(15, 6))
    # 经营活动产生的现金流量净额除以营业收入
    CFOToOR = Column("CFOToOR", Numeric(15, 6))
    # 经营性现金净流量除以净利润
    CFOToNP = Column("CFOToNP", Numeric(15, 6))
    # 经营性现金净流量除以营业总收入
    CFOToGr = Column("CFOToGr", Numeric(15, 6))
    __table_args__ = (UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),)


class BS_Dupont_Data(Base):
    """
    季频杜邦指数
    """

    __tablename__ = "odl_bs_dupont_data"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 统计年份
    year = Column("year", Integer, nullable=False)
    # 统计季度
    quarter = Column("quarter", Integer, nullable=False)
    # 公司发布财报的日期
    pubDate = Column("pubDate", Date, nullable=False)
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", Date, nullable=False)
    # 净资产收益率	归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
    dupontROE = Column("dupontROE", Numeric(15, 6))
    # 权益乘数，反映企业财务杠杆效应强弱和财务风险	平均总资产/平均归属于母公司的股东权益
    dupontAssetStoEquity = Column("dupontAssetStoEquity", Numeric(15, 6))
    # 总资产周转率，反映企业资产管理效率的指标	营业总收入/[(期初资产总额+期末资产总额)/2]
    dupontAssetTurn = Column("dupontAssetTurn", Numeric(15, 6))
    # 归属母公司股东的净利润/净利润，反映母公司控股子公司百分比。如果企业追加投资，扩大持股比例，则本指标会增加。
    dupontPnitoni = Column("dupontPnitoni", Numeric(15, 6))
    # 净利润/营业总收入，反映企业销售获利率
    dupontNitogr = Column("dupontNitogr", Numeric(15, 6))
    # 净利润/利润总额，反映企业税负水平，该比值高则税负较低。净利润/利润总额=1-所得税/利润总额
    dupontTaxBurden = Column("dupontTaxBurden", Numeric(15, 6))
    # 利润总额/息税前利润，反映企业利息负担，该比值高则税负较低。利润总额/息税前利润=1-利息费用/息税前利润
    dupontIntburden = Column("dupontIntburden", Numeric(15, 6))
    # 息税前利润/营业总收入，反映企业经营利润率，是企业经营获得的可供全体投资人（股东和债权人）分配的盈利占企业全部营收收入的百分比
    dupontEbittogr = Column("dupontEbittogr", Numeric(15, 6))
    __table_args__ = (UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),)


class BS_Performance_Express_Report(Base):
    """
    季频公司业绩快报
    """

    __tablename__ = "odl_bs_performance_express_report"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 业绩快报披露日
    performanceExpPubDate = Column("performanceExpPubDate", Date, nullable=False)
    # 业绩快报统计日期
    performanceExpStatDate = Column("performanceExpStatDate", Date, nullable=False)
    # 业绩快报披露日(最新)
    performanceExpUpdateDate = Column("performanceExpUpdateDate", Date, nullable=False)
    # 业绩快报总资产
    performanceExpressTotalAsset = Column("performanceExpressTotalAsset", Numeric(23, 6))
    # 业绩快报净资产
    performanceExpressNetAsset = Column("performanceExpressNetAsset", Numeric(23, 6))
    # 业绩每股收益增长率
    performanceExpressEPSChgPct = Column("performanceExpressEPSChgPct", Numeric(15, 6))
    # 业绩快报净资产收益率ROE-加权
    performanceExpressROEWa = Column("performanceExpressROEWa", Numeric(15, 6))
    # 业绩快报每股收益EPS-摊薄
    performanceExpressEPSDiluted = Column("performanceExpressEPSDiluted", Numeric(15, 6))
    # 业绩快报营业总收入同比
    performanceExpressGRYOY = Column("performanceExpressGRYOY", Numeric(15, 6))
    # 业绩快报营业利润同比
    performanceExpressOPYOY = Column("performanceExpressOPYOY", Numeric(15, 6))


class BS_forecast_report(Base):
    """
    季频业绩预告
    """

    __tablename__ = "odl_bs_forecast_report"
    id = Column("id", Integer, primary_key=True)
    # 证券代码
    code = Column("code", String(10), nullable=False)
    # 业绩预告发布日期
    profitForcastExpPubDate = Column("profitForcastExpPubDate", Date, nullable=False)
    # 业绩预告统计日期
    profitForcastExpStatDate = Column("profitForcastExpStatDate", Date, nullable=False)
    # 业绩预告类型
    profitForcastType = Column("profitForcastType", String(10))
    # 业绩预告摘要
    profitForcastAbstract = Column("profitForcastAbstract", Text)
    # 预告归属于母公司的净利润增长上限(%)
    profitForcastChgPctUp = Column("profitForcastChgPctUp", Numeric(15, 6))
    # 预告归属于母公司的净利润增长下限(%)
    profitForcastChgPctDwn = Column("profitForcastChgPctDwn", Numeric(15, 6))


class BS_Daily_Base:
    """
    BS日线历史行情数据基类
    """

    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date, nullable=False)  # 交易所行情日期
    code = Column("code", String(10), nullable=False)  # BS证券代码 格式：sh.600000。sh：上海，sz：深圳
    open = Column("open", Numeric(18, 4), nullable=False)  # 今开盘价格 精度：小数点后4位；单位：人民币元
    high = Column("high", Numeric(18, 4), nullable=False)  # 最高价 精度：小数点后4位；单位：人民币元
    low = Column("low", Numeric(18, 4), nullable=False)  # 最低价 精度：小数点后4位；单位：人民币元
    close = Column("close", Numeric(18, 4), nullable=False)  # 今收盘价 精度：小数点后4位；单位：人民币元
    preclose = Column("preclose", Numeric(18, 4))  # 昨日收盘价 精度：小数点后4位；单位：人民币元
    volume = Column("volume", BigInteger)  # 成交数量 单位：股
    amount = Column("amount", Numeric(23, 4))  # 成交金额	精度：小数点后4位；单位：人民币元
    adjustflag = Column("adjustflag", Enum("1", "2", "3"))  # 复权状态(1：后复权， 2：前复权，3：不复权）
    turn = Column("turn", Numeric(18, 6))  # 换手率 精度：小数点后6位；单位：%
    tradestatus = Column("tradestatus", Boolean)  # 交易状态	1：正常交易 0：停牌
    pctChg = Column("pctChg", Numeric(18, 6))  # 涨跌幅（百分比）	精度：小数点后6位
    peTTM = Column("peTTM", Numeric(18, 6))  # 滚动市盈率	精度：小数点后6位
    psTTM = Column("psTTM", Numeric(18, 6))  # 滚动市销率	精度：小数点后6位
    pcfNcfTTM = Column("pcfNcfTTM", Numeric(18, 6))  # 滚动市现率	精度：小数点后6位
    pbMRQ = Column("pbMRQ", Numeric(18, 6))  # 市净率	精度：小数点后6位
    isST = Column("isST", Boolean)  # 是否ST	1是，0否

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint("code", "date", name=f"UDX_CODE_DATE_{cls.__tablename__.upper()}"),)


class BS_Daily(BS_Daily_Base, Base):
    """
    日线历史行情数据
    """

    __tablename__ = "odl_bs_daily"


# ------后复权------------
class BS_Daily_hfq(BS_Daily_Base, Base):
    """
    后复权-日线历史行情数据
    """

    __tablename__ = "odl_bs_daily_hfq"


class BS_Weekly_Base:
    """
    周线历史行情数据
    """

    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date, nullable=False)  # 交易所行情日期
    code = Column("code", String(10), nullable=False)  # BS证券代码 格式：sh.600000。sh：上海，sz：深圳
    open = Column("open", Numeric(18, 4), nullable=False)  # 今开盘价格 精度：小数点后4位；单位：人民币元
    high = Column("high", Numeric(18, 4), nullable=False)  # 最高价 精度：小数点后4位；单位：人民币元
    low = Column("low", Numeric(18, 4), nullable=False)  # 最低价 精度：小数点后4位；单位：人民币元
    close = Column("close", Numeric(18, 4), nullable=False)  # 今收盘价 精度：小数点后4位；单位：人民币元
    volume = Column("volume", BigInteger)  # 成交数量 单位：股
    amount = Column("amount", Numeric(23, 4))  # 成交金额	精度：小数点后4位；单位：人民币元
    adjustflag = Column("adjustflag", Enum("1", "2", "3"))  # 复权状态(1：后复权， 2：前复权，3：不复权）
    turn = Column("turn", Numeric(18, 6))  # 换手率 精度：小数点后6位；单位：%
    pctChg = Column("pctChg", Numeric(18, 6))  # 涨跌幅（百分比）	精度：小数点后6位

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint("code", "date", name=f"UDX_CODE_DATE_{cls.__tablename__.upper()}"),)


class BS_Weekly_hfq(BS_Weekly_Base, Base):
    """
    后复权-周线历史行情数据
    """

    __tablename__ = "odl_bs_weekly_hfq"


class BS_min_Base:
    """
    BS分钟线历史行情数据基类
    """

    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date, nullable=False)  # 交易所行情日期,格式：YYYY-MM-DD
    time = Column("time", DateTime, nullable=False)  # 交易所行情时间,格式：YYYYMMDDHHMMSSsss
    code = Column("code", String(10), nullable=False)  # BS证券代码 格式：sh.600000。sh：上海，sz：深圳
    open = Column("open", Numeric(18, 4), nullable=False)  # 今开盘价格 精度：小数点后4位；单位：人民币元
    high = Column("high", Numeric(18, 4), nullable=False)  # 最高价 精度：小数点后4位；单位：人民币元
    low = Column("low", Numeric(18, 4), nullable=False)  # 最低价 精度：小数点后4位；单位：人民币元
    close = Column("close", Numeric(18, 4), nullable=False)  # 今收盘价 精度：小数点后4位；单位：人民币元
    volume = Column("volume", BigInteger)  # 成交数量 单位：股
    amount = Column("amount", Numeric(23, 4))  # 成交金额	精度：小数点后4位；单位：人民币元
    adjustflag = Column("adjustflag", Enum("1", "2", "3"))  # 复权状态(1：后复权， 2：前复权，3：不复权）

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint("code", "time", name=f"UDX_CODE_TIME_{cls.__tablename__.upper()}"),)


class BS_m60_hfq(BS_min_Base, Base):
    """
    后复权-60分钟线
    """

    __tablename__ = "odl_bs_m60_hfq"


class BS_m30_hfq(BS_min_Base, Base):
    """
    后复权-60分钟线
    """

    __tablename__ = "odl_bs_m30_hfq"


# ------------------------------------------


class Ft_plate_list(Base):
    """板块列表"""

    __tablename__ = "odl_ft_plate_list"
    code = Column("code", String(10), primary_key=True)  # 板块代码
    plate_name = Column("plate_name", String(25), nullable=False)  # 	板块名字
    plate_id = Column("plate_id", String(10), nullable=False)  # 	板块 ID
    market = Column("market", String(4), nullable=False)  # 市场标识。注意：这里不区分沪和深


class Ft_stock_basicinfo(Base):
    """
    docstring
    """

    __tablename__ = "odl_ft_stock_basicinfo"

    code = Column("code", String(20), primary_key=True)  # str	股票代码
    name = Column("name", String(200))  # str	股票名称
    lot_size = Column("lot_size", Integer)  # int	每手股数，期权表示每份合约股数（指数期权无该字段），期货表示合约乘数
    market = Column(Enum("NONE", "HK", "US", "SH", "SZ", "SG", "JP"))
    stock_type = Column("stock_type", String(10))  # SecurityType	股票类型
    stock_child_type = Column("stock_child_type", String(10))  # WrtType	窝轮子类型
    stock_owner = Column("stock_owner", String(10))  # str	窝轮所属正股的代码，或期权标的股的代码
    option_type = Column("option_type", String(10))  # OptionType	期权类型
    strike_time = Column("strike_time", DateTime)  # str	期权行权日（港股和 A 股市场默认是北京时间，美股市场默认是美东时间）
    strike_price = Column("strike_price", Numeric(23, 6))  # float	期权行权价
    suspension = Column("suspension", Boolean)  # bool	期权是否停牌（True：停牌，False：未停牌）
    listing_date = Column("listing_date", Date)  # str	上市时间
    stock_id = Column("stock_id", BigInteger)  # int	股票 ID
    delisting = Column("delisting", Boolean)  # bool	是否退市
    index_option_type = Column("index_option_type", String(10))  # str	指数期权类型
    main_contract = Column("main_contract", Boolean)  # bool	是否主连合约
    last_trade_time = Column("last_trade_time", DateTime)  # str	最后交易时间，主连，当月，下月等期货没有该字段


class Ft_plate_stock(Base):
    """
    富途板块内股票列表
    """

    __tablename__ = "odl_ft_plate_stock"
    plate_code = Column("plate_code", String(10), primary_key=True)
    code = Column("code", String(15), primary_key=True)  # 股票代码
    lot_size = Column("lot_size", Integer)  # 每手股数，期货表示合约乘数
    stock_name = Column("stock_name", String(200))  # 股票名称
    stock_type = Column("stock_type", String(10))  # 股票类型
    list_time = Column("list_time", Date)  # 上市日期 上市时间（港股和 A 股市场默认是北京时间，美股市场默认是美东时间）
    stock_id = Column("stock_id", BigInteger)  # 股票 ID
    main_contract = Column("main_contract", Boolean)  # 是否主连合约（期货特有字段）
    last_trade_time = Column("last_trade_time", String(30))  # 最后交易时间（期货特有字段，主连，当月，下月等期货没有该字段）
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Ft_History_Kline_Base:
    """
    历史 K 线
    """

    ktype = Column("ktype", Enum("K_DAY", "K_WEEK", "K_MON", "K_60M", "K_30M"), primary_key=True)  # KLType	K 线类型
    code = Column("code", String(15), primary_key=True)  # str	股票代码
    time_key = Column("time_key", DateTime, primary_key=True)  # str	K 线时间（港股和 A 股市场默认是北京时间，美股市场默认是美东时间）
    open = Column("open", Numeric(18, 4))  # float	开盘价
    close = Column("close", Numeric(18, 4))  # float	收盘价
    high = Column("high", Numeric(18, 4))  # float	最高价
    low = Column("low", Numeric(18, 4))  # float	最低价
    pe_ratio = Column("pe_ratio", Numeric(18, 6))  # float	市盈率（该字段为比例字段，默认不展示 %）
    turnover_rate = Column("turnover_rate", Numeric(18, 6))  # float	换手率
    volume = Column("volume", BigInteger)  # int	成交量
    turnover = Column("turnover", Numeric(23, 4))  # float	成交额
    change_rate = Column("change_rate", Numeric(18, 6))  # float	涨跌幅
    last_close = Column("last_close", Numeric(18, 4))  # float	昨收价
    autype = Column("autype", Enum("NONE", "QFQ", "HFQ"), nullable=False)  # K 线复权类型


class Ft_history_kline(Ft_History_Kline_Base, Base):
    """
    不复权-历史K线数据
    """

    __tablename__ = "odl_ft_history_kline"


class Ft_history_kline_hfq(Ft_History_Kline_Base, Base):
    """
    后复权-历史K线数据
    """

    __tablename__ = "odl_ft_history_kline_hfq"
