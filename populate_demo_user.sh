# for testing purpose, run just one cache
# testing the behavior when the cache is gone

./kill_users.sh
mkdir -p users

echo "user number:"
read option
if [ ! -z "$option" ] ; then
    num=$option
fi

cd "users"
echo "Initiating single user..."
rm -rf "user"$num
mkdir -p "user"$num
cd "user"$num
rm -rf video*

python ../../user_gui_demo.py ../../development.ini
cd "../.."
