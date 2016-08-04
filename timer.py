import time

def timer(func):
    def decorator(*args, **kw):
        p = time.time()
        res = func(*args, **kw)
        n = time.time()
        print '%r (%r, %r) %2.2f sec' % (func.__name__, args, kw, n-p)
        return res
    return decorator
