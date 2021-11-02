#support ipv6   
# coding=UTF-8
import struct,socket
from ctypes import *
MAX_UINT=4294967295 
def ip_num2str(ip):
    if ip == 0:
        return "0.0.0.0"
    if ip < 0:
        ip = struct.unpack("I", struct.pack('i', ip))[0]

    return socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))

def ip_str2num(ip):
    ip_num = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip)))[0])
    if ip_num > 2147483647:
        return ip_num - 4294967296
    return ip_num
    
class u128_t(Structure):
    _fields_ = [('x0', c_uint),
                ('x1', c_uint),
                ('x2', c_uint),
                ('x3', c_uint)]

# flag ==0 结构体 否则 为 字典
def get_ipv4(ip,flag):
    if flag == 0:
        ret = int(ip.x3)
    else:
        ret = int(ip['x3'])
    return ret
    
def get_ipv4_mask(mask,flag):
    if(flag == 0):
        ret = mask.x3
    else:
        ret = mask['x3']
    return ret
    
# flag ==0 结构体 否则 为 字典
def ip_equal(ip1,ip2,flag):
    if flag == 0:
        if ip1.x0 == ip2.x0 and ip1.x1 == ip2.x1 and ip1.x2 == ip2.x2 and ip1.x3 == ip2.x3:
            return True
        else:
            return False
    else:
        if ip1['x0'] == ip2['x0'] and ip1['x1'] == ip2['x1'] and ip1['x2'] == ip2['x2'] and ip1['x3'] == ip2['x3']:
            return True
        else:
            return False
            
def  ip_bit_and_mask(trueip,ip,mask,flag):
    if(flag ==0):
        trueip.x0 = ip.x0 & mask.x0
        trueip.x1 = ip.x1 & mask.x1
        trueip.x2 = ip.x2 & mask.x2
        trueip.x3 = ip.x3 & mask.x3
    else:
        trueip['x0'] = ip['x0'] & mask['x0']
        trueip['x1'] = ip['x1'] & mask['x1']
        trueip['x2'] = ip['x2'] & mask['x2']
        trueip['x3'] = ip['x3'] & mask['x3']

def is_ipv4(ip,flag):
    if flag == 0:
        ret = ip.x0 | ip.x1 | ip.x2
        if ret == 0:
            return True
        else:
            return False
    else:
        ret = ip['x0'] | ip['x1'] | ip['x2']
        if ret == 0:
            return True
        else:
            return False
            
def is_ipv6(ip,flag): # 没有考虑 ipv4兼容ipv6 的情况，这种需要版本号来说明
    if flag == 0:
        ret = ip.x0 | ip.x1 | ip.x2
        if ret > 0:
            return True
        else:
            return False
    else:
        ret = ip['x0'] | ip['x1'] | ip['x2']
        if ret > 0:
            return True
        else:
            return False
            

def pm_struct2dict(pm):
    return {'x0':pm.x0, 'x1':pm.x1, 'x2':pm.x2, 'x3':pm.x3}

    
def pm_dict(x0,x1,x2,x3):
    p0 = x0
    p1 = x1
    p2 = x2
    p3 = x3
    if x0 == None:
        p0 = MAX_UINT
    if x1 == None:
        p1 = MAX_UINT
    if x2 == None:
        p2 = MAX_UINT
    if x3 == None:
        p3 = MAX_UINT
    return {'x0':p0, 'x1':p1, 'x2':p2, 'x3':p3}

    
def pm_copy(d, s,flag):
    if flag == 0:
        d.x0 = s.x0
        d.x1 = s.x1
        d.x2 = s.x2
        d.x3 = s.x3
    else :
        d['x0'] = s['x0']
        d['x1'] = s['x1']
        d['x2'] = s['x2']
        d['x3'] = s['x3']

def pm_dict_2s(structure,dict):
    structure.x0 = dict['x0']
    structure.x1 = dict['x1']
    structure.x2 = dict['x2']
    structure.x3 = dict['x3']

def pm_s_2dict(dict,structure):
    dict['x0'] = structure.x0
    dict['x1'] = structure.x1
    dict['x2'] = structure.x2
    dict['x3'] = structure.x3
    
# flag == 0 from structure to string   flag != 0 from dict to str
def ipv6_2str(ipv6,flag):
    #if ip_equal_zero(ipv6,flag):
        #return '::'
    if flag == 0:
        ipv6_n = (socket.htonl(ipv6.x0),
              socket.htonl(ipv6.x1),
              socket.htonl(ipv6.x2),
              socket.htonl(ipv6.x3))
    else :
        ipv6_n = (socket.htonl(ipv6['x0']),
              socket.htonl(ipv6['x1']),
              socket.htonl(ipv6['x2']),
              socket.htonl(ipv6['x3']))

    data = struct.pack('IIII', ipv6_n[0], ipv6_n[1], ipv6_n[2], ipv6_n[3])
    ipv6_string = socket.inet_ntop(socket.AF_INET6, data)
 
    return ipv6_string

