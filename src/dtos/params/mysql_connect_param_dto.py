class MySQLConnectParamDto:
    """
    MySQLコネクションパラメータDTO
    """
    def __init__(
        self,
        host: str,
        port: int,
        db: str,
        user: str,
        password: str
    ) -> None:
        """
        コンストラクタ

        Args:
            host(str): ホスト名
            port(int): ポート
            db(str): DB名
            user(str): ユーザー名
            password(str): パスワード
        """
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

    # ホスト名
    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    # ポート名
    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value: int):
        if type(value) is not int:
            value = int(value)
        self.__port = value

    # DB名
    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value):
        self.__db = value

    # ユーザー名
    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    # パスワード
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value
