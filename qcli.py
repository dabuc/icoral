import click
from quant.odl import models as odl_model
from quant.util.database import engine
from quant.odl.baostock import stock_basic


@click.group()
def cli():
    """操作数据层"""
    pass


@cli.command()
def create_dw():
    """创建数据仓库"""
    click.confirm("正在创建数据库，是否继续？", abort=True)

    odl_model.Base.metadata.create_all(engine)

    click.echo("数据层数据表创建完成")


@cli.command()
def query_basic_info():
    """更新BS基本资料:证券代码，交易日期"""
    click.confirm("正在更新基本资料，是否继续？", abort=True)
    from quant.odl import models
    from quant.odl.baostock.trade_dates import get_trade_dates

    models.BS_Stock_Basic.clear_table()
    click.echo("BS_Stock_Basic已经清空")
    stock_basic.get_stock_basic()
    click.echo("证券基本资料完成")

    get_trade_dates()
    click.echo("交易日期更新完成")


@cli.command()
def query_profit_data():
    """更新季频盈利能力"""
    click.confirm("正在更新季频盈利能力，是否继续？", abort=True)
    from quant.odl.baostock.profit_data import get_profit_data

    get_profit_data()
    click.echo("季频盈利能力更新完成")


@cli.command()
def query_operation_data():
    """更新季频营运能力"""
    click.confirm("正在更新季频营运能力，是否继续？", abort=True)
    from quant.odl.baostock.operation_data import get_operation_data

    get_operation_data()
    click.echo("季频营运能力更新完成")


@cli.command()
def query_growth_data():
    """季频成长能力"""
    click.confirm("正在更新季频成长能力，是否继续？", abort=True)
    from quant.odl.baostock.growth_data import get_growth_data

    get_growth_data()
    click.echo("季频成长能力更新完成")


@cli.command()
def query_balance_data():
    """季频偿债能力"""
    click.confirm("正在更新季频偿债能力，是否继续？", abort=True)
    from quant.odl.baostock.balance_data import get_balance_data

    get_balance_data()
    click.echo("季频偿债能力更新完成")


@cli.command()
def query_cash_flow_data():
    """季频现金流量"""
    click.confirm("正在更新季频现金流量，是否继续？", abort=True)
    from quant.odl.baostock.cash_flow_data import get_cash_flow_data

    get_cash_flow_data()
    click.echo("季频现金流量更新完成")


@cli.command()
def query_dupont_data():
    """季频杜邦指数"""
    click.confirm("正在更新季频杜邦指数，是否继续？", abort=True)
    from quant.odl.baostock.dupont_data import get_dupont_data

    get_dupont_data()
    click.echo("季频杜邦指数更新完成")


@cli.command()
def query_performance_express_report():
    """季频业绩快报"""
    click.confirm("正在更新季频业绩快报，是否继续？", abort=True)
    from quant.odl.baostock.performance_express_report import get_performance_express_report

    get_performance_express_report()
    click.echo("季频业绩快报更新完成")


@cli.command()
def query_forecast_report():
    """季频业绩预告"""
    click.confirm("正在更新季频业绩预告，是否继续？", abort=True)
    from quant.odl.baostock.forecast_report import get_forecast_report

    get_forecast_report()
    click.echo("季频业绩预告更新完成")


@cli.command()
@click.option(
    "--f",
    type=click.Choice(["d", "w", "60", "30"]),
    default="d",
    help="默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟",
)
@click.option("--a", type=click.Choice(["1", "2", "3"]), default="3", help="复权类型，默认不复权：3；1：后复权；2：前复权")
def query_history_k_data(f, a):
    """获取历史A股K线数据"""
    click.confirm("正在更新历史A股K线数据({}-{})，是否继续？".format(f, a), abort=True)
    from quant.odl.baostock.history_k_data import get_history_k_data

    get_history_k_data(f, a)
    click.echo("历史A股K线数据更新完成")


@cli.command()
def ft_get_plate_list():
    """
    获取板块列表
    """
    click.confirm("正在更新（富途）板块列表，是否继续？", abort=True)
    from quant.odl.futu.plate_list import query_plate_list
    query_plate_list()
    click.echo("（富途）板块列表更新完成")

@cli.command()
def ft_get_plate_stock():
    """
    获取板块内股票列表
    """
    click.confirm("正在获取（富途）板块内股票列表，是否继续？", abort=True)
    from quant.odl.futu.plate_stock import query_plate_stock
    query_plate_stock()
    click.echo("获取（富途）板块内股票列表信息更新完成")

@cli.command()
def ft_get_stock_basicinfo():
    """
    获取静态数据
    """
    click.confirm("正在获取（富途）静态数据，是否继续？", abort=True)
    from quant.odl.futu.stock_basicinfo import query_stock_basicinfo
    query_stock_basicinfo()
    click.echo("（富途）静态数据更新完成")


@cli.command()
def daily_updating():
    """
    每日任务更新
    """
    click.confirm("批量更新，是否继续？", abort=True)
    from quant.odl import models
    from quant.odl.baostock.trade_dates import get_trade_dates

    models.BS_Stock_Basic.clear_table()
    stock_basic.get_stock_basic()
    click.echo("证券基本资料更新完成")
    get_trade_dates()
    click.echo("交易日期更新完成")

    from quant.odl.baostock.history_k_data import get_history_k_data
    from quant.util.helper import is_tc_env

    get_history_k_data('d', '1')
    click.echo("后复权-日K线数据更新完成")
    get_history_k_data('d', '3')
    click.echo("不复权-日K线数据更新完成")
    get_history_k_data('w', '1')
    click.echo("后复权-周K线数据更新完成")
    if not is_tc_env():
        get_history_k_data('30', '1')
        click.echo("后复权-30m-K线数据更新完成")
        get_history_k_data('60', '1')
        click.echo("后复权-60m-K线数据更新完成")

    click.echo("全部更新完成")



if __name__ == "__main__":
    cli()
    #query_history_k_data(['--f','60','--a','1'])
    #daily_updating()
