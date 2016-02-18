# for testing purpose, run just one cache
# testing the behavior when the cache is gone

./kill_caches.sh
mkdir -p caches
rm -rf caches/*

cd "caches"
echo "Initiating single cache..."
mkdir -p cache001
cd "cache001"
rm -rf video*
python ../../cache.py 1 public
cd "../.."
