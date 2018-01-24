.PHONY: clean dist tests

clean:
	rm -rf dist build *.egg-info tests/tempdir

# Dist requires Python 3, the binary pandoc & the pip packages wheel & pypandoc
dist:
	python setup.py sdist bdist_wheel

# Tests require Python 3
tests:
	python test_driver.py
