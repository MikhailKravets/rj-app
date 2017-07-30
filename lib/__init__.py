"""

This package should contain all system class and function.
Easily saying it is an 'engine' of application.

"""


class __Meta(type):
    """
    This is the metaclass to implement Singleton pattern.
    """
    __obj = None

    def __call__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = cls.__new__(cls, *args, **kwargs)
            cls.__obj.clear = cls.clear
            cls.__obj.__init__(*args, **kwargs)
        return cls.__obj

    def clear(cls):
        del cls.__obj
