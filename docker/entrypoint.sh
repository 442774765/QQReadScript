#!/bin/bash
set -e

[ ! -d ${SCRIPTS_DIR}/log ] && mkdir -p /root/log
crond

[ -f /tmp/crontab.list ] && rm -f /tmp/crontab.list
echo "55 * * * * git -C ${SCRIPTS_DIR} pull | ts \"%Y-%m-%d %H:%M:%S\" >> ${SCRIPTS_DIR}/log/git_pull.log 2>&1" >> /tmp/crontab.list
echo "25 4 * * 6 chmod +x ${SCRIPTS_DIR}/docker/rm_log.sh && bash ${SCRIPTS_DIR}/docker/rm_log.sh >/dev/null 2>&1" >> /tmp/crontab.list
[[ ${ENABLE_QQREAD_CRONTAB} == true ]] && echo "*/10 * * * * cd ${SCRIPTS_DIR}/scripts && python qq_read.py | ts \"%Y-%m-%d %H:%M:%S\" >> ${SCRIPTS_DIR}/log/qq_read.log 2>&1" >> /tmp/crontab.list
[[ ${ENABLE_BILIBILI_CRONTAB} == true ]] && echo "15 8 * * * cd ${SCRIPTS_DIR}/scripts && python bilibili.py | ts \"%Y-%m-%d %H:%M:%S\" >> ${SCRIPTS_DIR}/log/bilibili.log 2>&1" >> /tmp/crontab.list

crontab /tmp/crontab.list
rm -f /tmp/crontab.list

python3

exec "$@"