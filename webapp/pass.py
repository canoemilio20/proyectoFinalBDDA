from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

password = '666'

hash = generate_password_hash(password)

print(hash)

if check_password_hash(hash, password):
    print("A huevo")