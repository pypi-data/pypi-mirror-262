#!/!usr/bin/env python
__program__ = "fibonacci_up_to.py"
__description__ = "Give the fibonacci sequence up to and includinga given number"
__date__ = "13/03/2024"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright 2024 (c) Christophe Lagaillarde"

import sys
	
def fibonacci_up_to(number: int) -> list[int]:

	if number <= 0:	
		sys.exit("Should be a non null positive integer")

	current_number: int = 1
	fibonacci_sequence: list = [0, current_number]

	while fibonacci_sequence[-1] <= number: 
		current_number = fibonacci_sequence[-2] + fibonacci_sequence[-1]
		fibonacci_sequence.append(current_number)
	

	return fibonacci_sequence[:-1:]


if __name__ == "__main__":
	print(fibonacci_up_to(1000))
