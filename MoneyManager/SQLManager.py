import sqlite3

def quote(d) :
	return "`" + d + "`"

# Fungsi untuk Membuat Query kondisi SQL otomatis
# Parameter nya adalah dictionary
def sqlcondition(condition):
	sql = " WHERE"
	for key in condition.keys():
		qkey = quote(key)
		sql += " {}="
		if(isinstance(condition[key], str)):
			sql += "'{}'"
		else:
			sql += "{}"
		sql = sql.format(qkey,condition[key])
	sql += ";"
	return sql


class SQLite(object):
	# Fungsi untuk meload file database
	def load(self,filename):
		self.db = sqlite3.connect(filename)
		
	# Fungsi untuk menjalankan query SQL
	# jika commitnya false maka akan return dari hasil querynya
	def execute(self,command,commit=True):
		cursor = self.db.cursor()
		if(commit):
			cursor.execute(command)
			self.db.commit()
		else:
			return cursor.execute(command)
	
	# Fungsi untuk menjalankan query SQL
	# namun dalam fungsi ini querynya bersifat preparedstatement
	# yaitu querynya berubah sesuai data yang dimasukkan
	def executemany(self,command,data):
		cursor = self.db.cursor()
		data = list(data)
		cursor.execute(command,(data))
		self.db.commit()

	# Fungsi untuk membuat tabel dari SQL
	def createtable(self,tablename,tablevalue,pkey="null"):
		result = "CREATE TABLE IF NOT EXISTS " + tablename + " ("
		index = 0
		for key in tablevalue.keys():
			index += 1
			nn = " NOT NULL"
			ty = tablevalue[key]
			if "null" in ty:
				ty = ty.replace(" null","")
				nn = ""
			if(index >= len(tablevalue.keys())):
				result += "`" + key + "` " + ty + nn
			else:
				result += "`" + key + "` " + ty + nn+","
		if pkey != "null":
			result += ",PRIMARY KEY (`" + pkey + "`));"
		else:
			result += ");"
		self.execute(result)
	
	# Fungsi untuk menghapus data dalam tabel
	def droptable(self,tablename):
		self.execute("DROP TABLE IF EXISTS "+tablename)
	
	# Fungsi untuk memasukkan data kedalam tabel
	def insert(self,table,columns):
		column = "("
		values = "("
		index = 0;
		for c in columns.keys():
			column += quote(c)
			values += "?"
			if (index + 1 != len(columns.keys())):
				column += ","
				values += ","
			index += 1
		column += ")"
		values += ")"
		query = "REPLACE INTO " + table + " " + column + " " + "VALUES" + values + ";"
		self.executemany(query, columns.values())
		return query
	
	# Fungsi untuk mengambil data dari dalam tabel
	def select(self,table,column="*",condition=""):
		sql = "SELECT {} from {}".format(column,table)
		if(condition != ""):
			sql += sqlcondition(condition)
		return self.execute(sql,False)
	
	# Fungsi untuk mengubah data dari dalam tabel
	def update(self,table,values,condition=""):
		sql = "UPDATE {} SET".format(table)
		index = 1
		for key in values.keys():
			qkey = quote(key)
			sql += " {}="
			if(isinstance(values[key], str)):
				sql += "'{}'"
			else:
				sql += "{}"
			sql = sql.format(qkey,values[key])
			if(index != len(values.keys())):
				sql += ","
			index += 1
		if(condition != ""):
			sql += sqlcondition(condition)
		self.execute(sql)
