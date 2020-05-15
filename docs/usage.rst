基本用法
===========

文档中展示了 ``cita-sdk-python`` 的常见用法. 示例中的调用方式往往使用了默认参数, 所以建议点击方法名称, 跳转至Reference, 从而了解详细用法. 另外, 由于区块链的配置或内部状态不同, 所以每次执行示例可能会得到不同的结果.


使用CitaClient
----------------

初始化
~~~~~~~~~

:class:`~cita.CitaClient` 对 CITA JSON RPC 做了封装. 通常情况下, 初始化只需要提供 JSON RPC 服务的url即可, 比如: ``http://127.0.0.1:1337`` . 如果链的版本号 和 ``chain_id`` 不是默认值, 可以在构造时手工指定. 之后就可以进行方法调用了::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337', timeout=10)

如果操作会发起 RPC 调用且后端未在 ``timeout`` 时间内返回, 则会抛出超时异常. 建议同时参考CITA官方文档中的 `JSON-RPC 列表 <https://docs.citahub.com/zh-CN/cita/rpc-guide/rpc>`_ 部分.


.. note::

   目前仅支持 ``secp256k1`` 的加密方案.


节点信息
~~~~~~~~~~~~~~~~~

- :meth:`~cita.CitaClient.get_peer_count` 可以获得CITA 后端的兄弟节点数量.
- :meth:`~cita.CitaClient.get_peers` 可以获取节点的详细信息.

::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> client.get_peer_count()
    2
    >>> client.get_peers()
    {
        'amount': 3,
        'peers': {
            '0x2aaeacf658e49f58973b4ef6f37a5c574a28822c': '127.0.0.1',
            '0x3ea53608732da3761ef41805da73f0d45d3e8e09': '127.0.0.1',
            '0x01cb0a8012b75ea156eaef3e827547f760dd917a': '127.0.0.1'
        },
        'errorMessage': None
    }


元数据
~~~~~~~~~~~~~~~~~~~~

:meth:`~cita.CitaClient.get_meta_data` 获取链上元数据::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> client.get_meta_data()
    {
        'chainId': 0,
        'chainIdV1': '0x1', 
        'chainName': 'CITA-TEST',
        'operator': 'test-operator',
        'website': 'http://localhost',
        'genesisTimestamp': 1587639835490,
        'validators': ['0x1ea2fb0843953ecb15a79f9751ed963e0dc8720f'],
        'blockInterval': 3000,
        'tokenName': 'FJ',
        'tokenSymbol': 'FJ',
        'tokenAvatar': 'https://cdn.citahub.com/icon_cita.png',
        'version': 2,
        'economicalModel': 0
    }

区块信息
~~~~~~~~~~~~~~~

- :meth:`~cita.CitaClient.get_latest_block_number` 获取当前区块高度.
- :meth:`~cita.CitaClient.get_block_by_hash` 可以根据交易hash查询区块详情.
- :meth:`~cita.CitaClient.get_block_by_number` 可以根据区块编号查询区块详情.

::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> client.get_latest_block_number()
    733539
    >>> r1 = client.get_block_by_number(135342)
    >>> r2 = client.get_block_by_hash('0x5d28d1ceea302de6a935ee1ed8aff34aecd2c29543a75744301e581c2be366b3')
    >>> assert r1 == r2
    >>> r1
    {
        'version': 2,
        'hash': '0x5d28d1ceea302de6a935ee1ed8aff34aecd2c29543a75744301e581c2be366b3',
        'header': {
            'timestamp': 1588048233794,
            'prevHash': '0x338cb4b7c4e39c43cfa798884c7718cfb088babdc82e65aa2242c9d3aba0a398',
            'number': '0x210ae',
            'stateRoot': '0xf14d7af965ad2cd1ed1576bfb3dd3f64fae57d8652c13e6865516d9c83a1b856',
            'transactionsRoot': '0x2468067d5af66594ec070891edde6e45ae10dffb47f0d81467302a893a92bdac',
            'receiptsRoot': '0x81a7a530eaeae617bf617b4515077a033d8a6b3a0aaea9822491d1f1ce4e591a',
            'quotaUsed': '0x11822',
            'proof': {
                'Bft': {
                    'proposal': '0xc093d0fb3e31a0e0f182dd8058b3f822fce927bcae03fffbde478314914413bb',
                    'height': 135341,
                    'round': 0,
                    'commits': {
                        '0x1ea2fb0843953ecb15a79f9751ed963e0dc8720f': '0xeb7fe339067e8f33ca46ca4dbc5dc3527798ad8911d121156aa65f392dafb6b65b02a82a56a2a2d85a93b6d50e29e2c5e96e488f757468da4e6397f86a1343c301'
                    }
                }
            },
            'proposer': '0x1ea2fb0843953ecb15a79f9751ed963e0dc8720f'
        },
        'body': {
            'transactions': ['0x2468067d5af66594ec070891edde6e45ae10dffb47f0d81467302a893a92bdac']
        }
    }


