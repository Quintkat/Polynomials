# SUPPORTED FUNCTIONALITY:
# Where p is a variable of type Polynomial
# Written out polynomials in this documentation are encased in {}
# - Creating a polynomial: using the constructor Polynomial(c, m),
# 	you need to give a list of coefficients c going from highest degree to lowest degree, and a modulus m for the polynomial.
#
# - Getting the 'pretty print string' of the polynomial: str(p) (or print(p) of course, when testing)
#
# - Getting the list of coefficients of the polynomial: p.polynomial()
# 	As far as I know, only necessary when converting p to a list for the "answer-poly" and such parameters.
#
# - Getting the modulus of the polynomial: p.mod()
# 	Useful when needing to create a new polynomial without needing another parameter in the function.
#
# - Getting the maximum degree and leading coefficient: p.degreeMax() and p.leadingCoeff() or p.lc()
# 	Eg: if p represents {2x^3 + x + 1} then p.degreeMax() returns 3 and p.lc() returns 2
#
# - Boolean statements about the polynomial: p.isZero(), p.isIrreducible()
# 	- p.isZero() returns true if p represents {0}
# 	- p.isIrreducible() returns true if p is irreducible
#
# - Arithmetic operations on polynomials: +, -, *
# 	Support for both polynomials (q) and integers (i). !!!For operations with integers the integer always has to come after p.!!!
# 	- + : p + q or p + i
# 	- - : p - q or p - i
# 	- * : p*q   or p*i
#
# - Unary operations of the polynomial: -p
# 	- -p : Returns a new polynomial that is the negated version of p. Eg: -{3x + 1} returns {4x + 6} mod 7
#
# - Computing the value of the polynomial with x=value: p.compute(value)
# 	Eg: with p representing {2x^3 + x + 6} and p.mod() == 7, p.compute(6) returns 3.
#
# - Getting a list of degrees: p.degreeList() or p.degrees() and p.degreeListAsc()
# 	Eg: if p represents {x^6} then p.degrees() returns [6, 5, 4, 3, 2, 1, 0] (p.degreeListAsc() will return it but flipped)
# 	This is useful when operating on a polynomial per coefficient. Eg: 'for i in p.degrees: z = p[i] ...'
# 	Note: It turns out that in I think almost all operations you want to do on a polynomial, the order in which you go over the terms is
# 	irrelevant. So use of either p.degrees() or p.degreesAsc() is totally possible in almost all cases
#
# - Getting a coefficient: p[d].
# 	Gives the coefficient at degree d. Eg: if p represents {4x^3 + x^2 + 3x + 6} then p[0] == 6, p[3] == 4, and p[2] == 1.
# 	Note: if d > p.degreeMax() then p[d] returns 0. (this makes sense, as {4x^3} == {0*x^5 + 4x^3})
#
# - Setting a coefficient: p[d] = z
# 	Allows you to set individual coefficients of the polynomial p.
# 	This functionality should only really be used in the case of manipulating a polynomial without much care for the polynomial itself
# 	but instead inspecting different polynomials like in PolynomialArithmetic.findIrreducible(). Otherwise, constructing a new polynomial is
# 	better. Usually after setting however many coefficients in p it is useful to call p.reduce(), so that all coefficients are modded again.
# 	Note: if d > p.degreeMax() then nothing will happen. This functionality does not support modifying the polynomial to a higher degree.
#
# - Getting the values for which p.compute(value) == 0: p.zeros()
#
# - Two static methods: Poly.getX(d, mod), Poly.degreeIndexGen(max, d)
# 	- getX(degree, mod): for when you need a polynomial that is simply {x^d}. The mod parameter is necessary for the constructor.
# 	- degreeIndexGen(max, degree): tells you what index in a polynomial list degree d would appear at
# 		if that polynomial had max degree 'max'. This is useful when constructing a coefficient list that will become a polynomial.
# 		Small example on that: 'coefficients = [0]*(someDegree + 1)
# 								for d in p.degrees(): coefficients[Poly.degreeIndexGen(someDegree, d)] = p[d]*q[d]'
#
# UNSUPPORTED FUNCTIONALITY:
# - "for i in poly:" where poly is a Polynomial. This class does not implement iterability
# 	Instead: do "for d in poly.degrees():" and access the term at degree d with "poly[d]"
#
class Polynomial:
	poly : list
	modulo : int

	# Constructor
	# The list coefficients has the degree in descending order. Eg: X^2+3X+7 = [1, 3, 7]
	# Good to note: no need to preprocess the modulo of the coefficients if you create a new polynomial, this function do it itself
	def __init__(self, coefficients : list, modulo : int, removeLeadingZeroes : bool = True):
		self.poly = []
		self.modulo = modulo
		for c in coefficients:
			self.poly.append(c % self.modulo)

		# Get rid of any zeroes that are at the beginning, as they are not supposed to have them
		if removeLeadingZeroes:
			self.stripZeroes()

	# Returns the coefficient at degree 'degree'. Implementation of indexing as if the object were a list, basically. eg: p[2]
	def __getitem__(self, degree : int) -> int:
		# Even if this polynomial does not go up to this degree, it can say 0 and it's equivalent
		if degree > self.degreeMax():
			return 0

		return self.poly[self.degreeIndex(degree)]

	# Functionality for saying p[i] = something
	def __setitem__(self, degree : int, value : int):
		if degree > self.degreeMax():
			return

		self.poly[self.degreeIndex(degree)] = value

	# Reduces the current polynomial with the modulus (modifies the polynomial)
	def reduce(self):
		for d in self.degrees():
			self[d] = self[d] % self.mod()

	# Returns the index in poly of a certain degree
	def degreeIndex(self, degree : int) -> int:
		return self.degreeMax() - degree

	# Returns the index in poly of a certain degree in general, given a max degree
	@staticmethod
	def degreeIndexGen(max : int, degree : int) -> int:
		return max - degree

	# Returns the pretty printed string of the polynomial
	def __str__(self) -> str:
		if self.isZero():
			return "0"
		output = ""
		terms = []
		# Precomputes the string representations of the strings
		for d in self.degreeList():
			term = self.termStr(d)
			if term != "0":
				terms.append(term)

		# Adds the terms with the +'s in between
		output += terms[0]
		for t in terms[1:len(terms)]:
			output += "+" + t

		return output

	# Returns the string representation of a term
	def termStr(self, degree : int) -> str:
		output = ""
		coefficient = self[degree]
		if coefficient == 0:
			return "0"

		if coefficient > 1 or degree == 0:
			output += str(coefficient)

		if degree > 1:
			output += "X^" + str(degree)
		elif degree == 1:
			output += "X"

		return output

	def __eq__(self, other) -> bool:
		if type(other) != type(self):
			raise Exception("You can only compare Polynomials to other Polynomials")

		# The modulo and max degree have to be the same
		if self.mod() != other.mod() or self.degreeMax() != other.degreeMax():
			return False

		# Every coefficient has to be the same
		for d in self.degreeListAsc():
			if self[d] != other[d]:
				return False

		# Otherwise it has passed all tests
		return True

	# Returns a list that shows what degree is represented by what index in the poly list (eg. it's degrees in descending order)
	def degreeList(self) -> list:
		return list(range(len(self.poly) - 1, -1, -1))

	# The degree list but in ascending order
	def degreeListAsc(self) -> list:
		return list(reversed(self.degreeList()))

	# Shorthand for degreeList()
	def degrees(self) -> list:
		return self.degreeList()

	# Returns the max degree of the polynomial
	def degreeMax(self) -> int:
		return len(self.poly) - 1

	# Returns the leading coefficient
	def leadingCoeff(self) -> int:
		return self[self.degreeMax()]

	# Shorthand for leadingCoeff()
	def lc(self) -> int:
		return self.leadingCoeff()

	# Returns whether the polynomial represents 0
	def isZero(self) -> bool:
		result = True
		for d in self.degrees():
			c = self[d]
			if c != 0:
				result = False
				break

		return result

	# Modifies the polynomial to get rid of the leading zero terms
	def stripZeroes(self):
		while self[self.degreeMax()] == 0 and len(self.poly) > 1:
			self.poly.remove(0)

	# Returns a copy of this polynomial with zeroes added up to degree 0
	# Returns a polynomial
	def extendedZeros(self, degree : int):
		coefficients = self.poly.copy()
		# Insert 0 at the front up to the wanted degree
		for i in range(self.degreeMax(), degree):
			coefficients.insert(0, 0)

		return Polynomial(coefficients, self.mod())

	# Returns the internal list of this polynomial
	def polynomial(self) -> list:
		return self.poly

	# Returns the modulo of this polynomial
	def mod(self) -> int:
		return self.modulo

	# Returns a new polynomial that is a copy of this one
	# Returns a Polynomial
	def __copy__(self):
		coefficients : list = self.poly.copy()
		mod : int = self.mod()
		return Polynomial(coefficients, mod)

	# Tests if the other object is valid for +-*/ operations
	def testOther(self, other):
		if type(other) != type(self):
			raise Exception("You can only do operations with the Polynomial class or integers onto a Polynomial")

		if self.mod() != other.mod():
			raise Exception("You can only do operations on Polynomials of the same modulo")

	# Negation operation, eg: -a
	# Returns a polynomial
	def __neg__(self):
		coefficients = [0*i for i in self.degrees()]
		for d in self.degrees():
			coefficients[self.degreeIndexGen(self.degreeMax(), d)] = -self[d]

		return Polynomial(coefficients, self.mod())

	# Addition operation, eg: a + b
	# Returns a Polynomial
	def __add__(self, other):
		# If you are just adding an integer we have this special case.
		if isinstance(other, int):
			return self.addInt(other)

		# Exceptions
		self.testOther(other)

		# If either polynomial is zero, just return a copy of the other one.
		if self.isZero():
			return other.__copy__()

		if other.isZero():
			return self.__copy__()

		# Otherwise, do addition
		degrees = self.degrees() if self.degreeMax() > other.degreeMax() else other.degrees()
		maxDegree = degrees[0]
		resultCoefficients = [0*i for i in degrees]

		for d in degrees:
			resultCoefficients[self.degreeIndexGen(maxDegree, d)] = self[d] + other[d]

		resultPoly = Polynomial(resultCoefficients, self.mod())
		return resultPoly

	# Adds an integer to a polynomial
	# Returns a Polynomial
	def addInt(self, other):
		intPoly = Polynomial([other], self.mod())
		return self + intPoly

	# Subtraction operation, eg: a - b
	# Returns a Polynomial
	def __sub__(self, other):
		# Special case where other is simply an integer that is being subtracted
		if isinstance(other, int):
			return self + (-other)

		# Exceptions
		self.testOther(other)

		# The subtraction
		return self + (-other)

	# Multiplication operation, eg: a*b
	# Returns a Polynomial
	def __mul__(self, other):
		# Special case that's supported where other is just an int
		if isinstance(other, int):
			return self.mulInt(other)

		# Exceptions
		self.testOther(other)

		# The multiplication
		resultMaxDegree = self.degreeMax() + other.degreeMax()
		resultCoefficients = [0]*(resultMaxDegree + 1)

		for dSelf in self.degrees():
			for dOther in other.degrees():
				dResult = dSelf + dOther
				index = self.degreeIndexGen(resultMaxDegree, dResult)
				resultCoefficients[index] += self[dSelf]*other[dOther]

		resultPoly = Polynomial(resultCoefficients, self.mod())
		return resultPoly

	# Multiplies the polynomial with an integer
	# Returns a polynomial
	def mulInt(self, other):
		intPoly = Polynomial([other], self.mod())
		return self*intPoly

	# Returns a polynomial that is X^degree, and just that
	# Returns a polynomial
	@staticmethod
	def getX(degree, mod):
		coefficients = [1] + [0]*degree
		return Polynomial(coefficients, mod)

	# Returns the value of the polynomial with a given input for X
	def compute(self, x):
		answer = 0
		for d in self.degreeList():
			answer += (self[d]*pow(x, d, self.mod())) % self.mod()

		return answer % self.mod()

	# Returns whether or not the polynomial is irreducible
	def isIrreducible(self) -> bool:
		# Polynomials of degree 1 and 0 are always irreducible
		if self.degreeMax() < 2:
			return True

		return len(self.zeros()) == 0

	# Returns the zeros of this polynomial
	def zeros(self) -> list:
		zeros = []
		for i in range(self.mod()):
			if self.compute(i) == 0:
				zeros.append(i)

		return zeros


