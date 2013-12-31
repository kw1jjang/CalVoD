import commands
import time
import os

def cmd(command):
    os.system(command)

cmd('ec2-host --aws-key AKIAILDLCNOOFK4VBXGA --aws-secret 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 -r us-west-1 > ec2_nor_cal.ip')
cmd('ec2-host --aws-key AKIAILDLCNOOFK4VBXGA --aws-secret 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 -r us-east-1 > ec2_virginia.ip')

f = ['ec2_nor_cal.ip', 'ec2_virginia.ip']
output = [[],[]]

i_zone = 0
for each_f in f:
    fd = open(each_f, 'r')
    content = fd.readlines()
    for each_row in content:
        each_row = each_row.replace('\n', '\t')
        a = each_row.split('\t')
        if a[0] == 'jasmine':
            continue
        output[i_zone].append(a)
    i_zone += 1

key = ['key_north_cal.pem', 'key_virginia.pem']

# KILL SCRIPT
text = '#!/bin/bash\n'
for i in range(2):
    each_region = output[i]
    for each_host in each_region:
        text += 'ssh -i ' + key[i] + ' ec2-user@' + each_host[1] + ' "cd ftp-git; ./kill_all.sh"\n'
f = open('ec2_kill.sh', 'w')
f.write(text)
f.close()

# GIT SCRIPT
text = '#!/bin/bash\n'
for i in range(2):
    each_region = output[i]
    for each_host in each_region:
        text += 'ssh -i ' + key[i] + ' ec2-user@' + each_host[1] + ' "cd ftp-git; git pull origin master"\n'
f = open('ec2_git_pull.sh', 'w')
f.write(text)
f.close()

# SERVER SCRIPT
text = '#!/bin/bash\n'
for i in range(2):
    each_region = output[i]
    for each_host in each_region:
        if each_host[0].startswith('server'):
            text += 'ssh -n -f -i ' + key[i] + ' ec2-user@' + each_host[1] + ' "' + "sh -c 'cd ftp-git; " + "nohup ./populate_tracker.sh > /dev/null 2>&1 '" + '" &\n'
            text += 'sleep 1\n'
            text += 'ssh -n -f -i ' + key[i] + ' ec2-user@' + each_host[1] + ' "' + "sh -c 'cd ftp-git; " + "nohup ./populate_server.sh" + " &'" + '" &\n'
#            print text
            print 'running a server on', each_host
f = open('ec2_server.sh', 'w')
f.write(text)
f.close()

# CACHE SCRIPT
text2 = '#!/bin/bash\n'
for i in range(2):
    each_region = output[i]
    for each_host in each_region:
        if each_host[0].startswith('cache'):
            text2 += 'ssh -i ' + key[i] + ' ec2-user@' + each_host[1] + ' "' + "sh -c 'cd ftp-git; " + "nohup ./populate_cache.sh" + " &'" + '" &\n'
#            print text
            print 'running caches on', each_host
f = open('ec2_cache.sh', 'w')
f.write(text2)
f.close()

# USER SCRIPT
text3 = '#!/bin/bash\n'
for i in range(2):
    each_region = output[i]
    for each_host in each_region:
        if each_host[0].startswith('user'):
            text3 += 'ssh -i ' + key[i] + ' ec2-user@' + each_host[1] + ' "' + "sh -c 'cd ftp-git; " + "nohup ./populate_users.sh" + " &'" + '" &\n'
#            print text
            print 'running users on', each_host
f = open('ec2_user.sh', 'w')
f.write(text3)
f.close()
