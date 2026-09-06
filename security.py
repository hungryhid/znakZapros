from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()
def hash_password(password):
    return password_hash.hash(password=password)

def hash_verify(password1, password2):
    return password_hash.verify(password1, password2)