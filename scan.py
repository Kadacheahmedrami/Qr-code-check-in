import os
import cv2
import tkinter as tk
from tkinter import ttk, messagebox


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

    def initialize_scanner():
        for widget in camera_frame.winfo_children():
            widget.destroy()

        tk.Label(camera_frame, text="Point the camera at the QR code\nand click 'Scan QR Code'",
                 font=("Helvetica", 24), bg="#ffffff", justify="center").pack(pady=100)
        ttk.Button(camera_frame, text="Scan QR Code", command=scan_qr_code, style="Accent.TButton").pack(pady=50)

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
    camera_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    initialize_scanner()

    root.mainloop()


base_folder = "users"
verify_user(base_folder)
