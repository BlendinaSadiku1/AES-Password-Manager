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

    def load_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        self.selected_id = int(selected[0])
        values = self.tree.item(selected[0], 'values')
        self.account_entry.delete(0, tk.END)
        self.account_entry.insert(0, values[0])
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, values[1])
        self.category_combo.set(values[2])
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, values[3])
        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, values[4])

        def delete_selected(self):
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning('Kujdes', 'Zgjedh një rekord për fshirje.')
                return
            if not messagebox.askyesno('Konfirmo', 'A je i sigurt që dëshiron ta fshish?'):
                return
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM passwords WHERE id=%s AND user_id=%s', (int(selected[0]), self.user['id']))
            conn.commit()
            cursor.close()
            conn.close()
            self.clear_form()
            self.load_passwords()

        def export_sync(self):
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT account, username, category, encrypted_password, nonce, notes, updated_at FROM passwords WHERE user_id=%s', (self.user['id'],))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            data = {
                'email': self.user['email'],
                'exported_at': datetime.now().isoformat(timespec='seconds'),
                'passwords': rows
            }
            json_data = json.dumps(data, ensure_ascii=False, default=str)
            nonce, encrypted_backup = encrypt_text(json_data, self.aes_key)
            sync_file = {'version': 1, 'nonce': nonce, 'encrypted_data': encrypted_backup}

            path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON file', '*.json')])
            if not path:
                return
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(sync_file, f, indent=2)
            messagebox.showinfo('Export', 'Sync file u krijua me sukses.')
                    
                    
        def import_sync(self):
                path = filedialog.askopenfilename(filetypes=[('JSON file', '*.json')])
                if not path:
                    return
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        sync_file = json.load(f)
                    json_data = decrypt_text(sync_file['nonce'], sync_file['encrypted_data'], self.aes_key)
                    data = json.loads(json_data)
                except Exception:
                    messagebox.showerror('Gabim', 'Ky file nuk mund të dekriptohet me këtë master password.')
                    return

                imported = 0
                conn = get_connection()
                cursor = conn.cursor()
                for item in data.get('passwords', []):
                    cursor.execute('''
                        INSERT INTO passwords(user_id, account, username, category, encrypted_password, nonce, notes, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (self.user['id'], item['account'], item.get('username', ''), item.get('category', 'General'), item['encrypted_password'], item['nonce'], item.get('notes', ''), item.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))
                    imported += 1
                conn.commit()
                cursor.close()
                conn.close()
                self.load_passwords()
                messagebox.showinfo('Import', f'U importuan {imported} rekorde.')

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()