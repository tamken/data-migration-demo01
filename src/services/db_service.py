# from src.settings.setting import env, logger, db_conn
from src.settings.setting import logger, db_conn


class DbService:
    """
    DB関連サービス
    """

    SQL_TRUNC = "./sql/00_temp/trunc.sql"
    SQL_DROP = "./sql/00_temp/drop.sql"
    SQL_CREATE = "./sql/00_temp/create.sql"
    SQL_INSERT = "./sql/00_temp/insert.sql"

    def __init__(self, table_name: str):
        """
        コンストラクタ

        Args:
            table_name(str): 対象テーブル名
        """
        self.table_name = table_name

    def truncate_table(self):
        """
        truncate（データ削除）
        """
        # テーブルクリア
        with open(self.SQL_TRUNC) as f:
            trunc_sql_txt = f.read() \
                .replace("##TABLE_NAME##", self.table_name)

        with db_conn.cursor() as cursor:
            cursor.execute(trunc_sql_txt)

        logger.info(
            "### table truncate has done.  [{0}]".format(self.table_name)
        )

    def recreate_table(
        self,
        column_cnt: int,
        column_name_list: list,
        column_prefix: str,
    ):
        """
        recreate（テーブル再作成）

        Args:
            column_cnt(int): テーブル項目数
            column_name_list(list): 項目名（論理名）のリスト（コメント設定用） | またはnull
            column_prefix(str): 再作成テーブルの項目のプレフィックス
        """
        # カラム生成
        columns = []
        prefix = column_prefix if 0 < len(column_prefix) else "c"
        for i in range(column_cnt):
            column = "`{0}{1:0>3}` TEXT".format(prefix, i + 1)
            if column_name_list is not None:
                column += " COMMENT '{0}'".format(column_name_list[i])
            columns.append(column)

        # SQL準備
        with open(self.SQL_DROP) as f:
            drop_sql_txt = f.read() \
                .replace("##TABLE_NAME##", self.table_name)

        with open(self.SQL_CREATE) as f:
            create_sql_txt = f.read() \
                .replace("##TABLE_NAME##", self.table_name) \
                .replace("##COLUMNS##", ", ".join(columns))

        # テーブル作成
        with db_conn.cursor() as cursor:
            cursor.execute(drop_sql_txt)
            cursor.execute(create_sql_txt)

        logger.info(
            "### table recreate has done.  [{0}]".format(self.table_name)
        )

    def insert_list(self, data_list: list, column_cnt: int):
        """
        insert（テーブルデータ登録（複数データ））

        Args:
            data_list(list): 登録データリスト
            column_cnt(int): テーブル項目数

        Returns:
            int: 登録件数
        """
        # SQL組み立て
        with open(self.SQL_INSERT) as f:
            insert_sql_txt = f.read() \
                .replace("##TABLE_NAME##", self.table_name) \
                .replace("##BIND_PARAMS##", ", ".join(["%s"] * column_cnt))

        # インサート（バルク風）
        with db_conn.cursor() as cursor:
            cursor.executemany(insert_sql_txt, data_list)

        logger.info(
            "### table import has done.  [{0:,d} records]"
            .format(len(data_list))
        )

        return len(data_list)
