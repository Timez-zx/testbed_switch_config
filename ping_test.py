import os

def ping_test():
    for i in range(64*64):
        p = os.popen('ping 169.254.100.100 -W 0.1 -i 0.01 -c 1', 'r', 1)
        rule = p.read().split('\n')
    # print(rule)

if __name__ == '__main__':
    ping_test()