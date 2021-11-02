from network.gen.conf_manager import ConfigManager

cm = ConfigManager()
print cm.port_read(11)
print [ item.to_dict() for item in cm.port_list()]
print cm.port_delete(1)
print [ item.to_dict() for item in cm.port_list()]

print cm.port_update({
    "id": 2,
    "comment": "test1"
}).to_dict()
if True:
    print cm.port_create({
        "comment": "test",
        "idx": 1,
        "physicalname": "eth1"
    }).to_dict()


