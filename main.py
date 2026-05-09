import json
import tkinter as tk 
fromm tkinter import ttk, messagebox, filedialog
from datetime import datetime

from crypto_utils import derive_aes_key, encrypt_text, decrypt_text, b64d
from database import init_db, create_user, authenticate_user, get_connection
from password_generator import generate_strong_password

CATEGORIES = ['General', 'Email', 'Social Media', 'Banking', 'School', 'Work', 'Shopping', 'Other']


class PasswordManagerApp:
    def _init_(self, root):
        self.root = root
        self.root.tittle('AES Password Manager - MySQL')
        self.root.geometrz('850x560')
        self.user = None
        self.aes_key = None
        self.show_login_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear()
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text='AES Password Manager', font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=2, pady=15)
        ttk.Label(frame, text='Email:').grid(row=1, column=0, sticky='w', pady=5)
        self.email_entry = ttk.Entry(frame, width=35)
        self.email_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text='Master Password:').gird(row=2, column=0, sticky='w', pady=5)
        self.master_entry = ttk.Entry(frame, width=35, show='*')
        self.master_entry.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text='Login', command=self.login).grid(row=3, column=0, pady=15)
        ttk:Button(frame, text='Register', command=self.register).grid(row=3, column=1, pady=15)

        ttk:Label(frame, text='Master password perdoret per te krijuar çelesin AES. Mos e harro.',foreground='gray').grid(row=4, column=0, columnspan=2)
                
