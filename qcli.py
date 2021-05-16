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
    """更新证券基本资料
    """    
    click.confirm("正在更新证券基本资料，是否继续？", abort=True)
    from quant.odl import models
    models.BS_Stock_Basic.clear_table()
    click.echo("BS_Stock_Basic已经清空")
    stock_basic.get_stock_basic()
    click.echo("更新证券基本资料完成")



if __name__ == "__main__":
    cli()