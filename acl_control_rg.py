import telnetlib
import time

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
    




def public_acl_rg(just_del):
    host_ip = '10.174.216.49'
    password = 'Oxc_2012'

    commands = []
    # name: route-map name
    # the policy number in a route-map
    # source ip
    # redirect ip
    # interface
    # acl_number
    acl_rules = [['vlan_10_acl', '10', '192.168.1.3', '172.167.5.1', 'vlan 10', '10']]

    commands.append('config')
    for rule in acl_rules:
        route_map_name = rule[0]
        route_rule_num = rule[1]
        source_ip = rule[2]
        redirect_ip = rule[3]
        interface = rule[4]
        acl_num = rule[5]
        commands.append("no access-list %s" % acl_num)
        commands.append("interface %s" % interface)
        commands.append("no ip policy route-map")
        commands.append("exit")
        commands.append("no route-map %s" % route_map_name)

        if(just_del == 0):
            commands.append("ip access-list standard %s" % acl_num)
            commands.append("permit %s 0.0.0.0" % source_ip)
            commands.append("exit")
            commands.append("route-map %s permit %s" %(route_map_name, route_rule_num))
            commands.append("match ip address %s" % acl_num)
            commands.append("set ip next-hop %s" % redirect_ip)
            commands.append("exit")
            commands.append("interface %s" % interface)
            commands.append("ip policy route-map %s" % route_map_name)
            commands.append("exit")
        
        
    commands.append('exit')
    commands.append('exit')

    telnet_client = TelnetClient()
    if telnet_client.login_host(host_ip, password):
        for cmd in commands:
            telnet_client.execute_some_command(cmd, interval=0.1)
    else:
        print('Failed to connect to switch')

    time.sleep(1)



if __name__ == "__main__":
    public_acl_rg(0)



