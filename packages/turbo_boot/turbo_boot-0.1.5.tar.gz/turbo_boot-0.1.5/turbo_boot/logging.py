from turbo_boot.singleton_meta import SingletonMeta
from turbo_boot.config_loader import ConfigLoader
import logging
from logging.handlers import RotatingFileHandler
from turbo_boot.logging_level import LoggingLevel
import sys
import os

class Logger(metaclass=SingletonMeta):
    def __init__(self, config_loader: ConfigLoader) -> None:
        self.__config_loader = config_loader
        self.__logger_name = (self.__config_loader.get_config("turbo-boot.logging.name") or "app")
        self.__logger = logging.getLogger(self.__logger_name)
        self.__setup_logging()
    
    def __setup_logging(self):
        self.__global_log_level = str(self.__config_loader.get_config("turbo-boot.logging.level") or "INFO")
        self.__global_log_format = (self.__config_loader.get_config("turbo-boot.logging.format") or '%(asctime)s | %(levelname)8s | %(lineno)d | %(message)s')
        self.__setup_console_handler()
        self.__setup_file_handler()
        
    def __setup_file_handler(self):
        if (self.__config_loader.get_config("turbo-boot.file-handler.enabled") or False):
            logger = self.__logger
            log_dir = (self.__config_loader.get_config("turbo-boot.file-handler.dir-name") or "./")
            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except:
                    log_dir = '/tmp' if sys.platform.startswith('linux') else '.'
            
            log_file_name = (self.__config_loader.get_config("turbo-boot.file-handler.file-name") or "app")
            log_file_path = os.path.join(log_dir, log_file_name) + '.log'
            
            log_file_max_bytes = (self.__config_loader.get_config("turbo-boot.file-handler.max-bytes") or 20000)
            log_file_backup_count = (self.__config_loader.get_config("turbo-boot.file-handler.backup-count") or 5)
            
            logger.file_handler = RotatingFileHandler(log_file_path, maxBytes=log_file_max_bytes, backupCount=log_file_backup_count)
            logger.file_handler.setLevel(LoggingLevel[str(self.__config_loader.get_config("turbo-boot.file-handler.level") or self.__global_log_level).upper()])
            logger.file_handler.setFormatter(logging.Formatter((self.__config_loader.get_config("turbo-boot.file-handler.format") or self.__global_log_format)))
            logger.addHandler(logger.file_handler)
    
    def __setup_console_handler(self):
        if (self.__config_loader.get_config("turbo-boot.console-handler.enabled") or True):
            logger = self.__logger
            logger.stdout_handler = logging.StreamHandler(sys.stdout)
            
            logger.stdout_handler.setLevel(LoggingLevel[str(self.__config_loader.get_config("turbo-boot.console-handler.level") or self.__global_log_level).upper()])
            logger.stdout_handler.setFormatter(logging.Formatter((self.__config_loader.get_config("turbo-boot.console-handler.format") or self.__global_log_format)))
            logger.addHandler(logger.stdout_handler)