#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time:   2023/12/8 20:58
# File:   __init__.py.py
# Author: He Ma
# Email:  1692303843@qq.com


from .tool import *
from .constants import *
from .tool_draw import *
from .tool_class import *

# 全局参数
_ = logger

# os.chdir(manager_config.work_dir)

# 日志管理器
logger_config.setting('console', verbose=1)

# 变量跟踪管理器
tracker = VariableTracker()

# 公用变量
plt_global(font_path=manager_config.font_path)
