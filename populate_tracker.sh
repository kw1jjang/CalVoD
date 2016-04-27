mkdir -p log
mkdir -p server
mkdir -p server/user_log
rm -rf log/* 
rm -rf sessions/*
rm -f server/*.txt
echo ""
echo "cleared logs"

rm -rf caches/* users/*
mkdir -p caches/cache001
mkdir -p users/user001

echo "cleared ./caches directory"
echo "cleared ./useres directory"

./kill_all.sh
sleep 1
echo "killed all active processes"

echo ""
echo "Initiating tracker, pleae enter the option:"
echo "(no input -- run tracker on 0.0.0.0:8080)"
echo "(PORT_NUMBER -- run tracker on 0.0.0.0:PORT_NUMBER)"
echo "(p PORT_NUMBER -- run tracker on PUBLIC_ADDRESS:PORT_NUMBER)"
read option option2

if [ -z "$option" ]
then
  echo ""
  echo "Tracker will run on 0.0.0.0:8080"
  python tracker.py > log/tracker.txt &
  sleep .3
  curl 0.0.0.0:8080/req/RESET
elif [ "$option" == "p" ]
then
  address=`curl icanhazip.com`
  echo ""
  echo "Tracker will runn on [$address]:$option2"
  python tracker.py $address $option2 > log/tracker.txt &
  sleep .3
  curl $address:$option2/req/RESET
else
  echo ""
  echo "Tracker will run on localhost:$option"
  python tracker.py $option > log/tracker.txt &
  sleep .3
  curl localhost:$option/req/RESET
fi
