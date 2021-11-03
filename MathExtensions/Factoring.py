from math import sqrt
from typing import List
from MathExtensions import Prime


def primeFactors(n : int) -> List[int]:
	factors = []
	m = 1
	n_ = n
	prime = Prime.primeFirstResult(n)
	if prime[0]:
		return [n]
	else:
		n_ = n_//prime[1]
		m *= prime[1]
		factors.append(prime[1])

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


def primeFactorsUnique(n : int) -> List[int]:
	allFactors = primeFactors(n)
	uniqueFactors = []
	for f in allFactors:
		if f not in uniqueFactors:
			uniqueFactors.append(f)

	return uniqueFactors

# Initial version of divisors, that is 10x slower than the new version below
# def divisors(n : int) -> List[int]:
# 	ds = [1]
# 	for i in range(2, n//2 + 1):
# 		if n % i == 0:
# 			ds.append(i)
#
# 	ds.append(n)
#
# 	return ds


def divisors(n : int, sort=True) -> List[int]:
	factors = primeFactors(n)
	multiplyList = [0]*len(factors)
	ds = []

	# Iterate over "Binary" list as if it's counting
	finished = False
	while not finished:
		divisor = 1
		# With current list, create a divisor
		for i in range(len(multiplyList)):
			if multiplyList[i] == 1:
				divisor *= factors[i]
		ds.append(divisor)

		# Iterate
		multiplyList[0] += 1
		for i in range(len(multiplyList) - 1):
			if multiplyList[i] == 2:
				multiplyList[i + 1] += 1

		# End condition
		if multiplyList[-1] == 2:
			finished = True

		# Reduce integers back
		for i in range(len(multiplyList)):
			if multiplyList[i] == 2:
				multiplyList[i] = 0

	if sort:
		return sorted(ds)
	return ds


# print(primeFactors(34171))
# print(divisors(8162))
# print(divisorsAlt(8162))
