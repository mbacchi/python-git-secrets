import argparse
from dulwich import porcelain
from gitsecrets import GitSecrets
import os


class Devnull(object):
    """
    This mimics a stream to write to for dulwich porcelain status output. Since we
    don't want to see the status this is a hack to suppress anything printing on stdout.

    Borrowed from:
    https://stackoverflow.com/questions/2929899/cross-platform-dev-null-in-python
    """
    def write(self, *_): pass


def do_args():
    # FIXME: change this to list/provide only the scanning functionality
    usage = "git secrets --scan [<files>...] [-r|--recursive] [--cached] [--no-index] [--untracked]\n" \
            "or: git secrets --scan-history\n" \
            "or: git secrets --add [-a|--allowed] [-l|--literal] [--global] <pattern>\n" \
            "or: git secrets --add-provider [--global] <command> [arguments...]\n" \
            "or: git secrets --aws-provider [<credentials-file>]\n"

    parser = argparse.ArgumentParser(description="A Python implementation of git-secrets scanning functionality.\n"
                                     "\nDifferences compared to git-secrets:\n"
                                     "1. We don't do any git configuration, such as \"--register-aws\" "
                                     "or \"--install\"",
                                     usage=usage,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--scan', help='Scans <files> for prohibited patterns')
    parser.add_argument('--scan-history', help='Scans repo for prohibited patterns')
    #parser.add_argument('--install', help='Installs git hooks for Git repository or Git template directory')
    #parser.add_argument('--list', help='Lists secret patterns')
    parser.add_argument('--add', help='Adds a prohibited or allowed pattern, ensuring to de-dupe with existing patterns')
    parser.add_argument('--add-provider', help='Adds a secret provider that when called outputs secret patterns on new lines')
    parser.add_argument('--aws-provider', help='Secret provider that outputs credentials found in an ini file')
    #parser.add_argument('--register-aws', help='Adds common AWS patterns to the git config and scans for ~/.aws/credentials')
    parser.add_argument('-r', '--recursive', help='--scan scans directories recursively',
                        action='store_true')
    parser.add_argument('--cached', help='--scan scans searches blobs registered in the index file')
    parser.add_argument('--no-index', help='--scan searches files in the current directory that is not managed by Git')
    parser.add_argument('--untracked', help='In addition to searching in the tracked files in the working tree, --scan also in untracked files')
    parser.add_argument('-f', '--force', help='--install overwrites hooks if the hook already exists')
    parser.add_argument('-l', '--literal', help='--add and --add-allowed patterns are escaped so that they are literal')
    parser.add_argument('-a', '--allowed', help='--add adds an allowed pattern instead of a prohibited pattern')
    parser.add_argument('--global', help='Uses the --global git config')
    parser.add_argument('--repository', help='Git repository to clone')
    parser.add_argument('--use_local_repo', help='Git repository to clone', action='store_true')
    args = parser.parse_args()
    return args


def perform_scan():
    gs = GitSecrets()
    if args.recursive:
        print("Scanning {} recursively".format(args.scan))
        if gs.scan_recursively(args.scan):
            print("Found verboten string in path {}".format(args.scan))
    else:
        print("Scanning {}".format(args.scan))
        if gs.scan_file(args.scan):
            print("Found verboten string in file {}".format(args.scan))


if __name__ == "__main__":
    args = do_args()
    if args.scan:
        if args.use_local_repo:
            # verify local repo exists
            repo = args.scan
            if os.path.exists(repo):
                perform_scan()
            else:
                print("Error: directory not found: {}".format(repo))
                exit(1)
        else:
            # clone the repo locally
            repo = os.path.basename(args.repository)
            nullstream = open(os.devnull, "w")
            ourepo = porcelain.clone(args.repository, repo, errstream=Devnull())
            if os.path.exists(repo):
                perform_scan()
            else:
                print("Error: directory not found: {}".format(repo))
                exit(1)
