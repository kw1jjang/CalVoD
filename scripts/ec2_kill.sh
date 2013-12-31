#!/bin/bash
echo cache_1
ssh -i key_virginia.pem ec2-user@ec2-54-234-111-173.compute-1.amazonaws.com "cd ftp-git; ./kill_all.sh"
echo server_1
ssh -i key_virginia.pem ec2-user@54.227.254.17 "cd ftp-git; ./kill_all.sh"
echo user_1
ssh -i key_virginia.pem ec2-user@ec2-50-19-184-203.compute-1.amazonaws.com "cd ftp-git; ./kill_all.sh"
