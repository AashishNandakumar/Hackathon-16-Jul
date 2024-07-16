import tkinter as tk
from tkinter import ttk, scrolledtext
import base64
from ttkthemes import ThemedTk


class ZypherKeyApp:
    def __init__(self, master):
        self.master = master
        master.title("Zypher Key Encryption Tool")
        master.geometry("800x600")

        style = ttk.Style()
        style.theme_use("equilux")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10 10 10 10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_text = scrolledtext.ScrolledText(
            input_frame, height=8, width=70, font=("Segoe UI", 10)
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Key frame
        key_frame = ttk.Frame(main_frame)
        key_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(key_frame, text="Encryption Key:").pack(side=tk.LEFT, padx=(0, 10))
        self.key_entry = ttk.Entry(key_frame, width=30, font=("Segoe UI", 10))
        self.key_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Cipher selection
        ttk.Label(key_frame, text="Cipher:").pack(side=tk.LEFT, padx=(0, 10))
        self.cipher_var = tk.StringVar(value="Caesar")
        cipher_combo = ttk.Combobox(
            key_frame,
            textvariable=self.cipher_var,
            values=["Caesar", "Vigenère", "Base64"],
            state="readonly",
            width=15,
        )
        cipher_combo.pack(side=tk.LEFT)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        encrypt_button = ttk.Button(
            button_frame, text="Encrypt", command=self.encrypt, style="Accent.TButton"
        )
        encrypt_button.pack(side=tk.LEFT, padx=(0, 10))

        decrypt_button = ttk.Button(button_frame, text="Decrypt", command=self.decrypt)
        decrypt_button.pack(side=tk.LEFT)

        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10 10 10 10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=8, width=70, font=("Segoe UI", 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def encrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get()
        cipher = self.cipher_var.get()

        if cipher == "Caesar":
            result = self.caesar_cipher(text, int(key), encrypt=True)
        elif cipher == "Vigenère":
            result = self.vigenere_cipher(text, key, encrypt=True)
        elif cipher == "Base64":
            result = base64.b64encode(text.encode()).decode()

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    def decrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get()
        cipher = self.cipher_var.get()

        if cipher == "Caesar":
            result = self.caesar_cipher(text, int(key), encrypt=False)
        elif cipher == "Vigenère":
            result = self.vigenere_cipher(text, key, encrypt=False)
        elif cipher == "Base64":
            result = base64.b64decode(text.encode()).decode()

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    def caesar_cipher(self, text, shift, encrypt=True):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord("A") if char.isupper() else ord("a")
                shifted = (
                    ord(char) - ascii_offset + shift * (1 if encrypt else -1)
                ) % 26
                result += chr(shifted + ascii_offset)
            else:
                result += char
        return result

    def vigenere_cipher(self, text, key, encrypt=True):
        result = ""
        key_length = len(key)
        key_as_int = [ord(i) for i in key]

        for i, char in enumerate(text):
            if char.isalpha():
                ascii_offset = ord("A") if char.isupper() else ord("a")
                key_shift = key_as_int[i % key_length] - ord("A")
                shifted = (
                    ord(char) - ascii_offset + key_shift * (1 if encrypt else -1)
                ) % 26
                result += chr(shifted + ascii_offset)
            else:
                result += char
        return result


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = ZypherKeyApp(root)
    root.mainloop()
