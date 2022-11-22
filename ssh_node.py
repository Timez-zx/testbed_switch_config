import paramiko
import threading
def ssh_connect(ip, passwd, ip_net):
    ssh = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(policy)
    ssh.connect(
        hostname = ip, 
        port = 22,
        username = "root", 
        password = passwd
    )
    stdin,stdout,stderr = ssh.exec_command("python3 /home/hw/tmp_share/switch-control/rg/ping_test.py %s" % ip_net)
    result = stdout.read().decode()
    print(ip)
    print(result)

if __name__ == '__main__':
    passwd = "Huawei12#$"
    ip_list = ["10.174.216.254", "10.174.216.255", "10.174.217.0", "10.174.217.2", 
               "10.174.217.3", "10.174.217.4", "10.174.217.5"]
    net_list = ['1', '2', '4', '7', '6', '8', '3']
    thread_list = []
    for ip_index in range(len(ip_list)):
        ssh_ip_thread = threading.Thread(target = ssh_connect, args = (ip_list[ip_index], passwd, net_list[ip_index]))
        ssh_ip_thread.start()
        thread_list.append(ssh_ip_thread)
    for t in thread_list:
        t.join()
