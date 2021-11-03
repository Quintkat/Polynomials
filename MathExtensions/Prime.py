from math import sqrt
from typing import Tuple


def prime(n) -> bool:
	for i in range(2, int(sqrt(n)) + 1):
		if n % i == 0:
			return False

	return True


def primeFirstResult(n) -> Tuple[bool, int]:
	for i in range(2, int(sqrt(n)) + 1):
		if n % i == 0:
			return False, i

	return True, 0


# TODO: implement Miller-Rabin for primality testing, as this can be faster for very large n
def MillerRabinTest(n, samples) -> bool:
	pass