def ipv6_str2dict(ipv6):
    data = socket.inet_pton(socket.AF_INET6, ipv6)
    ipv6_n = struct.unpack('IIII', data)
    ipv6 = (socket.ntohl(ipv6_n[0]),
            socket.ntohl(ipv6_n[1]),
            socket.ntohl(ipv6_n[2]),
            socket.ntohl(ipv6_n[3]))
 
    return pm_dict(ipv6[0],ipv6[1],ipv6[2],ipv6[3])

# flag == 0 struct to num  flag == 1 dict to num
def mask_2num(mask, flag):
    mask_num = 0
    count = 0
    if flag == 0:
        mask_dict = pm_struct2dict(mask)
    else:
        mask_dict = mask
        
    while(mask_dict['x3'] and count < 32):
        if mask_dict['x3'] & 1<<count:
            mask_num +=1
        count +=1
        
    count = 0
    while(mask_dict['x2'] and count < 32):
        if mask_dict['x2'] & 1<<count:
            mask_num +=1
        count +=1
        
    count = 0
    while(mask_dict['x1'] and count < 32):
        if mask_dict['x1'] & 1<<count:
            mask_num +=1
        count +=1
        
    count = 0
    while(mask_dict['x0'] and count < 32):
        if mask_dict['x0'] & 1<<count:
            mask_num +=1
        count +=1
    return mask_num

def mask_num2dict(mask,flag): #flag == 0 ipv4 flag == 1 ipv6
    maskdict = pm_dict(0,0,0,0)
    if mask <= 32:
        count = mask
        while(count > 0):
            if(flag == 0):
                maskdict['x3']  +=  (1<<(32-count))
            else :
                maskdict['x0']  +=  (1<<(32-count))
            count -=1
            
    if mask > 32 and mask <= 64:
        count  = mask - 32
        maskdict['x0'] = MAX_UINT
        while (count > 0):
            maskdict['x1']  +=  (1<<(32-count))
            count -=1

    if mask > 64 and mask <= 96:
        count  = mask - 64
        maskdict['x0'] = MAX_UINT
        maskdict['x1'] = MAX_UINT
        while (count > 0):
            maskdict['x2']  +=  (1<<(32-count))
            count -=1
    
    if mask > 96 and mask <= 128:
        count  = mask - 96
        maskdict['x0'] = MAX_UINT
        maskdict['x1'] = MAX_UINT
        maskdict['x2'] = MAX_UINT
        while (count > 0):
            maskdict['x3']  +=  (1<<(32-count))
            count -=1
    
    return maskdict
    
'''
#from ip to string (ipv4 or ipv6 )
def ip_2str(ip, flag): #没有掩码 可以直接使用下面这个
    if is_ipv4(ip, flag):
        return ip_num2str(get_ipv4(ip, flag))
    else:
        return ipv6_2str(ip, flag)
'''

   
def str_is_ipv4(ip):
    ip4 = ip
    try:
        if '/' in ip:
            iptmp = ip
            ip4 = str(iptmp.split('/')[0])
            ip4m = int(iptmp.split('/')[1])
            if ip4m < 0 or ip4m > 32:
                return False
        if '.' in ip4:
            ip4 = str(int(ip4.split('.')[0])) + '.' + str(int(ip4.split('.')[1]))+'.' +str(int(ip4.split('.')[2])) + '.' + str(int(ip4.split('.')[3]))
    except:
        return False
        
    try:
        socket.inet_pton(socket.AF_INET, str(ip4))
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(str(ip))
        except socket.error:
            return False
        return str(ip).count('.') == 3
    except socket.error:  # not a valid ip
        return False
    return True

    
def str_is_ipv6(ip):
    ip6 = ip
    if '/' in ip:
        iptmp = ip
        ip6 = str(iptmp.split('/')[0])
        ip6m = int(iptmp.split('/')[1])
        if ip6m < 0 or ip6m > 128:
            return False
    try:
        socket.inet_pton(socket.AF_INET6, str(ip6))
    except socket.error:  # not a valid ip
        return False
    return True




