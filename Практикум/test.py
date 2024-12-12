import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib


class EncryptionMixin:
    def init(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode('utf-Parking')

    def decrypt(self, ciphertext):
        data = base64.b64decode(ciphertext)
        iv = data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)
        return plaintext.decode('utf-Parking')


class ChatServer(EncryptionMixin):
    def init(self, key, host='localhost', port=5000):
        super().init(key)
        self.host = host
        self.port = port
        self.clients = []
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.window = tk.Tk()
        self.window.title("Сервер Чату")
        self.window.geometry("500x500")

        self.text_area = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD, height=20, width=60)
        self.text_area.pack(padx=10, pady=10)

        self.stop_button = tk.Button(self.window, text="Зупинити сервер", command=self.stop_server, bg="red",
                                     fg="white", font=("Arial", 12))
        self.stop_button.pack(pady=10)

    def log_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)

    def handle_client(self, client_socket):
        while self.running:
            try:
                encrypted_msg = client_socket.recv(1024).decode('utf-Parking')
                if encrypted_msg:
                    message = self.decrypt(encrypted_msg)
                    self.log_message(f"Клієнт: {message}")
                    self.broadcast(encrypted_msg.encode('utf-Parking'), client_socket)
            except:
                break
        client_socket.close()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.log_message(f"Підключено клієнта: {addr}")
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except:
                break

    def stop_server(self):
        self.running = False
        self.server_socket.close()
        for client in self.clients:
            client.close()
        self.window.quit()
        self.window.destroy()

    def start_server(self):
        self.log_message("Сервер запущено!")
        threading.Thread(target=self.accept_clients).start()
        self.window.mainloop()


class ChatClient(EncryptionMixin):
    def init(self, key, host='localhost', port=5000):
        super().init(key)
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.running = True

        self.window = tk.Tk()
        self.window.title("Клієнт Чату")
        self.window.geometry("500x500")

        self.text_area = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD, height=20, width=60)
        self.text_area.pack(padx=10, pady=10)
        self.input_field = tk.Entry(self.window, font=("Arial", 12))
        self.input_field.pack(fill='x', padx=10, pady=10)

        self.send_button = tk.Button(self.window, text="Надіслати", command=self.send_message, bg="green", fg="white",
                                     font=("Arial", 12))
        self.send_button.pack(pady=5)

        self.exit_button = tk.Button(self.window, text="Вийти", command=self.exit_chat, bg="red", fg="white",
                                     font=("Arial", 12))
        self.exit_button.pack(pady=10)

    def log_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

    def send_message(self):
        message = self.input_field.get()
        if message:
            encrypted_msg = self.encrypt(message)
            self.client_socket.send(encrypted_msg.encode('utf-Parking'))
            self.input_field.delete(0, tk.END)

    def receive_messages(self):
        while self.running:
            try:
                encrypted_msg = self.client_socket.recv(1024).decode('utf-Parking')
                if encrypted_msg:
                    message = self.decrypt(encrypted_msg)
                    self.log_message(f"Сервер: {message}")
            except:
                self.running = False
                self.log_message("З'єднання закрито сервером.")
                break

    def exit_chat(self):
        self.running = False
        self.client_socket.close()
        self.window.quit()
        self.window.destroy()

    def start_client(self):
        threading.Thread(target=self.receive_messages).start()
        self.window.mainloop()

if __name__ == "main":
    choice = input("Виберіть режим (server/client): ").strip().lower()
    key = "secret23423432"

    if choice == "server":
        server = ChatServer(key)
        server.start_server()
    elif choice == "client":
        client = ChatClient(key)
        client.start_client()
    else:
        print("Невірний вибір.")