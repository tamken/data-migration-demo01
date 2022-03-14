import pymysql

from src.dtos.params.mysql_connect_param_dto import MySQLConnectParamDto


class MySQLConnect:
    """
    DB(MySQL)コネクションクラス
    """

    __instance = None

    @staticmethod
    def getInstance(mysql_connect_param_dto: MySQLConnectParamDto):
        """
        コネクション情報取得

        Args:
            mysql_connect_param_dto(MySQLConnectParamDto): MySQLコネクションパラメータDTO
        """
        if MySQLConnect.__instance is None:
            MySQLConnect(mysql_connect_param_dto=mysql_connect_param_dto)

        return MySQLConnect.__instance

    def __init__(self, mysql_connect_param_dto: MySQLConnectParamDto):
        """
        コンストラクタ

        Args:
            mysql_connect_param_dto(MySQLConnectParamDto): MySQLコネクションパラメータDTO
        """
        if MySQLConnect.__instance is not None:
            raise Exception("DBコネクション生成エラー(no singleton)")

        MySQLConnect.__instance = pymysql.connect(
            host=mysql_connect_param_dto.host,
            port=mysql_connect_param_dto.port,
            database=mysql_connect_param_dto.db,
            user=mysql_connect_param_dto.user,
            password=mysql_connect_param_dto.password,
            cursorclass=pymysql.cursors.DictCursor,
        )
