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







        ttk.Button(form, text='Generate Strong Password', command=self.generate_password).grid(row=3, column=2, padx=8)
        ttk.Button(form, text='Save', command=self.save_password).grid(row=5, column=1, sticky='w', pady=8)
        ttk.Button(form, text='Clear', command=self.clear_form).grid(row=5, column=1, sticky='e', pady=8)

        table_frame = ttk.Frame(self.root, padding=10)
        table_frame.pack(fill='both', expand=True)

        columns = ('account', 'username', 'category', 'password', 'notes', 'updated_at')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(fill='both', expand=True, side='left')
        self.tree.bind('<<TreeviewSelect>>', self.load_selected)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        bottom = ttk.Frame(self.root, padding=10)
        bottom.pack(fill='x')
        ttk.Button(bottom, text='Delete Selected', command=self.delete_selected).pack(side='left')
        ttk.Button(bottom, text='Refresh', command=self.load_passwords).pack(side='left', padx=5)

        self.load_passwords()

    def load_passwords(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM passwords WHERE user_id=%s ORDER BY category, account', (self.user['id'],))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            try:
                plain_password = decrypt_text(row['nonce'], row['encrypted_password'], self.aes_key)
            except Exception:
                plain_password = '[Nuk mund të dekriptohet]'
            self.tree.insert('', 'end', iid=row['id'], values=(row['account'], row['username'], row['category'], plain_password, row['notes'], row['updated_at']))
    
        
                  
                
