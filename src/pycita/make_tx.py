from typing import Dict, Tuple
import random
import string

import sha3
from ecdsa import SigningKey, SECP256k1
from secp256k1 import PrivateKey

from .blockchain_pb2 import Transaction, UnverifiedTransaction, Crypto
from .util import param_to_str, param_to_bytes


class SignerBase:
    def __init__(self, version: int = 2, chain_id: int = 1):
        if version not in (0, 1, 2):
            raise NotImplementedError(f'unexpected version {version}')
        self.version = version
        self.chain_id = chain_id

    def generate_account(self, private_key: bytes = b'') -> Tuple[str, str, str]:
        """
        生成账户的地址和密钥对.

        :param private_key: 私钥. 如果为空, 则重新生成, 否则从私钥还原.
        :return: (私钥, 公钥, 账户地址)
        """
        raise NotImplementedError('virtual method')

    def make_raw_tx(self, private_key: bytes, receiver: bytes, bytecode: bytes, valid_until_block: int, value: int, quota: int) -> bytes:
        """
        对交易数据进行签名.

        :param private_key: 私钥.
        :param receiver: 接收方地址. 如果是合约部署, 则为b''.
        :param bytecode: 字节码.
        :param valid_until_block: 交易的最后期限. 默认为当前区块高度+88
        :param value: 金额.
        :param quota: 调用配额.
        :return: 签名后的bytes.
        """
        raise NotImplementedError('virtual method')


# 目前支持两种加密方法 secp256k1, ed25519
class SignerSecp256k1(SignerBase):
    def __init__(self, version: int = 2, chain_id: int = 1):
        super().__init__(version, chain_id)

    def generate_account(self, private_key: bytes = b'') -> Tuple[str, str, str]:
        """
        生成账户的地址和密钥对.

        :param private_key: 私钥. 如果为空, 则重新生成, 否则从私钥还原.
        :return: (私钥, 公钥, 账户地址)
        """
        keccak = sha3.keccak_256()
        if private_key == b'':
            priv = SigningKey.generate(curve=SECP256k1)
        else:
            priv = SigningKey.from_string(private_key, curve=SECP256k1)

        pub = priv.get_verifying_key().to_string()

        keccak.update(pub)
        address = '0x' + keccak.hexdigest()[24:]

        return param_to_str(priv.to_string()), param_to_str(pub), address

    def make_raw_tx(self, private_key: bytes, receiver: bytes, bytecode: bytes, valid_until_block: int, value: int, quota: int) -> bytes:
        """
        对交易数据进行签名.

        :param private_key: 私钥.
        :param receiver: 接收方地址. 如果是合约部署, 则为b''.
        :param bytecode: 字节码.
        :param valid_until_block: 交易的最后期限. 默认为当前区块高度+88
        :param value: 金额.
        :param quota: 调用配额.
        :return: 签名后的bytes.
        """
        _, _, sender = self.generate_account(private_key)
        pri_key = PrivateKey(private_key)

        tx = Transaction()
        tx.valid_until_block = valid_until_block
        tx.nonce = get_nonce()
        tx.version = self.version

        if self.version == 0:
            tx.chain_id = self.chain_id
        else:
            tx.chain_id_v1 = self.chain_id.to_bytes(32, byteorder='big')

        if receiver:
            if self.version == 0:
                tx.to = receiver
            else:
                tx.to_v1 = receiver
        tx.data = bytecode
        tx.value = value.to_bytes(32, byteorder='big')
        tx.quota = quota

        keccak = sha3.keccak_256()
        keccak.update(tx.SerializeToString())
        message = keccak.digest()

        sign_recover = pri_key.ecdsa_sign_recoverable(message, raw=True)
        sig = pri_key.ecdsa_recoverable_serialize(sign_recover)

        signature = param_to_str(sig[0] + bytes(bytearray([sig[1]])))

        unverify_tx = UnverifiedTransaction()
        unverify_tx.transaction.CopyFrom(tx)
        unverify_tx.signature = param_to_bytes(signature)
        unverify_tx.crypto = Crypto.Value('DEFAULT')

        return unverify_tx.SerializeToString()


def get_nonce(size=6):
    """Get a random string."""
    return (''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(size)))


def decode_unverified_transaction(data: bytes) -> Dict:
    """
    反序列化 ``UnverifiedTransaction`` .

    :param data: ``UnverifiedTransaction`` 的序列化数据.
    :return: 等价的JSON结构.
    """
    utx = UnverifiedTransaction()
    utx.ParseFromString(data)
    tx = utx.transaction
    return {
        'transaction': {
            'chaid_id': tx.chain_id,
            'chain_id_v1': param_to_str(tx.chain_id_v1),
            'data': param_to_str(tx.data),
            'nonce': tx.nonce,
            'quota': tx.quota,
            'to': tx.to,
            'to_v1': param_to_str(tx.to_v1),
            'valid_until_block': tx.valid_until_block,
            'value': param_to_str(tx.value),
            'version': tx.version,
        },
        'signature': param_to_str(utx.signature),
        'crypto': utx.crypto,
    }
