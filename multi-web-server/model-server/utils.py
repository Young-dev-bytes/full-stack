import os
import sys
import datetime
import logging
import requests
import logging.handlers

from constants import LOGDIR


# global variables
handler = None

def build_logger(logger_name, logger_filename):
    # 使用 global handler 声明 handler 为全局变量
    global handler
    # 创建一个日志格式器 formatter，指定日志消息的格式和时间格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set the format of root handlers
    # 如果根日志记录器没有处理程序（handlers），则使用 logging.basicConfig 设置基本的日志配置，日志级别为 INFO
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO)

    # 将先前创建的格式器 formatter 设置为根日志记录器的第一个处理程序的格式。
    logging.getLogger().handlers[0].setFormatter(formatter)

    # Redirect stdout and stderr to loggers
    # 创建一个名为 stdout 的日志记录器，并将其日志级别设置为 INFO。
    stdout_logger = logging.getLogger("stdout")
    stdout_logger.setLevel(logging.INFO)
    # 创建一个 StreamToLogger 对象 sl，将标准输出（stdout）重定向到 stdout_logger
    sl_info = StreamToLogger(stdout_logger, logging.INFO)
    # Ensure we are only redirecting standard output, not standard error
    # 将 sys.stdout 重定向到 sl，这样所有写入标准输出的内容都会被记录到 stdout_logger
    sys.stdout = sl_info


    stderr_logger = logging.getLogger("stderr")
    stderr_logger.setLevel(logging.ERROR)
    sl_error = StreamToLogger(stderr_logger, logging.ERROR)
    # Ensure we are only redirecting standard error, not standard output
    sys.stderr = sl_error


    # Get logger
    # 获取一个名为 logger_name 的日志记录器，并将其日志级别设置为 INFO
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Add a file handler for all loggers
    # 如果 handler 为 None，执行以下步骤：
    # 创建日志目录 LOGDIR，如果不存在则创建。
    # 生成日志文件路径 filename。
    # 创建一个 TimedRotatingFileHandler，该处理程序会根据时间旋转日志文件（每天一个新文件），并设置其格式为之前定义的 formatter。
    # 遍历所有日志记录器，将 handler 添加到每一个日志记录器中
    if handler is None:
        os.makedirs(LOGDIR, exist_ok=True)
        filename = os.path.join(LOGDIR, logger_filename)
        handler = logging.handlers.TimedRotatingFileHandler(
            filename, when='D', utc=True)
        handler.setFormatter(formatter)

        for name, item in logging.root.manager.loggerDict.items():
            if isinstance(item, logging.Logger):
                item.addHandler(handler)
    return logger


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    # 定义 StreamToLogger 类，该类模拟文件流对象，将写入的数据重定向到日志记录器。
    # 在初始化方法中，存储标准输出 sys.stdout，设置日志记录器 logger 和日志级别 log_level，并初始化一个缓冲区 linebuf
    def __init__(self, logger, log_level):
        self.terminal = sys.stdout
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    # 定义 __getattr__ 方法，将属性访问委托给 self.terminal（标准输出）。
    # 定义 write 方法，将写入的数据缓冲并重定向到日志记录器：
    # 将缓冲区 linebuf 和写入的数据 buf 合并。
    # 清空 linebuf。
    # 遍历合并后的数据，将每一行数据写入日志记录器。
    # 如果行末是换行符，则将其记录到日志中，否则将其添加到缓冲区 linebuf。
    def __getattr__(self, attr):
        return getattr(self.terminal, attr)

    def write(self, buf):
        temp_linebuf = self.linebuf + buf
        self.linebuf = ''
        for line in temp_linebuf.splitlines(True):
            # From the io.TextIOWrapper docs:
            #   On output, if newline is None, any '\n' characters written
            #   are translated to the system default line separator.
            # By default sys.stdout.write() expects '\n' newlines and then
            # translates them so this is still cross platform.
            if line[-1] == '\n':
                self.logger.log(self.log_level, line.rstrip())
            else:
                self.linebuf += line

    # 定义 flush 方法，将缓冲区中的数据写入日志记录器，并清空缓冲区 linebuf
    def flush(self):
        if self.linebuf != '':
            self.logger.log(self.log_level, self.linebuf.rstrip())
        self.linebuf = ''