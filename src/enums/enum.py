from enum import Enum
import logging


class LogLevelEnum(Enum):
    """
    ログレベルEnum
    """
    DEBUG = {
        "code": "debug",
        "value": logging.DEBUG,
    }
    INFO = {
        "code": "info",
        "value": logging.INFO,
    }
    WARNING = {
        "code": "warn",
        "value": logging.WARNING,
    }
    ERROR = {
        "code": "error",
        "value": logging.ERROR,
    }

    def getLogLevelEnumByCode(code):
        """
        ログレベルのコード値に該当するEnum値を返却

        Args:
            code (str): ログレベルのコード値

        Returns:
            LogLevelEnum: ログレベルのコード値に該当するEnum値を返却 | 該当無し時は「DEBUG」を返却
        """
        for line in LogLevelEnum:
            if line.value["code"] == code:
                return line
        return LogLevelEnum.DEBUG


class LogModeEnum(Enum):
    """
    ログ出力モードのEnumクラス
    """
    # コンソール出力
    STDOUT = {
        "code": "0",
        "logger": "root",
    }
    # コンソール ＋ ファイル出力
    STDOUT_FILE = {
        "code": "1",
        "logger": "addfile",
    }

    def getLogModeEnumByCode(code):
        """
        ログ出力モードに該当するEnum値を返却する

        Args:
            code (str): ログ出力モードのコード値

        Returns:
            LogModeEnum: ログ出力モードのコード値に該当するEnum値を返却 | 該当無し時は「STDOUT」を返却
        """
        for line in LogModeEnum:
            if line.value["code"] == code:
                return line
        return LogModeEnum.STDOUT


class OpenModeEnum(Enum):
    """
    ファイルのオープンモードに関するEnumクラス
    """
    READ = "r"
    WRITE = "w"
    APPEND = "a"
    EXCLUSIVE = "x"


class AdditionalOptionEnum(Enum):
    """
    実行追加オプション
    """
    TRUNCATE = "truncate"
    RECREATE = "recreate"

    def getAdditionalOptionEnumByValue(value):
        for line in AdditionalOptionEnum:
            if line.value == value:
                return line
        return None


class EncodeEnum(Enum):
    """
    文字コードに関するEnumクラス
    """
    UTF8 = {
        "code": "utf8",
        "value": "utf_8",
    }
    UTF8BOM = {
        "code": "utf8bom",
        "value": "utf_8_sig",
    }
    SJIS = {
        "code": "sjis",
        "value": "shift_jis",
    }
    CP932 = {
        "code": "cp932",
        "value": "cp932",
    }

    def getEndoceEnumByCode(code: str):
        """
        文字コードに該当するEnum値を返却する

        Args:
            code (str): 文字コード値

        Returns:
            EncodeEnum: 文字コード値に該当するEnum値を返却 | 該当無し時は「UTF8」を返却
        """
        for line in EncodeEnum:
            if line.value["code"] == code:
                return line
        return EncodeEnum.UTF8


class LineTerminatorEnum(Enum):
    """
    改行コードに関するEnumクラス
    """
    LF = "\n"
    CRLF = "\r\n"
