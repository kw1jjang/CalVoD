echo "updating cache.py on C2 - C6..."
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/P2PVoD/cache.py ec2-user@52.7.236.218:~/P2PVoD/cache.py #C2
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/P2PVoD/cache.py ec2-user@52.200.196.119:~/P2PVoD/cache.py #C3
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/P2PVoD/cache.py ec2-user@52.201.5.148:~/P2PVoD/cache.py #C4
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/P2PVoD/cache.py ec2-user@52.201.45.124:~/P2PVoD/cache.py #C5
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/P2PVoD/cache.py ec2-user@52.23.229.177:~/P2PVoD/cache.py #C6
echo "done!"