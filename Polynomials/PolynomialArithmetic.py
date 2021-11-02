from Polynomial import Polynomial as Poly
from copy import copy
from typing import Tuple


# Returns whether or not a function like those below can be performed on the two polynomials in general
# Can raise an exception.
# Do not encase this function in a try/except block, as it is supposed to show a notify you of trying to do something which you can't
def testValidity(f : Poly, g : Poly):
	if f.mod() != g.mod():
		raise Exception("You can only do operations on Polynomials of the same modulo")


# Returns, in a tuple (q, r), the polynomial divisor q and the polynomial remainder r such that f = g*q + r mod ...
# Can raise exception when dividing by zero.
# Therefore, when executing, please put inside of a try/except bit and handle that edge case where you want to use it.
# Limitation, the modulo has to be prime, for this function to return a correct result.
def longDivision(f : Poly, g : Poly) -> Tuple[Poly, Poly]:
	# Check for invalidity of the usage of this function
	testValidity(f, g)

	if g.isZero():
		raise Exception("Division by 0")

	# Special case where g can't divide f, no matter what
	if g.degreeMax() > f.degreeMax():
		return Poly([0], f.mod()), f

	# Normal long division case
	m = f.mod()		# The modulus
	degreeDiff = f.degreeMax() - g.degreeMax()
	q = Poly([0], m)
	stepPoly : Poly = copy(f)
	# Go over every degree that g is missing compared to f
	for d in f.degrees()[0:degreeDiff + 1]:
		# The case where all terms of F have been subtracted away. Eg. g is a divisor of f
		if stepPoly.isZero():
			break

		coeffF = stepPoly[d]		# The coefficient of (the remaining terms of) F at this degree
		coeffG = g.lc()		# The leading coefficient of g
		# If the term of this degree has coefficient 0 then skip over this degree.
		if coeffF == 0:
			continue

		coeffStepQ = findQ(coeffF, coeffG, m)		# The coefficient necessary to subtract the current degree away from F
		if coeffStepQ == -1:
			break

		stepTerm = Poly.getX(d - g.degreeMax(), m)*coeffStepQ		# Eg, if the stepQ = 4 and we multiplied by X^2 then 4X^2 will be added to Q
		q += stepTerm
		stepPoly -= g*stepTerm

	r = stepPoly		# After the for loop, the stepPoly variable will hold the remainder

	return q, r


# Finds the q such that a = q*b mod m
# !!!If such a q does not exist, then this function returns -1!!!
def findQ(a, b, m) -> int:
	for q in range(m):
		if a == (q*b) % m:
			return q

	return -1


# Find the modular inverse of a mod m
# !!!If such an inverse does not exist, then this function returns -1!!!
def modInverse(a, m) -> int:
	for q in range(m):
		if 1 == (q*a) % m:
			return q

	return -1


# Returns, in a tuple (x, y, d), such that x*f + y*g = d mod ... with d = gcd(f, g)
def euclidExtended(f : Poly, g : Poly) -> Tuple[Poly, Poly, Poly]:
	# Check for invalidity of the usage of this function
	testValidity(f, g)

	a : Poly = copy(f)
	b : Poly = copy(g)
	m = f.mod()
	x, v = Poly([1], m), Poly([1], m)
	y, u = Poly([0], m), Poly([0], m)

	# The algorithm from the algebra script [2.3.10]
	# The use of a try/except block is not necessary here, as the while statement ensures there is never division by zero.
	while not b.isZero():
		q, r = longDivision(a, b)
		a, b = b, r
		x1, y1 = x, y
		x, y = u, v
		u = x1 - q*u
		v = y1 - q*v

	xFinal : Poly = x*modInverse(a.lc(), m)
	yFinal : Poly = y*modInverse(a.lc(), m)

	return xFinal, yFinal, xFinal*f + yFinal*g


# Returns whether f and g are congruent, eg: f === g mod h
def congruence(f : Poly, g : Poly, h : Poly) -> bool:
	# Check for invalidity of the usage of this function
	testValidity(f, g)
	testValidity(f, h)

	diff = f - g
	try:
		q, r = longDivision(diff, h)		# If the difference of f and g is a multiple of h then it's congruent. Eg, r == 0
	except:
		return False

	return r.isZero()


# Returns a polynomial mod 'mod' of degree 'degree' that is irreducible
def findIrreducible(degree : int, mod : int) -> Poly:
	testedPoly = Poly([1] + [0]*degree, mod)
	# Special case where the requested degree is 1, where all polynomials are irreducible
	if degree == 1:
		return testedPoly

	checkedAll = False
	while not checkedAll:
		if testedPoly.isIrreducible():
			return testedPoly

		# Iterate over the coefficients
		testedPoly[0] += 1
		for d in testedPoly.degreeListAsc():
			if testedPoly[d] == mod:
				testedPoly[d + 1] += 1
		testedPoly.reduce()

		# Check if all options have been looked at
		if testedPoly.lc() == 0:
			checkedAll = True


