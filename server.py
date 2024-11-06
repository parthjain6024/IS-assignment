import socket
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

# Function to handle incoming encrypted messages
def handle_client_connection(client_socket, key):
    try:
        # Receive the encrypted message from the client
        encrypted_message = client_socket.recv(1024)
        if encrypted_message:
            # Decrypt the message using DES
            decrypted_message = decrypt_message(encrypted_message, key)
            print("Decrypted message from client:", decrypted_message)
            
            # Respond to the client (optional)
            response = "Message received securely!"
            encrypted_response = encrypt_message(response, key)
            client_socket.send(encrypted_response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Server setup
def start_server(host, port, key):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}...")
    
    while True:
        # Accept a new client connection
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        
        # Handle the client connection
        handle_client_connection(client_socket, key)

# Server execution
if __name__ == "__main__":
    # DES Key (must be 8 bytes long)
    key = b"8bytekey"
    
    # Start the server
    start_server('127.0.0.1', 65432, key)
