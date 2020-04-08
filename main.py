from flask import Flask, render_template, jsonify, request
import pandas as pd
import paramiko
import re
import json

app = Flask(__name__)

def healthdata(hostIP,hostUser,keyFileName):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostIP,username=hostUser, key_filename=keyFileName)
    response_list = {}
    command_list = ["top -b -n1 | grep 'Cpu(s)' | awk '{print $2 + $4}'","df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5}'","free | grep Mem | awk '{print $4/$2 * 100.0}'","df -h --total | grep total | awk '{print $5+0}'"]
    commandKeys_list = ["CPU","Disk","Memory","Availablespace"]
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


def getDataFromInstance(hostIP,hostUser,keyFileName):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostIP,username=hostUser, key_filename=keyFileName)
    response_list = {}
    command_list = ["uname -a","uptime","free -m","ps -eo pcpu,pmem,pid,ppid,user,stat,args | sort -k 1 -r | head -6","df -PTh|egrep -iw \"ext4|ext3|xfs|gfs|gfs2|btrfs\"|grep -v \"loop\"|sort -k6n|awk '!seen[$1]++'",'users',' netstat -lntu | sed "1 d"']
    commandKeys_list = ["OS & Kernel Info","Uptime","Memory Usage","CPU Usage","Mount Disk usage","Logged in users","OpenPorts"]
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
        if iter in ["uname -a","uptime","df -PTh|egrep -iw \"ext4|ext3|xfs|gfs|gfs2|btrfs\"|grep -v \"loop\"|sort -k6n|awk '!seen[$1]++'"]:
            if iter == "uname -a":
                keys_list = [ "OS & Kernel Info" ]
            elif iter == "uptime":
                keys_list = [ "Uptime" ]
            else:
                keys_list = [ "Mount Disk usage" ]

        for line in data:
            #print(line)
            each_lineList = []
            each_lineDict = {}
            if line_iter == 0 and len(keys_list) == 0:
                line = line.decode("utf-8")
                for each_word in re.split("\s+",line):
                    each_lineList.append(each_word)
                    keys_list.append(each_word)
                    numberOfKey = numberOfKeys+1
                    # print(each_word)
            else:
                line = line.decode("utf-8").strip()
                word_iterator = 0
                keysLen = len(keys_list)
                prev_word = ""
                for each_word in re.split("\s+", line):
                    value_list.append(each_word)
                    if word_iterator >= keysLen - 1:
                        # each_lineDict[keys_list[word_iterator]] =
                        prev_word = prev_word + each_word + " "
                        each_word = prev_word
                        # word_iterator = word_iterator - 1
                    each_lineDict[keys_list[word_iterator if word_iterator < keysLen else keysLen-1]] = each_word
                    word_iterator = word_iterator + 1
            # response_list.append(each_lineDict)
            for key in each_lineDict:
                each_lineList.append(each_lineDict[key])
            line_iter = line_iter + 1
            final_list.append(each_lineList)

        response_list[commandKeys_list[commandsIter]] = final_list
        commandsIter = commandsIter + 1
    ssh.close()
    #print(json.dumps(response_list))

    value = json.dumps(response_list)
    return value

@app.route('/')
def hello():
    list = ["52.90.121.139"]
    openlist = []
    for li in list:
        a = healthdata(li,"ubuntu","danesh_keypair.pem")
        openlist.append(a)

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
    print(mem_list)
    print(disk)
    table_data = [[list[i], cpu_list[i], mem_list[i], disk[i]] for i in range(0, len(cpu_list))]
    return render_template("home.html",list=table_data)

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        ip = request.form['ip']
        print(ip)
        values = getDataFromInstance(ip,"ubuntu","danesh_keypair.pem")
        value = json.loads(values)
        print(value)
    return render_template("board.html",values=value, ip=ip)



if __name__ == '__main__':
    app.run(debug=True)
