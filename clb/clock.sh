#!/bin/bash

# 获取当前时间
current_time=$(date +%s)

# 计算两分钟后的时间
start_time=$((current_time + 60))

# 循环调度任务，每隔两分钟执行一次
for i in {0..0}; do
    # 计算每次执行的时间
    exec_time=$((start_time + 30 * i))
    
    # 将时间转换为可读格式
    exec_time_readable=$(date -d @$exec_time +%H:%M)
    
    # 调度任务
    echo "sh /root/AliConnCountTest/clb/start.sh 7" | at $exec_time_readable
done

# 查看已提交的任务
atq
