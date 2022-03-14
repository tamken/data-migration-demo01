import csv

from src.enums.enum import OpenModeEnum
from src.enums.in_csv_conf_enum import InCsvConfEnum


class FileService:
    """
    ファイル操作関連サービス
    """

    def reader(self, in_csv_enum: InCsvConfEnum, file_name: str):
        """
        ファイル読み込み

        Args:
            in_csv_enum(InCsvConfEnum): CSV情報enum
            file_name(str): ファイル名
        """
        file_list = []
        column_name_list = []

        with open(
            in_csv_enum.value["input"]["dir"] + "/" + file_name,
            OpenModeEnum.READ.value,
            encoding=in_csv_enum.value["input"]["encode"].value["value"],
            newline="",
        ) as f:
            reader = csv.reader(
                f,
                delimiter=in_csv_enum.value["input"]["delimiter"],
                quotechar=in_csv_enum.value["input"]["quotechar"],
            )

            # ヘッダ
            if in_csv_enum.value["input"]["exists_header"]:
                column_name_list = next(reader)

            # 読み込み（リストセット）
            for row in reader:
                file_list.append(row)

        # return
        return file_list, \
            len(file_list[0]) if 0 < len(file_list) else 0, \
            column_name_list if 0 < len(column_name_list) else None
