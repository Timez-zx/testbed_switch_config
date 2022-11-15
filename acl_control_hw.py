import time

def public_acl_small_clos():
    host_ip = '192.168.1.18'
    username = 'admin123'
    passward = 'Oct_2012'
    changepwd = 'N'


    commands = []

    commit = 'commit'
    quit = 'q'
    sy = "system-view"
    admin = 'admin'
    port_mode = "port-mode port"
    confirm = 'y'

    vs_num = 12
    port_per_vs = 8
    port_per_slot = 24
    id_for_100g = {}


    acl_to_publish = {}
    acl_to_publish["vs1"] = [("192.168.81.10", None, "192.168.115.3", "110"), ("192.168.81.11", None, "192.168.116.3", "111")]
    acl_to_publish["vs2"] = [("192.168.82.10", None, "192.168.125.3", "210"), ("192.168.82.11", None, "192.168.126.3", "211"), ("192.168.82.12", None, "192.168.127.3", "212"), ("192.168.82.13", None, "192.168.128.3", "213")]
    acl_to_publish["vs4"] = [("192.168.84.14", None, "192.168.137.3", "414"), ("192.168.84.15", None, "192.168.138.3", "415")]

    for vs_name in acl_to_publish.keys():
        commands.append("switch virtual-system %s" % vs_name)
        commands.append(sy)

        for entry in acl_to_publish[vs_name]:
            mark = entry[-1]
            src_ip = entry[0]
            dst_ip = entry[1]
            interface = entry[2]

            commands.append("undo traffic-policy p%s global inbound" % mark)
            commands.append(commit)

            commands.append("undo traffic policy p%s" % mark)
            commands.append(commit)

            commands.append("undo traffic behavior b%s" % mark)
            commands.append(commit)

            commands.append("undo traffic classifier c%s" % mark)
            commands.append(commit)

            commands.append("undo acl 3%s" % mark)
            commands.append(commit)


            commands.append("acl number 3%s" % mark)
            cmd = "rule permit ip "
            if(src_ip != None):
                cmd += ("source %s 0 " % src_ip)
            if(dst_ip != None):
                cmd += ("destnation %s 0 " % dst_ip)
            commands.append(cmd)
            commands.append(commit)
            commands.append(quit)

            commands.append("traffic classifier c%s" % mark)
            commands.append("if-match acl 3%s" % mark)
            commands.append(commit)
            commands.append(quit)

            commands.append("traffic behavior b%s " % mark)
            commands.append("redirect remote %s" % interface)
            commands.append(commit)
            commands.append(quit)

            commands.append("traffic policy p%s " % mark)
            commands.append("classifier c%s behavior b%s" % (mark, mark))
            commands.append(commit)
            commands.append(quit)

            commands.append("traffic-policy p%s global inbound" % mark)
            commands.append(commit)
        commands.append(quit)
        commands.append(quit)

    for cmd in commands:
        print(cmd)
    time.sleep(3)


if __name__ == "__main__":
    public_acl_small_clos()