交易信息
~~~~~~~~~~~~

- :meth:`~cita.CitaClient.get_transaction_count` 统计由指定账户发起的交易数量.
- :meth:`~cita.CitaClient.get_transaction` 获取交易详情.
- :meth:`~cita.CitaClient.decode_transaction_content` 解码交易内容.

::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> client.get_transaction_count('0x0c6e2197844c7bff3a87f60ce931746f17572a00')
    1144
    >>> r = client.get_transaction('0x2468067d5af66594ec070891edde6e45ae10dffb47f0d81467302a893a92bdac')
    >>> r
    {
        'hash': '0x2468067d5af66594ec070891edde6e45ae10dffb47f0d81467302a893a92bdac',
        'content': '0x0a950612064f5143374d371880808080042084a2082aa40582cc33270000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000025c38f11b7ad49c437d69851136c202d505aab4999500000244017c4f38000000000000000000000000297cb9765bb8abb603740b352ed549cf656a295262343766313164326162633234383236613466653735363233383466336436310000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000012b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000001727b22757365725f61646472223a22307832393763623937363562623861626236303337343062333532656435343963663635366132393532222c226576656e745f6e616d65223a2271696e67636875616e67706b5f335f33222c22616374696f6e5f74696d65223a22323032302d30342d32382031323a33303a32382e353936323438222c22616374696f6e5f74797065223a22766f7465222c22616374696f6e5f706172616d223a7b22746172676574223a226234376631316432616263323438323661346665373536323338346633643631222c227469636b6574223a312c22636f6e74726962223a312c227a68756c695f726577617264223a66616c73652c2272656d61696e5f7469636b6574223a3239397d2c22616374696f6e5f64657363223a225c75363239355c75373936382c205c75386432315c75373332652b312c205c75376432665c75386261315c75386432315c753733326520312c205c75346635395c753739363820323939227d0000000000000000000000000000000000003220000000000000000000000000000000000000000000000000000000000000000040024a14ffffffffffffffffffffffffffffffffff02000e5220000000000000000000000000000000000000000000000000000000000000000112415e1c0796e7bed6f7b5d29f661bec846f6b57328de27cfb4b3919315cc64268237bdfb64c7b317ebf58451bcd7a7d9ad1f0a4c3055db2e1a6526b8e60b242e2a700',
        'from': '0x0c6e2197844c7bff3a87f60ce931746f17572a00',
        'blockNumber': '0x210ae',
        'blockHash': '0x5d28d1ceea302de6a935ee1ed8aff34aecd2c29543a75744301e581c2be366b3',
        'index': '0x0'
    }    
    >>> client.decode_transaction_content(r['content'])
    {
        'transaction': {
            'chaid_id': 0,
            'chain_id_v1': '0x0000000000000000000000000000000000000000000000000000000000000001',
            'data': '0x82cc33270000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000025c38f11b7ad49c437d69851136c202d505aab4999500000244017c4f38000000000000000000000000297cb9765bb8abb603740b352ed549cf656a295262343766313164326162633234383236613466653735363233383466336436310000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000012b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000001727b22757365725f61646472223a22307832393763623937363562623861626236303337343062333532656435343963663635366132393532222c226576656e745f6e616d65223a2271696e67636875616e67706b5f335f33222c22616374696f6e5f74696d65223a22323032302d30342d32382031323a33303a32382e353936323438222c22616374696f6e5f74797065223a22766f7465222c22616374696f6e5f706172616d223a7b22746172676574223a226234376631316432616263323438323661346665373536323338346633643631222c227469636b6574223a312c22636f6e74726962223a312c227a68756c695f726577617264223a66616c73652c2272656d61696e5f7469636b6574223a3239397d2c22616374696f6e5f64657363223a225c75363239355c75373936382c205c75386432315c75373332652b312c205c75376432665c75386261315c75386432315c753733326520312c205c75346635395c753739363820323939227d000000000000000000000000000000000000',
            'nonce': 'OQC7M7',
            'quota': 1073741824,
            'to': '',
            'to_v1': '0xffffffffffffffffffffffffffffffffff02000e',
            'valid_until_block': 135428,
            'value': '0x0000000000000000000000000000000000000000000000000000000000000000',
            'version': 2
        },
        'signature': '0x5e1c0796e7bed6f7b5d29f661bec846f6b57328de27cfb4b3919315cc64268237bdfb64c7b317ebf58451bcd7a7d9ad1f0a4c3055db2e1a6526b8e60b242e2a700',
        'crypto': 0
    }


