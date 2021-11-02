#coding=utf-8
import os
import struct,socket
from ray_network.kernel.netray_type import RAY_DEBUG,ray_append,ray_int,ray_str
from ray_network.kernel.netray_type import ERROR_DEBUGINFO,OUT_DEBUG_INFO
from ray_network.kernel.netray_ip import get_ver_from_str,pm_2str,ip_str_2dict,mask_2num
from libpy.public import kernel

PORTMAX = 64
'''
def ip_to_hex(ip):
    ip_num = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip)))[0])
    aa = hex(ip_num)[2:]
    return aa[::-1]
'''

def ip_to_hex(available_id):
    ip_key = "L%03d"%available_id
    return ip_key
    
def ray_network_trunk_kcli_add_byname(trunkname, idx):
    cmd = "vconfig add " + str(trunkname) + ' ' + str(idx) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_network_trunk_kcli_add_byname error')
        return False
    return True
    
    
def ray_network_trunk_kcli_remove_byname(trunkname):
    cmd = "vconfig rem " + str(trunkname) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_network_trunk_kcli_remove_byname error')
        return False
    return True
    
    
def ray_trunk_kcli_set_status(trunkname, enable):
    uw = 'up'
    if enable:
        uw = 'up'
    else:
        uw = 'down'
    cmd = 'ifconfig '+ str(trunkname) + ' ' + str(uw) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_trunk_kcli_set_status error')
        return False
    return True
    
def ray_trunk_add_if(trunkname, if_name):
    cmd = 'brctl addif ' + ray_str(trunkname) + ' ' + ray_str(if_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_trunk_add_if error !')
        return False
    return True
    
def ray_trunk_remove_if(trunkname, if_name):
    cmd = 'brctl delif ' + ray_str(trunkname) + ' ' + ray_str(if_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_trunk_remove_if error !')
        return False
    return True
    
    
def ray_trunk_add_ip(trunkname, ip_mask, reload, available_id):#ip_mask: *.*.*.*/*
    if get_ver_from_str(ip_mask) != 4 and get_ver_from_str(ip_mask) != 6:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_trunk_add_ip: ipver error!')
        return False
        
    # if get_ver_from_str(ip_mask) == 4:
    #     ip = pm_2str(ip_str_2dict(ip_mask, 0), None, 4 ,1)
    #     mask = pm_2str(ip_str_2dict(ip_mask, 1), None, 4 ,1)
    #     cmd = 'ifconfig ' + ray_str(trunkname) + ':' + str(ip_to_hex(available_id)) + ' ' + ip  + ' netmask  ' + mask + ' up' + " 1>/dev/null 2>/dev/null"
    # else:
    #     cmd = 'ifconfig ' + ray_str(trunkname) + ' inet6 add ' + ray_str(ip_mask) + ' up' + " 1>/dev/null 2>/dev/null"
    
    cmd = "ip addr add %s dev %s 1>/dev/null 2>/dev/null "%(ip_mask, ray_str(trunkname))

    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_trunk_add_ip: add ' + ray_str(ip_mask) + ' error!!')
        return False
    return True
        
        
def ray_trunk_remove_ip(trunkname, ip_mask, reload, available_id):
    if get_ver_from_str(ip_mask) != 4 and get_ver_from_str(ip_mask) != 6:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_trunk_remove_ip: ipver error!')
        return False
        
    # if get_ver_from_str(ip_mask) == 4:
    #     ip = pm_2str(ip_str_2dict(ip_mask, 0), None, 4 ,1)
    #     cmd = 'ifconfig ' + ray_str(trunkname) + ':' + str(ip_to_hex(available_id)) + ' ' + ip + ' down' + " 1>/dev/null 2>/dev/null"
    # else:
    #     cmd = 'ifconfig ' + ray_str(trunkname) + ' inet6 del ' + ray_str(ip_mask) + " 1>/dev/null 2>/dev/null"
    cmd = "ip addr del %s dev %s 1>/dev/null 2>/dev/null "%( ray_str(ip_mask), ray_str(trunkname))
        
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'ray_trunk_remove_ip: remove ' + ray_str(ip_mask) + ' error!!')
        return False
    return True
    
def webray_trunk_bridge_kcli_add_byname(bri_name):
    cmd = 'brctl addbr ' +  ray_str(bri_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        #cmd = 'brctl delbr ' +  ray_str(bri_name) + " 1>/dev/null 2>/dev/null"
        RAY_DEBUG(ERROR_DEBUGINFO, 'bridge name '+ ray_str(bri_name) + ' add error !')
        return False
    cmd = 'brctl setfd ' + ray_str(bri_name) + ' 1' + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'bridge name '+ ray_str(bri_name) + 'error !')
        return False
    cmd = 'ifconfig ' + ray_str(bri_name) + ' up' + " 1>/dev/null 2>/dev/null"
    kernel.k.ray_system(cmd)
    return True
    
    
def webray_trunk_bridge_kcli_remove_byname(bri_name):
    cmd = 'ifconfig ' +  ray_str(bri_name) + ' down ' + " 1>/dev/null 2>/dev/null"
    kernel.k.ray_system(cmd)
    cmd = 'brctl delbr ' +  ray_str(bri_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(ERROR_DEBUGINFO, 'bridge name '+ bri_name + 'del  error !')
        return False
    return True
    
    
class trunk():
    def add(self,trunkname, idx):
        return ray_network_trunk_kcli_add_byname(trunkname, idx)
        
    def dele(self,trunkname):
        return ray_network_trunk_kcli_remove_byname(trunkname)
        
    def addbr(self, brname):
        return webray_trunk_bridge_kcli_add_byname(brname)
        
    def delbr(self, brname):
        return webray_trunk_bridge_kcli_remove_byname(brname)
        
    def set_status_byname(self,trunkname, enable):
        return  ray_trunk_kcli_set_status(trunkname, enable)
        
    def add_ip(self, trunkname, ip_mask, reload, available_id):
        return ray_trunk_add_ip(trunkname, ip_mask, reload, available_id)
        
    def del_ip(self, trunkname, ip_mask, reload, available_id):
        return ray_trunk_remove_ip(trunkname, ip_mask, reload, available_id)
        
    def add_if(self, trunkname, if_name):
        return ray_trunk_add_if(trunkname, if_name)
        
    def remove_if(self, trunkname, if_name):
        return ray_trunk_remove_if(trunkname, if_name)
'''
    def set_mac_mtu(self, bri_name, mtu, mac = None):
        return ray_bridge_set_mac_mtu(bri_name, mtu, mac)
        
    def get_link_status(self,bri_name):
        return webray_get_link_status(bri_name)
        
    def get_mac(self,bri_name):
        return ray_bridge_get_mac(bri_name)
    
    def get_mtu(self,bri_name):
        return ray_get_mtu(bri_name)
    
    def map(self,phyname,logname):
        return ray_map(phyname,logname)
'''
Ktrunk = trunk()