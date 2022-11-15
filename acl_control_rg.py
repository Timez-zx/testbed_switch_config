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
    




def public_acl_rg():
    host_ip = '10.174.216.49'
    password = 'Oxc_2012'

    commands = []

    # node6 --- host0  192.168.1.3~9
    ip_dic0 = {'192.168.1.2':'ens12f0', '192.168.1.3':'ens12f1', '192.168.1.4':'ens11f0', '192.168.1.5':'ens11f1',
             '192.168.1.6':'ens10f0', '192.168.1.7':'ens10f1', '192.168.1.8':'enp41s0f0', '192.168.1.9':'enp41s0f1'}
    # node7 --- host1  192.168.2.3~9
    ip_dic1 = {'192.168.2.2':'ens12f0', '192.168.2.3':'ens12f1', '192.168.2.4':'ens11f0', '192.168.2.5':'ens11f1',
             '192.168.2.6':'ens10f0', '192.168.2.7':'ens10f1', '192.168.2.8':'enp41s0f0', '192.168.2.9':'enp41s0f1'}
    # node5 --- host2  192.168.3.3~9
    ip_dic2 = {'192.168.3.2':'ens12f0', '192.168.3.3':'ens12f1', '192.168.3.4':'ens11f0', '192.168.3.5':'ens11f1',
             '192.168.3.6':'ens10f0', '192.168.3.7':'ens10f1', '192.168.3.8':'enp41s0f0', '192.168.3.9':'enp41s0f1'}
    # node0 --- host3  192.168.4.3~9
    ip_dic3 = {'192.168.4.2':'ens12f0', '192.168.4.3':'ens12f1', '192.168.4.4':'ens11f0', '192.168.4.5':'ens11f1',
             '192.168.4.6':'ens10f0', '192.168.4.7':'ens10f1', '192.168.4.8':'enp41s0f0', '192.168.4.9':'enp41s0f1'}
    # node6 --- host0  192.168.1.3~9
    host0 = {'ens12f0': 'Hu0/1', 'ens12f1': 'Hu0/37', 'ens11f0': 'Hu0/3', 'ens11f1': 'Hu0/4',
             'ens10f0': 'Hu0/5', 'ens10f1': 'Hu0/6', 'enp41s0f0': 'Hu0/34', 'enp41s0f1': 'Hu0/8'}
    # node7 --- host1  192.168.2.3~9
    host1 = {'ens12f0': 'Hu0/9', 'ens12f1': 'Hu0/10', 'ens11f0': 'Hu0/36', 'ens11f1': 'Hu0/42',
             'ens10f0': 'Hu0/13', 'ens10f1': 'Hu0/14', 'enp41s0f0': 'Hu0/15', 'enp41s0f1': 'Hu0/16'}
    # node5 --- host2  192.168.3.3~9
    host2 = {'ens12f0': 'Hu0/17', 'ens12f1': 'Hu0/18', 'ens11f0': 'Hu0/19', 'ens11f1': 'Hu0/35',
             'ens10f0': 'Hu0/21', 'ens10f1': 'Hu0/22', 'enp41s0f0': 'Hu0/23', 'enp41s0f1': 'Hu0/24'}
    # node0 --- host3  192.168.4.3~9
    host3 = {'ens12f0': 'Hu0/25', 'ens12f1': 'Hu0/26', 'ens11f0': 'Hu0/27', 'ens11f1': 'Hu0/28',
             'ens10f0': 'Hu0/29', 'ens10f1': 'Hu0/39', 'enp41s0f0': 'Hu0/40', 'enp41s0f1': 'Hu0/32'}

    out_port = {}
    for i in range(49, 65):
        out_port[i] = 'Hu0/' + str(i)

    host_port = [host0, host1, host2, host3]
    ip_dict = [ip_dic0, ip_dic1, ip_dic2, ip_dic3]
    # [index_number, src_ip, next_port, table_label]
    # index_number: machine number, if 0, index the information in first machie in the host_port and ip_dict
    # table_label:  rg switch's label is different from hw, standard table label is 1-99, 1300-1999 extended is larger than 99
    acl_rules = [[0, '192.168.1.3', 61, '10']]

    commands.append('config')
    for rule in acl_rules:
        host_index = rule[0]

        src_ip = rule[1]
        dst_port = rule[2]
        table_label = rule[3]

        commands.append("no ip access-list standard %s" % table_label)
        commands.append("ip access-list standard %s" % table_label)
        commands.append("permit %s %s" % (src_ip, '255.255.255.255'))
        commands.append("exit")
        commands.append('show access-lists')

        input_interface = host_port[host_index][ip_dict[host_index][src_ip]]
        output_interface = out_port[dst_port]
        commands.append("interface %s" % input_interface)
        commands.append("no redirect destination interface %s acl %s in" % (output_interface, table_label))
        commands.append("redirect destination interface %s acl %s in" % (output_interface, table_label))
        commands.append('exit')
        commands.append('show redirect interface %s' % input_interface)

        
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
    public_acl_rg()



