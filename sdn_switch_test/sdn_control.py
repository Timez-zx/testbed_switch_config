import os
import sys
import telnetlib
import time

class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()
    
    def login_host(self, host_ip, username, password, changepws):
        try:
            self.tn.open(host_ip, port=23)
        except:
            return False
        self.tn.read_until(b'Username:', timeout=10)
        self.tn.write(username.encode('ascii') +b'\n')
        self.tn.read_until(b'Password:', timeout=10)
        self.tn.write(password.encode('ascii') +b'\n')
        self.tn.read_until(b'The passord needs to be changed. Change now? [Y/N]:', timeout=10)
        self.tn.write(changepws.encode('ascii') +b'\n')
        time.sleep(2)
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            print('%sSuccess'%host_ip)
            return True
        else:
            print("Fail login")
            return False

    def execute_some_command(self, command, interval = 0.5):
        self.tn.write(command.encode('ascii')+b'\n')
        if(command == 'Y'):
            time.sleep(2)
        else:
            time.sleep(interval)
        command_result = self.tn.read_very_eager().decode('ascii')
        print("Result: \n%s" % command_result)

    def logout_host(self):
        self.tn.write(b"exit\n")


def acl_deploy(dele):
    basic_command = 'python3 /home/hw/tmp_share/hxc/exp_control-master/exp_control-master/switch_control/acl_hw.py '
    paras = [['10.174.216.35', '192.168.6.3', '100GE1/0/10', '172.166.14.1', '510'],
             ['10.174.216.48', '192.168.6.3', '100GE1/0/30', '172.166.16.2', '511'],  
             ['10.174.216.48', '192.168.6.3', '100GE1/0/31', '172.166.16.2', '512'],
             ['10.174.216.35', '192.168.6.3', '100GE1/0/64', '192.168.8.3', '513']]
    delete = ''
    if(dele):
        delete = '--onlydel True'
    for para in paras:
        switchIp = '--switchIp ' + para[0] + ' '
        source = '--source ' + para[1] + ' '
        inport = '--inport ' + para[2] + ' '
        outport = '--outport ' + para[3] + ' '
        aclId = '--aclId ' + para[4] + ' '
        command = basic_command + switchIp + source + inport + outport + aclId + delete
        # print(command)
        os.system(command)

def eth_trunk_leaf_hw():
    host_ip = '10.174.216.35'
    username = 'admin1234'
    password = 'Oxc_2012'
    command = []
    command.append('sy')
    command.append('clear configuration interface 100GE1/0/62')
    command.append('Y')
    command.append('clear configuration interface 100GE1/0/63')
    command.append('Y')
    command.append('commit')
    command.append('int eth-trunk 10')
    command.append('undo portswitch')
    command.append('ip address 172.166.14.2 24')
    command.append('trunkport 100GE1/0/62')
    command.append('q')
    command.append('commit')


    telnet_client = TelnetClient()
    if telnet_client.login_host(host_ip, username, password, 'N'):
        for cmd in command:
            telnet_client.execute_some_command(cmd, interval=0.2)
    else:
        print('Failed to connect to switch')

def eth_trunk_spine_hw():
    host_ip = '10.174.216.48'
    username = 'admin1234'
    password = 'Oxc_2012'
    command = []
    command.append('sy')
    command.append('clear configuration interface 100GE1/0/30')
    command.append('Y')
    command.append('clear configuration interface 100GE1/0/31')
    command.append('Y')
    command.append('commit')
    command.append('int eth-trunk 10')
    command.append('undo portswitch')
    command.append('ip address 172.166.14.1 24')
    command.append('trunkport 100GE1/0/30')
    command.append('q')
    command.append('commit')
    telnet_client = TelnetClient()
    if telnet_client.login_host(host_ip, username, password, 'N'):
        for cmd in command:
            telnet_client.execute_some_command(cmd, interval=0.2)
    else:
        print('Failed to connect to switch')


if __name__ == '__main__':
    eth_trunk_leaf_hw()
    eth_trunk_spine_hw()
    # acl_deploy(0)