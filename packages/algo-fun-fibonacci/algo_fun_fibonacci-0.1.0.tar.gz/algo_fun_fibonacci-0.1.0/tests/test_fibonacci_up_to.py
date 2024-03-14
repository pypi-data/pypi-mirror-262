#!/!usr/bin/env python
__program__ = "test_fibonacci_up_to"
__description__ = "test the fibonacci_up_to function" 
__date__ = "13/03/24"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2024 Christophe Lagaillarde"

import sys
sys.path.append('../')
from algo_fun.fibonacci_up_to import fibonacci_up_to

def test_fibonacci_up_to() -> None:

	assert fibonacci_up_to(2000) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

	assert fibonacci_up_to(7000) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765] 

	assert fibonacci_up_to(121393) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393] 

	assert fibonacci_up_to(1346270) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269]

	assert fibonacci_up_to(102334156) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155] 
	
	return None

if __name__ == '__main__':
	test_fibonacci_up_to()
