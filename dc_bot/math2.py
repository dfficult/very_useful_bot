import math


"[√] <-- This is square root"

# 分數
class Fraction:
	def __init__(self, a: int, b: int):
		# a/b
		self.a = a
		self.b = b
	def simplify(self) -> None:
		gcd = math.gcd(self.a, self.b)
		self.a = self.a // gcd
		self.b = self.b // gcd
	def add(self, to_add) -> None:
		self.a = self.a*to_add.b + to_add.a*self.b
		self.b = self.b*to_add.b
		self.simplify()
	def minus(self, to_minus) -> None:
		self.a = self.a*to_minus.b - to_minus.a*self.b
		self.b = self.b*to_minus.b
		self.simplify()
	def multiply(self, to_multiply) -> None:
		self.a *= to_multiply.a
		self.b *= to_multiply.b
		self.simplify()
	def divide(self, to_divide) -> None:
		self.a *= to_divide.b
		self.b *= to_divide.a
		self.simplify()
	def to_float(self) -> float:
		return self.a / self.b
	def to_percentage(self) -> float:
		return self.a / self.b * 100


# 整理方程式 
def cleanup(eq: str) -> list:
	# 3x-5+2y+6=7 -> [{'x': 3.0, 'y': 2},6]
	
	# find variables
	vars = []
	non_vars = "1234567890=+-*/×÷√><."
	for i in eq:
		if i not in non_vars and i not in vars:
			vars.append(i)
	if len(vars) in [1,2]:
		pass
	elif len(vars) == 0:
		raise TypeError("No variables entered into the function")
	else:
		raise TypeError("Too many variables (Maximum two, and the max length of a var is 1)")
	
	# seperate left and right
	left = []
	right = []
	is_left = True
	r = ""
	skip = False
	for x in eq:
		if (skip): skip = False ; continue
		if(x == "+"):
			if (is_left):
				left.append(r)
			else:
				right.append(r)
			r = ""
		elif (x == "-"):
			if (is_left):
				left.append(r)
			else:
				right.append(r)
			r = "-"
		elif (x in "><="):
			left.append(r)
			is_left = False
			if ("<=" in eq or ">=" in eq):
				skip = True
			r = ""
		else:
			r += x
	right.append(r)
	try: left.remove("")
	except: pass
	try: right.remove("")
	except: pass

	# deg1/deg2 to left and deg0 to right
	for i in range(len(left)):
		try:
			left[i] = -int(left[i])
			right.append(left[i])
			left[i] = '&' # Placeholder
		except: pass
	for i in range(len(right)):
		try:
			right[i] = int(right[i])
		except:
			left.append(f"-{right[i]}" if right[i][0] != '-' else right[i][1:])
			right[i] = '&' # Placeholder
	try: left.remove('&')
	except: pass
	try: right.remove('&')
	except: pass

	# add up everything in deg0
	r = 0
	for i in right:
		r += i
	
	# finish deg1 and deg2
	l = {}
	for i in vars:
		l[f"{i}"] = 0
	for i in left:
		for j in vars:
			if j in i:
				temp = i
				temp = temp.replace(f'{j}','')
				if temp == '': temp = 1
				if temp == '-': temp = -1
				temp = float(temp)
				l[f"{j}"] += temp

	return [l, r]
				

# 二元一次聯立方程式
def solve_21(eq1: str, eq2: str) -> list[str]:
	e1 = cleanup(eq1)
	e2 = cleanup(eq2)
	
	# { a1x + b1y = c1
	# { a2x + b2y = c2
	# 
	# D=|a1 b1|, Dx=|c1 b1|, Dy=|a1 c1|
	#   |a2 b2|     |c2 b2|     |a2 c2|
	# 
	# D!=0 -> x=Dx/D, y=Dy/D
	# D=0, Dx=0, Dy=0 -> 無限多解
	# D=0, Dx^2+Dy^2!=0 -> 無解
	




# 質因數分解
def factorize(num) -> list:
	i = 2
	f = []
	while i * i <= num:
		if num % i == 0:
			num //= i
			f.append(i)
		else:
			i += 1
	if num > 1:
		f.append(num)
	return f

# 簡化根號
def sim_sqrt(num: int) -> list:
	# return s [a,b] means a√b
	f = factorize(num)
	if len(f) == 1:
		return [1, num]
	else:
		s = [1,1]
		i = 0
		while i < len(f):
			current_amount = f.count(f[i])
			if current_amount % 2 == 0:
				# ex: 4
				for _ in range(current_amount // 2): s[0] *= f[i]
				i += current_amount
			elif (current_amount-1) % 2 == 0:
				# ex: 3
				s[1] *= f[i]
				for _ in range((current_amount-1) // 2): s[0] *= f[i]
				i += current_amount
			else:
				i += 1
	return s


print(cleanup("3x-5+9+2y=7-5y"))