import multiprocessing.pool
import functools

def timeout(s):
    """
    Decorator function to timeout a process after s seconds
    """
    def timeout_decorator(item):
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # Raise a timeout error if it takes too long
            return async_result.get(s)
        return func_wrapper
    return timeout_decorator
