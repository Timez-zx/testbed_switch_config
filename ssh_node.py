import paramiko
#实例化ssh客户端

def ssh_connect(ip, passwd):
    ssh = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(policy)
    ssh.connect(
        hostname = ip, #服务器的ip
        port = 22, #服务器的端口
        username = "root", #服务器的用户名
        password = passwd #用户名对应的密码
    )
#远程执行命令
    stdin,stdout,stderr = ssh.exec_command("python3 /home/hw/tmp_share/switch-control/rg/ip_route_search.py")


# 按字节返回结果
    result = stdout.read().decode()
    print(result)

# 按行返回结果
    for i in stdout.readlines():
	    print(i)

if __name__ == '__main__':
    passwd = "Huawei12#$"
    ip_list = ["10.174.216.254", "10.174.216.255", "10.174.217.0", "10.174.217.2", 
               "10.174.217.3", "10.174.217.4", "10.174.217.5"]
    ssh_connect(ip_list[0], passwd)
