#!/bin/bash
set -e

[ ! -d ${SCRIPTS_DIR}/log ] && mkdir -p /root/log
crond
[ -f /tmp/crontab.list ] && rm -f /tmp/crontab.list
echo "55 * * * * git -C ${SCRIPTS_DIR} pull | ts \"%Y-%m-%d %H:%M:%S\" >> ${SCRIPTS_DIR}/log/git_pull.log" >> /tmp/crontab.list
echo "25 4 * * 6 { DateDelLog=$(date \"+%Y-%m-%d" -d "${RM_LOG_DAYS_BEFORE} days ago\"); for log in $(ls ${SCRIPTS_DIR}/log/*.log); do { LineDel=$(cat ${log} | grep -n ${DateDelLog} | tail -1 | awk -F ' ' '{print $1}'); sed \"1,${LineDel}d\" ${log} }; done } >/dev/null 2>&1" >> /tmp/crontab.list
[[ ${ENABLE_QQREAD_CRONTAB} == true ]] && echo "*/10 * * * * { cd ${SCRIPTS_DIR}/scripts; python qq_read.py } | ts \"%Y-%m-%d %H:%M:%S\" >> ${SCRIPTS_DIR}/log/qq_read.log" >> /tmp/crontab.list
[[ ${ENABLE_BILIBILI_CRONTAB} == true ]] && echo "15 8 * * * { cd ${SCRIPTS_DIR}/scripts; python bilibili.py } | ts \"%Y-%m-%d %H:%M:%S\" >> ${SCRIPTS_DIR}/log/bilibili.log" >> /tmp/crontab.list

crontab /tmp/crontab.list
rm -f /tmp/crontab.list

if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
  set -- python3 "$@"
fi

exec "$@"