# ssdclient3 (Claude.ai fix)

import socket
import time

MULTICAST_ADDR = "224.0.0.251"
MULTICAST_PORT = 33335
SSDP_ADDR = (MULTICAST_ADDR, MULTICAST_PORT)
SERVICE_TYPE = "urn:schemas-upnp-org:service:SampleService:1"

M_SEARCH = """M-SEARCH * HTTP/1.1
HOST: 224.0.0.251:33335
MAN: "ssdp:discover"
MX: 2
ST: {service_type}

"""

def send_ssdp_message(sock, message):
    sock.sendto(message.encode(), SSDP_ADDR)

def discover_service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	# Need to reuse socket address with SO_REUSEADDR option
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	# Need to use IP_MULTICAST_LOOP to allow Client to receive locally
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    
    # Bind to the multicast port
    sock.bind(('', MULTICAST_PORT))
    
    # Join the multicast group
    mreq = socket.inet_aton(MULTICAST_ADDR) + socket.inet_aton('0.0.0.0')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    # Set a timeout
    sock.settimeout(8)  # 5 seconds timeout # JB: set timeout to 8

    m_search = M_SEARCH.format(service_type=SERVICE_TYPE)
    send_ssdp_message(sock, m_search)
    print("Sent M-SEARCH request for service type:", SERVICE_TYPE)

    # Wait for responses
    while True:
        try:
            print("Waiting for receive")
            data, addr = sock.recvfrom(1024)
            print(addr)
            print("Received response from:", addr)
            print(data.decode())
        except socket.timeout:
            print("Socket timeout")
            break
        except KeyboardInterrupt:
            print("Program interrupted")
            break			

if __name__ == "__main__":
    discover_service()