import commands

GIT_KILL_ALL =[True, True]

def cmd(command):
    commands.getstatusoutput(command)

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

# GIT KILL ALL
for i in range(2):
    if GIT_KILL_ALL[i] == False:
        continue
    each_region = output[i]
    for each_host in each_region:
        ssh_str = 'ssh -i ' + key[i] + ' ec2-user@' + each_host[1] + ' "cd ftp-git; ./kill_all.sh"'
        print ssh_str
        cmd(ssh_str)
        print 'killing all on', each_host
