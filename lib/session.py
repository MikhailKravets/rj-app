"""

Here must be laid classes and functions of managing of client sessions.

"""
import redis


class HashSession:
    """
    The wrapper that easily manages of sessions through Redis
    """

    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379)

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        name = f"sessoin:{value}"
        # self.redis.set(name, value)
