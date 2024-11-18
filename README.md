<h1>QR Code User Management</h1>

<h2>How to Run</h2>
<p>To run the application, you can use one of the following methods:</p>
<ul>
    <li>Run the script using the shell script: <code>./run.sh</code></li>
    <li>Alternatively, run the Python script directly: <code>python start.py</code></li>
</ul>

<h2>Overview</h2>
<p>This program provides a user management system where users can create a folder with their details, generate a unique QR code for identification, and verify user information by scanning the QR code. It is built using <strong>Python</strong>, with <strong>tkinter</strong> for the graphical user interface (GUI) and <strong>OpenCV</strong> for QR code scanning.</p>

<h2>Features</h2>
<ul>
    <li>Create a user folder with a unique ID and QR code</li>
    <li>Display user details on QR code scan</li>
    <li>Simple graphical interface for creating and verifying users</li>
    <li>Ability to handle multiple users and their details</li>
</ul>

<h2>How It Works</h2>

<h3>Create User Folder</h3>
<p>When a user provides their full name and Gmail address, the program creates a folder for them in a designated directory. Inside the folder, it saves a text file with the user's information and generates a unique QR code based on a UUID (Universally Unique Identifier).</p>

<h3>Scan QR Code</h3>
<p>The program uses a camera to scan QR codes. When a QR code is detected, the program looks for the corresponding user folder and displays the user's information, including their full name, Gmail, and unique key.</p>

<h3>Main Menu</h3>
<p>The program starts with a main menu allowing the user to either create a new user or verify an existing user by scanning their QR code.</p>

<h2>Code Breakdown</h2>

<h3>Create User Folder</h3>
<pre><code>
def create_user_folder(base_folder, gmail, full_name):
  try:
      unique_key = str(uuid.uuid4())  <!-- Generates a unique key for the user -->
      user_folder = os.path.join(base_folder, gmail)  <!-- Creates a folder based on Gmail -->
      os.makedirs(user_folder, exist_ok=True)  <!-- Creates the folder if it doesn't exist -->
      
  user_info_file = os.path.join(user_folder, "user_info.txt")  <!-- Creates a text file to save user info -->
  with open(user_info_file, "w") as file:
      file.write(f"Full Name: {full_name}\n")
      file.write(f"Gmail: {gmail}\n")
      file.write(f"Unique Key: {unique_key}\n")
  
  qr = qrcode.QRCode(version=1, box_size=10, border=4)  <!-- Creates a QR code object -->
  qr.add_data(unique_key)  <!-- Adds the unique key to the QR code -->
  qr.make(fit=True)  <!-- Fits the data to the QR code -->
  qr_img = qr.make_image(fill_color="black", back_color="white")  <!-- Creates the image of the QR code -->
  
  qr_code_file = os.path.join(user_folder, "qr_code.png")  <!-- Saves the QR code image -->
  qr_img.save(qr_code_file)
  return f"User created successfully!\nFolder: {user_folder}\nUnique Key: {unique_key}"
except Exception as e:
    return f"Error: {e}"
</code></pre>

<h3>Verify User by Scanning QR Code</h3>
<pre><code>
def verify_user(base_folder):
    keys, user_data = load_all_keys(base_folder)  <!-- Loads all the users' keys and data -->

  def scan_qr_code():
      qr_code_data = read_qr_code_from_camera()  <!-- Reads the QR code using the camera -->
      if qr_code_data in keys:
          display_user_interface(user_data[qr_code_data])  <!-- Displays the user's details if QR code is valid -->
      else:
          messagebox.showerror("Error", "User not found!")  <!-- Shows error if QR code is invalid -->

  def display_user_interface(user_info):
      <!-- Displays the user details like Full Name, Gmail, and Unique Key -->
      tk.Label(camera_frame, text=f"Full Name: {user_info['Full Name']}", font=("Helvetica", 22), bg="#ffffff").pack(pady=20)
      tk.Label(camera_frame, text=f"Gmail: {user_info['Gmail']}", font=("Helvetica", 22), bg="#ffffff").pack(pady=20)
      tk.Label(camera_frame, text=f"Unique Key: {user_info['Unique Key']}", font=("Helvetica", 22), bg="#ffffff").pack(pady=20)
  </code></pre>

<h3>Scanning QR Code</h3>
<pre><code>
def read_qr_code_from_camera():
    cap = cv2.VideoCapture(0)  <!-- Captures video from the camera -->
    detector = cv2.QRCodeDetector()  <!-- Detects QR code in the video stream -->

  while True:
      ret, frame = cap.read()  <!-- Captures each frame from the video -->
      if not ret:
          continue

  data, bbox, _ = detector.detectAndDecode(frame)  <!-- Detects and decodes the QR code -->
  if data:
      cap.release()
      cv2.destroyAllWindows()
      return data  <!-- Returns the decoded data -->
  </code></pre>

<h2>Requirements</h2>
<ul>
    <li><strong>Python 3.x</strong></li>
    <li><strong>tkinter</strong> (for GUI)</li>
    <li><strong>OpenCV</strong> (for QR code scanning)</li>
    <li><strong>qrcode</strong> (for QR code generation)</li>
</ul>

<h2>Usage</h2>
<ol>
    <li>Run the Python script.</li>
    <li>Choose "Create User" to create a new user, or "Verify User" to scan a QR code.</li>
    <li>If creating a user, enter the required details, and a unique QR code will be generated.</li>
    <li>If verifying a user, scan the QR code to view their information.</li>
</ol>

<h2>License</h2>
<p>This code is open-source and can be used freely under the MIT license.</p>
