# -*- coding: utf-8 -*-
"""辅助函数"""

from quant.settings import QtConfig, DevelopmentConfig


def is_dev_env():
    if isinstance(QtConfig, DevelopmentConfig):
        return True
    else:
        return False
