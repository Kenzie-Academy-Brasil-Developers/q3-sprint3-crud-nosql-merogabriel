def verify_types(payload: dict):
    if (type(payload['title']) == str and
        type(payload['author']) == str and
        type(payload['content']) == str and
        type(payload['tags']) == list and
        len(payload) == 4):

        return True
    else:
        return False


def verify_patch_request(payload: dict):
    str_keys = ['title', 'author', 'content']

    for key in payload.keys():
        if key not in str_keys and key != 'tags':
            return False

    for key, value in payload.items():
        if key in str_keys and type(value) != str:
            return False
        elif key == 'tags' and type(value) != list:
            return False
    
    return payload