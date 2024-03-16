from multiprocessing import Pool, cpu_count

from aiokadiapi.mp.static import secure_wrap

def run_in_pool(func, obj):
    func = secure_wrap(func)

    with Pool(cpu_count()) as p:
        data = p.map(func, obj)

    return data, func.__allowed_decoders(func)