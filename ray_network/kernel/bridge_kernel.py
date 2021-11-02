#coding=utf-8
import os
import struct,socket
from ray_network.kernel.port_kernel import webray_get_link_status, ray_map
from ray_network.kernel.netray_type import RAY_DEBUG,ray_append,ray_int,ray_str
from ray_network.kernel.netray_ip import get_ver_from_str,pm_2str,ip_str_2dict,ip_str2num
from libpy.public import kernel
PORTMAX = 64

def ip_to_hex(available_id):
    '''
    ip_num = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip)))[0])
    aa = hex(ip_num)[2:]
    return aa[::-1]
    '''
    ip_key = "L%03d"%available_id
    return ip_key

def webray_network_bridge_kcli_add_byname(bri_name):
    cmd = 'brctl addbr ' +  ray_str(bri_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        #cmd = 'brctl delbr ' +  ray_str(bri_name) + " 1>/dev/null 2>/dev/null"
        RAY_DEBUG(2, 'bridge name '+ ray_str(bri_name) + 'error !')
        return False
    cmd = 'brctl setfd ' + ray_str(bri_name) + ' 1' + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'bridge name '+ ray_str(bri_name) + 'error !')
        return False
    cmd = 'ifconfig ' + ray_str(bri_name) + ' up' + " 1>/dev/null 2>/dev/null"
    kernel.k.ray_system(cmd)
    return True
    
    
def webray_network_bridge_kcli_remove_byname(bri_name):
    cmd = 'ifconfig ' +  ray_str(bri_name) + ' down ' + " 1>/dev/null 2>/dev/null"
    kernel.k.ray_system(cmd)
    cmd = 'brctl delbr ' +  ray_str(bri_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'bridge name '+ bri_name + 'error !')
        return False
    return True
    
    
def ray_bridge_set_status_byname(bri_name, enable):
    if enable:
        uw = ' up '
    else:
        uw = ' down '
    cmd = 'ifconfig ' + ray_str(bri_name) + ' ' +  ray_str(uw) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_set_status_byname error')
        return False
    return True
    
    
