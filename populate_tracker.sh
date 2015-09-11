rm log/*
echo "Initiating tracker..."
python tracker.py 8080 > log/tracker.txt &

