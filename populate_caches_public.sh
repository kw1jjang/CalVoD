./kill_caches.sh

num_of_caches=5
echo "Initiating cache, pleae enter the number of caches (default 5):"
read option
if [ ! -z "$option" ] ; then
    num_of_caches=$option
fi

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
    #python ../../cache.py $i > ../../log/cache_$i.txt &
    python ../../cache.py $i public > ../cache$i.txt &

    cd ..
    sleep .1
done
cd ".."
