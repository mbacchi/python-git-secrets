import errno
import os
import unittest
import random
import re
import tarfile
from string import ascii_uppercase, ascii_lowercase, digits

from gitsecrets import GitSecrets


class GSTestCase(unittest.TestCase):
    """
    Base test case for GitSecrets
    """

    def setUp(self):
        self.datdir = 'tests/data'
        self.tempdir = 'tests/tempdir'
        self.gs = GitSecrets()

    def newdir(self, path):
        # print("newdir path: {}".format(path))  # DEBUG
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def newfile(self, path, content):
        # print("path: {}; content: {}".format(path, content))  # DEBUG
        match = re.search('/', path)
        if match:
            dirpath = os.path.dirname(path)
            self.newdir(dirpath)
        with open(path, "w") as f:
            f.write(content + '\n')

    def newbinaryfile(self, path):
        match = re.search('/', path)
        if match:
            dirpath = os.path.dirname(path)
            self.newdir(dirpath)
        with open(path, "wb") as f:
            f.write(b"\x0a\x1b\x2c")
            f.write(b"\x3d\x4e\x5f")

    def newxzfile(self, path):
        longstring = "The quick brown fox jumped over the lazy dog."
        self.newfile(path, longstring + '\n' + longstring + '\n' +
                        longstring + '\n' + longstring + '\n' + longstring
                        + '\n' + longstring)
        with tarfile.open(path + ".tar.xz", "w:xz") as tar:
            tar.add(path, arcname=os.path.basename(path))

    def cleanupfile(self, path):
        os.remove(path)

    def tearDown(self):
        pass


class TestGitSecrets(GSTestCase):

    def test_plain_text(self):
        # None is returned if a pattern match is not found
        self.newfile('tests/tempdir/plain.txt', "Plain text file")
        self.assertIsNone(self.gs.scan_file('tests/tempdir/plain.txt'))
        self.cleanupfile('tests/tempdir/plain.txt')

    def test_new_aws_creds_access_key_id(self):
        patterns = [''.join("A3T" + random.choice(ascii_uppercase)), 'AKIA',
                    'AGPA', 'AIDA', 'AROA', 'AIPA', 'ANPA', 'ANVA', 'ASIA']
        for item in patterns:
            generated = ''.join(random.choice(ascii_uppercase) for _ in range(16))
            key = ''.join(item + generated)
            # print("testing pattern: \'{}\'".format(key))  # DEBUG
            self.newfile('tests/tempdir/aws-credentials', "aws_access_key_id=" + key)
            self.assertTrue(self.gs.scan_file('tests/tempdir/aws-credentials'))
            self.cleanupfile('tests/tempdir/aws-credentials')

    def test_aws_creds_secret_access_key(self):
        chars = ascii_uppercase + ascii_lowercase + digits
        key = ''.join(random.choice(chars) for _ in range(40))
        self.newfile('tests/tempdir/aws-credentials', "aws_secret_access_key=" + key)
        self.assertTrue(self.gs.scan_file('tests/tempdir/aws-credentials'))
        self.cleanupfile('tests/tempdir/aws-credentials')

    def test_add_pattern(self):
        self.newfile('tests/tempdir/add.txt', "funky cold medina")
        self.gs.add_pattern(r'.*cold.*')
        self.assertTrue(self.gs.scan_file('tests/tempdir/add.txt'))
        self.cleanupfile('tests/tempdir/add.txt')

    def test_binary_file(self):
        self.newbinaryfile('tests/tempdir/binfile.bin')
        self.assertIsNone(self.gs.scan_file('tests/tempdir/binfile.bin'))
        self.cleanupfile('tests/tempdir/binfile.bin')

    def test_xz_file(self):
        self.newxzfile('tests/tempdir/xzfile.txt')
        self.assertIsNone(self.gs.scan_file('tests/tempdir/xzfile.txt.tar.xz'))
        self.cleanupfile('tests/tempdir/xzfile.txt.tar.xz')
        self.cleanupfile('tests/tempdir/xzfile.txt')

class TestAWSLabsGitSecrets(GSTestCase):
    """
    These tests mimic the tests from AWSLabs git-secrets. I.e. from the directory here:
    https://github.com/awslabs/git-secrets/tree/master/test

    We will try to approximate many of them but some will be impossible as we don't
    provide the entire functionality that they do.
    """

    def test_invalid_filename_fails(self):
        """
        Approximates test:
        https://github.com/awslabs/git-secrets/blob/master/test/git-secrets.bats#L15
        """

        with self.assertRaises(FileNotFoundError):
            self.gs.scan_file('tests/data/not-a-file')

    def test_no_prohibited_matches_exit_0(self):
        self.newfile("tests/tempdir/test.txt", "it is ok")
        self.assertIsNone(self.gs.scan_file('tests/tempdir/test.txt'))
        self.cleanupfile("tests/tempdir/test.txt")


# TODO: use pattern similar to Dulwich where
#   we add all tests in the suite this way vs.
#   individually. Ref:
#   https://github.com/jelmer/dulwich/blob/master/dulwich/tests/__init__.py#L175

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGitSecrets('test_plain_text'))
    suite.addTest(TestGitSecrets('test_new_aws_creds_access_key_id'))
    suite.addTest(TestGitSecrets('test_aws_creds_secret_access_key'))
    suite.addTest(TestGitSecrets('test_add_pattern'))
    suite.addTest(TestGitSecrets('test_binary_file'))
    suite.addTest(TestGitSecrets('test_xz_file'))
    suite.addTest(TestAWSLabsGitSecrets('test_invalid_filename_fails'))
    suite.addTest(TestAWSLabsGitSecrets('test_no_prohibited_matches_exit_0'))
    return suite


if __name__ == '__main__':
    # TODO: Make -v verbose work
    runner = unittest.TextTestRunner()
    runner.run(suite())
