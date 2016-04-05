#populate multiple users onto the system
num_of_users=5
echo "Initiating users, pleae enter the number of caches (default 5):"
read option
if [ ! -z "$option" ] ; then
    num_of_users=$option
fi

mkdir -p users
rm -rf users/*
cd "users"
for (( i = 60; i <= num_of_users; i++ ))
do
    echo "Initiating user with id # $i ..."
    if [ ! -d "user"$i ]; then
        mkdir "user"$i
    fi
    cd "user"$i
    rm -rf video*
    #python ../../cache.py $i > ../../log/cache_$i.txt &
    python ../../user_gui_demo.py ../../develpment.ini > /dev/null &

    cd ..
    sleep 2
done
cd ".."