def ip_str_2dict(ip,flag): # flag = 0 返回IP的字典 flag = 1 返回掩码的地址
    if ip == '':
        return pm_dict(0,0,0,0)
    if str_is_ipv4(ip):
        if '/' in ip:
            iptmp = ip
            ip4 = str(iptmp.split('/')[0])
            ip4 = str(int(ip4.split('.')[0])) + '.' + str(int(ip4.split('.')[1]))+'.' +str(int(ip4.split('.')[2])) + '.' + str(int(ip4.split('.')[3]))
            ip4m = int(iptmp.split('/')[1])
            if flag == 0:
                return pm_dict(0,0,0,ip_str2num(ip4))
            else :
                return mask_num2dict(ip4m,0) #pm_dict(0,0,0,int(ip4m))
        else:
            ip = str(int(ip.split('.')[0])) + '.' + str(int(ip.split('.')[1]))+'.' +str(int(ip.split('.')[2])) + '.' + str(int(ip.split('.')[3]))
            if flag == 0:
                return pm_dict(0,0,0,ip_str2num(str(ip)))
            else :
                return pm_dict(0,0,0,MAX_UINT)
                '''
                if ip == '0.0.0.0':
                    return pm_dict(0,0,0,0)
                else:
                    return pm_dict(0,0,0,MAX_UINT)
                '''
#ipv6
    else: #str_is_ipv6(ip):
        if '/' in ip:
            iptmp = ip
            ip6 = str(iptmp.split('/')[0])
            ip6m = int(iptmp.split('/')[1])
            if flag == 0:
                return ipv6_str2dict(str(ip6))
            else :
                return mask_num2dict(int(ip6m),1)
        else:
            if flag == 0:
                return ipv6_str2dict(str(ip))
            else :
                return pm_dict(MAX_UINT,MAX_UINT,MAX_UINT,MAX_UINT)
                '''
                if ip == '::' or ip == '0:0:0:0:0:0:0:0':
                    return pm_dict(0,0,0,0)
                else:
                    return pm_dict(MAX_UINT,MAX_UINT,MAX_UINT,MAX_UINT)
                '''
                

def ip_equal_zero(ip,flag):
    if flag == 0:
        if ip.x0 == 0 and ip.x1 == 0 and ip.x2 == 0 and ip.x3 == 0:
            return True
        else :
            return False
    elif flag == 1:
        if ip['x0'] == 0 and ip['x1'] == 0 and ip['x2'] == 0 and ip['x3'] == 0:
            return True
        else :
            return False    
    else:# flag == 2
        ip_p = ip_str_2dict(ip,0)
        ip_m = ip_str_2dict(ip,1)
        trueip = pm_dict(0,0,0,0)
        ip_bit_and_mask(trueip,ip_p,ip_m,1)
        if trueip['x0'] == 0 and trueip['x1'] == 0 and trueip['x2'] == 0 and trueip['x3'] == 0:
            return True
        else:
            return False

def pm_2str(ip,mask,version,flag):# 有掩码,version:当IP和掩码不能区分ipv4和ipv6时候需要传入version 版本来说明，一般有两种情况不能区分：①全0时不能区分，②ipv兼容ipv6时，当不能区分这两种情况出现，而参数又没有传入版本号时候默认ipv4处理
    if is_ipv6(ip, flag):
        if mask == None:
            return ipv6_2str(ip, flag)
        else:
            return str(ipv6_2str(ip, flag)) + '/' + str(mask_2num(mask,flag))
            
    else:## 这种 包含了ipv4 地址、全0 的情况 、ipv4 兼容ipv6 、这三种情况
        if version == 6:
            if mask == None:
                return ipv6_2str(ip, flag)
            else:
                return str(ipv6_2str(ip, flag)) + '/' + str(mask_2num(mask,flag))
                
        if mask == None:
            return ip_num2str(int(get_ipv4(ip, flag)))
        else:
            return str(ip_num2str(int(get_ipv4(ip, flag)))) + '/' + str(mask_2num(mask,flag))
            
def get_mask_from_4str(ip):
    if str_is_ipv4(ip):
        return pm_2str(ip_str_2dict(ip,1), None, 4, 1)
    else:
        return False
        
        
def str_2trueip(ip):
    ip_dict = ip_str_2dict(ip,0)
    mask_dict = ip_str_2dict(ip,1)
    trueip = pm_dict(0,0,0,0)
    version = get_ver_from_str(ip)
    ip_bit_and_mask(trueip,ip_dict,mask_dict,1)
    ip11 = pm_2str(trueip,mask_dict,version,1)
    return ip11

def ip_str_equal(ip1,ip2):
    ip11 = str_2trueip(ip1)
    ip22 = str_2trueip(ip2)
    if  ip11 == ip22:
        return True
    else:
        return False
        


def ip_is_bst(ip,flag): #flag 0 IP为结构体，flag = 1 IP为字典 flag 为2 IP为字符串
    bip = 'ff00::'
    bst_ip = ip_str_2dict(bip,0)
    input_ip = pm_dict(0,0,0,0)
    ture_ip = pm_dict(0,0,0,0)
    if flag == 0:
        pm_s_2dict(input_ip,ip)
    elif flag == 1:
        input_ip = ip
    else:
        input_ip = ip_str_2dict(ip,0)

    ip_bit_and_mask(ture_ip,input_ip,bst_ip,1)
    if ip_equal(ture_ip,bst_ip,1):
        return True
    else:
        return False

