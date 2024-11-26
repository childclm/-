from logging import Formatter, StreamHandler, INFO, Logger
'''
Formatter:日志格式化输出
StreamHandler:日志处理器（Handler），用于指定日志消息应该输出到哪里
INFO:代表日志级别之一  DEBUG（调试）INFO（信息）WARNING（警告）ERROR（错误）CRITICAL（严重错误）
Logger:Logger 对象是日志系统的核心组件，负责生成日志消息。
'''

LOG_FORMAT = F"%(asctime)s [%(name)s] %(levelname)s: %(message)s"


class LoggerManage:
    logger = {}

    @classmethod
    def get_logger(cls, name: str = 'default', log_level=None, log_format=LOG_FORMAT):
        key = (name, log_level)

        def get_logger():
            logger_format = Formatter(log_format)
            handler = StreamHandler()
            handler.setFormatter(logger_format)
            handler.setLevel(log_level or INFO)
            _logger = Logger(name)
            _logger.addHandler(handler)
            _logger.setLevel(log_level or INFO)
            cls.logger[key] = _logger
            return _logger
        # 根据name和log_level作为键， 如果存在则用之前的不用重新生成否则重新生成
        return cls.logger.get(key, None) or get_logger()


get_loger = LoggerManage.get_logger

if __name__ == '__main__':
    LoggerManage.get_logger(name='xxx')