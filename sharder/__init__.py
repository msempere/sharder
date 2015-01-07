import redis
import functools
from commands import REDIS_COMMANDS
from hashring import HashRing


class HashMethod(object):
    CRC32 = 'crc32'
    MD5 = 'md5'
    SHA1 = 'sha1'


class Sharder(object):
    def __init__(self, servers, hash_method=HashMethod.CRC32):
        self.connections = {}
        self.nodes = []

        for connection in servers:
            server_name = connection['name']
            self.connections[server_name] = redis.StrictRedis(connection['host'], connection['port'], connection['db'])
            self.nodes.append(server_name)

        self.ring = HashRing(self.nodes, hash_method=hash_method)


    def __wrap(self, method, *args, **kwargs):
        try:
            key = args[0]
            assert isinstance(key, basestring)
        except:
            raise ValueError("method '%s' requires a key param as the first argument" % method)
        server = self.get_server(key)
        f = getattr(server, method)
        return f(*args, **kwargs)


    def get_server_name(self, key):
        return self.ring.get_node(key)


    def get_server(self, key):
        name = self.get_server_name(key)
        return self.connections[name]


    def __getattr__(self, method):
        if method in REDIS_COMMANDS:
            return functools.partial(self.__wrap, method)
        else:
            raise Exception("Operation '%s' does not exist" % method)


    def keys(self, numeric=True):
        keys = {}
        for node in self.nodes:
            server = self.connections[node]
            if server:
                keys[node] = int(server.dbsize()) if numeric else server.keys()
        return keys

