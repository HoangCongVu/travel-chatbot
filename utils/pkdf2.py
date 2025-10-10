import hashlib
import os
import binascii  # For hex encoding

def hash_password_pbkdf2(password, salt=None, iterations=100000):
    if salt is None:
        salt = os.urandom(16)  # Generate a random 16-byte salt if not provided
    # Derive the key using PBKDF2 with HMAC-SHA256
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
    # Return hex-encoded hash and salt (store both in DB)
    return binascii.hexlify(dk).decode('utf-8'), binascii.hexlify(salt).decode('utf-8')

# Example usage
# password = "mysecretpassword"
# hashed, salt = hash_password_pbkdf2(password)
# print(f"Salt: {salt}")
# print(f"Hashed: {hashed}")

# To verify later:
def verify_password(stored_hash, stored_salt, provided_password, iterations=100000):
    new_hash, _ = hash_password_pbkdf2(provided_password, binascii.unhexlify(stored_salt), iterations)
    return new_hash == stored_hash

# Test verification
# is_valid = verify_password(hashed, salt, "mysecretpassword")
# print(f"Valid: {is_valid}")  # True