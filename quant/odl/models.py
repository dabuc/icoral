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
)

from quant.util.database import Base
from datetime import datetime


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


class BS_Profit_Data(Base):
    """
    季频盈利能力
    """

    __tablename__ = "odl_bs_profit_data"
    id = Column("id", BigInteger, primary_key=True)
    code = Column("code", String(10))  # 证券代码
    pubDate = Column("pubDate", String(10))  # 公司发布财报的日期
    statDate = Column("statDate", String(10))  # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    roeAvg = Column("roeAvg", String(23))  # 净资产收益率(平均)(%)
    npMargin = Column("npMargin", String(23))  # 销售净利率(%)
    gpMargin = Column("gpMargin", String(23))  # 销售毛利率(%)
    netProfit = Column("netProfit", String(23))  # 净利润(元)
    epsTTM = Column("epsTTM", String(23))  # 每股收益
    MBRevenue = Column("MBRevenue", String(23))  # 主营营业收入(元)
    totalShare = Column("totalShare", String(23))  # 总股本
    liqaShare = Column("liqaShare", String(23))  # 流通股本


class BS_Operation_Data(Base):
    """
    季频营运能力
    """

    __tablename__ = "odl_bs_operation_data"
    id = Column("id", BigInteger, primary_key=True)
    # 证券代码
    code = Column("code", String(10))
    # 公司发布财报的日期
    pubDate = Column("pubDate", String(10))
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", String(10))
    # 应收账款周转率(次)——营业收入/[(期初应收票据及应收账款净额+期末应收票据及应收账款净额)/2]
    NRTurnRatio = Column("NRTurnRatio", String(23))
    # 应收账款周转天数(天)——季报天数/应收账款周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    NRTurnDays = Column("NRTurnDays", String(23))
    # 存货周转率(次)——营业成本/[(期初存货净额+期末存货净额)/2]
    INVTurnRatio = Column("INVTurnRatio", String(23))
    # 存货周转天数(天)——季报天数/存货周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    INVTurnDays = Column("INVTurnDays", String(23))
    # 流动资产周转率(次)——营业总收入/[(期初流动资产+期末流动资产)/2]
    CATurnRatio = Column("CATurnRatio", String(23))
    # 总资产周转率——营业总收入/[(期初资产总额+期末资产总额)/2]
    AssetTurnRatio = Column("AssetTurnRatio", String(23))


class BS_Growth_Data(Base):
    """
    季频成长能力
    """

    __tablename__ = "odl_bs_growth_data"
    id = Column("id", BigInteger, primary_key=True)
    # 证券代码
    code = Column("code", String(10))
    # 公司发布财报的日期
    pubDate = Column("pubDate", String(10))
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", String(10))
    # 净资产同比增长率	(本期净资产-上年同期净资产)/上年同期净资产的绝对值*100%
    YOYEquity = Column("YOYEquity", String(23))
    # 总资产同比增长率	(本期总资产-上年同期总资产)/上年同期总资产的绝对值*100%
    YOYAsset = Column("YOYAsset", String(23))
    # 净利润同比增长率	(本期净利润-上年同期净利润)/上年同期净利润的绝对值*100%
    YOYNI = Column("YOYNI", String(23))
    # 基本每股收益同比增长率	(本期基本每股收益-上年同期基本每股收益)/上年同期基本每股收益的绝对值*100%
    YOYEPSBasic = Column("YOYEPSBasic", String(23))
    # 归属母公司股东净利润同比增长率	(本期归属母公司股东净利润-上年同期归属母公司股东净利润)/上年同期归属母公司股东净利润的绝对值*100%
    YOYPNI = Column("YOYPNI", String(23))


class BS_Balance_Data(Base):
    """
    季频偿债能力
    """

    __tablename__ = "odl_bs_balance_data"
    id = Column("id", BigInteger, primary_key=True)
    # 证券代码
    code = Column("code", String(10))
    # 公司发布财报的日期
    pubDate = Column("pubDate", String(10))
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", String(10))
    # 流动比率	流动资产/流动负债
    currentRatio = Column("currentRatio", String(23))
    # 速动比率	(流动资产-存货净额)/流动负债
    quickRatio = Column("quickRatio", String(23))
    # 现金比率	(货币资金+交易性金融资产)/流动负债
    cashRatio = Column("cashRatio", String(23))
    # 总负债同比增长率	(本期总负债-上年同期总负债)/上年同期中负债的绝对值*100%
    YOYLiability = Column("YOYLiability", String(23))
    # 资产负债率	负债总额/资产总额
    liabilityToAsset = Column("liabilityToAsset", String(23))
    # 权益乘数	资产总额/股东权益总额=1/(1-资产负债率)
    assetToEquity = Column("assetToEquity", String(23))


