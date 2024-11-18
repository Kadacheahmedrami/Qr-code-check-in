import os
import uuid
import qrcode
import tkinter as tk
from tkinter import ttk, messagebox

def create_user_folder(base_folder, gmail, full_name):
    try:
        unique_key = str(uuid.uuid4())
        user_folder = os.path.join(base_folder, gmail)
        os.makedirs(user_folder, exist_ok=True)
        user_info_file = os.path.join(user_folder, "user_info.txt")
        with open(user_info_file, "w") as file:
            file.write(f"Full Name: {full_name}\n")
            file.write(f"Gmail: {gmail}\n")
            file.write(f"Unique Key: {unique_key}\n")
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(unique_key)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_code_file = os.path.join(user_folder, "qr_code.png")
        qr_img.save(qr_code_file)
        return f"User created successfully!\nFolder: {user_folder}\nUnique Key: {unique_key}"
    except Exception as e:
        return f"Error: {e}"

def gui_create_user_folder():
    def on_submit():
        full_name = name_entry.get().strip()
        gmail = gmail_entry.get().strip()
        if not full_name or not gmail:
            messagebox.showerror("Error", "Both fields are required!")
            return
        result = create_user_folder(base_folder, gmail, full_name)
        messagebox.showinfo("Result", result)
        name_entry.delete(0, tk.END)
        gmail_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("User Folder Creator")
    root.attributes('-fullscreen', True)
    root.configure(bg="#e8f4f8")

    frame = tk.Frame(root, bg="#ffffff", relief="raised", bd=10)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    title_label = tk.Label(frame, text="Create User Folder", font=("Helvetica", 28, "bold"), bg="#ffffff", fg="#007acc")
    title_label.pack(pady=20)

    name_label = tk.Label(frame, text="Full Name", font=("Helvetica", 16), bg="#ffffff", fg="#333333")
    name_label.pack(pady=10)
    name_entry = ttk.Entry(frame, font=("Helvetica", 14), width=40)
    name_entry.pack(pady=5)

    gmail_label = tk.Label(frame, text="Gmail", font=("Helvetica", 16), bg="#ffffff", fg="#333333")
    gmail_label.pack(pady=10)
    gmail_entry = ttk.Entry(frame, font=("Helvetica", 14), width=40)
    gmail_entry.pack(pady=5)

    submit_button = ttk.Button(frame, text="Create User", command=on_submit)
    submit_button.pack(pady=30)

    close_button = ttk.Button(frame, text="Exit", command=root.destroy)
    close_button.pack()

    style = ttk.Style(root)
    style.configure("TButton", font=("Helvetica", 14), padding=10)

    root.mainloop()

base_folder = "users"
os.makedirs(base_folder, exist_ok=True)
gui_create_user_folder()
