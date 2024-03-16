"""
闪电机器人-日志输出
"""
# 定义颜色代码常量
COLOR_ERROR = "\033[31m"
COLOR_WARNING = "\033[33m"
COLOR_INFO = "\033[94m"
COLOR_RESET = "\033[0m"

async def error(msg):
    if not isinstance(msg, str):
        raise ValueError("日志消息必须是字符串类型")
    print(f"{COLOR_ERROR}[错误-Error]{COLOR_RESET}", msg)

async def warning(msg):
    if not isinstance(msg, str):
        raise ValueError("日志消息必须是字符串类型")
    print(f"{COLOR_WARNING}[警告-Warning]{COLOR_RESET}", msg)

async def info(msg):
    if not isinstance(msg, str):
        raise ValueError("日志消息必须是字符串类型")
    print(f"{COLOR_INFO}[信息-Info]{COLOR_RESET}", msg)