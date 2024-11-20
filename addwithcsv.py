import os
import uuid
import qrcode
import csv
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
        return f"User created successfully! Folder: {user_folder} Unique Key: {unique_key}"
    except Exception as e:
        return f"Error: {e}"

def process_csv_and_create_users(csv_file, base_folder):
    try:
        with open(csv_file, mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=["Adresse e-mail", "Name", "Family Name", "Situation"])
            next(reader)  # Skip the header row
            for row in reader:
                gmail = row["Adresse e-mail"].strip()
                full_name = f"{row['Name'].strip()} {row['Family Name'].strip()}"
                if row["Situation"].strip().lower() == "accepted":
                    result = create_user_folder(base_folder, gmail, full_name)
                    print(result)
    except Exception as e:
        print(f"Error processing CSV: {e}")

def gui_create_user_folder():
    def on_submit():
        csv_file = csv_file_entry.get().strip()
        if not csv_file or not os.path.exists(csv_file):
            messagebox.showerror("Error", "Please provide a valid CSV file path!")
            return
        process_csv_and_create_users(csv_file, base_folder)
        messagebox.showinfo("Result", "All accepted users have been added!")
        csv_file_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Batch User Folder Creator")
    root.attributes('-fullscreen', True)
    root.configure(bg="#e8f4f8")

    frame = tk.Frame(root, bg="#ffffff", relief="raised", bd=10)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    title_label = tk.Label(frame, text="Batch User Folder Creator", font=("Helvetica", 28, "bold"), bg="#ffffff", fg="#007acc")
    title_label.pack(pady=20)

    csv_file_label = tk.Label(frame, text="CSV File Path", font=("Helvetica", 16), bg="#ffffff", fg="#333333")
    csv_file_label.pack(pady=10)
    csv_file_entry = ttk.Entry(frame, font=("Helvetica", 14), width=40)
    csv_file_entry.pack(pady=5)

    submit_button = ttk.Button(frame, text="Process CSV", command=on_submit)
    submit_button.pack(pady=30)

    close_button = ttk.Button(frame, text="Exit", command=root.destroy)
    close_button.pack()

    style = ttk.Style(root)
    style.configure("TButton", font=("Helvetica", 14), padding=10)

    root.mainloop()

base_folder = "users"
os.makedirs(base_folder, exist_ok=True)
csv_file_path = "people.csv"
gui_create_user_folder()
