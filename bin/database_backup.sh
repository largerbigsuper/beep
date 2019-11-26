#!/bin/bash

SAVE_PATH="/root/.beep/db/beep_db.sql_$(date '+%Y_%m_%d_%H_%M_%S')"
echo $SAVE_PATH
DB_USER="root"
DB_PASSWORD="888888"
DB_NAME="beep_db_production"
DB_HOST="127.0.0.1"
DB_PORT=3306

# mysqldump 提示不安全拒绝执行
export MYSQL_PWD=${DB_PASSWORD}

 /usr/local/bin/mysqldump --result-file=${SAVE_PATH} ${DB_NAME} --user=${DB_USER} --host=${DB_HOST} --port=${DB_PORT}

