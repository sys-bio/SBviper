"""
Runner for km_test
Arguments:
    path to an XML file
    option [Basics, ...]
"""

import sys
from km_test import StaticTestCase


def Usage():
    """
    Prints the usage and exit
    """
    print("usage: km_test.py path_to_XML [option]")
    print("[option]: Basic")
    exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # set the option to "basic" as default
        tester = StaticTestCase(sys.argv[1], "Basic")
    elif len(sys.argv) == 3:
        tester = StaticTestCase(sys.argv[1], sys.argv[2])
    else:
        Usage()