def get_ver_from_str(ip):
    try:
        if str_is_ipv6(ip):
            return 6
        elif str_is_ipv4(ip):
            return 4
        else:
            return 0
    except:
        return 0
        
def ip_is_loop(ip,flag): # flag == 0 struct  flag
    str6 = '::1'
    str4 = '127.0.0.1'
    ip6 = ip_str_2dict(str6,0)
    ip4 = ip_str_2dict(str4,0)
    ipx = pm_dict(0,0,0,0)
    if flag == 0:
        pm_s_2dict(ipx,ip)
    elif flag == 1:
        ipx = ip
    else:## flag == 2
        ipx = ip_str_2dict(ip,0)
        
    if ip_str_equal(ipx,ip4) or ip_str_equal(ipx,ip6):
        return True
    else:
        return False
        
special_ipv6_3 = ["fe8","fe9","fea","feb","fec"]
special_ipv6_2 = ["ff"]
def is_special_ipv6(value):
    try:
        if str(value[:3]) in special_ipv6_3:
            return True
        if str(value[:2]) in special_ipv6_2:
            return True
        return False
    except:
        return False
        
def ipstr_2criterion_ip(ip):
    version = get_ver_from_str(ip)
    ip1 = ip_str_2dict(ip,0)
    mask = ip_str_2dict(ip,1)
    if '/' in ip:
        return pm_2str(ip1,mask,version,1)
    return pm_2str(ip1,None,version,1)

'''
flag没做特殊说明的flag== 0 和结构体相关 flag== 1 和字典相关，比如第一个 flag== 0 为从结构体里面获取IP
pm_dict(x0,x1,x2,x3) 定义一个字典
get_ipv4(ip,flag) 获取IPv4地址
get_ipv4_mask(mask,flag) 获取ipv4掩码
ip_equal(ip1,ip2,flag) 判断两个IP 是否相同
ip_equal_zero(ip,flag) 判断IP是否为0 ,flag == 0 和 flag == 1 同上  flag == 2 判断一个带掩码或者不带掩码的字符串IP真实地址是否为0
is_ipv4(ip,flag) 判断是否为IPv4地址 是返回True 。。
pm_struct2dict(u128_ip) ip或者掩码结构体转成字典
pm_copy(d, s,flag) ip 或者掩码 copy
pm_dict_2s(structure,dict) 字典copy到结构体
pm_s_2dict(dict,structure)结构体 copy 字典
ipv6_2str(ipv6,flag) ipv6 转成字符串
ipv6_str2dict(ipv6) ipv6 字符串转成字典//可以直接使用ip_str_2dict这个函数
str_is_ipv4(ip) 判断一个字符串是否为IPv4地址
str_is_ipv6(ip) 同上
ip_str_2dict(ip,flag) ipv4 或者 ipv6 字符串转成字典 如果是带 / 或者ipv6 带/的这种形式 flag = 0 返回IP的字典 flag = 1 返回掩码的字典
mask_2num(mask, flag) ipv4、ipv6的掩码转成 数字
mask_num2dict(mask,flag)ipv4、ipv6掩码数字转成字典 注意 这个flag == 0 为ipv4 flag== 1 为ipv6 因为当掩码小于等于32 时候 函数不能判断 传参是ipv4 的前缀 还是ipv6 的前缀
pm_2str(ip,mask,version,flag) # ip 和 掩码 一起转成字符串形式 1.1.1.1/24 fe:80/64
ip_bit_and_mask(trueip,ip,mask,flag) ip按位相与得到真实IP
ip_str_equal(ip1,ip2) 判断两个字符串IP实际是否为同一IP 或者网段
str_2trueip(ip) 一个字符串IP转成其真实的IP 比如 fe22::/3 转换后变成其真实的IP 为：e000::/3
ip_is_bst(ip,flag): 查看一个IPv6 是否为广播地址 #flag 0 IP为结构体，flag = 1 IP为字典 flag 为2 IP为字符串
get_ver_from_str(ip):通过ip字符串返回版本号。
get_mask_from_4str(ip):从1.1.1.1/24 中获取ipv4的字符串掩码
常用函数：
pm_dict(x0,x1,x2,x3)
ip_equal_zero(ip,flag)
pm_dict_2s(structure,dict)
pm_s_2dict(dict,structure)
ip_str_2dict(ip,flag)
pm_2str(ip,mask,version,flag)
ip_str_equal(ip1,ip2)
str_2trueip(ip)
get_ver_from_str(ip)
'''   
