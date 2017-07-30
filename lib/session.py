"""

Here must be laid classes and functions of managing of client sessions.

"""
from lib import __Meta
import random
import redis


class HashSession(metaclass=__Meta):
    """
    The wrapper that easily manages of sessions through Redis
    """

    def __init__(self, host='localhost', port=6379):
        self.redis = redis.StrictRedis(host=host, port=port)

    def __getitem__(self, key):
        """
        :param key: must be random string of hex number (preferably the length of 32 or 64).
        :return: Python's ``dict`` if found; else None
        """
        key = f"session:{key}"
        value = self.redis.hgetall(key)
        if len(value) == 0:
            return None
        else:
            value = {k.decode('utf8'): v.decode('utf8') for k, v in value.items()}
            return value

    def __setitem__(self, key, value):
        """
        Set the given dict (**value**) to the next key: ``session:{**key**}``

        :param key: must be random string of hex number (preferably the length of 32 or 64).
        :param value: the dict that must be saved in the hash.
            Preferably to have following format:
            ``{'login': '...', 'email': '...', 'access': '...'}``
        """
        name = f"session:{key}"
        self.redis.hmset(name, value)
        self.redis.expire(name, 600)

    @staticmethod
    def gen_key(length=64):
        return f"{random.randrange(16**length):0{length}x}"
