import configparser
import logging
import os
import sys


PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")

class Base:
    """
    全てのモジュールの規定クラス
    """
    _PROJECT_ROOT = PROJECT_ROOT

    @property
    def logger(self):
        if getattr(self, "_logger", None) is None:
            self._logger = Logger.create_logger(__name__)
        return self._logger

    @property
    def config(self):
        if getattr(self, "_config", None) is None:
            self._config = Config.config
        return self._config         

class Logger:
    """
    loggerの設定を管理するクラス
    """
    
    _LEVEL_MAP = {
        "DEBUG": logging.debug,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    _FORMATTER = "%(asctime)s : %(levelname)s - %(filename)s - %(message)s"

    @classmethod
    def create_logger(cls, mod_name):
        logger = logging.getLogger(mod_name)
        level = Config.config["logging"]["level"].upper()
        logger.setLevel(cls._LEVEL_MAP[level])
        if Config.config["logging"]["file_log"].upper() == "TRUE":
            log_file_path = os.path.join(PROJECT_ROOT, Config.config["logging"]["file_name"])
            fh = logging.FileHandler(
                log_file_path, 
                encoding=Config.config["logging"]["file_encoding"],
            )
            fh_formatter = logging.Formatter(cls._FORMATTER)
            fh.setFormatter(fh_formatter)
            logger.addHandler(fh)
        if Config.config["logging"]["console_log"].upper == "TRUE":
            sh = logging.StreamHandler()
            sh_formatter = logging.Formatter(cls._FORMATTER)
            sh.setFormatter(sh_formatter)
            logger.addHandler(sh)
        return logger

class _Config:
    """
    configファイルの設定情報を保持するSingletoneクラス
    """
    def __init__(self):
        self.load_config()

    def load_config(self):
        config_path = os.path.join(PROJECT_ROOT, "config.ini")
        if not os.path.exists(config_path):
            raise
        self._config = configparser.ConfigParser()
        self._config.read(config_path)
    
    @property
    def config(self):
        return self._config

Config = _Config()






