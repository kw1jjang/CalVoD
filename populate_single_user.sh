# for testing purpose, run just one cache
# testing the behavior when the cache is gone

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
python ../../user_gui.py ../../development.ini chen 11111
cd "../.."
