#!/!usr/bin/env python
__program__ = "test_is_anagram"
__description__ = "test the is_anagram function" 
__date__ = "14/03/24"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2024 Christophe Lagaillarde"

import sys
sys.path.append('../')
from algo_fun.is_anagram import is_anagram

def test_is_anagram() -> None:
	assert is_anagram("any", "nya") is True 
	assert is_anagram("cheater", "teacher") is True 
	assert is_anagram("dog", "god") is True 
	assert is_anagram("the morse code", "here come dots") is True 

	assert is_anagram("dog", "gods") is False 
	assert is_anagram("rin", "rain") is False 
	assert is_anagram("cupcake", "cake") is False 
	assert is_anagram("teach", "torch") is False 
	
	return None

if __name__ == '__main__':
	test_is_anagram()
