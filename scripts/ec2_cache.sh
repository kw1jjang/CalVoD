#!/bin/bash
echo cache_1
ssh -i key_virginia.pem ec2-user@ec2-54-234-111-173.compute-1.amazonaws.com "sh -c 'cd ftp-git; nohup ./populate_cache.sh &'" &
