# Python Git Secrets
> A pure Python library providing [git-secrets](https://github.com/awslabs/git-secrets) functionality.

[![Build Status][travis-image]][travis-url]

We don't plan to do everything that [git-secrets](https://github.com/awslabs/git-secrets) does
(i.e. placing patterns in your .gitconfig file), but provide you with the building blocks for
matching patterns you don't want exposed to the world via Github. This will allow you to run
the tool in an AWS Lambda function with no dependence on external binaries.

There are no longer AWS credentials in this repository (at one time there were
inactive AWS credentials used for testing purposes.) Now testing is performed
by generating AWS credential strings on the fly using the same pattern that AWS
uses for their creds.

## Requirements

* [Dulwich](https://github.com/jelmer/dulwich) - A pure Python Git implementation.

## Sample usage

Run the `python-git-secrets.py` command to try it out:

    (venv) [mbacchi@hostname python-git-secrets]$ python samples/python-git-secrets.py --scan flask-quotes --repository https://github.com/mbacchi/flask-quotes --use_local_repo -r
    Scanning flask-quotes recursively
    flask-quotes
    SCANNING: flask-quotes/app.py
    Found verboten string in path flask-quotes

## Running Tests

To run tests, execute `test_driver.py` from the top level directory, you'll see output similar to:


    (venv) [mbacchi@hostname python-git-secrets]$ python test_driver.py
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.005s
    
    OK

## TODO

* create logging capabilities
* enable verbose output

## Meta

Matt Bacchi - mbacchi@gmail.com

Distributed under the BSD (Simplified) license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/mbacchi/python-git-secrets/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


<!-- Markdown link & img dfn's -->
[travis-image]: https://travis-ci.org/mbacchi/python-git-secrets.svg?branch=master
[travis-url]: https://travis-ci.org/mbacchi/python-git-secrets
