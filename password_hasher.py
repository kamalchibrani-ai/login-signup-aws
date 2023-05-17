import argon2

ph = argon2.PasswordHasher()
hash = ph.hash(b"correct horse battery staple")
try:
    ph.verify(hash,"correct horse battery staple")
    print("correct horse battery")
except:
    print("Passwords dont match")

print(hash)


def generate_hashed_pass(password):
    hashed_password = ph.hash(password)
    return hashed_password

def verify_hashed_pass(hashed_password,entered_password):
    try:
        ph.verify(hashed_password,entered_password)
        print("correct")
        return True
    except:
        print("Passwords dont match")





