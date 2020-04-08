import paramiko
import re
import json

def healthdata(hostIP,hostUser,keyFileName):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostIP,username=hostUser, key_filename=keyFileName)
        response_list = {}

        command_list = ["top -b -n1 | grep 'Cpu(s)' | awk '{print $2 + $4}'","df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5}'","free | grep Mem | awk '{print $4/$2 * 100.0}'","dig +short myip.opendns.com @resolver1.opendns.com","df -h --total | grep total | awk '{print $5+0}'"]
        commandKeys_list = ["CPU","Disk","Memory","IP","Availablespace"]
        commandsIter = 0
        for iter in command_list:
            stdin, stdout, stderr = ssh.exec_command(iter)#uptime;ls -l;touch mickymouse;ls -l;uptime")
            stdin.flush()
            data = stdout.read().splitlines()
            line_iter = 0
            final_list=[]
            keys_list = []
            value_list = []
            each_lineDict = {}
            numberOfKeys = 0
            if iter in ["CPU ","Disk","Memory"]:
                if iter == "CPU":
                    keys_list = [ "CPU_load" ]
                elif iter == "Disk":
                    keys_list = [ "Disk_Utilization" ]
                else:
                    keys_list = [ "Memory_Utilized" ]
            for line in data:
                each_lineList = []
                each_lineDict = {}
                if line_iter == 0 and len(keys_list) == 0:
                    line = line.decode("utf-8")
                    for each_word in re.split("\s+",line):
                        each_lineList.append(each_word)
                        keys_list.append(each_word)
                        numberOfKey = numberOfKeys+1
                else:
                    line = line.decode("utf-8").strip()
                    word_iterator = 0
                    keysLen = len(keys_list)
                    prev_word = ""
                    for each_word in re.split("\s+", line):
                        value_list.append(each_word)
                        if word_iterator >= keysLen - 1:
                            prev_word = prev_word + each_word + " "
                            each_word = prev_word
                        each_lineDict[keys_list[word_iterator if word_iterator < keysLen else keysLen-1]] = each_word
                        word_iterator = word_iterator + 1
                for key in each_lineDict:
                    each_lineList.append(each_lineDict[key])
                line_iter = line_iter + 1
                final_list.append(each_lineList)
            response_list[commandKeys_list[commandsIter]] = final_list
            commandsIter = commandsIter + 1
        ssh.close()
        resp = (json.dumps(response_list))
        return(json.loads(resp))



openlist = []
list = ["13.235.77.65","13.127.69.143"]
for li in list:
    a = healthdata(li,"ec2-user","putty_keypair.pem")
    openlist.append(a)
print(openlist)

disk=[]
for i in range(0,len(openlist)):
    for j in openlist[i]['Availablespace']:
        for k in j:
            a = float(k)
            disk.append(a)

cpu_list = []
for i in range(0,len(openlist)):
    for j in openlist[i]['CPU']:
        for k in j:
            a = float(k)
            cpu_list.append(a)

mem_list = []
for i in range(0,len(openlist)):
    for j in openlist[i]['Memory']:
        for k in j:
            a = float(k)
            mem_list.append(a)
print(cpu_list)
print(disk)
print(mem_list)
