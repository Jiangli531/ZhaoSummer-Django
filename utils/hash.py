import hashlib


def hash_code(s, salt='ZhaoSummer'):  # generate s+salt into hash_code
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update method get bytes(type)
    return h.hexdigest()

