mkdir -p log
mkdir -p server
rm -rf log/*
rm -f server/*.txt
echo ""
echo "cleared logs"

rm -rf caches/* users/*
mkdir caches/cache001
mkdir users/user001

echo "cleared ./caches directory"
echo "cleared ./useres directory"
./kill_all.sh
echo "killed all active processes"

echo ""
echo "Initiating tracker, pleae enter the option:"
echo "(no input -- run tracker on locahost:8080)"
echo "(PORT_NUMBER -- run tracker on localhost:PORT_NUMBER)"
echo "(p PORT_NUMBER -- run tracker on PUBLIC_ADDRESS:PORT_NUMBER)"
read option option2

if [ -z "$option" ]
then
  echo ""
  echo "Tracker will run on localhost:8080"
  python tracker.py > log/tracker.txt &
  sleep .3
  curl localhost:8080/req/RESET

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
