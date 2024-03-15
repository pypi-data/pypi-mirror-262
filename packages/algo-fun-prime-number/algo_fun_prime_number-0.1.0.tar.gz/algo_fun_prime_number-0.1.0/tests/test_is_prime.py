#!/!usr/bin/env python
__program__ = "test_is_prime"
__description__ = "test the is_prime function" 
__date__ = "14/03/24"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2024 Christophe Lagaillarde"

import sys
sys.path.append('../')
from algo_fun.is_prime import is_prime

def test_is_prime() -> None:

	assert  is_prime(2) is True
	assert  is_prime(3) is True
	assert  is_prime(631) is True
	assert  is_prime(1109) is True
	assert  is_prime(1223) is True
	
	assert  is_prime(2550) is False
	assert  is_prime(2712) is False
	assert  is_prime(2673) is False
	assert  is_prime(4) is False

	return None

if __name__ == '__main__':
	test_is_prime()
