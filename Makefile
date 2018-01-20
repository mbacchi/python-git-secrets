.PHONY: clean dist tests

clean:
	rm -rf dist build *.egg-info

# Dist requires the binary pandoc & the pip packages wheel & pypandoc
dist:
	python setup.py sdist bdist_wheel

# Tests require python 3
tests:
	python test_driver.py
