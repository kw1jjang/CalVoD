./kill_caches.sh

num_of_caches=5
username="alagu"
password="11111"

if [ ! -z "$1" ] ; then
    num_of_caches=$1
fi
if [ ! -z "$2" ] ; then
    username=$2
fi
if [ ! -z "$3" ] ; then
    password=$3
fi
# echo "Initiating cache, pleae enter the number of caches (default 5):"
# read option
# if [ ! -z "$option" ] ; then
#     num_of_caches=$option
# fi

mkdir -p caches
rm -rf caches/*
cd "caches"
for (( i = 1; i <= num_of_caches; i++ ))
do
    echo "Initiating cache with id # $i ..."
    if [ ! -d "cache"$i ]; then
        mkdir "cache"$i
    fi
    cd "cache"$i
    rm -rf video*
    python ../../cache.py $i public $username $password > /dev/null 2>&1 &
    cd ..
    sleep .1
done
cd ".."