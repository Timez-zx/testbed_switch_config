import os
import sys

def get_table():
    p = os.popen('ip rule', 'r', 1)
    rule = p.read().split('\n')
    data =  [i for i in rule if i and not i.startswith('lo')]
    table = []
    for line in data:
        num = line.split()[-1]
        if(num not in table):
            if(num[0] == '4'):
                table.append(num)
         
    return table
        

if __name__ == '__main__':
    get_table()