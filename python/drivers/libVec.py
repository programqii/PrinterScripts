from libUtils import JsonType

class MathError(Exception):
	def __init__(self, message):
		self.message = message;
	def __str__(self):
		return repr(self.message);
@JsonType("vector")
class vec(object):
	def __init__(self, *nums, **args):
		self._data = [];
		self._names = {"x":0, "y":1, "z":2,"w":3, "u":0, "v":1, "r":0, "g":1, "b":2, "a": 3}
		value =0;
		if "value" in args:
			value = args["value"]
		if "names" in args:
			self._names = args["names"];
			maxValue  = 0;
			for i in self._names:
				maxValue = max(maxValue, self._names[i]);
			self._data = [0] * (maxValue +1);
		if "size" in args:
			if len(nums) == 1 and (isinstance(nums[0], int) or isinstance(nums[0], float)):
				self._data = [nums[0]] * args["size"];
			else:
				self._data = [0] * args["size"];
		if len(nums) == 1 and not (isinstance(nums[0], int) or isinstance(nums[0], float) ):
			if isinstance(nums[0], list):
				self._data = nums[0][:];
			elif isinstance(nums[0], tuple):
				self._data = [x for x in nums[0]];
			elif isinstance(nums[0], vec):
				self._data = nums[0]._data[:];
				self._names = {};
				for i in nums[0]._names:
					self._names[i] = nums[0]._names[i];
		elif (not "size" in args) and len(nums) > 0:
			self._data = [x for x in nums];
		if "list" in args:
			self._data = args["list"][:]; #create copy
		temp = {};
		for i in self._names:
			if self._names[i] < len(self._data):
				temp[i] = self._names[i];
		self._names = temp;
		#Convert to floats if data contains a single float
		isFloat = False;
		for i in self._data:
			isFloat = isFloat or isinstance(i, float);
		if isFloat:
			self._data = [float(x) for x in self._data];
	@staticmethod
	def fromJson(jsonNode):
		return vec(*jsonNode["data"]);
	def toJson(self):
		return {"data": self._data};
	def updateFromJson(self, jsonNode, blackList=[], whiteList=None):
		self._data = jsonNode["data"];
	def toString(self):
		return str(self._data);
	def __str__(self):
		return str(self._data);
	def magnitude(self):
		sum = 0;
		for i in self._data:
			sum += i*i;
		return sum ** 0.5
	def copy(self):
		return vec(names=self._names, list=self._data)
	def __getattr__(self, name):
		if name[0] == "_":
			return super(vec, self).__getattr__(name);
		else:	
			for i in name:
				if not (i in self._names):
					raise AttributeError("Getter for " + name + " Does not exist/Missing name " + i);
			retList = [];
			for i in name:
				retList += [self._data[self._names[i]]];
			return vec(list=retList, names=self._names);
	def __setattr__(self, name, value):
		if name[0] == "_":
			super(vec, self).__setattr__(name, value);
		else:
			if len(name) != len(value._data):
				raise AttributeError("Attempted to assign a vector of size " + str(len(value._data)) + " to a vector of size " + str(len(self._data)) + " When Assigning " + name);
			for i in name:
				if not (i in self._names):
					raise AttributeError("Setter for " + name + " Does not exist/Missing name " + i);
			for i in names:
				self._data[self._names[i]] = value._data[i];  
	def mag(self):
		self.magnitude();
	def __add__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a + b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the + aka __add__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a + b
		return ret;
	def __radd__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b + a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the + aka __radd__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b + a
		return ret;
	def __sub__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a - b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the - aka __sub__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a - b
		return ret;
	def __rsub__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b - a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the - aka __rsub__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b - a
		return ret;
	def __div__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a / b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the / aka __div__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a / b
		return ret;
	def __rdiv__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b / a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the / aka __rdiv__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b / a
		return ret;
	def __truediv__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a / b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the / aka __truediv__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a / b
		return ret;
	def __rtruediv__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b / a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the / aka __rtruediv__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b / a
		return ret;
	def __mul__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a * b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the * aka __mul__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a * b
		return ret;
	def __rmul__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b * a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the * aka __rmul__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b * a
		return ret;
	def __floordiv__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a // b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the // aka __floordiv__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a // b
		return ret;
	def __rfloordiv__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b // a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the // aka __rfloordiv__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b // a
		return ret;
	def __mod__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a % b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the % aka __mod__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a % b
		return ret;
	def __rmod__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b % a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the % aka __rmod__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b % a
		return ret;
	def __pow__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a ** b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the ** aka __pow__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a ** b
		return ret;
	def __rpow__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b ** a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the ** aka __rpow__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b ** a
		return ret;
	def __xor__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a ^ b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the ^ aka __xor__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a ^ b
		return ret;
	def __rxor__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b ^ a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the ^ aka __rxor__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b ^ a
		return ret;
	def __and__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a & b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the & aka __and__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a & b
		return ret;
	def __rand__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b & a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the & aka __rand__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b & a
		return ret;
	def __or__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a | b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the | aka __or__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a | b
		return ret;
	def __ror__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [b | a for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the | aka __ror__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = b | a
		return ret;
	def __rshift__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a >> b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the >> aka __rshift__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a >> b
		return ret;
	def __lshift__(self, v):
		ret = None;
		if isinstance(v, int) or isinstance(v, float):
			ret = self.copy();
			b = v;
			ret._data = [a << b for a in ret._data]
			return ret;
		input_b = vec(v);
		if len(input_b._data) != len(self._data):
			# Raise Exception ?
			raise MathError("Bad Data when preforming the << aka __lshift__ operator (different sizes of vec) " + str(len(input_b._data)) + " vs. " + str(len(self._data)) )
			return None;
		ret = self.copy();
		for i in range(0,len(input_b._data)):
			a = ret._data[i];
			b = v._data[i];
			ret._data[i] = a << b
		return ret;
	def __iadd__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] += v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] += v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] += input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation += aka __iadd__");
		# raise Exception here ?
	def __isub__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] -= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] -= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] -= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation -= aka __isub__");
		# raise Exception here ?
	def __idiv__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] /= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] /= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] /= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation /= aka __idiv__");
		# raise Exception here ?
	def __itruediv__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] /= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] /= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] /= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation /= aka __itruediv__");
		# raise Exception here ?
	def __imul__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] *= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] *= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] *= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation *= aka __imul__");
		# raise Exception here ?
	def __imod__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] %= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] %= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] %= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation %= aka __imod__");
		# raise Exception here ?
	def __iand__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] &= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] &= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] &= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation &= aka __iand__");
		# raise Exception here ?
	def __ixor__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] ^= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] ^= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] ^= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation ^= aka __ixor__");
		# raise Exception here ?
	def __ifloordiv__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] //= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] //= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] //= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation //= aka __ifloordiv__");
		# raise Exception here ?
	def __ilshift__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] <<= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] <<= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] <<= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation <<= aka __ilshift__");
		# raise Exception here ?
	def __irshift__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] >>= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] >>= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] >>= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation >>= aka __irshift__");
		# raise Exception here ?
	def __ior__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] |= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] |= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] |= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation |= aka __ior__");
		# raise Exception here ?
	def __ipow__(self, v):
		if isinstance(v, int) or isinstance(v, float):
			for i in range(0, len(self._data)):
				self._data[i] **= v;
			return ;
		if isinstance(v, vec) and len(v._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] **= v._data[i];
			return ;
		input_b = vec(v);
		if len(input_b._data) == len(self._data):
			for i in range(0, len(self._data)):
				self._data[i] **= input_b._data[i];
			return ;
		raise MathError("Cannot preform in-fix operation **= aka __ipow__");
		# raise Exception here ?
	def __pos__(self):
		return vec(names=self._names, list=[+a for a in self._data]);
	def __neg__(self):
		return vec(names=self._names, list=[-a for a in self._data]);
	def __inv__(self):
		return vec(names=self._names, list=[~a for a in self._data]);
	def __invert__(self):
		return vec(names=self._names, list=[~a for a in self._data]);
	def __abs__(self):
		return vec(names=self._names, list=[abs(a) for a in self._data]);
	def asFloat(self):
		return vec(names=self._names, list=[float(a) for a in self._data]);
	def asInt(self):
		return vec(names=self._names, list=[int(a) for a in self._data]);