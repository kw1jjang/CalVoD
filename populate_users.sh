#populate multiple users onto the system
num_of_users=5
echo "Initiating users, pleae enter the number of users (default 5):"
read option
if [ ! -z "$option" ] ; then
    num_of_users=$option
fi

mkdir -p users
rm -rf users/*
cd "users"
for (( i = 1; i <= num_of_users; i++ ))
do
    echo "Initiating user with id # $i ..."
    if [ ! -d "user"$i ]; then
        mkdir "user"$i
    fi
    cd "user"$i
    rm -rf video*
    python ../../user_gui_demo.py ../../develpment.ini $i > ../user$i.txt &

    cd ..
    sleep 30
done
cd ".."
