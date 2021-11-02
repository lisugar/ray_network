#coding=utf-8
import os
from ray_network.kernel.netray_type import RAY_DEBUG,ray_append,ray_int,ray_str
from libpy.public import kernel
PORTMAX = 64

    
def ray_channel_kcli_mode(mode):
    cmd =  'echo ' + str() + ' > channel.conf' + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'channel set mode error !')
        return False
    return True
    
def ray_channel_set_status_byname(channel_name, enable):
    if enable:
        uw = ' up '
    else:
        uw = ' down '
    cmd = 'ifconfig ' + ray_str(channel_name) + ' ' +  ray_str(uw) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_set_status_byname error')
        return False
    return True
    
    
def ray_channel_add_port(channel_name, port_name):
    cmd = 'ifenslave ' + ray_str(channel_name) + ' ' + ray_str(port_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_add_port error !')
        return False
    return True
    
def ray_channel_del_port(channel_name, port_name):
    cmd = 'ifenslave -d ' + ray_str(channel_name) + ' ' + ray_str(port_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_del_port error !')
        return False
    return True
    
    
def get_max_bond_id():
    for id in range(0,16):
        cmd = 'ifconfig |grep bond' + str(id) + " 1>/dev/null 2>/dev/null"
        cmd1 = 'ifconfig -a |grep bond' + str(id) + " 1>/dev/null 2>/dev/null"
        ret = kernel.k.ray_system(cmd)
        ret1 = kernel.k.ray_system(cmd1)
        if ret and not ret1:
            return id
    return None
        
        
def check_bond(name):
    #cmd = 'ifconfig |grep ' + str(name) + " 1>/dev/null 2>/dev/null"
    cmd1 = 'ifconfig -a |grep ' + str(name) + " 1>/dev/null 2>/dev/null"
    #ret = kernel.k.ray_system(cmd)
    ret1 = kernel.k.ray_system(cmd1)
    if not ret1:
        return True
    else:
        return False
        

###################vpp modules#############
def ray_vpp_channel_kcli_mode(mode):
    cmd =  'echo ' + str() + ' > channel.conf' + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'channel set mode error !')
        return False
    return True
    
def ray_vpp_channel_set_status_byname(channel_name, enable):
    if enable:
        uw = ' up '
    else:
        uw = ' down '
    cmd = 'vppctl set interface state ' + ray_str(channel_name) + ' ' +  ray_str(uw) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_set_status_byname error')
        return False
    return True


def ray_vpp_channel_create(id):
    cmd = 'vppctl create bond mode round-robin id ' + ray_str(id) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_set_status_byname error')
        return False
    cmd = 'vppctl set interface state BondEthernet' + ray_str(id) + " up" + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_set_status_byname error')
        return False
    return True


def ray_vpp_channel_delete(physical_name):
    cmd = 'vppctl delete bond ' + ray_str(physical_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_set_status_byname error')
        return False
    return True
    
    
def ray_vpp_channel_add_port(channel_name, port_name):
    cmd = 'vppctl bond add ' + ray_str(channel_name) + ' ' + ray_str(port_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_add_port error !')
        return False
    return True
    
def ray_vpp_channel_del_port(channel_name, port_name):
    cmd = 'vppctl bond del ' + ray_str(channel_name) + ' ' + ray_str(port_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_channel_del_port error !')
        return False
    return True
    
    
def vpp_get_max_bond_id():
    for id in range(0,16):
        cmd = 'ifconfig |grep bond' + str(id) + " 1>/dev/null 2>/dev/null"
        cmd1 = 'ifconfig -a |grep bond' + str(id) + " 1>/dev/null 2>/dev/null"
        ret = kernel.k.ray_system(cmd)
        ret1 = kernel.k.ray_system(cmd1)
        if ret and not ret1:
            return id
    return None


class channel():
    def add(self,physical_name):
        return ray_channel_set_status_byname(physical_name, 1)
        
    def dele(self,physical_name):
        return ray_channel_set_status_byname(physical_name, 0)
        
    def set_status(self,physical_name, enable):
        return  ray_channel_set_status_byname(physical_name, enable)
        
    def add_port(self,channel_name, port_name):
        return ray_channel_add_port(channel_name, port_name)
        
    def del_port(self, channel_name, port_name):
        return ray_channel_del_port(channel_name, port_name)
        
    def get_bond_id(self):
        return get_max_bond_id()
        
    def check(self,cname):
        return check_bond(cname)

    ###################vpp modules#############
    def vpp_add(self,id):
        return ray_vpp_channel_create(id)

    def vpp_dele(self,physical_name):
        return ray_vpp_channel_delete(physical_name)

    def vpp_set_status(self,physical_name, enable):
        return  ray_vpp_channel_set_status_byname(physical_name, enable)

    def vpp_add_port(self,channel_name, port_name):
        return ray_vpp_channel_add_port(channel_name, port_name)

    def vpp_del_port(self, channel_name, port_name):
        return ray_vpp_channel_del_port(channel_name, port_name)

    def vpp_get_bond_id(self):
        return vpp_getmax_bond_id()

    def vpp_check(self,cname):
        return vpp_check_bond(cname)
Kchannel = channel()