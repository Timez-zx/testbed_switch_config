#!/usr/bin/python
#encoding: utf-8
 
import os
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
    p = os.popen('arp _gateway', 'r', 1)
    arp = p.read().split('\n\n')
    data =  [i for i in arp if i and not i.startswith('lo')]
    for mac_line in data:
        lines = mac_line.split('\n')
        mac = lines[1].split()[2]
    return mac
        


if __name__ == '__main__':
    ip_dic = getIfconfig()
    gatemac = get_gatemac()

    Source_ip = '192.168.1.3'
    Dst_ip = '192.168.6.8'

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