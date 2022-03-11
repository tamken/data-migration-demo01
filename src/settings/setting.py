from os.path import join, dirname

from dotenv import load_dotenv, dotenv_values

from src.dtos.params.mysql_connect_param_dto import MySQLConnectParamDto
from src.enums.enum import LogLevelEnum, LogModeEnum
from src.utils.db_conn import MySQLConnect
from src.utils.logger import LogUtil

# dotenv
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(verbose=True, dotenv_path=dotenv_path)
env = dotenv_values(verbose=True)

# logger
logger = LogUtil.getInstance(
    LogLevelEnum.getLogLevelEnumByCode(env["LOG_LEVEL"]),
    LogModeEnum.getLogModeEnumByCode(env["LOG_MODE"]),
    env["LOG_DIR"]
)

# db_connection
try:
    db_conn = MySQLConnect.getInstance(
        MySQLConnectParamDto(
            env["DB_HOST"],
            env["DB_PORT"],
            env["DB_NAME"],
            env["DB_USER"],
            env["DB_PASSWORD"],
        )
    )
except Exception as e:
    logger.error("DB接続エラー")
    logger.debug(e)
    raise
