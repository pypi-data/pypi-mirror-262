class CODER():
	code = {}
	def __init__(self, code2=False):
		import os
		try:
			os.mkdir("coderFiles")
		except:
			pass
		if code2:
			self.code = code2
		else:
			try:
				file = open("coderFiles/code.txt", 'x')
				file.close()
				self.set_code({'Q': '7436', 'W': '3394', 'E': '8777', 'R': '7611', 'T': '2202', 'Y': '7079', 'U': '5802', 'I': '3016', 'O': '6854', 'P': '6324', 'A': '9551', 'S': '4658', 'D': '2534', 'F': '6545', 'G': '3541', 'H': '9596', 'J': '7903', 'K': '9551', 'L': '3355', 'Z': '9651', 'X': '2139', 'C': '3306', 'V': '9678', 'B': '2497', 'N': '259', 'M': '3033', '0': '3439', '1': '7613', '2': '4441', '3': '3910', '4': '5273', '5': '9981', '6': '9741', '7': '5729', '8': '7181', '9': '6152', 'Й': '9472', 'Ц': '7515', 'У': '8745', 'К': '352', 'Е': '8987', 'н': '6937', 'Г': '4856', 'Ш': '4393', 'Щ': '4173', 'З': '6131', 'Х': '2700', 'Ї': '7228', 'Ф': '3779', 'І': '1469', 'В': '9572', 'А': '9672', 'П': '6841', 'Р': '3184', 'О': '4882', 'Л': '1220', 'Д': '2891', 'Ж': '7549', 'Є': '6249', 'Я': '7829', 'Ч': '3257', 'С': '1491', 'М': '2235', 'И': '654', 'Т': '2047', 'Ь': '5643', 'Б': '5', 'Ю': '8841', 'Ґ': '9538', 'Ъ': '6156', 'Э': '7625', 'Ы': '8407', 'Ё': '4703', ' ': '1015', '@': '6958', '#': '6239', '₴': '7966', '₽': '1994', '_': '1548', '&': '3634', '-': '801', '+': '2090', '(': '6770', ')': '7014', '/': '8070', '*': '8141', '"': '8999', "'": '7818', ':': '9341', ';': '1100', '!': '3187', '?': '4978', '~': '8971', '`': '5236', '=': '5996'})
			except:
				pass
			file = open("coderFiles/code.txt", 'r')
			import ast
			a = file.read()
			self.code = ast.literal_eval(a)
	def encode(self, data):
	   encoded = ""
	   for char in data:
	   	encoded += self.code[char.upper()]
	   return encoded

	def decode(self, data):
	   decoded = ""
	   while data:
	        for char, sequence in self.code.items():
	            if data.startswith(sequence):
	            	decoded += char
	            	data = data[len(sequence):]
	            	break
	   return decoded

	def create_code(self, save=False):
		import random
		a = list(self.code.keys())
		for i in range(len(self.code)):
			u = str(random.randint(0, 10000))
			for io in self.code.values():
				while u == io:
					u = str(random.randint(0,10000))
				self.code[a[i]] = u
		if save:
			self.set_code(self.code)

	def set_code(self, code2):
		self.code = code2
		file = open("coderFiles/code.txt", "w")
		file.write(str(code2))
		file.close()