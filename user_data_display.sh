uploaded=0
downloaded=0
if [ ! -z "$1" ] ; then
    uploaded=$1
fi
if [ ! -z "$2" ] ; then
    downloaded=$2
fi

echo $uploaded
echo $downloaded

python ../../user_data.py $uploaded $downloaded
