# coding=utf8
import hashlib


def md5_hex(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def sha1_hex(data):
    m = hashlib.sha1()
    m.update(data)
    return m.hexdigest()


if __name__ == "__main__":
    print md5_hex('hello, world')
    print sha1_hex('hello, world')
