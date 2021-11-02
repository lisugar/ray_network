from ray_network.gen.mo.resource_api_gen import ResourceApiGen
from ray_network.gen.mo.resource_object import Dns
from libpy.public import kernel
from libpy.public.ray_ip import get_ver_from_str
from ray_network.kernel.netray_type import RAY_DEBUG,ray_append,ray_int,ray_str

#port
from ray_network.kernel.port_kernel import Kport
#bridge
from ray_network.kernel.bridge_kernel import Kbridge
#channel
from ray_network.kernel.channel_kernel import Kchannel
#Trunk
from ray_network.kernel.trunk_kernel import Ktrunk
#Arp
from ray_network.kernel.arp_kernel import Karp
#Dns
from ray_network.kernel.dns_kernel import Kdns
#Route
from ray_network.kernel.route_kernel import Kroute

COMMENTLEN = 60
BRIDGE_IDX_MAX = 4094
BRIDGE_IDX_MIN = 1
WEBRAY_MIN_BRIDGE_SUPPORT = 8

CHANNEL_MAX = 8

VLANNAME = "MngtBridge"

class NetworkExtension(ResourceApiGen):

    def __init__(self, *args, **kwar):
        super(NetworkExtension, self).__init__()

###### Port Function ######
    def pre_port_create(self, cm, ctx, mo):

        mo.logicname = ray_str(mo.logicname)
        if not mo.logicname:
            error_msg = 'logicname  error'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        p_list = cm.port_list(filter={
            "logicname": mo.logicname
        })

        if p_list:
            error_msg = mo.logicname + " is exist!"
            RAY_DEBUG(3,error_msg)
            raise Exception(error_msg)

        mo.physicalname =ray_str(mo.physicalname)
        mo.speed = ray_str(mo.speed)

        ret = Kport.port_set_status_byname(mo.physicalname, 1)
        if not ret:
            error_msg = 'add ' + mo.logicname + " faild!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        mo.admin_status = 1
        mo.link_status = Kport.get_link_status(mo.physicalname)
        mo.mac = Kport.get_mac(mo.physicalname)
        mo.mtu = Kport.get_mtu(mo.physicalname)

    def pre_port_delete(self, cm, ctx, id):

        port = cm.port_read(id=id)
        if port:
            ret = Kport.port_set_status_byname(port.physicalname,0)
            if ret is False and False:
                raise Exception("port " + str(port.physicalname) + " disable failed")
        else:
            error_msg = "port " + str(id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

    def post_port_delete(self, cm, ctx, id, mo):
        if mo:
            RAY_DEBUG(3,"port " + str(mo.logicname) + " del success!")

    def port_sync(self, cm, ctx):
        port = cm.port_list()
        if port:
            for item in port:
                if item.physicalname and item.logicname:
                    pay_load = {
                        "id": item.id,
                        "mac": Kport.get_mac(item.physicalname),
                        "mtu": Kport.get_mtu(item.physicalname),
                        "link_status":Kport.get_link_status(item.physicalname)
                    }
                    cm.port_update(pay_load)
                    RAY_DEBUG(3,"Update port {} sucessfully".format(item.logicname))
        else:
            RAY_DEBUG(3,"Not port exist!")

    def port_enable(self, cm, ctx, id=None):
        port = cm.port_read(id)
        if port:
            if not port.logicname or not port.physicalname:
                RAY_DEBUG(3,'logicname/physicalname error')
                return None

            port.admin_status = 1
            cm.port_update({
                "id": id,
                "admin_status": 1
            })

            Kport.port_set_status_byname(port.physicalname,1)
            RAY_DEBUG(3, port.logicname + " enable success!")
            return True
        else:
            RAY_DEBUG(3, "port " + str(id) + " does not exist!")

    def port_disable(self, cm, ctx, id=None):
        port = cm.port_read(id)
        if port:
            if not port.logicname or not port.physicalname:
                RAY_DEBUG(3,'logicname/physicalname error')
                return None

            port.admin_status = 0
            cm.port_update({
                "id": id,
                "admin_status": 0
            })

            Kport.port_set_status_byname(port.physicalname,0)
            RAY_DEBUG(3, port.logicname + " disable success!")
            return True
        else:
            RAY_DEBUG(3, "port " + str(id) + " does not exist!")

###### Bridge Function ######
    def pre_bridge_create(self, cm, ctx, mo):
        #force int for idx
        mo.idx = ray_int(mo.idx)
        mo.mtu = ray_int(mo.mtu, 1500)
        mo.stp = ray_int(mo.stp, 0)
        if ray_str(mo.logicname) == '':
            mo.logicname = 'br' + ray_str(mo.idx)
        mo.physicalname = mo.logicname

        #check whether comment is too long
        if mo.comment and len(ray_str(mo.comment)) > COMMENTLEN:
            error_msg = 'comment is to long'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        max_bri = WEBRAY_MIN_BRIDGE_SUPPORT
        bridge_list = cm.bridge_list()
        lic_num = kernel.k.ray_popen("/RayOS/utils/lictm -L |grep vlan_maxnum |awk '{print $3}'",'r').strip()
        try:
            if int(lic_num):
                max_bri = int(lic_num)
        except:
            pass

        #check max bridge munber limitation
        if bridge_list and len(bridge_list) == ray_int(max_bri):
            error_msg = 'bridge number reaches max license number:' + ray_str(max_bri)
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        #idx needs to be uniq
        if bridge_list:
            for b in bridge_list:
                if b.idx == mo.idx:
                    error_msg = 'bridge create faild : idx is exist!'
                    RAY_DEBUG(3, error_msg)
                    raise Exception(error_msg)

        #idx should be in correct range
        if mo.idx < BRIDGE_IDX_MIN or mo.idx > BRIDGE_IDX_MAX:
            error_msg = 'bridge create faild: idx out of range!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        #logic name should not be too long
        if len(mo.logicname) > 10:
            error_msg = 'bridge create faild: logicname name is too long!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        ret = Kbridge.add(mo.logicname)
        if ret != True:
            Kbridge.dele(mo.logicname)
            error_msg = 'bridge add error!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        Kbridge.set_mac_mtu(mo.logicname, mo.mtu)
        Kbridge.set_stp(mo.logicname, mo.stp)

        mo.mac = Kbridge.get_mac(mo.logicname)
        mo.mtu = ray_int(Kbridge.get_mtu(mo.logicname))
        mo.mode = 0

        if mo.admin_status is not None:
            mo.admin_status = ray_int(mo.admin_status)

        mo.port = ''
        mo.ref_cnt = 0

    def post_bridge_create(self, cm, ctx, mo):
        ret = Kbridge.set_status_byname(mo.logicname, mo.admin_status)
        #TODO
        #routesync.init()
        #proutesync.reload()

    def pre_bridge_update(self, cm, ctx, mo):

        bridge = cm.bridge_read(id=mo.id)
        if bridge is None:
            error_msg = "bridge " + str(mo.id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        #check whether comment is too long
        if mo.comment and len(ray_str(mo.comment)) > COMMENTLEN:
            error_msg = 'comment is to long'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if mo.idx is not None and ray_int(mo.idx) != ray_int(bridge.idx):
            #change idx
            b_list = cm.bridge_list(filter={
                "idx": ray_int(mo.idx)
            })
            if b_list:
                #new name already exist
                error_msg = 'bridx is exist!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)

            mo.idx = ray_int(mo.idx)

        if mo.logicname is not None and str(mo.logicname) and str(mo.logicname) != bridge.logicname:
            #this is the case to change name
            b_list = cm.bridge_list(filter={
                "logicname": str(mo.logicname)
            })

            if b_list:
                #new name already exist
                error_msg = 'brname is  exist!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)

            mo.logicname = str(mo.logicname)

        mo.physicalname = mo.logicname

        if mo.mtu is not None:
            Kbridge.set_mac_mtu(mo.logicname, ray_int(mo.mtu))
        if mo.stp is not None:
            Kbridge.set_stp(mo.logicname, ray_int(mo.stp))

        if mo.logicname is not None:
            mo.mac = Kbridge.get_mac(mo.logicname)
            mo.mtu = ray_int(Kbridge.get_mtu(mo.logicname))

        mo.mode = 0

        if mo.admin_status is not None:
            mo.admin_status = ray_int(mo.admin_status)

        mo.port = ''
        mo.ref_cn = 0

    def post_bridge_update(self, cm, ctx, mo):
        self.post_bridge_create()

    def pre_bridge_delete(self, cm, ctx, id):

        bridge = cm.bridge_read(id=id)
        if bridge:
            bp_list = cm.bridgeip_list(filter={
                "logicname": bridge.logicname
            })
            if bp_list:
                error_msg = 'bridge has ip address'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)


            t_list = cm.trunk_list()
            for item in t_list:
                if str(item.logicname).split('.')[0] == bridge.logicname:
                    error_msg = 'bridge is used by trunk !'
                    RAY_DEBUG(3, error_msg)
                    raise Exception(error_msg)

            p_list = cm.port_list(filter={
                "bridge": bridge.logicname
            })
            if p_list:
                error_msg = 'bridge has port!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)

            c_list = cm.channel_list(filter={
                "bridge": bridge.logicname
            })
            if c_list:
                error_msg = 'bridge has channel!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)

        else:
            error_msg = "bridge " + str(id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

    def post_bridge_delete(self, cm, ctx, id, mo):
        if mo:
            Kbridge.set_status_byname(mo.logicname, 0)
            Kbridge.dele(mo.logicname)
            RAY_DEBUG(3,"bridge " + str(mo.logicname) + " del success!")

###### Channel Function ######
    def pre_channel_create(self, cm, ctx, mo):
        #force int for idx
        mo.idx = 0
        mo.mtu = ray_int(mo.mtu, 1500)
        mo.stp = ray_int(mo.stp, 0)
        if ray_str(mo.logicname) == '' or ray_str(mo.logicname) == 'None':
            error_msg = 'name is not validate'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)
        mo.physicalname = ""

        #check whether comment is too long
        if mo.comment and len(ray_str(mo.comment)) > COMMENTLEN:
            error_msg = 'comment is to long'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        max_channel = CHANNEL_MAX
        channel_list = cm.channel_list()
        lic_num = kernel.k.ray_popen("/RayOS/utils/lictm -L |grep channel_maxnum |awk '{print $3}'",'r').strip()
        try:
            if int(lic_num):
                max_channel = int(lic_num)
        except:
            pass

        #check max channel munber limitation
        if channel_list and len(channel_list) == ray_int(max_channel):
            error_msg = 'channel number reaches max license number:' + ray_str(max_channel)
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if channel_list and len(channel_list) == 16:
            error_msg = 'the maximum channel number of channel is 16'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        #idx needs to be uniq
        idx_dict = {}
        if channel_list:
            for b in channel_list:
                if b.logicname == mo.logicname:
                    error_msg = 'channel create faild : {} exist!'.format(mo.logicname)
                    RAY_DEBUG(3, error_msg)
                    raise Exception(error_msg)

                idx_dict[b.idx] = b

        #logic name should not be too long
        if len(mo.logicname) > 16:
            error_msg = 'channel create faild: logicname name is too long!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        phyname = ''
        new_idx = 0
        for idx in range(0, max_channel):
            if idx not in idx_dict:
                #find available idx
                phyname = 'bond' + str(idx)
                new_idx = idx

                if not Kchannel.check(phyname):
                    error_msg = 'channel create faild: system internal error!'
                    RAY_DEBUG(3, error_msg)
                    raise Exception(error_msg)
                else:
                    break# the bond is available!

        ret = Kchannel.add(phyname)
        if not ret:
            error_msg = 'channel add  error!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        mo.idx = new_idx
        mo.physicalname = phyname
        mo.admin_status = ray_int(mo.admin_status, 1)
        mo.port = ''
        mo.ref_cnt = 0

    def post_channel_create(self, cm, ctx, mo):
        if mo.admin_status:
            Kchannel.set_status(mo.physicalname, 1)
        else:
            Kchannel.set_status(mo.physicalname, 0)

    def pre_channel_update(self, cm, ctx, mo):

        channel = cm.channel_read(id=mo.id)
        if channel is None:
            error_msg = "channel " + str(mo.id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        #check whether comment is too long
        if mo.comment and len(ray_str(mo.comment)) > COMMENTLEN:
            error_msg = 'comment is to long'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if mo.bridge is not None:
            #no change to current bridge, do nothing
            pass
        elif mo.bridge != channel.bridge:
            if channel.bridge:
                #TODO unlink channel and bridge
                pass

            if mo.bridge != 'none':
                #TODO link channel and bridge
                pass


        if mo.admin_status is not None:
            mo.admin_status = ray_int(mo.admin_status, 1)

    def post_channel_update(self, cm, ctx, mo):
        self.post_channel_create()

    def pre_channel_delete(self, cm, ctx, id):

        channel = cm.channel_read(id=id)
        if channel:
            p_list = cm.port_list(filter={
                "channel": channel.logicname
            })
            if p_list:
                error_msg = 'channel has port, del faild!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)

            if channel.bridge:
                error_msg = 'channel is used by bridge!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)
        else:
            error_msg = "channel " + str(id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

    def post_channel_delete(self, cm, ctx, id, mo):
        if mo:
            RAY_DEBUG(3,"channel " + str(mo.physicalname) + " del success!")

###### Trunk Function ######
    def webray_network_trunk_add_port(self, bridgename, port_name, idx):
        #webray_network_trunk_kcli_add_byname(port_name, idx);
        Ktrunk.add(port_name, idx)
        trunk_name = str(bridgename) + '.' + str(idx)
        trunk_port = str(port_name)  + '.' + str(idx)
        Ktrunk.add_if(trunk_name, trunk_port)
        #webray_network_vlan_kcli_add_if(trunk_name, trunk_port)
        Ktrunk.set_status_byname(trunk_port, 1)
        #webray_network_trunk_kcli_set_status_byname(trunk_port, 1)

    def webray_network_trunk_del_port(self, port_name, idx):
        trunk_port = str(port_name)  + '.' + str(idx)
        Ktrunk.dele(trunk_port)
        #webray_network_trunk_kcli_remove_byname(trunk_port)

    def webray_network_trunk_add_del_port(self, cm, bridgename, idx, flag):

        p_list = cm.port_list(filter={
            "bridge": bridgename
        })
        c_list = cm.channel_list(filter={
            "bridge": bridgename
        })

        for item in p_list:
            if flag:
                self.webray_network_trunk_add_port(bridgename, item.physicalname, idx)
            else:
                self.webray_network_trunk_del_port(item.physicalname, idx)

        for item in c_list:
            if flag:
                self.webray_network_trunk_add_port(bridgename, item.physicalname, idx)
            else:
                self.webray_network_trunk_del_port(item.physicalname, idx)

    def webray_network_trunk_tag(self, cm, trunkname, status):
        if not trunkname or '.' not in trunkname:
            return False
        bridgename = trunkname.split('.')[0]
        idx = trunkname.split('.')[1]
        if status:
            self.webray_network_trunk_add_del_port(cm, bridgename, idx, 0)

            Ktrunk.set_status_byname(trunkname,0)
            #webray_network_trunk_kcli_set_status_byname(trunkname,0)

            Ktrunk.delbr(trunkname)
            #webray_network_vlan_kcli_remove_byname(trunkname)

            #webray_network_trunk_kcli_add_byname(bridgename, idx)
            Ktrunk.add(bridgename, idx)

            #webray_network_trunk_kcli_set_status_byname(trunkname,1)
            Ktrunk.set_status_byname(trunkname,1)
        else:
            Ktrunk.dele(trunkname)
            #webray_network_trunk_kcli_remove_byname(trunkname)

            self.webray_network_trunk_add_del_port(cm, bridgename, idx, 0)

            Ktrunk.addbr(trunkname)
            #webray_network_vlan_kcli_add_byname(trunkname)

            self.webray_network_trunk_add_del_port(cm, bridgename, idx, 1)

            Ktrunk.set_status_byname(trunkname,1)
            #webray_network_trunk_kcli_set_status_byname(trunkname,1)
        return True

    def webray_network_trunk_kcli_restart(self, cm, trunkname, flag, admin_status):
        self.webray_network_trunk_tag(trunkname, flag)
        trunkip = cm.trunkip_list(filter={
            'logicname': trunkname
        })
        if trunkip:
            for item in trunkip:
                Ktrunk.add_ip(trunkname, item.ip, 1, item.id)
                try:
                    mgt = item.ismngtip
                    ip = item.ip
                    assert_name = "Mngt_" + ip.split('/')[0]
                    assert_name = assert_name.replace(":","-")
                    cmd = "/RayOS/scli/rayast add svr -name " + assert_name + " -ip " +  ip.split('/')[0]
                    kernel.k.ray_system(cmd)
                except:
                    pass
            Ktrunk.set_status_byname(trunkname,int(admin_status))

        return True

    def pre_trunk_create(self, cm, ctx, mo):
        #force int for idx
        mo.mtu = ray_int(mo.mtu, 1500)
        mo.flag = ray_int(mo.flag)

        #check whether comment is too long
        if mo.comment and len(ray_str(mo.comment)) > COMMENTLEN:
            error_msg = 'comment is to long'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if mo.logicname is None:
            error_msg = 'trunk name is not validate'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        brname = ""
        idx = 0
        try:
            brname = mo.logicname.split('.')[0]
            idx = ray_int(mo.logicname.split('.')[1])
        except:
            error_msg = 'trunk name is not validate'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if int(idx) < 1 or  int(idx) > 4095:
            error_msg = 'trunk idx must between 2-4094'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if brname == VLANNAME:
            error_msg = 'bridge name error'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        b_list = cm.bridge_list(filter={
            "logicname": brname
        })

        if not b_list:
            error_msg = 'bridge ' + str(brname) + " is not exist"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        t_list = cm.trunk_list(filter={
            "logicname": mo.logicname
        })

        if t_list:
            error_msg = mo.logicname +' is  exist'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        p_list = cm.port_list(filter={
            "bridge": brname
        })
        c_list = cm.channel_list(filter={
            "bridge": brname
        })

        if not p_list and not c_list:
            error_msg = brname + ' has no  interfaces!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        ret = self.webray_network_trunk_tag(cm, mo.logicname, 1)
        if not ret:
            error_msg = 'trunk create faild'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        mo.physicalname = mo.logicname
        mo.admin_status = ray_int(mo.admin_status)
        mo.idx = idx

    def post_trunk_create(self, cm, ctx, mo):
        if ray_int(mo.admin_status):
            Ktrunk.set_status_byname(mo.logicname,1)
        else:
            Ktrunk.set_status_byname(mo.logicname,0)
        self.webray_network_trunk_kcli_restart(cm, mo.logicname,ray_int(mo.flag),ray_int(mo.admin_status))

    def pre_trunk_update(self, cm, ctx, mo):

        trunk = cm.trunk_read(id=mo.id)
        if trunk is None:
            error_msg = "trunk " + str(mo.id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        #check whether comment is too long
        if mo.comment and len(ray_str(mo.comment)) > COMMENTLEN:
            error_msg = 'comment is to long'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if mo.logicname is not None and mo.logicname != trunk.logicname:
            error_msg = 'Can not change trunk name'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        mo.physicalname = mo.logicname
        if mo.admin_status is not None:
            mo.admin_status = ray_int(mo.admin_status, 1)

        if mo.flag is not None:
            mo.flag = ray_int(mo.flag, 1)

    def post_trunk_update(self, cm, ctx, mo):
        self.webray_network_trunk_kcli_restart(cm, mo.logicname,ray_int(mo.flag),ray_int(mo.admin_status))

    def pre_trunk_delete(self, cm, ctx, id):

        trunk = cm.trunk_read(id=id)
        if trunk:
            brname = str(trunk.logicname).split('.')[0]
            idx = int(trunk.idx)
            flag = trunk.flag

            trunkip = cm.trunkip_list(filter={
                "logicname": trunk.logicname
            })

            if trunkip:
                error_msg = trunk.logicname + ' has ip address'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)

            if flag:
                Ktrunk.set_status_byname(trunk.logicname, 0)
                #webray_network_trunk_kcli_set_status_byname(trunkname, 0)

                Ktrunk.dele(trunk.logicname)
                #webray_network_trunk_kcli_remove_byname(trunkname)
            else:
                Ktrunk.set_status_byname(trunk.logicname, 0)
                #webray_network_trunk_kcli_set_status_byname(trunkname,0)

                Ktrunk.delbr(trunk.logicname)
                #webray_network_vlan_kcli_remove_byname(trunkname)

                self.webray_network_trunk_add_del_port(brname, idx,0)
        else:
            error_msg = "trunk " + str(id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

###### Arp Function ######
    def is_valid_macaddr(self, addr):
        if not isinstance( addr, str):
            pass
        s = addr.split(':')
        if len(s) != 6:
            return False
        for item in s :
            if len(item) != 2 :
                return False
            for c in item:
                if( not ((c >= '0' and c <= '9') or (c >= 'a' and c <= 'f') or (c >= 'A' and c <= 'F' ) ) ):
                    return False
        return True

    def pre_arp_create(self, cm, ctx, mo):

        mo.ip = ray_str(mo.ip)
        mo.mac = ray_str(mo.mac)
        if get_ver_from_str(mo.ip) !=4 :
            error_msg = 'Invalid IP'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        mac = mo.mac.replace('-', ':')
        if not self.is_valid_macaddr(mac):
            error_msg = 'Invalid mac address'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        arplst = cm.apr_list(filter={
            "ip": mo.ip,
            "mac": mac
        })

        if(arplst):
            error_msg = "IP or MAC already exsists"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        ret = Karp.add(mo.ip, mac)
        if ret :
            error_msg = "Command excution wrong"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

    def pre_arp_update(self, cm, ctx, mo):

        arp = cm.arp_read(id=mo.id)
        if arp is None:
            error_msg = "arp " + str(mo.id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)


        mo.ip = ray_str(mo.ip)
        mo.mac = ray_str(mo.mac)
        if get_ver_from_str(mo.ip) !=4 :
            error_msg = 'Invalid IP'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        mac = mo.mac.replace('-', ':')
        if not self.is_valid_macaddr(mac):
            error_msg = 'Invalid mac address'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if Karp.delete(arp.ip):
            error_msg = "Command excution wrong"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)
        if Karp.add(mo.ip, mac):
            Karp.delete(mo.ip)
            Karp.add(arp.ip, arp.mac)
            error_msg = "Command excution wrong"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

    def pre_arp_delete(self, cm, ctx, id):
        arp = cm.arp_read(id=id)
        if arp:
            if Karp.delete(arp.ip):
                error_msg = "Command excution wrong"
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)
        else:
            error_msg = "arp " + str(id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

###### Dns Function ######
    def pre_dns_create(self, cm, ctx, mo):

        mo.dns1 = ray_str(mo.dns1)
        mo.dns2 = ray_str(mo.dns2)

        if not mo.dns1:
            error_msg = 'primary_dns is need!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        ip1_list = mo.dns1.split('.')
        if len(ip1_list)!=4:
            error_msg = 'wrong dns!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        for i in range(0,4):
            if ip1_list[i].isdigit():
                continue
            else:
                error_msg = 'wrong dns!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)

        dnsconfig = cm.dns_list()
        ret = Kdns.ray_system_dns_set(mo.dns1, mo.dns2)
        if not ret:
            error_msg = 'Command excution wrong!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if dnsconfig:
            res_obj = ctx.get('dm').update_resource(ctx, 'Dns', {
                "id": dnsconfig[0].id,
                "dns1": mo.dns1,
                "dns2": mo.dns2
            })
            if res_obj:
                return { "result": Dns.from_dict(**res_obj)}
        else:
            res_obj = ctx.get('dm').create_resource(ctx, 'Dns', {
                "dns1": mo.dns1,
                "dns2": mo.dns2
            })
            if res_obj:
                return { "result": Dns.from_dict(**res_obj)}

    def pre_dns_update(self, cm, ctx, mo):
        return self.pre_dns_create()

    def pre_dns_delete(self, cm, ctx, id):
        error_msg = 'Dns can not be deleted!'
        RAY_DEBUG(3, error_msg)
        raise Exception(error_msg)

###### Ruote Function ######
    def pre_route_create(self, cm, ctx, mo):

        mo.metric = ray_int(mo.metric)
        mo.ip = ray_str(mo.ip)
        mo.gateway = ray_str(mo.gateway)
        if get_ver_from_str(mo.ip) == 0:
            error_msg = 'Invalid IP'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        if get_ver_from_str(mo.gateway) == 0:
            error_msg = 'Invalid Gateway'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)


        if (get_ver_from_str(mo.ip) == 6 and (not mo.ifname) ):
            mo.ifname = ""
        if (get_ver_from_str(mo.ip) == 6 and (not mo.metric ) ):
            mo.metric = 1

        routlist = cm.route_list(filter={
            "ip": mo.ip,
            "gateway": mo.gateway,
            "metric": mo.metric
        })

        if(routlist):
            error_msg = 'route rule already exist!'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)

        ret = Kroute.route_add(ip = mo.ip , gateway=mo.gateway, metric= mo.metric, ifname=mo.ifname)
        if not ret:
            error_msg = 'gateway wrong'
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)
        pip = mo.ip.split('/')[0]

        temp = Kroute.route_query(ip = pip , gateway = mo.gateway, metric = mo.metric, ifname='')

        if not mo.ifname :
            if not temp :
                Kroute.route_del(ip = mo.ip, gateway = mo.gateway, metric = mo.metric, ifname = '')
                error_msg = 'system internal error'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)
            else :
                mo.ifname = temp

    def pre_route_update(self, cm, ctx, mo):
        error_msg = 'Route does not support update, please delete and re-add!'
        RAY_DEBUG(3, error_msg)
        raise Exception(error_msg)

    def pre_route_delete(self, cm, ctx, id):
        route = cm.route_read(id=id)
        if route:
            try :
                metric = int(route.metric)
            except :
                metric = 0

            ret = Kroute.route_del(ip = route.ip ,  gateway = route.gateway, metric = metric, ifname='')
            if not ret:
                error_msg = 'gateway wrong!'
                RAY_DEBUG(3, error_msg)
                raise Exception(error_msg)
        else:
            error_msg = "route " + str(id) +  " is not exist!"
            RAY_DEBUG(3, error_msg)
            raise Exception(error_msg)