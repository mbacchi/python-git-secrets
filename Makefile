.PHONY: clean dist tests

clean:
	rm -rf dist build *.egg-info tests/tempdir

# Dist requires Python 3, the binary pandoc & the pip packages wheel & pypandoc
dist:
	python setup.py sdist bdist_wheel

# Tests require Python 3
tests:
	python3 test_driver.py

upload:
	twine upload dist/*

upload-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
