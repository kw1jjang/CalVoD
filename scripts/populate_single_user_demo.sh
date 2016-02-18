# for testing purpose, run just one cache
# testing the behavior when the cache is gone

./kill_users.sh
mkdir -p users
rm -rf users/user001

cd "users"
echo "Initiating single user..."
mkdir -p user001
cd "user001"
rm -rf video*
python ../../single_user_gui_demo.py ../../development.ini
cd "../.."