创建账户
~~~~~~~~~~~

:meth:`~cita.CitaClient.create_key` 可以创建账户, 返回账户地址, 公钥, 私钥. 用于交易签名或合约调用::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> client.create_key()
    {
        'private': '0xc2c9d4828cd0755542d0dfc9deaf44f2f40bb13d35f5907a50f60d8ccabf9832',
        'public': '0xce5bd22370bd45c17210babfb0d357c0b6ff74e9fd66fa120c795d849feaa49b115d49f82ffa27854c884fed25feee0bafc3833847abafaddb423a16af301b2c',
        'address': '0xc9ee0f9193796ffbbed9cd6d63ed4e1483b1eafc'
    }


发起并确认交易
~~~~~~~~~~~~~~

- :meth:`~cita.CitaClient.send_raw_transaction` 直接对应JSON RPC的 ``sendRawTransaction`` 方法. 输入参数是签名后的数据.
- :meth:`~cita.CitaClient.send_transaction` 比前者更进一步, 封装了签名算法.
- :meth:`~cita.CitaClient.get_transaction_receipt` 获取交易回执. 如果在指定时间内获得回执, 说明交易已经在一个节点执行完毕.
- :meth:`~cita.CitaClient.confirm_transaction` 等待交易在全部节点达成共识后再返回交易回执.

::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> private_key = '0x...'
    >>> to_addr = '0x...'
    >>> code = '0x...'
    >>> tx_hash = client.send_transaction(private_key, to_addr, code)
    >>> tx_hash
    '0x2468067d5af66594ec070891edde6e45ae10dffb47f0d81467302a893a92bdac'
    >>> r1 = client.get_transaction_receipt(tx_hash, timeout=10)
    >>> r2 = client.confirm_transaction(tx_hash, timeout=10)
    >>> assert r1 == r2
    >>> r1
    {
        'transactionHash': '0x2468067d5af66594ec070891edde6e45ae10dffb47f0d81467302a893a92bdac',
        'transactionIndex': '0x0',
        'blockHash': '0x5d28d1ceea302de6a935ee1ed8aff34aecd2c29543a75744301e581c2be366b3',
        'blockNumber': '0x210ae',
        'cumulativeQuotaUsed': '0x11822',
        'quotaUsed': '0x11822',
        'contractAddress': None,
        'logs': [],
        'root': None,
        'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        'errorMessage': None
    }


部署合约
~~~~~~~~~~~

本质上就是一个交易. 所以也可以使用 :meth:`~cita.CitaClient.send_raw_transaction` 和 :meth:`~cita.CitaClient.send_transaction` 方法完成. 但是使用 :meth:`~cita.CitaClient.deploy_contract` 可以更明确一些. 所需参数是私钥, 合约的bytecode, 合约初始化参数::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> private_key = '0x...'
    >>> bytecode = '0x...'
    >>> param = '0x...'
    >>> tx_hash = client.deploy_contract(private_key, bytecode, param)
    >>> tx_hash
    '0x85077e49b10e57bd93f107570ced9c7046157d891a1873c3339a270246800c90'
    >>> client.get_transaction_receipt(tx_hash)
    {
        'transactionHash': '0x85077e49b10e57bd93f107570ced9c7046157d891a1873c3339a270246800c90',
        'transactionIndex': '0x0',
        'blockHash': '0xf0dde2aa7b427b9bbb11e03c2adfced395463ba095d9ce7487eee0c1026ecb6a',
        'blockNumber': '0x22261',
        'cumulativeQuotaUsed': '0x2fa8d',
        'quotaUsed': '0x2fa8d',
        'contractAddress': '0xe74a75fa682664dcee4b41f34e76bcfbbb45cdd6',
        'logs': [],
        'root': None,
        'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        'errorMessage': None
    }    

