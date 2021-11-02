#coding=utf-8
import os
from ray_network.kernel.netray_type import RAY_DEBUG,ray_append,ray_int,ray_str
from libpy.public import kernel

PORTMAX = 64


def webray_network_port_kcli_set_status_byname(physical_name, enable):
    if enable:
        uw = ' up '
    else:
        uw = ' down '
    cmd = 'ifconfig ' + ray_str(physical_name) + ' ' +  ray_str(uw) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        print('webray_network_port_kcli_set_status_byname error')
        return False
    return True
    
    
    
def webray_get_mac(phy, mac=[]):
    cmd = 'ifconfig ' + ray_str(phy) +  " | grep ether | awk '{print $2}'"
    text = kernel.k.ray_popen(cmd)

    
    try:
        mac.append(text)
    except:
        print("type of parameter mac is error")
        
    return ray_str(text.replace('\n',''))
    
    
def webray_get_link_status(physical_name):
    try:
        physical_name = ray_str(physical_name)
    except:
        return False
        
    cmd = 'ethtool ' + ray_str(physical_name) +  " |grep detected |awk '{print $3}'"
    text = kernel.k.ray_popen(cmd)

    if ray_str(text.replace('\n','')) == 'yes':
        return 1
    else:
        return 0
        
def ray_get_mtu(physical_name):
    try:
        physical_name = ray_str(physical_name)
    except:
        return False
        
    cmd = 'ifconfig ' + ray_str(physical_name) +  " |grep mtu | awk '{print $4}'"
    text = kernel.k.ray_popen(cmd)

    return ray_int(text)
        
def ray_map(phyname,logname):
    try:
        physical_name = ray_str(phyname)
        logname = ray_str(logname)
    except:
        return False
        
    cmd = '/RayOS/utils/portmap ' + ray_str(physical_name) + " " + ray_str(logname)
    ret = kernel.k.ray_system(cmd)
    if ret:
        return False
    else:
        return True

##############vpp modules##############
    
def webray_network_vpp_port_kcli_set_status_byname(physical_name, enable):
    if enable:
        uw = ' up '
    else:
        uw = ' down '
    cmd = 'vppctl set interface state ' + ray_str(physical_name) + ' ' +  ray_str(uw) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        print('webray_network_vpp_port_kcli_set_status_byname error')
        return False
    return True   
    

def webray_get_vpp_mac(phy, mac=[]):
    cmd = 'vppctl show hardware-interface ' + ray_str(phy) + " | grep 'Ethernet address' | awk '{print $3}' "
    text = kernel.k.ray_popen(cmd)

    
    try:
        mac.append(text)
    except:
        print("type of parameter mac is error")
        
    return ray_str(text.replace('\n',''))


def webray_get_vpp_link_status(physical_name):
    try:
        physical_name = ray_str(physical_name)
    except:
        return False
        
    cmd = 'vppctl show hardware-interfaces ' + ray_str(physical_name) +  " |grep " + ray_str(physical_name) + " |awk '{print $3}'"
    text = kernel.k.ray_popen(cmd)

    if ray_str(text.replace('\n','')) == 'up':
        return 1
    else:
        return 0
        
def ray_get_vpp_mtu(physical_name):
    try:
        physical_name = ray_str(physical_name)
    except:
        return False
        
    cmd = 'vppctl show hardware-interface ' + ray_str(physical_name) +  " |grep mtu |awk '{print $6}'"
    text = kernel.k.ray_popen(cmd)

    return ray_int(text)

class port():
    def port_set_status_byname(self,physical_name, enable):
        return  webray_network_port_kcli_set_status_byname(physical_name, enable)
        
    def get_link_status(self,physical_name):
        return webray_get_link_status(physical_name)
        
    def get_mac(self,physical_name):
        return webray_get_mac(physical_name)
    
    def get_mtu(self,physical_name):
        return ray_get_mtu(physical_name)
    
    def map(self,phyname,logname):
        return ray_map(phyname,logname)
    
    def vpp_port_set_status_byname(self,physical_name, enable):
        return  webray_network_vpp_port_kcli_set_status_byname(physical_name, enable)

    def get_vpp_link_status(self,physical_name):
        return webray_get_vpp_link_status(physical_name)

    def get_vpp_mac(self,physical_name):
        return webray_get_vpp_mac(physical_name)

    def get_vpp_mtu(self,physical_name):
        return ray_get_vpp_mtu(physical_name)
        
Kport = port()