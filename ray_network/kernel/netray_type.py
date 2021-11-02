#coding=utf-8
import os
import sys
if (sys.version_info > (3, 0)):
    xrange=range
    long=int

NO_DEBUG_INFO = 1
OUT_DEBUG_INFO = 2
INT_DEBUG_INFO = 3
ERROR_DEBUGINFO = 4
DEBUG = INT_DEBUG_INFO # True 1 2 3 4 

out_msg = {'success':'true','message':'none','key':'','exit':'true','action':''}

##error
SUCCESS =          0 #Sussess 成功
ERR_UNINIT =       1 #Component not initialized. 模块未初始化
ERR_NULL =         2 #Parameter not allowed to be NULL. 参数为空
ERR_RANGE =        3 #Parameter outside allowable range. 参数范围错误
ERR_ALIGN =        4 #Parameter not appropriately aligned. 参数未对齐
ERR_OOM =          5 #Out of memory. 内存分配失败
ERR_OVERFLOW =     6 #Overflow. 出现向上溢出
ERR_UNDERFLOW =    7 #Underflow. 出现向下溢出
ERR_NOT_FOUND =    8 #Entry not found. 对象不存在
ERR_DUPLICATE =    9 #Duplicate entry. 存在重复对象
ERR_CONFLICTING =  10#Conflicting entry. 存在冲突对象
ERR_INTERNAL =     11#Internal error. 系统内部错误
ERR_UNIMPL =       12#Feature Not Implemented. 不支持的特性
ERR_FULL =         13#Excess capacity  超出容量
ERR_BUSY =         14#Object in use 对象正被使用
ERR_UNKNOWN =      15#Unknown error

def RCK(arg, msg = {}):
    if isinstance(msg,dict):
        pass
    else:
        RAY_DEBUG(INT_DEBUG_INFO, 'PCK msg is not a dict!!!!')
        exit()
        
    if arg == True:
        #RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Sussess')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_UNINIT:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Component not initialized')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_NULL:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Parameter not allowed to be NULL')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_RANGE:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Parameter outside allowable range')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_ALIGN:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Parameter not appropriately aligned')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_OOM:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Out of memory')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_OVERFLOW:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Overflow')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_UNDERFLOW:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Underflow')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_NOT_FOUND:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Entry not found')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_DUPLICATE:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Duplicate entry')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_CONFLICTING:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Conflicting entry')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_INTERNAL:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Internal error')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_UNIMPL:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Feature Not Implemented')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_FULL:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Excess capacity')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_BUSY:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Object in use')
        if msg.get('exit','') == 'true':
            exit()
        
    elif arg == ERR_UNKNOWN or arg == False:
        RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')))
        if msg.get('exit','') == 'true':
            exit()
        
    else:
        #RAY_DEBUG(OUT_DEBUG_INFO, ray_str(msg.get('action','')) + 'Internal fun return error')
        if msg.get('exit','') == 'true':
            exit()
    return True
        
        
        
        
def RAY_DEBUG(DEBUG_LEVEL, *args):
    if DEBUG:
        pass
    else:
        return 
    len_args = range(len(args))
    if DEBUG == True or DEBUG == OUT_DEBUG_INFO:
        if DEBUG_LEVEL == OUT_DEBUG_INFO:
            for Index in len_args:
                print(args[Index])
    elif DEBUG == True or DEBUG == INT_DEBUG_INFO:
        if DEBUG_LEVEL == INT_DEBUG_INFO:
            for Index in len_args:
                print(args[Index])
            
    elif DEBUG == True or DEBUG == ERROR_DEBUGINFO:
        if DEBUG_LEVEL == ERROR_DEBUGINFO:
            for Index in len_args:
                print(args[Index])
    elif DEBUG_LEVEL == NO_DEBUG_INFO :
        pass
    else:
        pass
    return True
        
        
def ray_append(elem, default, arg):
    if arg == None:
        if default:
            elem.append(default)
        else:
            elem.append('')
    else:
        elem.append(arg)
    
def ray_int(value, default=None):
    try:
        return int(value)
    except:
        if default != None:
            return default
        else:
            return 0

def ray_str(value, default=None):
    try:
        if value is None:
            raise

        return str(value)
    except:
        if default != None:
            return default
        else:
            return ''
            
def ray_long(value, default=None):
    try:
        return long(value)
    except:
        if default != None:
            return default
        else:
            return long(0)
            
            
            
            
