import os
import sys
from ray_network.kernel.netray_type import RAY_DEBUG,ray_append,ray_int,ray_str
from ray_network.kernel.netray_ip import get_ver_from_str, str_2trueip
from libpy.public import kernel

try:
    from libpy.public.ray_vpp import rayvpp 
except:
    pass 

def webray_network_route_kcli_add(ip, gateway='', metric=0, ifname=''):

    version = get_ver_from_str(ip)
    
    
    if(version == 4):
        ver = '-4'
        op = ip.split('/')
        if op[1] == "32":
            host = ' -host '
        else :
            host = " -net "
    else:
        ver = '-6'
        host = ' '
    
    cmd = 'route ' + ver + ' add ' + host + ip 
    if(gateway):
        cmd = cmd + ' gw ' + gateway
    if(ray_int(metric)):
        cmd = cmd + " metric " + str(metric)
    if(ray_str(ifname)):
        cmd = cmd +" " +  ray_str(ifname)
    cmd = cmd + " 1>/dev/null 2>/dev/null"
    #print(cmd)
    ret = kernel.k.ray_system(cmd)
    if ret:
        return False
    return True


def webray_network_route_kcli_del(ip,  gateway='', metric=0, ifname=''):
    #print("cli gw:%s"%gateway)
    version = get_ver_from_str(ip)
    if(version == 4):
        ver = '-4'
        op = ip.split('/')
        if op[1] == "32":
            host = ' -host '
        else :
            host = " -net "
    else:
        ver = '-6'
        host = ' '
    
    cmd = 'route ' + ver + ' del ' + host + ip 

    if(gateway):
        cmd = cmd + ' gw ' + gateway
    if(ray_int(metric)):
        cmd = cmd + " metric " + str(metric)
    if(ray_str(ifname)):
        cmd = cmd + " " + ray_str(ifname)
    cmd = cmd + " 1>/dev/null 2>/dev/null"
    #print(cmd)
    ret = kernel.k.ray_system(cmd)
    if ret:
        return False
    return True 


def webray_network_route_kcli_query(ip, gateway='', metric=0, ifname=''):
    ipver = get_ver_from_str(ip)
    if ipver == 4 : 
        cmd = ' route -n '
        res = kernel.k.ray_popen(cmd)
        data = res
        lines = data.split('\n')
        lines = lines[1:]
        for line in lines :
       
            values = line.split()
            if len(values) != 8:
                continue 
       
            if (values[0] == ip and values[1] == gateway and values[4] == str(metric)) :
                return values[7]
    else :
        cmd = ' route -6 -n '
        res = kernel.k.ray_popen(cmd)
        data = res
        lines = data.split('\n')
        lines = lines[1:]
        for line in lines :
       
            values = line.split()
            if len(values) != 7 :
                continue 
       
            if (values[0] == ip and values[1] == gateway and values[3] == str(metric)) :
                return values[6]
        

    return ''


def vpp_network_route_kcli_add(ip, gateway = "", weight=1, ifname = ''):
    cmd = "ip route %s via %s %s weight %d"%(ip, gateway, ifname, weight)
    rayvpp.connect("route_add")
    ret ,msg =  rayvpp.system(cmd)
    rayvpp.close()
    if not ret :
        print(msg)
    return ret 

def vpp_network_route_kcli_del(ip, gateway = "", weight=1, ifname = ''):
    cmd = "ip route del %s via %s %s weight %d"%(ip, gateway, ifname, weight)
    rayvpp.connect("route_del")
    ret ,msg =  rayvpp.system(cmd)
    rayvpp.close()
    if not ret :
        print(msg)
    return ret 

def vpp_network_route_kcli_query():
    pass 

class route():
    def route_add(self, ip,  gateway='', metric=0, ifname=''):
        return webray_network_route_kcli_add(ip, gateway, metric, ifname)
    def route_del(self, ip , gateway='', metric=0, ifname=''):
        return webray_network_route_kcli_del(ip, gateway, metric, ifname)
    def route_query(self, ip, gateway='', metric=0, ifname = ''):
        return webray_network_route_kcli_query( ip, gateway, metric, ifname)

    def vpp_route_add(self, ip, gateway='', weight=1, ifname=''):
        return vpp_network_route_kcli_add(ip = ip, gateway=gateway, weight=weight, ifname=ifname)
    def vpp_route_del(self, ip, gateway='', weight=1, ifname=''):
        return vpp_network_route_kcli_del(ip = ip, gateway=gateway, weight=weight, ifname=ifname)

Kroute = route()
###############################################################
if(__name__ == "__main__"):
    ip = '192.168.129.8'
    mask = '255.255.255.255'
    gw = '192.168.129.2'
    metric = 5
    ifname = 'eth0'

    if( webray_network_route_kcli_add(ip, mask, ifname=ifname) ):
        print("good")
    else:
        print("bad")



    
