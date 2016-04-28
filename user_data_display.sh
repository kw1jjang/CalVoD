uploaded_server=0
downloaded_server=0
uploaded_cache=0
downloaded_cache=0
if [ ! -z "$1" ] ; then
    uploaded_server=$1
fi
if [ ! -z "$2" ] ; then
    uploaded_cache=$2
fi
if [ ! -z "$3" ] ; then
    downloaded_server=$3
fi
if [ ! -z "$4" ] ; then
    downloaded_cache=$4
fi

echo $uploaded_server
echo $uploaded_cache
echo $downloaded_server
echo $downloaded_cache

python ../../user_data.py $uploaded_server $uploaded_cache $downloaded_server $downloaded_cache
