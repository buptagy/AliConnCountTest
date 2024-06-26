#!/bin/bash
SEND_SCRIPT="/root/AliConnCountTest/clb/test.py"
timegap=$1
python3 $SEND_SCRIPT > /dev/null 2>&1
sleep $timegap
python3 $SEND_SCRIPT > /dev/null 2>&1
#sleep $timegap
#python3 $SEND_SCRIPT > /dev/null 2>&1

