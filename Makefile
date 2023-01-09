.PHONY: test

test:
	python -m unittest discover -s test -v	

install_local:
	pip install -e .

build:
	python setup.py bdist_wheel

push_to_pypi:
	twine upload dist/*