import os
import uuid
import qrcode
import tkinter as tk
from tkinter import ttk, messagebox
import cv2


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


def load_all_keys(base_folder):
    keys = {}
    user_data = {}
    for user_folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, user_folder)
        if os.path.isdir(folder_path):
            user_info_file = os.path.join(folder_path, "user_info.txt")
            if os.path.exists(user_info_file):
                with open(user_info_file, "r") as file:
                    data = {}
                    for line in file:
                        if "Full Name:" in line:
                            data["Full Name"] = line.split(":")[1].strip()
                        elif "Gmail:" in line:
                            data["Gmail"] = line.split(":")[1].strip()
                        elif "Unique Key:" in line:
                            unique_key = line.split(":")[1].strip()
                            keys[unique_key] = user_folder
                            data["Unique Key"] = unique_key
                    user_data[unique_key] = data
    return keys, user_data


def read_qr_code_from_camera():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            cap.release()
            cv2.destroyAllWindows()
            return data

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


def verify_user(base_folder):
    keys, user_data = load_all_keys(base_folder)

    def scan_qr_code():
        qr_code_data = read_qr_code_from_camera()
        if qr_code_data in keys:
            display_user_interface(user_data[qr_code_data])
        else:
            messagebox.showerror("Error", "User not found!")

    def display_user_interface(user_info):
        for widget in camera_frame.winfo_children():
            widget.destroy()

        tk.Label(camera_frame, text="User Details", font=("Helvetica", 32, "bold"), bg="#ffffff", fg="#4caf50").pack(pady=40)
        tk.Label(camera_frame, text=f"Full Name: {user_info['Full Name']}", font=("Helvetica", 22), bg="#ffffff").pack(pady=20)
        tk.Label(camera_frame, text=f"Gmail: {user_info['Gmail']}", font=("Helvetica", 22), bg="#ffffff").pack(pady=20)
        tk.Label(camera_frame, text=f"Unique Key: {user_info['Unique Key']}", font=("Helvetica", 22), bg="#ffffff").pack(pady=20)
        ttk.Button(camera_frame, text="Return to Scanner", command=initialize_scanner, style="Accent.TButton").pack(pady=50)
        ttk.Button(camera_frame, text="Return to Main", command=go_to_main_page).pack(pady=20)

    def initialize_scanner():
        for widget in camera_frame.winfo_children():
            widget.destroy()

        tk.Label(camera_frame, text="Point the camera at the QR code\nand click 'Scan QR Code'",
                 font=("Helvetica", 24), bg="#ffffff", justify="center").pack(pady=100)
        ttk.Button(camera_frame, text="Scan QR Code", command=scan_qr_code, style="Accent.TButton").pack(pady=50)
        ttk.Button(camera_frame, text="Return to Main", command=go_to_main_page, style="Accent.TButton").pack(pady=50)

    def go_to_main_page():
        root.destroy()
        create_main_page()

    root = tk.Tk()
    root.title("QR Code Scanner")
    root.attributes('-fullscreen', True)
    root.configure(bg="#e8f4f8")

    style = ttk.Style(root)
    style.configure("TButton", font=("Helvetica", 18), padding=15)
    style.configure("Accent.TButton", font=("Helvetica", 18), padding=15, background="#4caf50", foreground="#ffffff")
    style.map("Accent.TButton", background=[("active", "#45a049")])

    header_frame = tk.Frame(root, bg="#4caf50", height=80)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="QR Code Scanner", font=("Helvetica", 28, "bold"), bg="#4caf50", fg="#ffffff").pack(pady=15)

    camera_frame = tk.Frame(root, bg="#ffffff", relief="flat", bd=10)
    camera_frame.pack(fill=tk.BOTH, expand=True)

    initialize_scanner()

    root.mainloop()


def create_user_page():
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

    def go_to_main_page():
        root.destroy()
        create_main_page()

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

    close_button = ttk.Button(frame, text="Return to Main", command=go_to_main_page)
    close_button.pack()

    style = ttk.Style(root)
    style.configure("TButton", font=("Helvetica", 14), padding=10)

    root.mainloop()


def create_main_page():
    def go_to_create_user_page():
        root.destroy()
        create_user_page()

    def go_to_verify_user_page():
        root.destroy()
        verify_user(base_folder)

    def exit():
        root.destroy()

    root = tk.Tk()
    root.title("Main Page")
    root.attributes('-fullscreen', True)
    root.configure(bg="#e8f4f8")

    main_frame = tk.Frame(root, bg="#ffffff", relief="raised", bd=10)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    title_label = tk.Label(main_frame, text="Main Menu", font=("Helvetica", 28, "bold"), bg="#ffffff", fg="#007acc")
    title_label.pack(pady=20)

    create_user_button = ttk.Button(main_frame, text="Create User", command=go_to_create_user_page, width=20)
    create_user_button.pack(pady=20)

    verify_user_button = ttk.Button(main_frame, text="Verify User", command=go_to_verify_user_page, width=20)
    verify_user_button.pack(pady=20)

    exit_button = ttk.Button(main_frame, text="Exit", command=exit, width=20)
    exit_button.pack(pady=20)

    root.mainloop()


base_folder = "users"
os.makedirs(base_folder, exist_ok=True)

create_main_page()
