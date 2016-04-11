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
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.205.254.196

elif [ "$1" == "c4" ]
then
  echo ""
  echo "running c4"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.164.82.188

elif [ "$1" == "c5" ]
then
  echo ""
  echo "running c5"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.175.175.98

elif [ "$1" == "c6" ]
then
  echo ""
  echo "running c6"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.152.0.39

elif [ "$1" == "c7" ]
then
  echo ""
  echo "running c7"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.89.21.173

elif [ "$1" == "c8" ]
then
  echo ""
  echo "running c8"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.90.52.152

elif [ "$1" == "c9" ]
then
  echo ""
  echo "running c9"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.87.158.10

elif [ "$1" == "c10" ]
then
  echo ""
  echo "running c10"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.87.228.14

elif [ "$1" == "c11" ]
then
  echo ""
  echo "running c11"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.90.30.117

elif [ "$1" == "a1" ]
then
  echo ""
  echo "running a1"
  ssh -i ~/.ssh/sanj.pem ec2-user@52.9.120

else
  echo ""
  echo "invalid argument!"
fi