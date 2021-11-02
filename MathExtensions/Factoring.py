from math import sqrt
from typing import List
import datetime
import time

def primeFactors(n) -> List[int]:
	factors = []
	m = 1
	n_ = n
	while n_ % 2 == 0:
		n_ = n_//2
		m *= 2
		factors.append(2)

	for d in range(3, n_ + 1, 2):
		while n_ % d == 0:
			n_ = n_//d
			m *= d
			factors.append(d)

		if m == n:
			break

	return factors


def primeFactorsUnique(n) -> List[int]:
	allFactors = primeFactors(n)
	uniqueFactors = []
	for f in allFactors:
		if f not in uniqueFactors:
			uniqueFactors.append(f)

	return uniqueFactors

print(primeFactors(34171))
