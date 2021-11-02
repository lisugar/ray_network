#coding=utf-8
import os
import sys

from libpy.public.ray_type import RAY_DEBUG,ray_append,ray_int,ray_str
from libpy.public.ray_ip import get_ver_from_str
from libpy.public import kernel
try:
    from libpy.public.ray_vpp import rayvpp, INVALID_INDEX
except:
    pass 

BASE_ID = 50000
PROUTE6_BASE_IDX = 500


def ray_proute_reload(idx,sip,dip,gip):
    cmd = 'ip route add default via ' + ray_str(gip) + ' table ' + ray_str(idx) + '  1>/dev/null 2>/dev/null'
    res = kernel.k.ray_system(cmd)
    if res :
        return False 
    cmd = 'ip rule add table ' + ray_str(idx) + ' priority ' + ray_str(idx) + ' from ' + ray_str(sip) + ' to ' + ray_str(dip) + '  1>/dev/null 2>/dev/null'
    ress = kernel.k.ray_system(cmd)
    if ress :
        return False 

    return True

def ray_proute_flush(idx):
    cmd = 'ip route flush table ' + ray_str(idx) + '  1>/dev/null 2>/dev/null'
    res = kernel.k.ray_system(cmd)
    cmd = 'ip rule del table ' + ray_str(idx) + '  1>/dev/null 2>/dev/null'
    ress = kernel.k.ray_system(cmd)
    if res or ress:
        return False
    else:
        return True
def ray_proute_cached():
    cmd = 'ip route flush cached'
    kernel.k.ray_system(cmd)

def ray_ipv6_proute_reload(idx,sip,dip,gip):
    cmd = 'ip -6 route add default via ' + ray_str(gip) + ' table ' + ray_str(idx)
    res = kernel.k.ray_system(cmd)
    if res  :
        return False 
    cmd = 'ip -6 rule add table ' + ray_str(idx) + ' priority ' + ray_str(idx) + ' from ' + ray_str(sip) + ' to ' + ray_str(dip)
    ress = kernel.k.ray_system(cmd)
    if  ress:
        return False
    return True

def ray_ipv6_proute_flush(idx):
    cmd = 'ip -6 route flush table ' + ray_str(idx)
    res = kernel.k.ray_system(cmd)
    cmd = 'ip -6 rule del table ' + ray_str(idx)
    ress = kernel.k.ray_system(cmd)
    if res or ress:
        return False
    else:
        return True
def vpp_acl_add(rule):
    rules = [rule.encode()]
    res = rayvpp.api.acl_add_replace(acl_index=INVALID_INDEX, tag='', r=rules, count= len(rules) )
    if not res.retval :
        return res.acl_index
    else :
        return -1

def vpp_acl_del(acl_id):
    res = rayvpp.api.acl_del(acl_index= acl_id)
    return not bool(res.retval)


def vpp_proute_add( rule, policy_id, gateway, ifname, bindingto):
    rayvpp.connect("proute_add")
    acl_internal_id = vpp_acl_add(rule)

    print("get acl id %d"%(acl_internal_id))
    if acl_internal_id == -1 :
        return acl_internal_id

    cmd = "abf policy add id %d acl %d via %s %s"%(policy_id, acl_internal_id, gateway, ifname)
    print(cmd)
    ret, msg = rayvpp.system(cmd)
    if not ret :
        vpp_acl_del(acl_internal_id)
        print(msg)
        return -1
    
    option = "ip4"
    if get_ver_from_str(gateway) == 6:
        option = 'ip6'
    cmd = "abf attach %s policy %d %s"%(option, policy_id, bindingto)
    print(cmd)
    ret, msg = rayvpp.system(cmd)
    if not ret :
        rayvpp.system("abf policy del id %d acl %d"%(policy_id, acl_internal_id))
        vpp_acl_del(acl_internal_id)
        print(msg)
        return -1 
    
    return acl_internal_id

def vpp_proute_del(acl_id, policy_id, gateway, ifname, bindingto):
    rayvpp.connect("proute_delete")

    option = "ip4"
    if get_ver_from_str(gateway) == 6:
        option = 'ip6' 
    cmd_del_attach = "abf attach %s del policy %d %s"%(option, policy_id, bindingto)
    cmd_del_abf_policy = "abf policy del id %d acl %d via %s %s"%(policy_id, acl_id, gateway, ifname)

    print(cmd_del_attach)
    print(cmd_del_abf_policy)
    ret, msg = rayvpp.system(cmd_del_attach)
    if not ret :
        print(msg)
    ret, msg = rayvpp.system(cmd_del_abf_policy)
    if not ret :
        print(msg)
    vpp_acl_del(acl_id=acl_id)

    rayvpp.close()
    return True 



    
    
        




class proute():
    def ray_proute_reload(self,idx,sip,dip,gip):
        return ray_proute_reload(idx,sip,dip,gip)
    def ray_proute_flush(self,idx):
        return ray_proute_flush(idx)
    def ray_ipv6_proute_reload(self,idx,sip,dip,gip):
        return ray_ipv6_proute_reload(idx,sip,dip,gip)
    def ray_ipv6_proute_flush(self,idx):
        return ray_ipv6_proute_flush(idx)
    def vpp_proute_add(self, rule, policy_id, gateway, ifname, bindingto):
        return vpp_proute_add(rule, policy_id, gateway, ifname, bindingto)
        
    def vpp_proute_del(self, acl_id, policy_id, gateway, ifname, bindingto):
        return vpp_proute_del(acl_id, policy_id, gateway, ifname, bindingto)

Kproute = proute()
