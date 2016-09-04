import sys
import paho.mqtt.client as mqtt
try:
    import urllib2
except:
    pass
try:
    import urllib.request
except:
    pass

class DashIoTConnector:
    OBSERVER = 1
    SERVER = 2
        
class DashIoTProtocol:
    HTTP = 1
    MQTT = 2

class DashIoT(object):
    Connector = DashIoTConnector()
    Protocol = DashIoTProtocol()
    
    def __init__(self, connector, protocol):
        if connector == self.Connector.OBSERVER:
            sys.path.insert(0, 'observer')
        elif connector == self.Connector.SERVER:
            sys.path.insert(0, 'openwrt')
        else:
            print("Error! Unknown connector")
            return
        
        if protocol == self.Protocol.MQTT:
            self.client = mqtt.Client()
        
        self.prot = protocol
        self.callbacks = {}
    
    
    def publish_handler(self, mac, handler):
        self.callbacks[mac.replace(":", "")] = handler
        
    
    def callback(self, mac):
        ret = self.callbacks[mac.replace(":", "")](mac)
        if isinstance(ret, tuple):
            topic = ret[0]
            msg = ret[1]
        else:
            topic = "dash"
            msg = ret
            
        if self.prot == self.Protocol.MQTT:
            self.client.publish(topic, msg, 1)
            
        if self.prot == self.Protocol.HTTP:
            try:
                urllib2.urlopen(self.host + "?" + topic + "=" + msg).read()
            except:
                pass
            try:
                urllib.request.urlopen(self.host + "?" + topic + "=" + msg).read()
            except:
                pass
    

    def connect(self, host, port = 1883):
        if self.prot == self.Protocol.MQTT:
            self.client.connect(host, port, 60)
        elif self.prot == self.Protocol.HTTP:
            self.host = host
            
        
    def run(self):
        import listen
        
        for cb in self.callbacks.keys():
            listen.add_handler(cb, self.callback)
        listen.listen()
        
    