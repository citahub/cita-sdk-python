|Python| |Travis| |Coverage| |License|


CITA Python SDK
-------------------

``cita-sdk-python`` 是 `CITA高性能区块链 <https://www.citahub.com>`_ 的Python binding, 提供下述功能:

- ``CitaClient`` 类封装了CITA JSON RPC的调用.
- ``ContractClass`` 类封装了合约的ABI. 使用Python的语法来完成合约部署.
- ``ContractProxy`` 类封装了已部署的合约. 使得对合约方法的调用看起来就像对Python Object方法的调用.


安装
----------

``cita-sdk-python`` 需要 Python 3.7 或以上版本的Python来运行::

    $ PYTHONPATH=$PWD/src python setup.py install


打包
----------

::

    $ make dist
    $ ls dist/
    cita_sdk_python-0.1.0-py37-none-any.whl  cita_sdk_python-0.1.0.tar.gz


文档
----------

::

    $ make doc
    $ ls docs/_build/html
    genindex.html  index.html  _modules  objects.inv  py-modindex.html  search.html  searchindex.js  _sources  src.html  _static  usage.html

启动浏览器打开 ``index.html`` 即可查看详细文档.


常见用法
----------

使用 ``CitaClient`` 执行 JSON RPC::

    >>> from cita import CitaClient
    >>> client = CitaClient('http://127.0.0.1:1337', timeout=10)
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

    >>> client.get_latest_block_number()
    733539

    >>> client.create_key()
    {
        'private': '0xc2c9d4828cd0755542d0dfc9deaf44f2f40bb13d35f5907a50f60d8ccabf9832',
        'public': '0xce5bd22370bd45c17210babfb0d357c0b6ff74e9fd66fa120c795d849feaa49b115d49f82ffa27854c884fed25feee0bafc3833847abafaddb423a16af301b2c',
        'address': '0xc9ee0f9193796ffbbed9cd6d63ed4e1483b1eafc'
    }


假设下述合约保存在当前目录下的 ``SimpleStorage.sol`` 文件中::

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


使用 ``solc`` 编译合约, 将结果保存在同一路径下的 ``SimpleStorage.bin`` 文件中::

    $ cat SimpleStorage.sol | sudo docker run -i --rm ethereum/solc:0.4.24 --bin --abi --optimize - > SimpleStorage.bin


使用 ``ContractClass`` 加载 ``SimpleStorage.bin`` 中的内容, 部署并执行合约::

    >>> from cita import CitaClient, ContractClass
    >>> client = CitaClient('http://127.0.0.1:1337')
    >>> private_key = client.create_key()['private']

    # 初始化ContractClass
    >>> simple_class = ContractClass(Path('tests/SimpleStorage.sol'), client)

    # 部署一个合约实例
    >>> init_x = 100
    >>> simple_obj, contract_addr, tx_hash = simple_class.instantiate(private_key, init_x)

    # 调用Immutable合约方法
    >>> simple_obj.get()
    100

    # 调用Mutable合约方法
    >>> tx_hash = simple_obj.set(200)

    # 等待交易确认
    >>> client.confirm_transaction(tx_hash)

    # 再次调用Immutable合约方法
    >>> simple_obj.get()
    200


.. |Python| image:: https://img.shields.io/badge/Python-3.7-blue?logo=python&logoColor=white
    :alt: PyPI - Python Versions

.. |Travis| image:: https://travis-ci.org/melonux/cita-sdk-python.svg?branch=dev
    :target: https://travis-ci.org/melonux/cita-sdk-python

.. |Coverage| image:: https://coveralls.io/repos/github/melonux/cita-sdk-python/badge.svg?branch=dev
    :target: https://coveralls.io/github/melonux/cita-sdk-python?branch=dev

.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
