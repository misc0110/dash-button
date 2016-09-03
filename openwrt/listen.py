import socket
import subprocess
import sys
            
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
    
    print(mac)
    # do something depending on mac address