交易回执中的 ``contractAddress`` 字段表明了合约的链上地址. 合约参数需要进行编码, 把Python中的数值转化为区块链可以理解的格式. 这部分在 :ref:`编码解码` 中详述.


合约的bytecode和ABI
~~~~~~~~~~~~~~~~~~~~~~~~~~~

合约文件经过编译后形成bytecode, 从而定义其链上行为. 为了让其他用户了解合约的使用方法, 还可以指定ABI.

- :meth:`~cita.CitaClient.store_abi` 可以对给定地址的合约添加ABI.
- :meth:`~cita.CitaClient.get_abi` 可以读取给定地址的合约的ABI.
- :meth:`~cita.CitaClient.get_code` 可以读取给定地址的合约的ABI.


::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')

    # 部署合约
    >>> private_key = '0x...'
    >>> bytecode = '0x...'
    >>> param = '0x...'
    >>> tx_hash = client.deploy_contract(private_key, bytecode, param)
    >>> contract_addr = client.confirm_transaction(tx_hash)['contractAddress']

    # 获取合约的字节码
    >>> assert client.get_code(contract_addr) == bytecode

    # 给合约添加ABI
    >>> abi = [{
                    "constant": true,
                    "inputs": [],
                    "name": "get",
                    "outputs": [{
                        "name": "",
                        "type": "uint256"
                    }],
                    "payable": false,
                    "stateMutability": "view",
                    "type": "function"
                }, {
                    "inputs": [{
                        "name": "_x",
                        "type": "uint256"
                    }],
                    "payable": false,
                    "stateMutability": "nonpayable",
                    "type": "constructor"
              }]
    >>> tx_hash = client.store_abi(private_key, contract_addr, json.dumps(abi))
    >>> client.confirm_transaction(tx_hash)

    # 读取合约的ABI
    >>> assert client.get_abi(contract_addr) == abi



调用合约
~~~~~~~~~~

直接使用 :class:`~cita.CitaClient` 进行合约的部署或方法调用是比较繁琐的, 因为需要手工处理参数和返回值的编码解码问题, 手工处理方法hash等问题, 语法上也不够自然. 建议使用 :ref:`使用ContractClass` 来完成这些工作.


编码解码
^^^^^^^^^^^^^^

编码解码需要使用四个辅助函数来完成.

- 编码 :func:`~cita.encode_param`
- 解码 :func:`~cita.decode_param`
- 将数据转化为 ``0x...`` 的形式 :func:`~cita.param_to_str`
- 将数据转化为 ``bytes`` 的形式 :func:`~cita.param_to_bytes`


::

    >>> from cita import encode_param, decode_param, param_to_str, param_to_bytes

    # 处理单一参数
    >>> r = encode_param('string', 'abc')
    >>> param_to_str(r)
    '0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000036162630000000000000000000000000000000000000000000000000000000000'
    >>> assert decode_param('string', r) == 'abc'

    # 处理多个参数
    >>> r = encode_param('(int,bool,bytes[])', (-1, True, [b'abc', b'def']))
    >>> param_to_str(r)
    '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000003616263000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000036465660000000000000000000000000000000000000000000000000000000000'
    >>> assert decode_param('(int,bool,bytes[])', r) == (-1, True, (b'abc', b'def'))

.. note::

   - 类型字符串, 比如 ``(int,bool,bytes[])`` 中是不可以有空格的. 否则函数会报错.
   - 对于单一参数, 无需写成 ``(string)`` 元组形式. 解码后也是直接得到数值, 无需提取元组的元素. 也就是说类型字符串 ``(string)`` 和 ``string`` 是等价的.
   - 对于数组, 解码后会得到 ``tuple`` 而不是 ``list``. 一般情况下, 这个区别并不影响业务逻辑.


执行调用
^^^^^^^^^^^^

合约方法有Immutable和Mutable的区别. 声明为 ``const``, ``view``, ``pure`` 的合约方法为Immutable方法, 其他为Mutable方法:

