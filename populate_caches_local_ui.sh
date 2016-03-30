#./kill_caches.sh

cache_multiplier=1
username="chen"
password="11111"

if [ ! -z "$1" ] ; then
    cache_multiplier=$1
fi
if [ ! -z "$2" ] ; then
    username=$2
fi
if [ ! -z "$3" ] ; then
    password=$3
fi

mkdir -p caches
rm -rf caches/*
cd "caches"
echo "Initiating cache with id # $i ..."
if [ ! -d "cache001" ]; then
    mkdir "cache001"
fi
cd "cache001"

rm -rf video*
python ../../cache.py $cache_multiplier $username $password > /dev/null 2>&1 &
cd ".."
cd ".."
