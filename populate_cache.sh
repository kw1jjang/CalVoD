num_of_caches=5
if [ ! -z "$1" ] ; then
    num_of_caches=$1
fi
base_port=49152 # this is the first of the private ports, so we won't disrupt
                # operations using reserved ports.
cd "config"
#./edit_cache_config.sh
cd ".."
rm -rf caches
if [ ! -d "caches" ]; then
    mkdir "caches"
fi
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
    python ../../cache.py $i > /dev/null  &
	
    cd ..
    sleep .1
done
cd ".."
