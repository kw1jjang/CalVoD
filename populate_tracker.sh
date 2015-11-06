rm -r log/*
mkdir -p log
mkdir -p users/user001
mkdir -p caches/cache001
rm -r caches/cache001/* users/user001/* rm -r log/*
./kill_all.sh
echo "Initiating tracker..."

if [ -z "$1" ]
then
  python tracker.py > log/tracker.txt &
  sleep .3
  curl localhost:8080/req/RESET
  echo ""
  echo "Tracker is running on localhost:8080"
elif [ "$1" == "p" ]
then
  address=`curl icanhazip.com`
  python tracker.py $address $2 > log/tracker.txt &
  sleep .3
  curl $address:$2/req/RESET
  echo ""
  echo "Tracker is running on [$address]:$2"
else
  python tracker.py $1 > log/tracker.txt &
  sleep .3
  curl localhost:$1/req/RESET
  echo ""
  echo "Tracker is running on localhost:$1"
fi
