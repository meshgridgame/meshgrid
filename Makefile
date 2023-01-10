.PHONY: test build dist

test:
	python -m unittest discover -s test -v	

environment:
	conda env export > environment.yml

uninstall:
	conda env remove -n meshgrid

install_local:
	conda env create -f environment.yml
	conda run -n meshgrid pip install .

build:
	python setup.py bdist_wheel

push_to_pypi:
	twine upload dist/*