#!/bin/bash
url_server="ec2-user@ec2-107-22-68-35.compute-1.amazonaws.com"
url_cache_1="ec2-user@ec2-50-19-67-54.compute-1.amazonaws.com"
url_user_1="ec2-user@ec2-54-234-244-238.compute-1.amazonaws.com"
echo $url_server
scp -i vod_test.pem -r $url_cache_1:ftp-git/log results/$1
scp -i vod_test.pem -r $url_user_1:ftp-git/log results/$1
