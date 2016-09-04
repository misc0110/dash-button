import socket
import subprocess
import sys
       
BUTTON = "ac63be5aea19" # change this to your mac for the demo



buttons = {}

def add_handler(mac, handler):
    buttons[mac.replace(":", "")] = handler

def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("0.0.0.0", 443))
    serversocket.listen(5)

    while True:
        # wait for connection
        connection, addr = serversocket.accept()
        address = addr[0]
        # dash button closes it anyways, to close it to maybe save battery
        connection.close()
        
        # get dash button's mac address
        cmd="arp -a"
        mac = None
        p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output, errors = p.communicate()
        if output is not None :
            if sys.platform in ['linux','linux2']:
                for i in output.split("\n"):
                    if address in i:
                        for j in i.split():
                            if ":" in j:
                                mac = j
            elif sys.platform in ['win32']:
                item =  output.split("\n")[-2]
                if address in item:
                    mac = item.split()[1]
        
        mac_raw = mac.replace(":", "")
        if mac_raw in buttons:
            buttons[mac_raw](mac)
    

def demo_print(mac):
    print("%s pressed" % (mac))
    
if __name__ == "__main__":
    add_handler(BUTTON, demo_print)
    listen()