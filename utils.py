def dict_to_list(d):
    result = {}
    for key, value in d.items():
        if not isinstance(value, dict): 
            result[key] = value.pop()
        else:
            result[key] = dict_to_list(value)
    return result


def parse(key):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            forecast = func(*args, **kwargs)
            result = []
            while forecast[key]:
                result = [dict_to_list(forecast)] + result
            return result
        return wrapped
    return wrapper




