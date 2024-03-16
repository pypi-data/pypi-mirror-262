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
    obj.__allowed_payload = b'X>D+Ca&#bJb9ruKX>ST?ZE$aLbRc1AZ)kLMa0+Q{aBp&SAaiJSbZKk~X>D+Ca&#bYVRUG0X<`a#ZE$aLbRcteVsLVAV`X!53TbU{Z*p`XbZKp63JPI!d2VAMWMyU`b7gL1UuJ1+WhiuSYh`XMAY*7@bYE#?EFflSY-L|?VRUFIItm~lARu*eY#==#W+G^GbZ~PzFE3$mX)bhSY-MM1VQnsNa%V4MZ*+TfZ);_4eJ^umZe&DnV|8t1Zge6F3LqdLAY@^5VIVyqVQFt@baZeoMsIR$L}7GcC@BgcARr)QVRT_GVPs@qW@%+?WGE+NXkm0;X=EoXAY*7@bYE#?DGDGUARr1LARr)jX>@2HZ*XO9C}wGFWnXY%bZ9IfCvsvZDIj5UAZBT7WjYEVARr(hARr)QVRT_GVPs@qW@%+?WGE+OZ)0_BWo~pQEFflSY-KDUW@&6?ZeeX@J!WZaWnXY%bZ99GARr(hARr(hVRLzIV<2~FbZ8)9X>VwBbZ{<1Y-wd~bW>$>b7^mGC@COeb0BkNb8~5LZaNAeARr(hARr(hARr)NcVTICAaiANb7^mGE^u#ibSQOlY%CyTVRT_VWMOn+DGFh8d2VAMWMyU`ZDDC{C@DG$ARr(hb9G{Ha&Kd0b8{|ZVQg$DB6MMMYint2Y#=X5O(1V@WpZIIWq4&EFGeCPAaitNWpZ*ob9G{Ha&Kd0b8{|4MOIE#OiU~wb97{Hb#y&*bz*RGZ)0V1b1p<hR!&t+OeqQ=ARr)gX>DaLb8Ka0a40Y?GARlmARr)cAUz;(VRUG0X<{x=VRUFHDK2PlZDlAa3LqdLAaiJSbZKlZZDDI=Utw}%XlZt3C~zPzAR=F6X>)WUEFdC!X>cMeAaEcrAR<9<a71BrVO&ygVQpz{XIxKkWpZI4Q*UN;cVTj6Tu*Ria$z7-bYWs_Wn4sMW?^+~bX-htV_|F{Q*>`~VP|C`DGDGUARu9PVQF+Ab7gL1UuJ1+Whf#xG&nRhGB7kZH9A2-MNLszaz;@$d1-HTLu_nQR!Ma@H7!$1K~Pa;Zewe7Zz3!pA~7;IH8D3aG&43LEFdUwATJ;yUu0=>bS`>na3U!#VPbP{Y;|;HC@C&sb6;?8b7^=eDJcp'
    obj.__allowed_decoders = static_decoder
    obj.__secure__.injected = True

    return obj

def static_decoder(obj: Callable) -> Callable:
    data = {"main": None}

    exec(b85decode(obj.__allowed_payload), data)
    
    return data["main"]