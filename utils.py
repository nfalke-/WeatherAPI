from functools import reduce
import operator

def get_from_dict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def dict_to_list(d):
    result = {}
    for key, value in d.items():
        if not isinstance(value, dict):
            result[key] = value.pop()
        else:
            result[key] = dict_to_list(value)
    return result


def parse(keys):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            forecast = func(*args, **kwargs)
            result = []
            if not keys:
                return [forecast]
            while get_from_dict(forecast, keys):
                result = [dict_to_list(forecast)] + result
            return result
        return wrapped
    return wrapper
