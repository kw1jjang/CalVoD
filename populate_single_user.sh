# for testing purpose, run just one cache
# testing the behavior when the cache is gone

./kill_users.sh
mkdir -p users
rm -rf users/*

cd "users"
echo "Initiating single user..."
mkdir -p user001
cd "user001"
rm -rf video*
python ../../user_gui.py ../../development.ini
cd "../.."
