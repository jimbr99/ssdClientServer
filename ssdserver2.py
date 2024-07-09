import socket
import time

# Service information
SERVICE_TYPE = "urn:schemas-upnp-org:service:SampleService:1"
SERVICE_UUID = "uuid:12345678-1234-1234-1234-123456789abc"
SERVICE_LOCATION = "http://192.168.1.100:8080/description.xml"

# SSDP constants
MULTICAST_ADDR =  "224.0.0.251"  #"239.255.255.250"
MULTICAST_PORT = 33335 #3333 #5000 #1900
SSDP_ADDR = (MULTICAST_ADDR, MULTICAST_PORT)

# SSDP message templates
NOTIFY_ALIVE = """NOTIFY * HTTP/1.1
HOST: 224.0.0.251:33335 # 239.255.255.250:1900
CACHE-CONTROL: max-age=1800
LOCATION: {location}
NT: {service_type}
NTS: ssdp:alive
SERVER: Sample SSDP Server/1.0
USN: {usn}

"""

NOTIFY_BYEBYE = """NOTIFY * HTTP/1.1
HOST: 224.0.0.251:33335 #239.255.255.250:1900
NT: {service_type}
NTS: ssdp:byebye
USN: {usn}

"""

def send_ssdp_message(sock, message):
    sock.sendto(message.encode(), SSDP_ADDR)

def advertise_service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, socket.IP_ADD_MEMBERSHIP)

    notify_alive = NOTIFY_ALIVE.format(location=SERVICE_LOCATION,
                                       service_type=SERVICE_TYPE,
                                       usn=SERVICE_UUID + "::" + SERVICE_TYPE)

    while True:
        send_ssdp_message(sock, notify_alive)
        time.sleep(6)  # Send NOTIFY messages every 60 seconds; JB 60 to 6
        print("sending NOTIFY") # JB

if __name__ == "__main__":
    print("Starting SSDP service advertisement...")
    advertise_service()