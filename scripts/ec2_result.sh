#!/bin/bash
echo cache_1
scp -i key_virginia.pem -r ec2-user@ec2-54-234-111-173.compute-1.amazonaws.com:ftp-git/log results/$1
echo server_1
scp -i key_virginia.pem -r ec2-user@54.227.254.17:ftp-git/log results/$1
echo user_1
scp -i key_virginia.pem -r ec2-user@ec2-50-19-184-203.compute-1.amazonaws.com:ftp-git/log results/$1
