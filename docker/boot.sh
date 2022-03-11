#!/bin/bash

# ######
# DB(mysql8.0コンテナ)起動
# ######

# 環境変数
MYSQL_ROOT_PASSWORD="demo_root_pw"
MYSQL_DATABASE="demo_database"
MYSQL_USER="demo_user"
MYSQL_PASSWORD="demo_pw"

# DB起動（Docker実行）
cd `dirname "$0"`
EXEC_SH_PATH=`pwd -P`

docker run \
	--rm \
	-it \
	--name mysql-demo \
	-e MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} \
	-e MYSQL_DATABASE=${MYSQL_DATABASE} \
	-e MYSQL_USER=${MYSQL_USER} \
	-e MYSQL_PASSWORD=${MYSQL_PASSWORD} \
	-v ${EXEC_SH_PATH}/mnt:/var/lib/mysql \
	-v ${EXEC_SH_PATH}/conf:/etc/mysql/conf.d \
	-p 3306:3306 \
	-d mysql:8.0
