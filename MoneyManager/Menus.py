import os
import DateManager

userman = ""
usersession = ""

# Untuk load class UserManager
def load(user):
	global userman
	userman = user

# Untuk menghapus tulisan di console
def clear():
	os.system('cls')

# Untuk menulis header dari console
def header(pesan):
	clear()
	print(15 * "-*-")
	print("")
	print(pesan)
	print("")
	print(15 * "-*-")
	print("")

# Untuk menyapa user saat menjalankan program
# berisi info tentang program ini
def greet():
	header("Selamat Datang di program MoneyManager")
	print("Apa itu Money Manager ??")
	print("Program ini berguna untuk melihat Pengeluaran/Pendapatan Harian Anda")
	print("Anda dapat melihat apakah anda mengalami kerugian/keuntungan setiap harinya")
	print("Jadi anda dapat memantau keuangan anda")
	print("")

# Pesan untuk user yang tidak memiliki akun
# Dia juga akan diarahkan ke halaman register
def first():
	greet()
	print("Kamu Harus Membuat Akun !")
	print("")
	input("Tekan Enter untuk lanjut...")
	userRegister("Masukkan username dan password yang kamu inginkan")

def tentang():
	clear()
	print("Author:")
	print("- Dimas Sigit Prasetyo")
	print("- Enrico Fajar Ferdiansyah")
	print("- Jody")
	print("- Jonathan Graciano Situmorang")
	print("- Rino Ramadhan")
	print("- Septian Isnu Kristianto")
	print("")
	input("Tekan Enter untuk Kembali...")
	main()

def keluar():
	print("")
	print("Terimakasih sudah menggunakan program kami :)")

# Pesan untuk user yang sudah memiliki akun
# Dia diberi pilihan untuk login atau membuat akun
def main():
	greet()
	print("Apa yang ingin kamu lakukan ?")
	print("")
	choices = {}
	choices["Login"] = userLogin
	choices["Buat Akun"] = userRegister
	choices["Tentang"] = tentang
	choices["Keluar"] = keluar
	choice(choices)
	
# Halaman login
# User diminta untuk memasukkan username dan password
# Jika berhasil login maka akan diteruskan ke Halaman User
# Jika gagal login maka user disuruh memasukkan password kembali
def userLogin(message=""):
	header("Menu Login\n\nTulis 'Quit' untuk kembali ke Menu Utama")
	if(len(message) > 0):
		print(message)
		print("")
	username = input("Username> ")
	if(username.lower()=="quit"):
		main()
	password = input("Password> ")
	if(password.lower()=="quit"):
		main()
	state = userman.login(username,password)
	if(state == ""):
		userLogin("User {} tidak terdaftar !".format(username))
	elif(state):
		print("")
		print("Berhasil Login Sebagai {}".format(username))
		print("")
		input("Tekan Enter untuk lanjut...")
		global usersession
		usersession = username
		userPage()
	else:
		userLogin("Anda memasukkan password yang salah")


# Halaman Daftar akun
# User diminta untuk memasukkan username dan password
# Jika berhasil mendaftar maka akan diteruskan ke Halaman User
# Jika gagal mendaftar atau user sudah ada maka user disuruh memasukkan username kembali
def userRegister(message=""):
	header("Daftar Akun\n\nTulis 'Quit' untuk kembali ke Menu Utama")
	if(len(message) > 0):
		print(message)
		print("")
	
	username = input("Username> ")
	if(username.lower()=="quit"):
		main()
	password = input("Password> ")
	if(password.lower()=="quit"):
		main()
	
	state = userman.register(username,password)
	if(state):
		print("")
		print("Berhasil Mendaftarkan user {}".format(username))
		print("")
		input("Tekan Enter untuk lanjut...")
		global usersession
		usersession = username
		userPage()
		
	else:
		userRegister("User {} sudah terdaftar !".format(username))

# Fungsi untuk menampilkan menu pilihan berdasarkan Array
def choice(choices):
	index = 0
	for c in choices.keys():
		index += 1
		print("{}> {}".format(index,c))
	print("")
	num = input("> ")
	if num.lower() == "quit":
		main()
	try:
		num = int(num)
	except ValueError:
		print("Tolong Masukkan Angka...")
		choice(choices)
		return
	list(choices.values())[num - 1]()

# Fungsi untuk memformat integer menjadi String mata uang rupiah
def formatRupiah(number):
	if number == 0:
		number = "Rp.{:,}".format(number)
	elif number > 0:
		number = "+Rp.{:,}".format(number)
	else:
		number = "-Rp.{:,}".format(number*-1)
	number = number.replace(",",".")
	return number

