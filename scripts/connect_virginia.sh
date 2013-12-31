#!/bin/bash
ip=`ec2-host --aws-key AKIAILDLCNOOFK4VBXGA --aws-secret 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 $1`
echo $ip
ssh -i key_virginia.pem ec2-user@$ip
