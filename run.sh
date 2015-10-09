#rm -r log/*
mkdir -p log
mkdir -p users/user001
mkdir -p caches/cache001
rm -r caches/cache001/* users/user001/* rm -r log/*

./kill_all.sh
./populate_tracker.sh
./populate_server.sh
