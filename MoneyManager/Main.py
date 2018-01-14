from SQLManager import SQLite
from UserManager import Manager
import Security
import DateManager
import Menus

sqlman = ""
userman = ""

# Fungsi untuk menghapus semua data yang ada di database
def reset():
	sqlman.droptable("users")
	sqlman.droptable("trans")

# Fungsi ini untuk meload file database dan memasukkannya ke Class SQLManager
def loadSql():
	global sqlman
	sqlman = SQLite()
	sqlman.load("data.db")


# Fungsi ini untuk membuat table dari database 
def sqlSetup():
	if(sqlman == ""):
		loadSql()

	# Table untuk menyimpan Data dari User 
	# Username, Password dan Balance dari user tersebut
	tables = {}
	tables["username"] = "text"
	tables["password"] = "text"
	tables["balance"] = "text"
	sqlman.createtable("users",tables,"username")
	
	# Table untuk menyimpan data pengeluaran dan pemasukkan user
	tables = {}
	tables["username"] = "text"
	tables["date"] = "text"
	tables["type"] = "text"
	tables["amount"] = "text"
	tables["note"] = "text"
	sqlman.createtable("trans",tables)

# Fungsi yang dipanggil saat user menjalankan program pertama kali
# Fungsi ini meload class SQLManager dan UserManager
# Agar class tersebut bisa digunakan
# Lalu jika tidak ada user yang terdaftar di database maka user diharuskan mendaftar
# Jika ada user yang terdaftar maka user diberi pilihan untuk register atau login
def start():
	global userman
	sqlSetup()
	userman = Manager()
	userman.load(sqlman)
	Menus.load(userman)
	data = userman.getUsers()
	if(len(data) == 0):
		Menus.first()
	else:
		Menus.main()

start()
