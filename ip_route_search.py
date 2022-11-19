import os
import sys

def get_table():
    p = os.popen('ip rule', 'r', 1)
    rule = p.read().split('\n')
    data =  [i for i in rule if i and not i.startswith('lo')]
    table = {}
    for line in data:
        num = line.split()[-1]

        ip = line.split()[-3]
        if(num not in table):
            if((num[0] == '4') & (ip[0] == '1') ):
                table[num] = ip 
    return table

def find_rout_loss(table):
    lost_ip = []
    for key in table.keys():
        p = os.popen("ip route list table %s" % key, 'r', 1)
        rule = p.read().split('\n')
        if(len(rule) == 1):
            lost_ip.append(table[key])
            continue
    
    print("IP who lost table")
    for ip in lost_ip:
        print(ip)
        




        

if __name__ == '__main__':
    find_rout_loss(get_table())