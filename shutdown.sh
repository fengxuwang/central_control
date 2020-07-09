#!/bin/sh

pid=`ps -ef|grep "python3 /opt/central_control/main.py"| grep -v "grep"|awk '{print $2}'`

if [ "$pid" != "" ]
then
  kill -9 ${pid}
  echo "中控采集服务已停止"
else
  echo "中控采集服务未运行，不需要停止"
fi