if [ ! -d "server" ]; then
    mkdir "server"
fi

cd "server"
echo ""
echo "Initiating server, pleae enter the option:"
echo "(no input -- run server on locahost:8081)"
echo "(PORT_NUMBER -- run server on localhost:PORT_NUMBER)"
echo "(p PORT_NUMBER -- run server on public_address:PORT_NUMBER)"
read option option2

if [ -z "$option" ]
then
  echo ""
  echo "Server will run on localhost:8081"
  python ../server.py
elif [ "$option" == "p" ]
then
  address=`curl icanhazip.com`
  echo ""
  echo "Server will runn on [$address]:$option2"
  python ../server.py $address $option2
else
  echo ""
  echo "Server will run on localhost:$option"
  python ../server.py $option
fi
cd ".."

#to-do: add some code to write to log/server.txt