echo "Enter your option:"
echo "c1 - Chen's Virginia instance 1 - server"
echo "c2 - Chen's Virginia instance 2"
echo "c3 - Chen's Virginia instance 3"
echo "c4 - Chen's Virginia instance 4"
echo "c5 - Chen's Virginia instance 5"
echo "c6 - Chen's Virginia instance 6"
echo "c7 - Chen's Virginia instance 7"
echo "c8 - Chen's Virginia instance 8"
echo "c9 - Chen's Virginia instance 9"
echo "c10 - Chen's Virginia instance 10"
echo "c11 - Chen's Virginia instance 11"

if [ "$1" == "c1" ]
then
  echo ""
  echo "running c1 - the server"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.22.160.180
    #ssh -i ~/.ssh/MyFirstkey.pem ec2-user@54.153.85.152 #the original California instance

elif [ "$1" == "c2" ]
then
  echo ""
  echo "running c2"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.7.236.218

elif [ "$1" == "c3" ]
then
  echo ""
  echo "running c3"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.200.196.119

elif [ "$1" == "c4" ]
then
  echo ""
  echo "running c4"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.201.5.148

elif [ "$1" == "c5" ]
then
  echo ""
  echo "running c5"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.201.45.124

elif [ "$1" == "c6" ]
then
  echo ""
  echo "running c6"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.152.185.230

elif [ "$1" == "c7" ]
then
  echo ""
  echo "running c7"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.89.22.93

elif [ "$1" == "c8" ]
then
  echo ""
  echo "running c8"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.86.170.149

elif [ "$1" == "c9" ]
then
  echo ""
  echo "running c9"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.84.101.123

elif [ "$1" == "c10" ]
then
  echo ""
  echo "running c10"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.87.246.52

elif [ "$1" == "c11" ]
then
  echo ""
  echo "running c11"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.165.253.88

elif [ "$1" == "a1" ]
then
  echo ""
  echo "running a1"
  ssh -i ~/.ssh/sanj.pem ec2-user@52.9.120

else
  echo ""
  echo "invalid argument!"
fi
