from sharder import Sharder
from unittest import TestCase

class TestSharding(TestCase):

    def test_empty_instances_numeric(self):
        servers = [
                {'name': 'local-server-1', 'host': '127.0.0.1', 'port': 6379, 'db': 0},
                {'name': 'local-server-2', 'host': '127.0.0.1', 'port': 6380, 'db': 0}
        ]
        s = Sharder(servers)
        assert {'local-server-2': 0, 'local-server-1': 0} == s.keys(numeric=True)

    def test_empty_instances_non_numeric(self):
        servers = [
                {'name': 'local-server-1', 'host': '127.0.0.1', 'port': 6379, 'db': 0},
                {'name': 'local-server-2', 'host': '127.0.0.1', 'port': 6380, 'db': 0}
        ]
        s = Sharder(servers)
        assert {'local-server-2': [], 'local-server-1': []} == s.keys(numeric=False)

    def test_empty_instances_set(self):
        servers = [
                {'name': 'local-server-1', 'host': '127.0.0.1', 'port': 6379, 'db': 0},
                {'name': 'local-server-2', 'host': '127.0.0.1', 'port': 6380, 'db': 0}
        ]
        s = Sharder(servers)
        s.set('a_key', 'a_value')
        keys = s.keys(numeric=True)
        assert 1 == (keys.get('local-server-2', 0) + keys.get('local-server-1', 0))
        keys = s.keys(numeric=False)
        try:
            got = keys['local-server-2'][0]
            assert got == 'a_key'
        except:
            got = keys['local-server-1'][0]
            assert got == 'a_key'
