from cryptography.fernet import Fernet

number = {0: "encryptkeyone", 1: "encryptkeytwo", 2: "encryptkeythree"}

for i in range(3):
    print(number[i] + "=" + Fernet.generate_key().decode("ascii"))
