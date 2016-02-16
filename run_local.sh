#!/bin/bash

source ~/envs/hackpsu/bin/activate
python -m SimpleHTTPServer &
python server.py &
echo "-----"
echo "Both servers are running. To quit them you will need to manually"
echo "kill both processes. Use 'ps aux | grep python' to find the Pro-"
echo "cess ID (PID) of the running process. It is the number in the "
echo "first column to the right of your user. "
echo ""
echo "Kill process with 'kill [PID]', where PID (without brackets) is "
echo "the Process ID we found above."