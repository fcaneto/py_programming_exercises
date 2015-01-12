import socket
import sys
import struct

def write_all(sock):
    with open("input") as f:

        for line in f:
            command = line.strip().split()
            print command

            sock.send(struct.pack('!L', int(len(command))))

            for n in command:
                m = struct.pack('!L', int(n))
                sent = sock.send(m)

def read_all(sock):
    i = 0
    while True:
        m = struct.unpack('!L', sock.recv(4))
        print "%s : m


# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = './socket'
print >>sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect(server_address)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:
    write_all(sock)
    print "------------------------"
    read_all(sock)
    
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

