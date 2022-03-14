from src.settings.setting import logger, db_conn


class DbService:
    """
    DB関連サービス
    """

    SQL_TRUNC = "./sql/00_temp/trunc.sql"
    SQL_DROP = "./sql/00_temp/drop.sql"
    SQL_CREATE = "./sql/00_temp/create.sql"
    SQL_INSERT = "./sql/00_temp/insert.sql"

    def truncate_table(self, table_name: str):
        """
        truncate（データ削除）

        Args:
            table_name(str): テーブル名
        """
        self.execute_sql(self.build_sql(self.SQL_TRUNC, table_name=table_name))

        logger.info(
            "### table truncate has done.  [{0}]".format(table_name)
        )

    def drop_table(self, table_name: str):
        """
        drop（テーブル削除）

        Args:
            table_name(str): テーブル名
        """
        self.execute_sql(self.build_sql(self.SQL_DROP, table_name=table_name))

    def create_table(
        self,
        table_name: str,
        column_cnt: int,
        column_name_list: list,
        column_prefix: str
    ):
        """
        create（テーブル作成）

        Args:
            table_name(str): テーブル名
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

        self.execute_sql(
            self.build_sql(
                self.SQL_CREATE,
                table_name=table_name,
                columns=", ".join(columns)
            )
        )

    def recreate_table(
        self,
        table_name: str,
        column_cnt: int,
        column_name_list: list,
        column_prefix: str,
    ):
        """
        recreate（テーブル再作成）

        Args:
            table_name(str): テーブル名
            column_cnt(int): テーブル項目数
            column_name_list(list): 項目名（論理名）のリスト（コメント設定用） | またはnull
            column_prefix(str): 再作成テーブルの項目のプレフィックス
        """
        # テーブル削除
        self.drop_table(table_name)

        # テーブル作成
        self.create_table(
            table_name,
            column_cnt,
            column_name_list,
            column_prefix
        )

        logger.info(
            "### table recreate has done.  [{0}]".format(table_name)
        )

    def insert_list(self, table_name: str, data_list: list, column_cnt: int):
        """
        insert（テーブルデータ登録（複数データ））

        Args:
            table_name(str): テーブル名
            data_list(list): 登録データリスト
            column_cnt(int): テーブル項目数

        Returns:
            int: 登録件数
        """
        rows = self.execute_bulk_insert(
            self.build_sql(
                self.SQL_INSERT,
                table_name=table_name,
                bind_params=", ".join(["%s"] * column_cnt)
            ),
            data_list
        )

        logger.info(
            "### table import has done.  [{0:,d} records]".format(rows)
        )

        return rows

    def build_sql(
        self,
        tmp_sql: str,
        table_name: str,
        columns: str = "",
        bind_params: str = ""
    ):
        """
        SQL組み立て

        Args:
            tmp_sql(str): 組み立て対象のSQLテンプレートパス
            table_name(str): テーブル名
            columns(str): 組み立てSQLに設定するカラム文字列
            bind_params(str): 組み立てSQLにバインドするカラム値の文字列

        Returns:
            str: SQL文字列
        """
        with open(tmp_sql) as f:
            sql_txt = f.read() \
                .replace("##TABLE_NAME##", table_name) \
                .replace("##COLUMNS##", columns) \
                .replace("##BIND_PARAMS##", bind_params)
        return sql_txt

    def execute_sql(self, sql_txt: str):
        """
        SQL実行

        Args:
            sql_txt(str): 実行対象SQL文字列

        Returns:
            int: affected row
        """
        with db_conn.cursor() as cursor:
            row = cursor.execute(sql_txt)
        return row

    def execute_bulk_insert(self, sql_txt: str, data_list: list):
        """
        SQL（バルクインサート）実行

        Args:
            sql_txt(str): 実行対象SQL文字列
            data_list(list): 一括挿入対象データリスト

        Returns:
            int: affected rows
        """
        with db_conn.cursor() as cursor:
            rows = cursor.executemany(sql_txt, data_list)
        return rows