# Fungsi untuk menampilkan ringkasan keuangan user
def overview():
	header("Pengeluaran Bulanan")
	days = DateManager.getDays()
	data = userman.getLogs(usersession)
	cache = {}
	for d in data:
		date = DateManager.toDateOnly(d[1].split(" ")[0])
		d = list(d)
		d.append(d[1].split(" ")[1])
		if date in cache.keys():
			cache[date].append(d)
		else:
			cache[date] = []
			cache[date].append(d)
	summary = 0
	for k in cache.keys():
		print(75*"-")
		print("     Tanggal: {}".format(str(k).split(" ")[0]))
		print("")
		msummary = 0
		for d in cache[k]:
			hour = d[5]
			t = d[2]
			amount = int(d[3])
			note = d[4]
			if t == "Pengeluaran":
				amount = amount * -1
			msummary += amount
			amount = formatRupiah(amount)
			print("     [{}] {}: {} ({})".format(hour,t,amount,note))
		summary += msummary
		msummary = formatRupiah(msummary)
		print("")
		print("     Ringkasan Harian: {}".format(msummary))
		print(75*"-")
	summary = formatRupiah(summary)
	print("")
	print(40 * "*")
	print("")
	print(" Ringkasan Bulan Ini: {}".format(summary))
	print("")
	print(40 * "*")
	input("Press Enter to go back")
	userPage()

# Halaman dari user
# User akan diberi pilihan untuk 
# melihat ringkasan 
# menambah pendapatan/pengeluaran 
# mengubah uang mereka
def userPage(message=""):
	username = usersession
	header("Welcome {}".format(username))
	if(len(message) > 0):
		print(message)
	printBalance(username)
	print("")
	choices = {}
	choices["Ringkasan"] = overview
	choices["Tambah Pendapatan"] = userAddIncome
	choices["Tambah Pengeluaran"] = userAddOutcome
	choices["Ubah Uang"] = userSetBalance
	choices["Keluar"] = main
	choice(choices)

# Halaman menambah Pendapatan
# User diminta untuk memasukkan jumlah pendapatan
# Serta catatan keterangan akan pendapatan tersebut
# Pendapatan akan menambah uang dari user
def userAddIncome(message=""):
	header("Kamu sedang menambahkan Pendapatan")
	if(len(message) > 0):
		print(message)
	print("Tulis 'Quit' untuk batal")
	amount = input("Masukkan Jumlah> ")
	if amount.lower() == "quit":
		userPage()
	try:
		amount = int(amount)
	except ValueError:
		userAddOutcome("Tolong tulis angka sebagai jumlahnya !")
		return
	note = input("Tambahkan Catatan> ")
	if note.lower() == "quit":
		userPage()
	userman.insertLog(usersession,DateManager.getNow(),"Pendapatan",amount,note)
	userman.addBalance(usersession,amount)
	userPage("Berhasil Menambahkan Pendapatan {} hari ini".format(formatRupiah(amount)))


# Halaman menambah Pengeluaran
# User diminta untuk memasukkan jumlah pengeluaran
# Serta catatan keterangan akan pengeluaran tersebut
# Pengeluaran akan mengurangi uang dari user
def userAddOutcome(message=""):
	header("Kamu sedang menambahkan Pengeluaran")
	if(len(message) > 0):
		print(message)
	print("Tulis 'Quit' untuk batal")
	amount = input("Masukkan Jumlah> ")
	if amount.lower() == "quit":
		userPage()
	try:
		amount = int(amount)
	except ValueError:
		userAddOutcome("Tolong tulis angka sebagai jumlahnya !")
		return
	note = input("Tambahkan Catatan> ")
	if note.lower() == "quit":
		userPage()
	userman.insertLog(usersession,DateManager.getNow(),"Pengeluaran",amount,note)
	amount = amount * -1
	userman.addBalance(usersession,amount)
	userPage("Berhasil Menambahkan Pengeluaran {} hari ini".format(formatRupiah(amount)))


# Halaman mengubah Uang user
# User diminta untuk memasukkan jumlah uang sesuai dengan uang user
def userSetBalance(message=""):
	username = usersession
	header("Mengubah Uang")
	if(len(message) > 0):
		print(message)
	printBalance(username)
	print("")
	balance = input("Masukkan Jumlah> ")
	try:
		balance = int(balance)
	except ValueError:
		userAddOutcome("Tolong tulis angka sebagai jumlahnya !")
		return
	userman.setBalance(username,balance)
	userPage("Berhasil mengubah uang anda menjadi {}".format(formatRupiah(balance).replace("+","")))
	
# Fungsi untuk menampilkan uang dari user
def printBalance(username):
	print("Uang Anda: {}".format(formatRupiah(userman.getBalance(username)).replace("+","")))
