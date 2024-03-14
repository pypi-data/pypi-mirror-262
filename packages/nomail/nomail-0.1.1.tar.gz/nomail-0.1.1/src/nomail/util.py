def split_bytes(byte_str):
    return byte_str.split(b' ') if byte_str else []


def to_int(collection):
    return [int(item) for item in collection]