- :meth:`~cita.CitaClient.call_readonly_func` 可以调用合约的Immutable方法.
    - 输入合约地址
    - 输入合约方法的hash码
    - 输入编码后的方法参数
    - 输出编码后的返回值

- :meth:`~cita.CitaClient.call_func` 可以调用合约的Mutable方法.
    - 输入合约地址
    - 输入合约方法的hash码
    - 输入调用者私钥
    - 输入编码后的方法参数
    - 输出交易hash

::

    假设合约中定义了一个Mutable方法和一个Immutable方法:
    
    contract SimpleStorage {
        uint x;

        constructor(uint _x) public {
            x = _x;
        }

        function set(uint _x) public {
           x = _x;
        }  // 此方法的hash码为: 0x60fe47b1
       
        function get() public constant returns (uint) {
            return x;
        }  // 此方法的hash码为: 0x6d4ce63c
    }

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> contract_addr = '0x...'  # 合约部署地址
    >>> private_key = '0x...'
    >>> param = encode_param('uint', 200)
    # set x = 200
    >>> tx_hash = client.call_func(private_key, contract_addr, '0x60fe47b1', param=param)
    >>> client.confirm_transaction(tx_hash)
    # get x
    >>> result = client.call_readonly_func(contract_addr, '0x6d4ce63c')
    >>> decode_param(result)
    200


设置调用模式
~~~~~~~~~~~~~~~

在调用合约的只读方法时, 默认会使用已共识的区块信息, 即 ``latest`` . 但也可以设置为使用刚出块还未共识的区块信息, 即 ``pending`` . 这个模式适合于只有一个CITA节点或单元测试. 可以通过 :meth:`~cita.CitaClient.set_call_mode` 进行设置. 设置后会影响由此实例发起的之后所有的调用.

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> client.set_call_mode('pending')


使用ContractClass
-----------------------------

:class:`~cita.ContractClass` 将 ``.sol`` 的合约文件封装为一个Python的对象工厂, 产品就是一个个部署上链的合约对象. 同时, :class:`~cita.ContractProxy` 对合约对象进行封装, 将合约方法的调用转化为Python对象方法的调用, 隐藏了方法名, 参数, 返回值的编码解码步骤, 从而大幅简化开发工作, 语句表达上也更加自然. 下面的例子使用的合约跟 :ref:`执行调用` 中的相同::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> private_key = client.create_key()['private']
    
    # 构造 ContractClass, 输入合约文件所在的路径. 
    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)
    >>> simple_class.name
    'SimpleStorage'

    # 部署合约, 将 100 传递给合约构造函数. 返回 (ContractProxy对象, 合约地址, 交易hash) 三元组.
    >>> simple_obj, contract_addr, tx_hash = simple_class.instantiate(private_key, 100)
    >>> client.confirm_transaction(tx_hash)

    # 通过ContractProxy对象读取 x 的值
    >>> simple_obj.get()
    100

    # 通过ContractProxy对象改变 x 的值
    >>> tx_hash = simple_obj.set(200)
    >>> client.confirm_transaction(tx_hash)

    # 通过ContractProxy对象读取 x 的值
    >>> simple_obj.get()
    200
    

sol文件与bin文件
~~~~~~~~~~~~~~~~~~

``cita-sdk-python`` 并不能解析 ``.sol`` 文件的内容. 需要使用 ``solc`` 之类的编译器, 将其转化为字节码和ABI才行. 建议用户采用 ``Makefile`` 中的方法来将 ``.sol`` 文件编译成标准的 ``.bin`` 文件::

    cat some.sol | sudo docker run -i --rm ethereum/solc:0.4.24 --bin --abi --optimize - > some.bin

:class:`~cita.ContractClass` 构造函数的第一个参数是 ``.sol`` 文件的路径. 要求在同目录下有同名的 ``.bin`` 文件::

    ======= <stdin>:SimpleStorage =======
    Binary: 
    6080604052348015...957f150029
    Contract JSON ABI 
    [{"constant":false,"inputs"..."type":"event"}]

通过读取上述内容, :class:`~cita.ContractClass` 可以了解合约的bytecode, 以及每个方法的类型, 名字, 参数, 返回值. 以便后续将之适配成普通的 Python 对象. :meth:`~cita.ContractClass.get_code` 和 :meth:`~cita.ContractClass.get_raw_abi` 会返回上述信息.

