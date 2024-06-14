#!/bin/bash
SEND_SCRIPT="test.py"
#timeout 6s tcpdump udp port 11111 -w res.pcap &
#sleep 1
python3 $SEND_SCRIPT > /dev/null 2>&1
#wait
sleep 17
python3 $SEND_SCRIPT > /dev/null 2>&1
sleep 17
python3 $SEND_SCRIPT > /dev/null 2>&1

