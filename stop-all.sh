#!/usr/bin/env bash

echo "  ------ Killing all python3 process"
killall -9 python3
sleep 3
echo "  ------ Listing running process"
ps -aef | grep python | grep -v "grep"
echo "  ------ Listing log files "
ls -l logs/*.sysout