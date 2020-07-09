#!/bin/sh
pid=`ps -ef|grep "python3 /opt/central_control/main.py"| grep -v "grep"|awk '{print $2}'`

if [ "$pid" != "" ]
then
  echo "中控采集服务已经运行，正在停止..."
  kill -9 ${pid}
  echo "中控采集服务已停止"
fi

echo "中控采集服务启动中..."

/opt/central_control/venv/bin/python3 /opt/central_control/main.py &

pid=`ps -ef|grep "python3 /opt/central_control/main.py"| grep -v "grep"|awk '{print $2}'`

if [ "$pid" = "" ]
then
  echo "中控采集服务启动失败"
else
  echo "中控采集服务启动成功，进程pid："${pid}
fi

