import os
from libpy.public import kernel

def arp_cmd_add(ip , mac ):
    #cmd = 'arp -s ' + ip + " " + mac + " "
    cmd = 'arp -s %s %s 1>/dev/null 2>/dev/null ' % (ip, mac)
    #print("cmd: %s"%cmd)
    if(kernel.k.ray_system(cmd)):
         return 1
    return 0

def arp_cmd_del(ip = ''):
    cmd = 'arp -d %s 1>/dev/null 2>/dev/null ' %(ip)
    #print('cmd:%s' % cmd)
    if(kernel.k.ray_system(cmd)):
         return 1
    return 0

    

class arp:
    def add(self, ip = '', mac = ''):
        #print 'mac %s' % mac
        #print 'ip %s '% ip 
        return arp_cmd_add(ip, mac)
    def delete(self, ip = ''):
        return arp_cmd_del(ip)

Karp = arp()