.. warning::

   由于 Python 不支持函数重载, 而合约可以, 所以无法直接模拟这个功能. 建议避免在合约中使用重载. 如果某些方法必须重载, 则只能使用其方法hash码来触发调用了. 其他未重载的方法不受影响.


更方便的部署合约
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

有三种部署方法, 分别对应不同的使用场景.

- :meth:`~cita.ContractClass.instantiate_raw` 发起部署合约的交易, 立即返回交易hash, 不会等待合约部署完成. 属于Low Level操作, 不太常用.
- :meth:`~cita.ContractClass.instantiate` 部署合约并返回一个绑定于合约地址的 ``ContractProxy`` 对象. 很常用.
- :meth:`~cita.ContractClass.batch_instantiate` 部署一批合约, 返回一组 ``ContractProxy`` 对象.

对于接收 0, 1, 2 个参数的合约构造函数的调用示例::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> private_key = client.create_key()['private']

    # 合约构造函数 constructor()
    >>> dummy_class = ContractClass(Path('tests/Dummy.sol'), client)
    # 合约构造函数 constructor(uint _x)
    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)
    # 合约构造函数 constructor(uint _x, uint _y)
    >>> double_class = ContractClass(Path('tests/DoubleStorage.sol'), client)

    # 部署合约
    >>> x, y = 1, 2    
    >>> dummy_obj, contract_addr, tx_hash = dummy_class.instantiate(private_key)
    >>> simple_obj, contract_addr, tx_hash = simple_class.instantiate(private_key, x)
    >>> double_obj, contract_addr, tx_hash = double_class.instantiate(private_key, x, y)


绑定合约地址
~~~~~~~~~~~~~

如果已知某个 ``.sol`` 对应的 ``ContractClass`` , 以及合约地址. 可以通过 :meth:`~cita.ContractClass.bind` 来生成 ``ContractProxy`` 对象::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)
    >>> contract_addr = '0x...'
    >>> private_key = '0x...'
    >>> simple_obj = simple_class.bind(contract_addr, private_key)


使用ContractProxy
------------------------------

:class:`~cita.ContractProxy` 可以由 :class:`~cita.ContractClass` 的实例化方法或者绑定来生成. 一旦得到 ``ContractProxy`` 对象, 就可以像调用Python方法那样操作合约了. :ref:`执行调用` 中列出了不同种类的方法需要使用不同的代码来调用. ``ContractProxy`` 尽可能的统一了调用方式, 唯一的区别是:

- 对于Mutable合约方法, 只能返回交易hash;
- 对于Immutable合约方法, 则会返回解码后的返回值. 如果返回多个值, 解码后是 ``tuple`` 形式.

接收 0, 1, 2 个参数的合约方法的调用示例::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> private_key = client.create_key()['private']
    >>> contract_addr = '0x...'

    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)
    >>> simple_obj = simple_class.bind(contract_addr, private_key)

    # function set(uint _x) public
    >>> tx_hash = simple_obj.set(200)
    >>> client.confirm_transaction(tx_hash)

    # function get() public view returns (uint)
    >>> assert simple_obj.get() == 200

    # function function reset() public
    >>> simple_obj.reset()

    # function add_by_vec(uint[] a, uint[] b) public returns (uint)
    >>> tx_hash = simple_obj.add_by_vec([1, 2], [3, 4])
    >>> client.confirm_transaction(tx_hash)
    >>> expect = 1 * 3 + 2 * 4
    >>> assert simple_obj.get() == expect


Quota
~~~~~~~

每个Mutable合约方法的调用, 执行中都会消耗Quota, 如果计算比较复杂, Quota消耗殆尽, 交易就会失败回滚. ``ContractProxy`` 默认每次调用的Quota是 ``DEFAULT_QUOTA = 10_000_000`` . 可以更精细的控制每个方法的Quota::

    >>> new_quota = 1
    # 设置 function set 的quota
    >>> simple_obj.set.quota = new_quota
    # 设置 function add_by_vec 的quota
    >>> simple_obj.add_by_vec.quota = new_quota
    # 由于设置的quota很低, 所以合约方法的调用应该会失败.
    >>> tx_hash = simple_obj.set(300)
    >>> client.get_transaction_receipt(tx_hash)
    RuntimeError: Not enough base quota.

