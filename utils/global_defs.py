def response_data(message: str = None, data=[], json_additional={}):
    result = {'message': message}
    for key, value in json_additional.items():
        result[key] = value
    result['data'] = data
    return result
