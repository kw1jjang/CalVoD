#!/bin/bash
echo server_1
ssh -n -f -i key_virginia.pem ec2-user@54.227.254.17 "sh -c 'cd ftp-git; nohup ./populate_tracker.sh > /dev/null 2>&1 '" &
sleep 3
curl 54.227.254.17:8081/req/RESET
sleep 1
ssh -n -f -i key_virginia.pem ec2-user@54.227.254.17 "sh -c 'cd ftp-git; nohup ./populate_server.sh &'" &
