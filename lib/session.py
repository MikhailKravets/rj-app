"""

Here must be laid classes and functions of managing of client sessions.

"""
import config
import random
import redis
from lib import __SingletonMeta


class HashSession(metaclass=__SingletonMeta):
    """
    The singleton wrapper that easily manages of sessions through Redis.

    """

    def __init__(self, host=config.REDIS_ATTR['host'], port=config.REDIS_ATTR['port']):
        """
        The key of session in the Redis has the next pattern: `session:{key}`
        where `key` is random hexadecimal number.

        ====================================
        How to use
        ====================================

        In order to check if key exists in the Redis, use the following syntax:
        key **in** session.

        Example::

            # get session object
            session = HashSession()
            # check if Redis contains key
            if key in session:
                pass

        For key generation static method `HashSession.gen_key(length=64)` can be used.

        In order to get or set session object you can use ``dict`` syntax.

        Get session example::

            # get session dict
            dictionary = session[key]

        Set session example::

            session[key] = {
                    'id': '...'
                    'login': '...',
                    'email': '...',
                    'access': '...'
                }

        It is preferable to pass into session the following dictionary:
        ``{'id': '...', 'login': '...', 'email': '...', 'access': '...', 'activated': '{0 or 1}'}``.
        But you can invent your own session object format.
        """
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

        :param key: must be random string of hex number (preferably the length of 64).
        :param value: the dict that must be saved in the hash.
            Preferably to have following format:
            ``{'id': '...', 'login': '...', 'email': '...', 'access': '...', 'activated': '{0 or 1}'}``
        """
        name = f"session:{key}"
        self.redis.hmset(name, value)
        self.redis.expire(name, 600)

    def __contains__(self, key):
        return self.redis.exists(f"session:{key}")

    @staticmethod
    def gen_key(length=64):
        """

        :param length:
        :return:
        """
        return f"{random.randrange(16**length):0{length}x}"
