# -*- coding: utf-8 -*-
"""配置文件"""
import os
from dotenv import load_dotenv

load_dotenv()
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class BaseConfig:
    """
    基本配置类
    """

    IDB_DEBUG = "0"
    IS_TC_ENV = os.getenv("IS_TC_ENV", "0")
    TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN", "")
    LOG_PATH = os.getenv("LOG_PATH", base_dir + "/logs/quant.log")
    LOG_ERR_PATH= os.getenv("LOG_ERR_PATH", base_dir + "/logs/quant_err.log")
    BARK_HOST = os.getenv("BARK_HOST", "")
    BARK_KEY = os.getenv("BARK_KEY", "")


class DevelopmentConfig(BaseConfig):
    """
    开发配置类
    """

    IDB_DEBUG = "1"
    DB_QUANT = "{}_test".format(os.getenv("DB_SCHEMA"))
    DATABASE_URL = os.getenv("DATABASE_URL").format(DB_QUANT)


class ProductionConfig(BaseConfig):
    """
    生成环境正式配置类
    """
    
    DB_QUANT = os.getenv("DB_SCHEMA", "")
    DATABASE_URL = os.getenv("DATABASE_URL").format(DB_QUANT)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

config_name = os.getenv("QT_CONFIG", "development")
QtConfig = config[config_name]()


if __name__ == "__main__":
    pass
