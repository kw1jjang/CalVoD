./kill_caches.sh
#python remove_cache.py

num_of_caches=5
#address=`curl icanhazip.com`

echo "number of caches (lower):"
read option
if [ ! -z "$option" ] ; then
    num1=$option
fi
echo "number of caches (upper):"
read option
if [ ! -z "$option" ] ; then
    num2=$option
fi

mkdir -p caches
rm -rf caches/*
cd "caches"
for (( i = num1; i <= num2; i++ ))
do
    echo "Initiating cache with id # $i ..."
    if [ ! -d "cache"$i ]; then
        mkdir "cache"$i
    fi
    cd "cache"$i
    rm -rf video*
    python ../../cache.py $i > /dev/null &
    cd ..
    sleep .1
done
cd ".."
