import socket
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

# Function to encrypt the message
def encrypt_message(message, key):
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long.")

    # Generate a random 8-byte IV for CBC mode
    iv = os.urandom(8)

    # Create cipher object with key and IV
    cipher = DES.new(key, DES.MODE_CBC, iv)

    # Pad the message to be a multiple of block_size (8 bytes)
    padded_message = pad(message.encode(), DES.block_size)

    # Encrypt the message
    encrypted_message = cipher.encrypt(padded_message)

    # Return the IV prepended to the encrypted message
    return iv + encrypted_message

# Function to decrypt the message
def decrypt_message(encrypted_message, key):
    # Decrypt the message and remove padding
    cipher = DES.new(key, DES.MODE_CBC, encrypted_message[:8])
    decrypted_data = unpad(cipher.decrypt(encrypted_message[8:]), DES.block_size)
    return decrypted_data.decode()

# Client function to send an encrypted message to the server
def send_message_to_server(host, port, key, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Encrypt the message
    encrypted_message = encrypt_message(message, key)

    # Send the encrypted message to the server
    client.send(encrypted_message)

    # Receive the response from the server (it will be encrypted too)
    encrypted_response = client.recv(1024)  # May need to be adjusted based on message size

    # Decrypt the response
    decrypted_response = decrypt_message(encrypted_response, key)
    print("Decrypted response from server:", decrypted_response)

    client.close()

# Client execution
if __name__ == "__main__":
    # DES Key (must be 8 bytes long)
    key = b"8bytekey"

    # Message to send to the server
    message = "Hello, server. This is a secure message."

    # Send the message to the server
    send_message_to_server('127.0.0.1', 65432, key, message)
