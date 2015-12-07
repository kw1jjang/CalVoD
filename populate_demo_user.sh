# for testing purpose, run just one cache
# testing the behavior when the cache is gone

./kill_users.sh
#python remove_user.py
mkdir -p users

echo "number of users (lower):"
read option
if [ ! -z "$option" ] ; then
    num1=$option
fi
echo "number of users (upper):"
read option
if [ ! -z "$option" ] ; then
    num2=$option
fi

cd "users"
for (( i = num1; i <= num2; i++ ))
do
    echo "Initiating single user..."
    rm -rf "user"$i
    mkdir -p "user"$i
    cd "user"$i
    rm -rf video*
    python ../../user_gui_demo.py ../../development.ini > /dev/null &
    cd ".."
    sleep(3)
done

cd ".."
