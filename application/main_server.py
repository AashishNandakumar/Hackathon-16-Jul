import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        # instantiate the socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a particular IP address and port
        self.server_socket.bind((self.host, self.port))
        # make the socket to listen on that IP address and port
        self.server_socket.listen()

        self.clients = {}
        self.public_keys = {}

        # generate server's key pair
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

        # initalize the GUI of the server
        self.gui_init()

    def gui_init(self):
        self.window = tk.Tk()
        self.window.title("Zypher Chronicles Server")

        # create a log area for holding the messages
        self.log_area = scrolledtext.ScrolledText(
            self.window, wrap=tk.WORD, width=70, height=20
        )
        # set the appropriate padding
        self.log_area.pack(padx=10, pady=10)

        # create the appropriate action to take when clicked on the close button
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start(self):
        self.log_message(
            "Server has started successfully. Waiting for Clients to connect"
        )
        # spawn a thread for each Client connection
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()
        self.window.mainloop()

    def accept_connections(self):
        while True:
            # accept any incoming requests to the server
            client_socket, address = self.server_socket.accept()
            self.log_message(f"new connection from {address}")

            # exchange public key for encryption
            client_public_key = RSA.import_key(client_socket.recv(1024))
            client_socket.send(self.public_key.export_key())

            # store the socket address of the clients
            self.clients[address] = client_socket
            # store the public keys of the clients
            self.public_keys[address] = client_public_key

            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket, address)
            )
            client_thread.start()

    def handle_client(self, client_socket, address):
        while True:
            try:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break

                # decrypt the message
                cipher = PKCS1_OAEP.new(self.private_key)
                decrypted_message = cipher.decrypt(encrypted_message)

                self.log_message(
                    f"message from {address}: {decrypted_message.decode()}"
                )

                # broadcast the message to other clients
                self.broadcast(address, decrypted_message)
            except:
                break

        # if the control has come out of the loop it means the client has disconnected from the server
        self.clients.pop(address)
        self.public_keys.pop(address)

        client_socket.close()
        self.log_message(f"Connection from {address} closed")

    def broadcast(self, sender_address, message):
        for address, client_socket in self.clients.items():
            if address != sender_address:
                # Encrypt the message with the recipient's public key
                cipher = PKCS1_OAEP.new(self.public_keys[address])
                encrypted_message = cipher.encrypt(message)
                client_socket.send(encrypted_message)

    def log_message(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def on_closing(self):
        for client_socket in self.clients.values():
            client_socket.close()

        self.server_socket.close()
        self.window.destroy()


if __name__ == "__main__":
    server = Server("192.168.11.112", 5000)
    server.start()
