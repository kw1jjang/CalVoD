#!/bin/bash
ip=`ec2-host --aws-key AKIAILDLCNOOFK4VBXGA --aws-secret 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 -r us-west-1 $1`
echo $ip
ssh -i key_north_cal.pem ec2-user@$ip
