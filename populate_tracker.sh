rm log/*
echo "Initiating tracker..."
python tracker.py 8081 > log/tracker.txt &
sleep .3
curl localhost:8081/req/RESET
