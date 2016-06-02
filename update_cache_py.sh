echo "updating cache.py on C2 - C6..."
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/cache.py ec2-user@52.7.236.218:~/CalVoD/cache.py #C2
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/cache.py ec2-user@52.200.196.119:~/CalVoD/cache.py #C3
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/cache.py ec2-user@52.201.5.148:~/CalVoD/cache.py #C4
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/cache.py ec2-user@52.201.45.124:~/CalVoD/cache.py #C5
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/cache.py ec2-user@54.152.185.230:~/CalVoD/cache.py #C6

scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/populate_users.sh ec2-user@54.89.22.93:~/CalVoD/populate_users.sh
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/populate_users.sh ec2-user@54.86.170.149:~/CalVoD/populate_users.sh
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/populate_users.sh ec2-user@54.84.101.123:~/CalVoD/populate_users.sh
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/populate_users.sh ec2-user@52.87.246.52:~/CalVoD/populate_users.sh
scp -i ~/.ssh/NVirginakey.pem ~/Desktop/CalVoD/populate_users.sh ec2-user@54.165.253.88:~/CalVoD/populate_users.sh
echo "done!"
