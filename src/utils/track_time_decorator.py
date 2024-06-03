import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start tracking time
        result = func(*args, **kwargs)
        end_time = time.time()  # End tracking time
        execution_time = end_time - start_time  # Calculate execution time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result, execution_time
    return wrapper