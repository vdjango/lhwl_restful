
def logger(func):
    def inner(*args, **kwargs):
        request = args[0]
        print("DEBUG: %s, %s" % (request.build_absolute_uri(), kwargs))
        return func(*args, **kwargs)  # 2

    return inner
