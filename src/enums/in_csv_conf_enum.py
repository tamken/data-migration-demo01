from enum import Enum

from src.enums.enum import EncodeEnum


class InCsvConfEnum(Enum):
    """
    取り込むCSVに関する情報を定義したEnumクラス
    """

    # サンプル
    IN_SAMPLE = {
        "code": "sample",
        "table": {
            "name": "t_sample_001",
            "column_prefix": "s001_",
        },
        "input": {
            "dir": "input/01_sample",
            "encode": EncodeEnum.UTF8,
            "delimiter": ",",
            "quotechar": "\"",
            "exists_header": True,
        },
    }

    def getInCsvConfEnumByCode(code):
        """
        引数のコード値に該当するEnum値を返却する

        Args:
            code (str): 取り込むCSVのコード値

        Returns:
            LogModeEnum: 取り込むCSVのコード値に該当するEnum値を返却 | 該当無し時はエラー
        """
        for line in InCsvConfEnum:
            if line.value["code"] == code:
                return line
        raise ValueError("Error: getInCsvConfEnumByCode")
