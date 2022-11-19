import paramiko

def ssh_connect(ip, passwd):
    ssh = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(policy)
    ssh.connect(
        hostname = ip, 
        port = 22,
        username = "root", 
        password = passwd
    )
    stdin,stdout,stderr = ssh.exec_command("python3 /home/hw/tmp_share/switch-control/rg/ip_route_search.py")
    result = stdout.read().decode()
    print(ip, result)

if __name__ == '__main__':
    passwd = "Huawei12#$"
    ip_list = ["10.174.216.254", "10.174.216.255", "10.174.217.0", "10.174.217.2", 
               "10.174.217.3", "10.174.217.4", "10.174.217.5"]
    for ip in ip_list:
        ssh_connect(ip, passwd)
