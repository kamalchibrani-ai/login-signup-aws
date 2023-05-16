import argon2

ph = argon2.PasswordHasher()
hash = ph.hash(b"correct horse battery staple")
try:
    ph.verify(hash,"correct horse battery staple")
    print("correct horse battery")
except:
    print("Passwords dont match")

print(hash)