class BS_Cash_Flow_Data(Base):
    """
    季频现金流量
    """

    __tablename__ = "odl_bs_cash_flow_data"
    id = Column("id", BigInteger, primary_key=True)
    # 证券代码
    code = Column("code", String(10))
    # 公司发布财报的日期
    pubDate = Column("pubDate", String(10))
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", String(10))
    # 流动资产除以总资产
    CAToAsset = Column("CAToAsset", String(23))
    # 非流动资产除以总资产
    NCAToAsset = Column("NCAToAsset", String(23))
    # 有形资产除以总资产
    tangibleAssetToAsset = Column("tangibleAssetToAsset", String(23))
    # 已获利息倍数	息税前利润/利息费用
    ebitToInterest = Column("ebitToInterest", String(23))
    # 经营活动产生的现金流量净额除以营业收入
    CFOToOR = Column("CFOToOR", String(23))
    # 经营性现金净流量除以净利润
    CFOToNP = Column("CFOToNP", String(23))
    # 经营性现金净流量除以营业总收入
    CFOToGr = Column("CFOToGr", String(23))


class BS_Dupont_Data(Base):
    """
    季频杜邦指数
    """

    __tablename__ = "odl_bs_dupont_data"
    id = Column("id", BigInteger, primary_key=True)
    # 证券代码
    code = Column("code", String(10))
    # 公司发布财报的日期
    pubDate = Column("pubDate", String(10))
    # 财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30
    statDate = Column("statDate", String(10))
    # 净资产收益率	归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
    dupontROE = Column("dupontROE", String(23))
    # 权益乘数，反映企业财务杠杆效应强弱和财务风险	平均总资产/平均归属于母公司的股东权益
    dupontAssetStoEquity = Column("dupontAssetStoEquity", String(23))
    # 总资产周转率，反映企业资产管理效率的指标	营业总收入/[(期初资产总额+期末资产总额)/2]
    dupontAssetTurn = Column("dupontAssetTurn", String(23))
    # 归属母公司股东的净利润/净利润，反映母公司控股子公司百分比。如果企业追加投资，扩大持股比例，则本指标会增加。
    dupontPnitoni = Column("dupontPnitoni", String(23))
    # 净利润/营业总收入，反映企业销售获利率
    dupontNitogr = Column("dupontNitogr", String(23))
    # 净利润/利润总额，反映企业税负水平，该比值高则税负较低。净利润/利润总额=1-所得税/利润总额
    dupontTaxBurden = Column("dupontTaxBurden", String(23))
    # 利润总额/息税前利润，反映企业利息负担，该比值高则税负较低。利润总额/息税前利润=1-利息费用/息税前利润
    dupontIntburden = Column("dupontIntburden", String(23))
    # 息税前利润/营业总收入，反映企业经营利润率，是企业经营获得的可供全体投资人（股东和债权人）分配的盈利占企业全部营收收入的百分比
    dupontEbittogr = Column("dupontEbittogr", String(23))


class BS_Performance_Express_Report(Base):
    """
    季频公司业绩快报
    """

    __tablename__ = "odl_bs_performance_express_report"
    id = Column("id", BigInteger, primary_key=True)
    # 证券代码
    code = Column("code", String(10))
    # 业绩快报披露日
    performanceExpPubDate = Column("performanceExpPubDate", String(10))
    # 业绩快报统计日期
    performanceExpStatDate = Column("performanceExpStatDate", String(10))
    # 业绩快报披露日(最新)
    performanceExpUpdateDate = Column("performanceExpUpdateDate", String(10))
    # 业绩快报总资产
    performanceExpressTotalAsset = Column("performanceExpressTotalAsset", String(23))
    # 业绩快报净资产
    performanceExpressNetAsset = Column("performanceExpressNetAsset", String(23))
    # 业绩每股收益增长率
    performanceExpressEPSChgPct = Column("performanceExpressEPSChgPct", String(23))
    # 业绩快报净资产收益率ROE-加权
    performanceExpressROEWa = Column("performanceExpressROEWa", String(23))
    # 业绩快报每股收益EPS-摊薄
    performanceExpressEPSDiluted = Column("performanceExpressEPSDiluted", String(23))
    # 业绩快报营业总收入同比
    performanceExpressGRYOY = Column("performanceExpressGRYOY", String(23))
    # 业绩快报营业利润同比
    performanceExpressOPYOY = Column("performanceExpressOPYOY", String(23))


class BS_forecast_report(Base):
    """
    季频业绩预告
    """

    __tablename__ = "odl_bs_forecast_report"
    id = Column("id", BigInteger, primary_key=True)
    # 证券代码
    code = Column("code", String(10))
    # 业绩预告发布日期
    profitForcastExpPubDate = Column("profitForcastExpPubDate", String(10))
    # 业绩预告统计日期
    profitForcastExpStatDate = Column("profitForcastExpStatDate", String(10))
    # 业绩预告类型
    profitForcastType = Column("profitForcastType", String(10))
    # 业绩预告摘要
    profitForcastAbstract = Column("profitForcastAbstract", String(250))
    # 预告归属于母公司的净利润增长上限(%)
    profitForcastChgPctUp = Column("profitForcastChgPctUp", String(23))
    # 预告归属于母公司的净利润增长下限(%)
    profitForcastChgPctDwn = Column("profitForcastChgPctDwn", String(23))
