username="chen"
password="11111"
if [ ! -z "$1" ] ; then
    username=$1
fi
if [ ! -z "$2" ] ; then
    password=$2
fi

./kill_users.sh
mkdir -p users
rm -rf users/user001
#rm -rf users/.user001

cd "users"
mkdir -p user001
cd "user001"
# mkdir -p .user001
# cd ".user001"
rm -rf video*
python ../../user_gui.py ../../development.ini $username $password
cd "../.."