# Testing... Can be ignored and has to be removed in the end product
# mod = 7
# # print(findQ(6, 5, 7))
#
# x = Poly([6], mod)
# y = Poly([5], mod)
# q, r = longDivision(x, y)
# print(q, r)
#
# a = Poly([1, 1, 1], mod)
# b = Poly([2, -2], mod)
# q, r = longDivision(a, b)
# print(q, r)
#
# c = Poly([1, 0, 0, 2, 6, 3], mod)
# d = Poly([1, 0, 3], mod)
# q, r = longDivision(c, d)
# print(q, r)
#
# e = Poly([1, 2, 3, 4, 5, 6], mod)
# f = Poly([1, 5], mod)
# q, r = longDivision(e, f)
# print(q, r)
#
# g = Poly([3, 1, 0, 0, 1], 5)
# h = Poly([4, 2, 0], 5)
# q, r = longDivision(g, h)
# print(q, r)
#
# i = Poly([3, 2, 0], 11)
# j = Poly([2, 0, 1], 11)
# q, r = longDivision(i, j)
# print(q, r)
#
# k = Poly([1, 5, 4, 8, 9, 0], 7)
# l = Poly([1, 5, 4, 8, 2, 0], 7)
# q, r = longDivision(k, l)
# print(q, r)
#
# m = Poly([3, 5], 7)
# n = Poly([9, 11, 5], 7)
# q, r = longDivision(m, n)
# print(q, r)
#
# o = Poly([6, 5, 0], 7)
# p = Poly([0, 0, 0, 0], 7)
# # q, r = longDivision(o, p)
# # print(q, r)
# q, r = longDivision(p, o)
# print(q, r)

# mod = 7
# a = Poly([1, 1, 1], mod)
# b = Poly([3], mod)
# c = Poly([0], mod)
# print(congruent(a, b, c))
#
# mod = 3
# a = Poly([1, 0, 0, 2], mod)
# b = Poly([1], mod)
# c = Poly([1, 1], mod)
# print(congruent(a, b, c))

# print(findIrreducible(3, 2))
# print(findIrreducible(4, 2))
# print(findIrreducible(4, 2))

# x = Poly([5, 3], 7)
# y = Poly([5], 7)
# q, r = longDivision(x, y)
# print(q, r)

# a = Poly([1, 1, 1], 7)
# b = Poly([2, -2], 7)
# x, y, d = EuclidExtended(a, b)
# print(x, y, d)
#
# a = Poly([1, 0, 1], 7)
# b = Poly([1, 0, 0, 1], 7)
# x, y, d = EuclidExtended(a, b)
# print(x, y, d)
#
# a = Poly([1, 1, 1], 7)
# b = Poly([0], 7)
# x, y, d = EuclidExtended(a, b)
# print(x, y, d)
#
# a = Poly([2, 2, 2], 7)
# b = Poly([0], 7)
# x, y, d = EuclidExtended(a, b)
# print(x, y, d)
#
# a = Poly([1, 1, 0, 0], 2)
# b = Poly([1, 0, 1], 2)
# x, y, d = EuclidExtended(a, b)
# print(x, y, d)
#
# a = Poly([1, 2, 0, 1], 3)
# b = Poly([1, 1, 1], 3)
# x, y, d = EuclidExtended(a, b)
# print(x, y, d)

# a = Poly([1, 2, 2, 0, 1], 3)
# h = Poly([2, 2, 2, 2], 3)
# c = Poly([1, 0, 0, 1, 2], 3)
# one = Poly([1], 3)
# print(congruence(a, h, c))
# h2 = h*h
# print(h2)
# print(congruence(h2, one, c))
# print(c*Poly([1, 2, 0], 3))
# h2 = Poly([2, 1, 1], 3)
# h4 = h2*h2
# print(h4)
# print(congruence(h4, one, c))
# h4 = Poly([1, 2, 1, 0], 3)
# h8 = h4*h4
# print(h8)
# print(congruence(h8, one, c))
# print(c*Poly([1, 1, 0], 3))
# h8 = Poly([1, 1, 0], 3)
# h16 = h8*h8
# print(h16)
# print(congruence(h16, one, c))
# h16 = Poly([2, 1, 2, 1], 3)
# h32 = h16*h16
# print(h32)
# print(congruence(h32, one, c))
# print(c*Poly([1, 1, 0], 3))
# h32 = Poly([1, 0, 2, 1], 3)
# h40 = h32*h8
# print(congruence(h40, Poly([2,2,1,1], 3), c))
# print(h40)
# print(congruence(h40, one, c))
# print(c*Poly([1, 1], 3))

# print(findQ(0, 1, 5))
# a = Poly([1, 0, 4, 3], 5)
# h = Poly([3, 2], 5)
# c = Poly([1, 0, 1, 1], 5)
# one = Poly([1], 5)
# print(a, h, c)
# print(congruence(a, h, c))
# print(h*h)
# h2 = Poly([4, 4, 1, 3], 5)
# print(h2*h2)
# print(congruence(h2*h2, one, c))
# print(c*Poly([1, 2, 3, 4], 5))
# h4 = Poly([4, 0], 5)
# print(h4*h4)
# print(congruence(h4*h4, one, c))
# h8 = Poly([1, 0, 0], 5)
# print(h8*h8)
# print(congruence(h8*h8, one, c))
# print(c*Poly([1, 0], 5))
# h16 = Poly([4, 4, 0], 5)
# print(h16*h8)
# print(congruence(h16*h8, one, c))
# print(c*Poly([4], 5))
# h24 = Poly([1, 2, 1], 5)
# print(h24*h4)
# print(congruence(h24*h4, one, c))
# print(c*4)
# h28 = Poly([3, 0, 1], 5)
# print(h28*Poly([4, 2, 4], 5))
# print(congruence(h28*Poly([4, 2, 4], 5), one, c))
# print(c*Poly([2, 0], 5))
# h30 = Poly([4, 4, 3], 5)
# print(h30*h)
# print(congruence(h30*h, one, c))
# print(c*2)
# h31 = Poly([4], 5)
# print(h31*h31)
# print(congruence(h31*h31, one, c))

# print(Poly([1, 0, 0, 1], 2).isIrreducible())

# print(findIrreducible(3, 7))
