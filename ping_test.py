import os
import sys
import threading

def ping_test(host_ip_num, src_nic):
    diconnect_pairs = []
    src_nic_ip = "192.168.%s.%s" % (host_ip_num, str(src_nic))
    for dst_net in range(1, 9):
        if((dst_net != 5) & (dst_net != host_ip_num)):
            for dst_nic in range(2, 10):
                dst_nic_ip = "192.168.%s.%s" % (str(dst_net), str(dst_nic))
                output = os.popen("ping -I %s %s -W 1 -c 1" % (src_nic_ip, dst_nic_ip), 'r', 1)
                rule = output.read().split('\n')
                if(len(rule) <= 6):
                    diconnect_pairs.append((src_nic_ip, dst_nic_ip))
    for pair in diconnect_pairs:
        print("from %s to %s has problem" % pair)

if __name__ == '__main__':
    argv = sys.argv[1:]
    if(len(argv) < 1):
        print("Please input the net_ip of the host")
        exit()

    thread_list = []
    for src_nic in range(2, 10):
        nic_thread = threading.Thread(target = ping_test, args = (argv[0], str(src_nic)))
        nic_thread.start()
        thread_list.append(nic_thread)
    
    for t in thread_list:
        t.join()
    