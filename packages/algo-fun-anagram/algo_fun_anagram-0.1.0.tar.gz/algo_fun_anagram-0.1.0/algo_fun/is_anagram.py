#!/!usr/bin/env python
__program__ = "is_anagram.py"
__description__ = "Check if the 2 strings are anagram"
__date__ = "14/03/2024"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright 2024 (c) Christophe Lagaillarde"

import sys

def is_anagram(str1: str, str2: str) -> bool: 
	return ''.join(sorted(str1)) == ''.join(sorted(str2))


if __name__ == "__main__":
	is_anagram(sys.argv[1], sys.argv[2])

