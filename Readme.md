## The notes for some problems encountered when configuring the network
1. <font color=Crimson>net_os_detect</font> : the files under the directory are to test the status of the network and os in the cluster.   
    1. <font color=CornflowerBlue>ssh_node.py</font>: In order to start all the tests on differents to begin and then collect the information.(the other file are used by the nodes locally, by ssh_node.py, we ssh to different nodes and execute the local codes). 
    2. Why do we use the structure ?  
    **Because if we use the mode that sending the commands to other nodes and execute them, even if we can use multiple threads, but if we have to send and execute thousands of commands, we have only tens of cores, so the wise idea is to let most commands execute locally and there are one or several nodes to collect and filter the information (The distributed structure), so we can use all cores (from 200s to at most tens of seconds)**. 
2. <font color=Crimson>send_flow</font> : the files under the directory are used to send udp packet without the establishment of the connection.  
3. <font color=Crimson>switch_acl</font> : the files under the directory are used to configure the acl policies of the switches.  
    1. <font color=CornflowerBlue>acl_control_rg.py</font>: configure the acl policy, **when configuring the switch port, pay attention whether the port is at three-layer mode or two, there are two ways to configure acl for these to modes.(see 2)**. 
    2. **the next-hop is used for three layer mode, and the ip is the port of the next switch or host**. 
    3. <font color=CornflowerBlue>acl_control_hw.py</font>: similar to rg, and needed to be updated.
4.  <font color=Crimson>switch_bgp</font>: Configure the port to three-layer mode and assign ip for port because bgp only function for three-layer mode port.  
5.  <font color=Crimson>Other problem</font>:  
    1. How to configure the static route?  
    **man netplan: route is to make sure how to route in a table and route-policy is to map the ip and device to the table**
    2. How to start a process when reboot?  
    **Config the systemd.service, to be specific, see the process in the os_config (systemd_start.txt)** 