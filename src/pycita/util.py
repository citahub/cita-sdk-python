"""
定义一些基础工具.
"""
from typing import Union, List
from binascii import hexlify, unhexlify
from eth_abi import encode_single, decode_single


PARAM = Union[str, bytes]  # 用于CitaClient方法的参数类型. 如果是str, 默认都具有'0x'前缀
DEFAULT_QUOTA = 10000000  # 默认调用每个合约方法所消耗的quota上限.
LATEST_VERSION = 2  # 默认的区块链版本号.


def param_to_str(p: PARAM) -> str:
    """将PARAM统一到str形式."""
    assert (isinstance(p, str) and p.startswith('0x')) or isinstance(p, bytes)
    return p if isinstance(p, str) else f'0x{hexlify(p).decode()}'


def param_to_bytes(p: PARAM) -> bytes:
    """将PARAM统一到bytes形式."""
    assert (isinstance(p, str) and p.startswith('0x')) or isinstance(p, bytes)
    return p if isinstance(p, bytes) else unhexlify(p[2:])


def join_param(*param_list) -> str:
    """
    用于拼接多个PARAM类型.

    :param param_list: 参数列表. 如果某个元素是str, 则开头必须是'0x'
    :return: 拼接后的字符串
    """
    if not param_list:
        return ''

    # 参数中有str, 返回str类型
    ret: List[str] = ['0x']
    for i in param_list:
        if isinstance(i, bytes):
            ret.append(hexlify(i).decode())
        elif isinstance(i, str):
            assert i[:2] == '0x'
            ret.append(i[2:])
        else:
            assert 0
    return ''.join(ret)


def equal_param(lhs: PARAM, rhs: PARAM) -> bool:
    """判断两个参数的内容是否相同."""
    if type(lhs) is type(rhs):
        return lhs == rhs
    return param_to_bytes(lhs) == param_to_bytes(rhs)


def encode_param(types: str, values) -> bytes:
    r"""
    返回参数编码后的字符串.

    :param types, values: 参考eth_abi.encode_single的文档.
    :return: 如b'\x0b\xad\xf0\x0d'...
    """
    if not types:
        return b''

    if types[0] != '(':
        types = f'({types})'

    if isinstance(values, tuple):
        return encode_single(types, values)
    else:
        return encode_single(types, (values,))


def decode_param(types: str, bin: bytes):
    """
    返回解码后的python类型的数据.

    :param types, values: 参考eth_abi.decode_single的文档
    :return: python类型的数据. 如果包含2个以上的值, 返回Tuple. 如果只有一个值, 则解开Tuple
    """
    if (not types) or types[0] != '(':
        types = f'({types})'
    ret = decode_single(types, bin)
    if len(ret) == 0:
        return ()
    return ret if len(ret) >= 2 else ret[0]
