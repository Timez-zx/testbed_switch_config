#!/usr/bin/python
#encoding: utf-8
 
import os
import sys
from scapy.all import *

def getIfconfig():
    p = os.popen('ifconfig', 'r', 1)
    ifconfig = p.read().split('\n\n')
    data =  [i for i in ifconfig if i and not i.startswith('lo')]
    dic = {}
    for devs in data:
        lines = devs.split('\n')
        devname = lines[0].split(':')[0]
        if(devname[0] != 'e'):
            continue
        macaddr = lines[3].split()[1]
        ipaddr  = lines[1].split()[1]
        dic[ipaddr] = [devname, macaddr]
    return dic

def pack_callback(packet):
    print (packet.show())

if __name__ == '__main__':
    argv = sys.argv[1:]
    if(len(argv) < 1):
        print("Please input the ip we want to monitor")
        exit()
    ip_dic = getIfconfig()

    ip = argv[0]
    interface = ip_dic[ip][0]
    filterstr="udp"
    sniff(filter=filterstr,prn=pack_callback, iface=interface, count=0)

