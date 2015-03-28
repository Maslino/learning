# coding=utf8
import hashlib


def md5_hex(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


if __name__ == "__main__":
    print md5_hex('hello, world')
