__version__ = '0.0.3'

import os
import re


class GitSecrets(object):

    quote = r'(\'|\")'
    opt_quote = r'(\'|\")?'
    connect = r'\s*(:|=>|=)\s*'
    aws = r'(AWS|aws|Aws)'
    secret = r'(SECRET|secret|Secret)'
    access = r'(ACCESS|access|Access)'
    account = r'(ACCOUNT|account|Account)'
    id = r'(ID|id|Id)'
    key = r'(KEY|key|Key)'
    under = r'_'
    raw_access_key_pattern = r'^[A-Z0-9]{20}$'
    access_key_pattern = r'[A-Z0-9]{20}'
    raw_secret_access_key_pattern = r'^[0-9a-zA-Z]{40}$'
    secret_access_key_pattern = r'[0-9a-zA-Z]{40}'
    secret_access_key_regex = opt_quote + aws + under + secret + under + access + under + key + opt_quote + \
                              connect + opt_quote + secret_access_key_pattern + opt_quote
    access_key_regex = opt_quote + aws + under + access + under + key + under + id + opt_quote + connect + opt_quote + \
                       access_key_pattern + opt_quote

    default_patterns = [
        raw_access_key_pattern,         # AWS Access Key ID
        raw_secret_access_key_pattern,   # AWS Secret Access Key
        access_key_regex,
        secret_access_key_regex
    ]

    def __init__(self):
        self.patterns = []
        self.patterns = self.default_patterns

    def add_pattern(self, pattern):
        self.patterns.append(pattern)

    def search_file(self, pattern, f):
        with open(f) as infile:
            try:
                for i, line in enumerate(infile):
                    line = line.rstrip()
                    # print("searching for pattern: {} in line: {}".format(pattern, line))  # DEBUG
                    match = re.search(pattern, line)
                    if match:
                        # print(match.group())  # DEBUG
                        return True
            except UnicodeDecodeError as e:
                print("UnicodeDecodeError on file {}: {}".format(f, e))
                pass
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def scan_file(self, path):
        for pattern in self.patterns:
            # print("searching {} for pattern: {}".format(path, pattern))  # DEBUG
            if self.search_file(pattern, path):
                # print("match found in file {}".format(path))  # DEBUG
                return True

    def scan_recursively(self, path):
        for root, dirs, files in os.walk(path):
            if "venv" not in root and '.git' not in root:
                print(root)
                for f in files:
                    # print("SCANNING: {}".format(root + '/' + f))  # DEBUG
                    if self.scan_file(root + '/' + f):
                        return True
