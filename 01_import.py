import fire
import os
import shutil

from src.enums.enum import AdditionalOptionEnum
from src.enums.in_csv_conf_enum import InCsvConfEnum
from src.services.db_service import DbService
from src.services.file_service import FileService
from src.settings.setting import logger


def main(in_csv_code="", add_mode=""):
    """
    CSVインポート main

    Args:
        in_csv_code(str): InCsvConfEnumのコード値。required。
        add_mode(str):
            - 「truncate」が設定されている場合はテーブルクリアしてからデータインポート
            - 「recreate」が設定されている場合はテーブル再作成
    """
    logger.info("# CSV Import Start.")
    # 変数
    has_re_created = False
    total_insert_count = 0

    # 引数チェック（設定有無）
    if len(str(in_csv_code)) <= 0:
        logger.warning(
            "引数未指定: [usage - pipenv run python {0} 999]"
            .format(os.path.basename(__file__))
        )
        exit()

    # 引数チェック（有効値）
    try:
        in_csv_enum = InCsvConfEnum.getInCsvConfEnumByCode(str(in_csv_code))
    except ValueError:
        logger.warning("引数指定値に誤り: [" + str(in_csv_code) + "]")
        exit()

    add_mode_enum = \
        AdditionalOptionEnum.getAdditionalOptionEnumByValue(str(add_mode))

    # Serviceインスタンス
    db_service = DbService(in_csv_enum.value["table"]["name"])
    file_service = FileService()

    # テーブルクリア
    if add_mode_enum == AdditionalOptionEnum.TRUNCATE:
        db_service.truncate_table()

    # import済ファイルの移動/格納ディレクトリを作成（無いときのみ）
    os.makedirs(in_csv_enum.value["input"]["dir"] + "/done", exist_ok=True)

    # importファイルの一覧を取得しループ
    import_csvs = os.listdir(in_csv_enum.value["input"]["dir"])
    for import_csv in import_csvs:
        # 拡張子.csv判定
        if import_csv.lower().endswith(".csv"):
            # 開始ログ
            logger.info("## {0} -> {1} Start.".format(
                import_csv,
                in_csv_enum.value["table"]["name"])
            )

            # ファイル読み込み
            file_list, file_column_cnt, file_header_list = file_service.reader(
                in_csv_enum,
                import_csv
            )

            # テーブル再作成
            if add_mode_enum == AdditionalOptionEnum.RECREATE and \
               not has_re_created:
                db_service.recreate_table(
                    file_column_cnt,
                    file_header_list,
                    in_csv_enum.value["table"]["column_prefix"]
                )
                has_re_created = True

            # ファイルインポート
            total_insert_count += db_service.insert_list(
                file_list,
                file_column_cnt
            )

            # インポート済のファイルを移動する
            shutil.move(
                in_csv_enum.value["input"]["dir"] + "/" + import_csv,
                in_csv_enum.value["input"]["dir"] + "/done",
            )

            # 終了ログ
            logger.info("## {0} -> {1} End.".format(
                import_csv,
                in_csv_enum.value["table"]["name"])
            )

    # All Done
    logger.info(
        "# CSV Import End. [result: add {0:,d} records to {1}]".format(
            total_insert_count,
            in_csv_enum.value["table"]["name"],
        )
    )


if __name__ == "__main__":
    fire.Fire(main)
