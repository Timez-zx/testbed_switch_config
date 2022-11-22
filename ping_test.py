import os

def ping_test(host_ip_num):
    diconnect_pairs = []
    for src_nic in range(2, 10):
        src_nic_ip = "192.168.%s.%s" % (host_ip_num, str(src_nic))
        for dst_net in range(1, 9):
            if((dst_net != 5) & (dst_net != host_ip_num)):
                for dst_nic in range(2, 10):
                    dst_nic_ip = "192.168.%s.%s" % (str(dst_net), str(dst_nic))
                    output = os.popen("ping -I %s %s -W 0.2 -c 1" % (src_nic_ip, dst_nic_ip), 'r', 1)
                    rule = output.read().split('\n')
                    if(len(rule) <= 6):
                        diconnect_pairs.append((src_nic_ip, dst_nic_ip))
    for pair in diconnect_pairs:
        print("from %s to %s has problem" % pair)
if __name__ == '__main__':
    ping_test()