``obj.<method_name>.quota`` 会持续生效, 下一次对 ``method_name`` 的调用依旧会使用指定的quota. 除此之外, 还可以在 :meth:`cita.ContractClass.__init__` 时通过 ``func_name2quota`` 参数, 一次性指定每个合约方法的quota.


重载方法
~~~~~~~~~~

``ContractProxy`` 对象除了可以通过合约方法名触发调用, 还可以通过合约方法的hash码来触发调用. 从而支持合约方法的重载::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> contract_addr = '0x...'
    >>> private_key = '0x...'

    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)
    >>> simple_obj = simple_class.bind(contract_addr, private_key)
    >>> assert simple_obj.get() == simple_obj['0x6d4ce63c']()


批量交易
----------------

实际应用中, 经常会遇到需要处理大量交易的情况. 通过把一批零散交易打包成一个大交易, 可以大大提升 CITA 的吞吐量. ``cita-sdk-python`` 也对此提供了支持.


合约的批量部署
~~~~~~~~~~~~~~~~~

通过 :meth:`~cita.CitaClass.batch_instantiate` 可以部署同一合约的多个实例. 由于 CITA 本身并不支持批量部署, 所以实现上仍是通过循环逐一部署, 只是提供了一些便利. 合约构造函数所需的参数, 通过数组传入::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> private_key = '0x...'

    >>> dummy_class = ContractClass(Path('tests/Dummy.sol'), client)
    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)
    >>> double_class = ContractClass(Path('tests/DoubleStorage.sol'), client)

    # 构造函数 constructor() 不需要参数, 部署三个实例.
    >>> init_values = [(), (), ()]
    >>> for dummy_obj, addr, tx_hash in dummy_class.batch_instantiate(private_key, init_values):
    ...     print('Contract_addr:', addr)

    # 构造函数 constructor(uint _x), 部署三个实例. 对单一参数, 使用tuple包裹与uint等价.
    >>> init_values = [100, 200, (300,)]
    >>> for simple_obj, addr, tx_hash in simple_class.batch_instantiate(private_key, init_values):
    ...     print('Contract_addr:', addr)

    # 构造函数 constructor(uint _x, uint _y), 部署三个实例. 参数必须是tuple形式.
    >>> init_values = [(100, 200), (300, 400), (500, 600)]
    >>> for double_obj, addr, tx_hash in double_class.batch_instantiate(private_key, init_values):
    ...     print('Contract_addr:', addr)


批量调用
~~~~~~~~~~~~~~~

当合约部署完毕后, CITA 内置支持批量合约方法的调用. 其本质是将每个合约调用所需的数据一次性提交给一个特殊的合约, 由后者在合约内部循环逐个执行交易. 这样可以节约很多通信和共识的计算, 从而大大提高执行效率. 但如果一批交易中有一个失败, 则整体失败. 所以在使用时需要谨慎.

.. note::

    只有Mutable的合约方法可以进行批量交易. 一批交易只能使用同一私钥进行签名.


首先需要计算出每个交易所需的编码后的数据, 可以通过 :meth:`~cita.ContractProxy.get_tx_code` 解决::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> contract_addr1 = '0x...'
    >>> contract_addr2 = '0x...'
    >>> private_key = '0x...'

    # 绑定两个SimpleStorage合约实例
    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)
    >>> simple_obj1 = simple_class.bind(contract_addr1, private_key)
    >>> simple_obj2 = simple_class.bind(contract_addr2, private_key)

    # 收集每个交易所需的数据 tx_code
    >>> tx_code_list = []

    # function reset() public
    >>> tx_code = simple_obj1.get_tx_code('reset')  # 使用0个参数
    >>> tx_code_list.append(tx_code)

    # function set(uint _x) public
    >>> tx_code = simple_obj1.get_tx_code('set', 1)  # 使用1个参数
    >>> tx_code_list.append(tx_code)

    # function add_by_vec(uint[] a, uint[] b) public returns (uint)
    >>> tx_code = simple_obj2.get_tx_code('add_by_vec', ([1, 2], [3, 4]))  # 使用2个参数
    >>> tx_code_list.append(tx_code)

之后通过 :meth:`~cita.CitaClient.batch_call_func` 发起批量调用::

    >>> tx_hash = client.batch_call_func(private_key, tx_code_list)
    >>> client.confirm_transaction(tx_hash)
