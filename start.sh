#!/bin/bash
SEND_SCRIPT="udpwithtwoprocess.py"
timeout 6s tcpdump udp port 11111 -w res.pcap &
sleep 1
python3 $SEND_SCRIPT > /dev/null 2>&1
wait
