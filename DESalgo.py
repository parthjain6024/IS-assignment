from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import socket
import os

# DES Encryption and Decryption functions
def encrypt_message(message, key):
    """
    Encrypts the message using DES encryption.
    """
    # Ensure the key is 8 bytes (64 bits)
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long.")
    
    cipher = DES.new(key, DES.MODE_CBC)
    padded_message = pad(message.encode(), DES.block_size)  # Pad the message to be a multiple of block_size
    encrypted_message = cipher.encrypt(padded_message)
    return cipher.iv + encrypted_message  # Prepend IV for later decryption

def decrypt_message(encrypted_message, key):
    """
    Decrypts the message using DES decryption.
    """
    iv = encrypted_message[:8]  # Extract the IV from the start
    encrypted_data = encrypted_message[8:]  # The rest is the encrypted message
    
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)
    return decrypted_data.decode()  # Return the decrypted message as a string
