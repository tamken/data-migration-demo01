import logging
import logging.config
from datetime import datetime

from src.enums.enum import LogLevelEnum, LogModeEnum


class LogUtil:
    """
    ログ関連のユーティリティクラス
    """

    __instance = None

    @staticmethod
    def getInstance(
        log_level: LogLevelEnum,
        log_mode: LogModeEnum,
        log_dir,
        conf_path="config/logging.conf",
    ):
        """
        インスタンス取得

        Args:
            log_level (LogLevelEnum): ログレベル
            log_mode (LogModeEnum): ログ出力モード
            log_dir (str): ログ出力先ディレクトリパス
            conf_path (str): ログ関連の設定ファイルパス
                デフォルト: "config/logging.conf"

        Returns:
            obj : LogUtilインスタンス
        """
        if LogUtil.__instance is None:
            LogUtil(
                log_level=log_level,
                log_mode=log_mode,
                log_dir=log_dir,
                conf_path=conf_path,
            )
        return LogUtil.__instance

    def __init__(
        self,
        log_level: LogLevelEnum,
        log_mode: LogModeEnum,
        log_dir,
        conf_path,
    ):
        """
        コンストラクタ

        Args:
            self (obj):
            log_level (LogLevelEnum)
            log_mode (LogModeEnum)
            log_dir (str)
            conf_path (str):

        Raises:
            Exception: 想定外 - ≠シングルトン
        """
        # インスタンス生成済は想定外
        if LogUtil.__instance is not None:
            raise Exception("LogUtilインスタンス生成エラー（no singleton）")

        # コンソールハンドラ
        logging.config.fileConfig(conf_path)
        logger = logging.getLogger()

        # ファイルハンドラ
        if LogModeEnum.STDOUT_FILE == log_mode:
            fh = logging.FileHandler(
                log_dir + "{:%Y%m%d}.log".format(datetime.now())
            )
            formatter = logging.Formatter(
                "[%(asctime)s][%(levelname)s] "
                + "%(filename)s:%(lineno)s - %(message)s"
            )
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        # インスタンスセット
        LogUtil.__instance = logger
        LogUtil.__instance.setLevel(log_level.value["value"])
