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

    def register(self):
        ok, msg= create_user(self.email_entry.get(), self.master_entry.get())
        messagebox.showinfo('Register', msg) if ok else messagebox.showerror('Gabim', msg)

    def login(self):
        user = authenticate_user(self.email_entry.get(), self.master_entry.get())
        if not user:
            messagebox.showerror('Gabim', 'Email ose master password eshte gabim.')
            return
        self.user = user
        self.aes_key = derive_aes_key(self.master_entry.get(), b64d(user['salt']))
        self.show_main_screen()
        
    def show_main_screen(self):
        self.clear()
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill='x')
        ttk.Label(top, text=f'I kyçur si: {self.user['email']}', font=('Arial', 12, 'bold')).pack(side='left')
        ttk.Button(top, text='Export Sync File', command=self.export.sync).pack(side='right', padx=5)
        ttk.Button(top, text='Import Sync File', command=self.import_sync).pack(side='right', padx=5)
        ttk.Button(top, text='Logout', command=self.show_login_screen).pack(side='right', padx=5)

        form = ttk.LabelFrame(self.root, text='Shto / Perditeso fjalkalimin', padding=10)
        form.pack(fill='x', padx=10, pady=5)

        self.selected_id = None
        labels = ['Account:', 'Username:', 'Category:', 'Password:', 'Notes:']
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky='w', pady=3)

        self.account_entry = ttk.Entry(form, width=35)
        self.username_entry = ttk.Entry(form, width=35)
        self.category_combo = ttk.Combobox(form, values=CATEGORIES, state='readonly', width=32)
        self.password_entry = ttk.Entry(form, width=35)
        self.notes_entry = ttk.Entry(form, width=35)
        self.category_combo.set('General')

        self.account_entry.grid(row=0, column=1, pady=3)
        self. username_entry.grid(row=1, column=1, pady=3)
        self.category_combo.grid(row=2, column=1, pady=3)
        self.password_entry.grid(row=3, column=1, pady=3)  
        self.notes_entry.grid(row=4, column=1, pady=3) 
                  
                
