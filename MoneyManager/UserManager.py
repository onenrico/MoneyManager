import Security


class Manager(object):
	# Fungsi untuk meload class SQLManager
	def load(self,sqlmanager):
		self.sqlman = sqlmanager
	
	# Fungsi untuk mengambil semua user yang sudah register
	def getUsers(self):
		return self.sqlman.select("users","username").fetchall()
		
	# Fungsi untuk mengetahui apakah user tersebut sudah register atau belum
	def checkRegistered(self,username):
		data = self.sqlman.select("users","username",{"username":username}).fetchall()
		if(len(data) > 0):
			return True
		return False
	
	# Fungsi untuk melihat apakah user tersebut bisa login atau tidak
	# Jika password benar return True
	# Jika password salah return False
	# Jika user tidak terdaftar return string kosong
	def login(self,username,password):
		if(self.checkRegistered(username)):
			if(Security.check(self.getPassword(username),password)):
				return True
			return False
		else:
			return ""
	
	# Fungsi untuk register seorang user
	# jika bisa register maka returnnya True
	# jika username tersebut sudah register maka returnnya False
	def register(self,username,password):
		if(self.checkRegistered(username)):
			return False
		data = {}
		data["username"] = username
		data["password"] = Security.hash(password)
		data["balance"] = 0
		self.sqlman.insert("users",data)
		return True
	
	# Fungsi untuk mengubah balance dari user
	def setBalance(self,username,balance):
		if(self.checkRegistered(username)):
			self.sqlman.update("users",{"balance":balance},{"username":username})
			return True
		return False
		
	# Fungsi untuk mengubah password dari user
	def setPassword(self,username,password):
		if(self.checkRegistered(username)):
			self.sqlman.update("users",{"password":password},{"username":username})
			return True
		return False
	
	# Fungsi untuk melihat balance dari user
	def getBalance(self,username):
		data = self.sqlman.select("users","balance",{"username":username}).fetchall()
		for d in data:
			return int(d[0])
	
	# Fungsi untuk menambah balance dari user
	def addBalance(self,username,amount):
		self.setBalance(username,self.getBalance(username) + amount)
		
	# Fungsi untuk melihat password dari user
	def getPassword(self,username):
		data = self.sqlman.select("users","password",{"username":username}).fetchall()
		for d in data:
			return d[0]
	
	# Fungsi untuk melihat data transaksi dari user
	def getLogs(self,username):
		data = self.sqlman.select("trans","*",{"username":username}).fetchall()
		return data
	
	# Fungsi untuk menambahkan transaksi user
	def insertLog(self,username,date,typ,amount,note):
		data = {}
		data["username"] = username
		data["date"] = date
		data["type"] = typ
		data["amount"] = amount
		data["note"] = note
		self.sqlman.insert("trans",data)
		
