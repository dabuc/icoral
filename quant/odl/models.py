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
)

from quant.util.database import Base
from datetime import datetime
from quant.util.database import session_scope
from quant.util import logger
from quant.util.helper import is_dev_env

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
    def get_stock_codes():
        """获取所有上市股票代码列表；测试环境只获取前10个

        Returns:
            [List]: 股票代码列表
        """
        with session_scope() as sm:
            query = sm.query(BS_Stock_Basic.code).filter(
                BS_Stock_Basic.type == 1, BS_Stock_Basic.status == 1
            )

            if is_dev_env():
                codes = query.limit(10)
            else:
                codes = query.all()

            result = [(x.code) for x in codes]

            return result


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

    __table_args__ = (
        UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),
    )


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
    __table_args__ = (
        UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),
    )


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
    __table_args__ = (
        UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),
    )


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
    __table_args__ = (
        UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),
    )


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
    __table_args__ = (
        UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),
    )


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
    __table_args__ = (
        UniqueConstraint("code", "year", "quarter", name="UDX_CODE_YEAR_QUARTER"),
    )


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
    performanceExpressTotalAsset = Column(
        "performanceExpressTotalAsset", Numeric(23, 6)
    )
    # 业绩快报净资产
    performanceExpressNetAsset = Column("performanceExpressNetAsset", Numeric(23, 6))
    # 业绩每股收益增长率
    performanceExpressEPSChgPct = Column("performanceExpressEPSChgPct", Numeric(15, 6))
    # 业绩快报净资产收益率ROE-加权
    performanceExpressROEWa = Column("performanceExpressROEWa", Numeric(15, 6))
    # 业绩快报每股收益EPS-摊薄
    performanceExpressEPSDiluted = Column(
        "performanceExpressEPSDiluted", Numeric(15, 6)
    )
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
