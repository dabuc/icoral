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
def query_stock_basic():
    """更新证券基本资料"""
    click.confirm("正在更新证券基本资料，是否继续？", abort=True)
    from quant.odl import models

    models.BS_Stock_Basic.clear_table()
    click.echo("BS_Stock_Basic已经清空")
    stock_basic.get_stock_basic()
    click.echo("更新证券基本资料完成")


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

if __name__ == "__main__":
    cli()
