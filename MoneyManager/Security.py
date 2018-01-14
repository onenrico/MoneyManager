import uuid
import hashlib
 
# Fungsi untuk mengubah string menjadi hashedstring
# hashed string merupakan string aneh yang didapat dari perhitungan matematika yang rumit
# fungsi dari hashedstring agar tidak bisa dibaca 
# dan biasanya berfungsi untuk menyamarkan password dalam database
def hash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

# Fungsi untuk membandingkan string dengan hashedstring
# jika cocok maka returnnya True jika tidak maka returnnnya False
def check(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
