#!/bin/bash
echo user_1
ssh -i key_virginia.pem ec2-user@ec2-50-19-184-203.compute-1.amazonaws.com "sh -c 'cd ftp-git; nohup ./populate_fake_users.sh &'" &
