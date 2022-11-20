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





        

if __name__ == '__main__':
    print(get_table())