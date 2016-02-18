echo "Enter your option:"
echo "c1 - Chen's Virginia instance 1"
echo "c2 - Chen's Virginia instance 2"
echo "c3 - Chen's Virginia instance 3"
echo "c4 - Chen's N. California instance 1"
echo "a1 - Alagu's N. California instance 1"

if [ "$1" == "c1" ]
then
  echo ""
  echo "running c1"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.86.226.249

elif [ "$1" == "c2" ]
then
  echo ""
  echo "running c2"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@54.152.49.226

elif [ "$1" == "c3" ]
then
  echo ""
  echo "running c3"
  ssh -i ~/.ssh/NVirginakey.pem ec2-user@52.90.36.119

elif [ "$1" == "c4" ]
then
  echo ""
  echo "running c4"
  ssh -i ~/.ssh/MyFirstkey.pem ec2-user@54.153.85.152

elif [ "$1" == "a1" ]
then
  echo ""
  echo "running a1"
  ssh -i ~/.ssh/sanj.pem ec2-user@54.153.100.146

else
  echo ""
  echo "invalid argument!"
fi