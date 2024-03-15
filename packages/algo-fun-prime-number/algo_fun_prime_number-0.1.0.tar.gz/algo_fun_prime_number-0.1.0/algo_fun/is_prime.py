#!/!usr/bin/env python
__program__ = "is_prime.py"
__description__ = "Tell if a number is prime or not"
__date__ = "14/03/2024"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright 2024 (c) Christophe Lagaillarde"

import sys
from math import sqrt

def is_prime(number: int) -> bool: 

	if number <= 1:
		sys.exit("Only integer superior to 1")

	for i in range(2, int(sqrt(number) + 1)):
		if (number % i) == 0:
			return False

	return True 


if __name__ == "__main__":
	is_prime(int(sys.argv[1]))

