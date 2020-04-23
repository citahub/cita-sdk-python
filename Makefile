PROJ := pycita
TESTS ?= tests  # 测试的目标, 默认是./tests目录
SOL_INPUTS := $(wildcard tests/*.sol)
SOL_OUTPUTS := $(patsubst %.sol,%.bin,$(SOL_INPUTS))

.PHONY: doc clean test only sol

clean:
	rm -rf docs/_build dist/ tests/*.bin

%.bin: %.sol
	cat $^ | sudo docker run -i --rm ethereum/solc:0.4.24 --bin --abi --optimize - > $@

sol: $(SOL_OUTPUTS)  # 编译.sol文件

doc:
	cd docs && $(MAKE) html
	cd docs/_build/html && tar -zcvf ../docs.tar.gz . &> /dev/null

test: $(SOL_OUTPUTS) # 运行测试
	PYTHONPATH=$(PWD)/src pytest --cov=src -vv $(TESTS)

only: $(SOL_OUTPUTS) # 只运行打了 @pytest.mark.only 注解的测试
	PYTHONPATH=$(PWD)/src pytest -m only --cov=src -vv $(TESTS)

dist:  ## builds source and wheel package
	PYTHONPATH=$(PWD)/src python setup.py sdist
	PYTHONPATH=$(PWD)/src python setup.py bdist_wheel
	ls -l dist

