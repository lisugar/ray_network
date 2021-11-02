#coding=utf-8
import os
import sys
from ray_network.kernel.netray_type import RAY_DEBUG,ray_append,ray_int,ray_str
from libpy.public import kernel

def ray_system_dns_set(primary_dns,secondary_dns):
    cmd = ('echo nameserver %s>/etc/resolv.conf; echo nameserver %s>> /etc/resolv.conf' %(primary_dns,secondary_dns))
    ret = kernel.k.ray_system(cmd, paramcheck=0)
    if ret:
        return False
    else:
        return True 

class dns():
    def ray_system_dns_set(self,primary_dns,secondary_dns):
        return ray_system_dns_set(primary_dns,secondary_dns)
Kdns = dns()
