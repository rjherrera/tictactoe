from datetime import datetime


def time(message):
    def decorator(function):
        def wrapper(*args, **kwargs):
            i = datetime.now()
            value = function(*args, **kwargs)
            print(message, datetime.now() - i)
            return value
        return wrapper
    return decorator
