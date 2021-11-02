from math import sqrt


def prime(n) -> bool:
	for i in range(2, int(sqrt(n)) + 1):
		if n % i == 0:
			return False

	return True


# TODO: implement Miller-Rabin for primality testing, as this can be faster for very large n
def MillerRabinTest(n):
	pass