# Testing... Can be ignored and has to be removed in the end product
# def generatePolynomials(degree : int, mod : int):
# 	polynomials = []
# 	def generateRecursive

# p = Polynomial([0, 1, 10, -1, 0, 2, 3], 7)
# print(p.degreeList())
# print(p.degreeListAsc())
# print(p.degreeMax())
# print(p[0], p[1], p[2], p[5])
# print(p)
# print(str(p))
# print(p.poly)
# p[0] = 6
# print(p.poly)
# a = Polynomial([4, 5], 10)
# b = Polynomial([0, 4, 5], 10)
# c = Polynomial([1, 1], 10)
# d = Polynomial([4, 5], 9)
# e = Polynomial([2, 0, 2, 1, 0], 10)
# print(a == b)
# print(b == a)
# print(a == c)
# print(a == d)
# print(b == d)
# print(a + e)
# print(a - e)
# print(e - a)
# ap = a + 6
# am = a - 6
# print(ap.poly, ap)
# print(am.poly, am)
# x = Polynomial([1, 1], 3)
# y = Polynomial([1, 3], 3)
# z = Polynomial([1], 3)
# za = Polynomial([0], 3)
# a = Polynomial([1, 1], 10)
# b = Polynomial([1, 0], 10)
# c = Polynomial([0], 10)
# print(a*b)
# print(a*b*4)
# print(a*b*c+4)
#
# x = Polynomial([4,0,0,0,7,2,4,6,1,2], 7)
# y = Polynomial([8,39,18,1], 7)
# print(x*y)
# a = Polynomial([1, 0], 10)
# print(a)
# a += 1
# print(a)
# b = Polynomial([5, 0, 0, 6], 10)
# print(b)
# a += b
# print(a)
# a = Polynomial([1, 1, 1], 3)
# print(a.isIrreducible())

# a = Polynomial([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2, 0, 1, 6], 7)
# print(a.compute(6))

# a = Polynomial([1, 2, 2, 0, 1], 3)
# b = Polynomial([2, 2, 2, 2], 3)
# print(a - b)

# h = Polynomial([])
