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

def get_gatemac():
    p = os.popen('arp', 'r', 1)
    arp = p.read().split('\n')
    data =  [i for i in arp if i and not i.startswith('lo')]
    for mac_line in data:
        mac_list = mac_line.split()
        if((mac_list[0] == '_gateway') & (mac_list[-1] != 'eno1')):
            mac = mac_list[2]
            break
    return mac
        


if __name__ == '__main__':
    argv = sys.argv[1:]
    if(len(argv) < 2):
        print("Please input the src and dst ip")
        exit()
    ip_dic = getIfconfig()
    gatemac = get_gatemac()

    Source_ip = argv[0]
    Dst_ip = argv[1]

    interface = ip_dic[Source_ip][0]
    mac = ip_dic[Source_ip][1]

    packet_list = []
    appendix = '0'
    for i in range(1000):
        appendix = appendix + '0'
    for i in range(10000):
        packet = Ether(src=mac, dst=gatemac)/IP(src=Source_ip, dst=Dst_ip)/UDP()/(str(i)+appendix)
        packet_list.append(packet)
    sendpfast(packet_list, iface=interface, mbps = 100000, loop = 100)