# for testing purpose, run just one cache
# testing the behavior when the cache is gone

./kill_users.sh
python remove_user.py
mkdir -p users

echo "number of users:"
read option
if [ ! -z "$option" ] ; then
    num=$option
fi

cd "users"
for (( i = 1; i <= num; i++ ))
do
    echo "Initiating single user..."
    rm -rf "user"$i
    mkdir -p "user"$i
    cd "user"$i
    rm -rf video*
    python ../../user_gui_demo.py ../../development.ini > /dev/null &
    cd ".."
    sleep .1
done

cd ".."