def ray_bridge_add_if(bri_name, if_name):
    cmd = 'brctl addif ' + ray_str(bri_name) + ' ' + ray_str(if_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_add_if error !')
        return False
    return True
    
def ray_bridge_remove_if(bri_name, if_name):
    cmd = 'brctl delif ' + ray_str(bri_name) + ' ' + ray_str(if_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_remove_if error !')
        return False
    return True
    
    
def ray_bridge_add_ip(bri_name, ip_mask, reload, available_id):#ip_mask: *.*.*.*/*
    if get_ver_from_str(ip_mask) != 4 and get_ver_from_str(ip_mask) != 6:
        RAY_DEBUG(2, 'ray_bridge_add_ip: ipver error!')
        return False
        
    # if get_ver_from_str(ip_mask) == 4:
    #     ip = pm_2str(ip_str_2dict(ip_mask, 0), None, 4 ,1)
    #     mask = pm_2str(ip_str_2dict(ip_mask, 1), None, 4 ,1)
    #     cmd = 'ifconfig ' + ray_str(bri_name) + ':' + str(ip_to_hex(available_id)) + ' ' + ip  + ' netmask  ' + mask + ' up' + " 1>/dev/null 2>/dev/null"
    #     cmd = "ip addr add %s dev %s 1>/dev/null 2>/dev/null "%(ip_mask, ray_str(bri_name))
    # else:
    #     cmd = 'ifconfig ' + ray_str(bri_name) + ' inet6 add ' + ray_str(ip_mask) + ' up' + " 1>/dev/null 2>/dev/null"

    cmd = "ip addr add %s dev %s 1>/dev/null 2>/dev/null "%(ip_mask, ray_str(bri_name))

    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_add_ip: add ' + ray_str(ip_mask) + ' error!!')
        return False
    return True
        
        
def ray_bridge_remove_ip(bri_name, ip_mask, reload, available_id):
    # if get_ver_from_str(ip_mask) != 4 and get_ver_from_str(ip_mask) != 6:
    #     RAY_DEBUG(2, 'ray_bridge_remove_ip: ipver error!')
    #     return False
        
    # if get_ver_from_str(ip_mask) == 4:
    #     ip = pm_2str(ip_str_2dict(ip_mask, 0), None, 4 ,1)
    #     cmd = 'ifconfig ' + ray_str(bri_name) + ':' + str(ip_to_hex(available_id)) + ' ' + ip + ' down' + " 1>/dev/null 2>/dev/null"
    # else:
    #     cmd = 'ifconfig ' + ray_str(bri_name) + ' inet6 del ' + ray_str(ip_mask) + " 1>/dev/null 2>/dev/null"

    cmd = "ip addr del %s dev %s 1>/dev/null 2>/dev/null "%( ray_str(ip_mask), ray_str(bri_name))
        
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_remove_ip: remove ' + ray_str(ip_mask) + ' error!!')
        return False
    return True
    
    
    
def ray_bridge_set_stp(bri_name, stp):
    uw = 'on'
    if ray_int(stp) == 1:
        uw = 'on'
    else:
        uw = 'off'
        
    cmd = 'brctl stp ' + ray_str(bri_name) + ' ' + uw + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_set_stp error!')
        return False
    return True
    
def ray_bridge_stp_get(bri_name):
    stp_state_file =  "/sys/class/net/" + str(bri_name) + "/bridge/stp_state"
    if  not os.path.exists(stp_state_file):
        RAY_DEBUG(2, bri_name+" is not exist!")
        return 0
    cmd = "cat /sys/class/net/" + str(bri_name) + "/bridge/stp_state"
    enable = kernel.k.ray_popen(cmd).strip()
    return int(enable)
    
    
def ray_bridge_set_mac_mtu(bri_name, mtu, mac = None):
    if ray_int(mtu):
        cmd = 'ifconfig ' + ray_str(bri_name) + ' mtu '+ ray_str(mtu) + " 1>/dev/null 2>/dev/null"
        ret = kernel.k.ray_system(cmd)
        if ret:
            RAY_DEBUG(2, 'ray_bridge_set_mac_mtu error!')
            return False
        return True
    else:
        return True
    
def ray_bridge_get_mac(bri_name):
    cmd = 'ifconfig ' + ray_str(bri_name) +  " | grep ether | awk '{print $2}'"
    text = kernel.k.ray_popen(cmd)

    return ray_str(text.replace('\n',''))
    
def ray_get_mtu(bri_name):
    cmd = 'ifconfig ' + ray_str(bri_name) +  " | grep mtu | awk '{print $4}'"
    text = kernel.k.ray_popen(cmd)

    return ray_str(text.replace('\n',''))
    
def ray_bridge_restart():
    return True
    

##############vpp modules##############

def webray_network_vpp_bridge_kcli_add_byname(idx):
    try:
        cmd = 'vppctl create bridge-domain ' +  ray_str(idx)
        f = os.popen(cmd)
        message = f.readlines()
        f.close()
        message = ''.join(message)
        message = message.strip()
        if message != 'create bridge-domain: bd_add_del returned -119':
            cmd = "vppctl loopback create-interface"
            f = os.popen(cmd)
            loop_ret = f.readlines()
            f.close()
            loop_ret = ''.join(loop_ret)
            loop_ret = loop_ret.strip()
            if "loop" not in loop_ret:
                RAY_DEBUG(2, 'vpp loopback create error !')
                return False, 0
            cmd = 'vppctl set interface state ' + ray_str(loop_ret) + ' up' + " 1>/dev/null 2>/dev/null"
            kernel.k.ray_system(cmd)
            cmd = 'vppctl set interface l2 bridge ' + ray_str(loop_ret) + ' ' + ray_str(idx) + ' bvi' + " 1>/dev/null 2>/dev/null"
            kernel.k.ray_system(cmd)
            return True, loop_ret
        return True, False
    except:
        RAY_DEBUG(2, 'bridge create error !')
        return False, 0    

def webray_network_vpp_bridge_kcli_remove_byname(loop, idx):
    cmd = 'vppctl loopback delete-interface intfc ' +  ray_str(loop) + " 1>/dev/null 2>/dev/null"
    kernel.k.ray_system(cmd)
    cmd = 'vppctl create bridge-domain del ' +  ray_str(idx) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'bridge name error !')
        return False
    return True

    
def ray_vpp_bridge_set_status_byname(bri_name, enable):
    if enable:
        uw = ' up '
    else:
        uw = ' down '
    cmd = 'vppctl set interface state ' + ray_str(bri_name) + ' ' +  ray_str(uw) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_set_status_byname error')
        return False
    return True
    
def ray_vpp_bridge_add_if(bri_name, if_name):
    cmd = 'vppctl set interface l2 bridge ' + ray_str(if_name) + ' ' + ray_str(bri_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_vpp_bridge_add_if error !')
        return False
    return True
    
def ray_vpp_bridge_remove_if(if_name):
    cmd = 'vppctl set interface l3 ' + ray_str(if_name) + " 1>/dev/null 2>/dev/null"
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_vpp_bridge_remove_if error !')
        return False
    return True    

def ray_vpp_bridge_add_ip(bri_name, ip_mask, reload, available_id):#ip_mask: *.*.*.*/*
    if get_ver_from_str(ip_mask) != 4 and get_ver_from_str(ip_mask) != 6:
        RAY_DEBUG(2, 'ray_bridge_add_ip: ipver error!')
        return False
        
    if get_ver_from_str(ip_mask) == 4:
        #ip = pm_2str(ip_str_2dict(ip_mask, 0), None, 4 ,1)
        #mask = pm_2str(ip_str_2dict(ip_mask, 1), None, 4 ,1)
        cmd = 'vppctl set interface ip address ' + ray_str(bri_name) + ' ' + ray_str(ip_mask) + " 1>/dev/null 2>/dev/null"
    else:
        cmd = 'vppctl set interface ip address ' + ray_str(bri_name) + ' ' + ray_str(ip_mask) + " 1>/dev/null 2>/dev/null"
        
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_add_ip: add ' + ray_str(ip_mask) + ' error!!')
        return False
    return True
        
        
def ray_vpp_bridge_remove_ip(bri_name, ip_mask, reload, available_id):
    if get_ver_from_str(ip_mask) != 4 and get_ver_from_str(ip_mask) != 6:
        RAY_DEBUG(2, 'ray_bridge_remove_ip: ipver error!')
        return False
        
    if get_ver_from_str(ip_mask) == 4:
        #ip = pm_2str(ip_str_2dict(ip_mask, 0), None, 4 ,1)
        cmd = 'vppctl set interface ip address del ' + ray_str(bri_name) + ' ' + ray_str(ip_mask) + " 1>/dev/null 2>/dev/null"
    else:
        cmd = 'vppctl set interface ip address del ' + ray_str(bri_name) + ' ' + ray_str(ip_mask) + " 1>/dev/null 2>/dev/null"
        
    ret = kernel.k.ray_system(cmd)
    if ret:
        RAY_DEBUG(2, 'ray_bridge_remove_ip: remove ' + ray_str(ip_mask) + ' error!!')
        return False
    return True   

def ray_vpp_bridge_get_mac(bri_name):
    cmd = 'vppctl show hardware-interface ' + ray_str(bri_name) + " | grep Ethernet | awk '{print $3}'"
    text = kernel.k.ray_popen(cmd)

    return ray_str(text.replace('\n',''))

    
class bridge():
    def set_stp(self,bri_name,stp):
        return ray_bridge_set_stp(bri_name,stp)
        
    def get_stp(self,bri_name):
        return ray_bridge_stp_get(bri_name)
        
    def add(self,bri_name):
        return webray_network_bridge_kcli_add_byname(bri_name)
        
        
    def dele(self,bri_name):
        return webray_network_bridge_kcli_remove_byname(bri_name)
        
    def set_status_byname(self,bri_name, enable):
        return  ray_bridge_set_status_byname(bri_name, enable)
        
    def add_ip(self, bri_name, ip_mask, reload, available_id):
        return ray_bridge_add_ip(bri_name, ip_mask, reload, available_id)
        
    def del_ip(self, bri_name, ip_mask, reload, available_id):
        return ray_bridge_remove_ip(bri_name, ip_mask, reload, available_id)
        
    def add_if(self, bri_name, if_name):
        return ray_bridge_add_if(bri_name, if_name)
        
    def remove_if(self, bri_name, if_name):
        return ray_bridge_remove_if(bri_name, if_name)
        
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

    def vpp_add(self,bri_name):
        return webray_network_vpp_bridge_kcli_add_byname(bri_name)
        
    def vpp_dele(self,loop,idx):
        return webray_network_vpp_bridge_kcli_remove_byname(loop, idx)

    def set_vpp_status_byname(self,bri_name, enable):
        return  ray_vpp_bridge_set_status_byname(bri_name, enable)

    def vpp_add_ip(self, bri_name, ip_mask, reload, available_id):
        return ray_vpp_bridge_add_ip(bri_name, ip_mask, reload, available_id)   

    def vpp_del_ip(self, bri_name, ip_mask, reload, available_id):
        return ray_vpp_bridge_remove_ip(bri_name, ip_mask, reload, available_id)

    def vpp_add_if(self, bri_name, if_name):
        return ray_vpp_bridge_add_if(bri_name, if_name)   

    def vpp_remove_if(self, if_name):
        return ray_vpp_bridge_remove_if(if_name)

    def get_vpp_mac(self,bri_name):
        return ray_vpp_bridge_get_mac(bri_name)
    
Kbridge = bridge()