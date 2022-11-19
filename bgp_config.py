import telnetlib
import time

host_ip = '10.174.216.49'
password = 'Oxc_2012'

class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()
    
    def login_host(self, host_ip, password):
        try:
            self.tn.open(host_ip, port=23)
            print("%s access success"%host_ip)
        except:
            print("%s access failure"%host_ip)
            return False

        self.tn.read_until(b'Password:', timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        time.sleep(1)
        self.tn.write('enable'.encode('ascii') + b'\n')
        time.sleep(0.5)
        self.tn.read_until(b'Password:', timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        return True

    def execute_some_command(self, command, interval=0.5):
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(interval)
        command_result = self.tn.read_very_eager().decode('ascii')
        print('Result:\n%s', command_result)


def del_vlan_list():   
    commands = []
    vlan_list = []
    for i in range(51, 64):
        vlan_list.append(i)
    commands.append('config')
    for vlan_num in vlan_list:
        commands.append("no interface vlan %s" % str(vlan_num))
        commands.append("no vlan %s" % str(vlan_num))

    commands.append('show vlan')
    commands.append('exit')
    commands.append('exit')
    telnet_client = TelnetClient()
    if telnet_client.login_host(host_ip, password):
        for cmd in commands:
            telnet_client.execute_some_command(cmd, interval=0.5)
    else:
        print('Failed to connect to switch')

def ip_config():   
    commands = []
    port_list = []
    ip_list = []
    for i in range(50, 65):
        port_list.append(i)
    for i in range(2, 17):
        ip_list.append(i)
    commands.append('config')
    for port_num in range(len(port_list)):
        commands.append("interface Hu0/%s" % port_list[port_num])
        commands.append("no switchport")
        commands.append("ip address 172.167.%s.2 255.255.255.0" % ip_list[port_num])
        commands.append("show this")
        commands.append("exit")

    commands.append('exit')
    commands.append('exit')

    telnet_client = TelnetClient()
    if telnet_client.login_host(host_ip, password):
        for cmd in commands:
            telnet_client.execute_some_command(cmd, interval=0.5)
    else:
        print('Failed to connect to switch')

if __name__ == "__main__":
    ip_config()



        




