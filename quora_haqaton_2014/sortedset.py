import socket
import sys
import os
import threading
from struct import unpack, pack
from operator import itemgetter
from heapq import heappush, heappop

server_address = './socket'
OK = 0

class StreamScore(object):

    def __init__(self, stream, key, value):
        self.stream = stream
        self.key = key
        self.value = value

    def __lt__(self, other):
        if self.key == other.key:
            return self.value < other.value
        return self.key < other.key

    def __le__(self, other):
        if self.key == other.key:
            return self.value <= other.value
        return self.key <= other.key


    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return self.key != other.key

    def __gt__(self, other):
        if self.key == other.key:
            return self.value > other.value
        return self.key > other.key

    def __ge__(self, other):
        if self.key == other.key:
            return self.value >= other.value
        return self.key >= other.key
    
    def __repr__(self):
        return "(%s: %s, %s)" % (self.stream, self.key, self.value)
        
def k_way_merge(streams):
    response = []
    heap = []

    for i, stream in enumerate(streams):
        if stream:
            key, value = stream.pop(0)
            heappush(heap, StreamScore(i, key, value))
    
    while heap:
        next = heappop(heap)
        print >>sys.stderr, "k-way: heap = %s" % heap
        response.append((next.key, next.value))
        print >>sys.stderr, "k-way: response = %s" % response

        if streams[next.stream]:
            key, value = streams[next.stream].pop(0)
            heappush(heap, StreamScore(next.stream, key, value))

    return response

def within(x, lower, upper):
    return (x >= lower) and (x <= upper)

class SortedSet(object):
    
    def __init__(self):
        self.sets = {}
        self.sets_lock = threading.Lock()
        self.lock_set = {}
        
        self.operations = {1: self.put, 
                           2: self.remove, 
                           3: self.get_size, 
                           4: self.get, 
                           5: self.get_range}
        
    def _get_set(self, id):
        with self.sets_lock:
            if id not in self.sets:
                self.sets[id] = {}
                self.lock_set[id] = threading.Lock()
        
        return self.sets[id]
        
    def apply(self, command):
        return self.operations[command[0]](command)
    
    def put(self, command):
        set_id = command[1]
        key = command[2]
        score = command[3]
        
        current_set = self._get_set(set_id)
        
        with self.lock_set[set_id]:
            current_set[key] = score        
        
        return OK
    
    def remove(self, command):
        set_id = command[1]
        key = command[2]
        
        current_set = self._get_set(set_id)
        
        with self.lock_set[set_id]:
            if key in current_set:
               current_set.pop(key)
        
        return OK
        
    def get_size(self, command):
        set_id = command[1]
        
        current_set = self._get_set(set_id)
        
        with self.lock_set[set_id]:
            size = len(current_set)
        
        return [size]
    
    def get(self, command):
        set_id = command[1]
        key = command[2]
        
        current_set = self._get_set(set_id)
        
        score = 0
        with self.lock_set[set_id]:
            if key in current_set:
                score = current_set[key]

        return [score]
    
    def get_range(self, command):
        sets = []
        id = None
        i = 1
        while id != 0:
            id = command[i]
            i += 1
            if id != 0:
                sets.append(id)
                
        lower = command[i]
        upper = command[i+1]
        
        print >>sys.stderr, "range sets: %s" % sets
        
        # extracting sorted tuples from each set
        all_valid_items = []
        for set_id in sets:
            current_set = self._get_set(set_id)
            
            print >>sys.stderr, "> %s" % set_id
            
            with self.lock_set[set_id]:
                current_set_items = [(k, v) for k, v in current_set.iteritems() if within(v , lower, upper)]
                
            print >>sys.stderr, "items: %s" % current_set_items
            
            current_set_items.sort(key=itemgetter(0))
            all_valid_items.append(current_set_items)
            print >>sys.stderr, "all items: %s" % all_valid_items
        
        tuples = k_way_merge(all_valid_items)
        
        print >>sys.stderr, tuples
        
        flat_list = []
        for tuple in tuples:
            flat_list += list(tuple)
            
        print >>sys.stderr, flat_list
        
        return flat_list
    
    
class ConnectionHandler(threading.Thread):
    def __init__(self, connection, sorted_set):
        super(ConnectionHandler, self).__init__()
        self.connection = connection
        self.sorted_set = sorted_set
        
    def run(self):
        i = 0
        while True:
            header = unpack('!L', self.connection.recv(4))[0] # unpack's result is a tuple, even it's a single value
            print >>sys.stderr, '[handler %s] received %s - %s' % (self.name, header, type(header))
        
            command = []
            for _ in range(header):
                command.append(unpack('!L', self.connection.recv(4))[0])

            # check 'disconnect' command
            if command[0] == 6:
                break
             
            data = self.sorted_set.apply(command)
            
            if data == OK:
                self.connection.send(pack('!L', OK))
            else:                    
                self.connection.send(pack('!L', len(data)))
                for n in data:
                    self.connection.send(pack('!L', n))
            
        # Clean up the connection
        self.connection.close()

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)
        
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    conn, client_address = sock.accept()

    print >>sys.stderr, 'connection ', conn

    sorted_set = SortedSet()
    handler = ConnectionHandler(conn, sorted_set)
    handler.start()
    
    