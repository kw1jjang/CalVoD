if [ ! -d "server" ]; then
    mkdir "server"
fi

cd "server"
./kill_server.sh
echo "Initiating server..."

if [ -z "$1" ]
then
  python ../server.py
elif [ "$1" == "p" ]
then
  address=`curl icanhazip.com`
  python ../server.py $address $2
else
  port=$1
  python ../server.py $1
fi
cd ".."