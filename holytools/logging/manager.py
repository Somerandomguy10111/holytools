import logging
from io import StringIO


class LoggerManager:
    @staticmethod
    def force_identification():
        logging.basicConfig(level=logging.DEBUG)
        root_logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        for handler in root_logger.handlers:
            handler.setFormatter(formatter)

    @staticmethod
    def logger_exists(name : str) -> bool:
        logger_names = [name for name in logging.root.manager.loggerDict]
        return name in logger_names

    @staticmethod
    def show_loggers():
        logger_names = [name for name in logging.root.manager.loggerDict]
        print("-> Currently running Loggers:")
        for name in logger_names:
            print(f"- {name}")
        return logger_names

    @staticmethod
    def redirect(logger : logging.Logger, new_stream : StringIO):
        for h in logger.handlers:
            logger.removeHandler(hdlr=h)
        handler = logging.StreamHandler(new_stream)
        logger.addHandler(handler)

