import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def upload_file():
    file_path = file_entry.get()
    user_hash_value = user_hash.get()

    # Check if a file is selected
    if not file_path:
        messagebox.showerror('Error', 'Please select a file to upload.')
        return

    # Prepare the data payload for the POST request
    data = {'reqtype': 'fileupload'}
    if user_hash_value:
        data['userhash'] = user_hash_value

    # Prepare the files payload for the POST request
    files = {'fileToUpload': open(file_path, 'rb')}

    # Make the POST request to the Catbox API
    try:
        response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
        # Close the file after the request is made
        files['fileToUpload'].close()

        # Check the response status
        if response.status_code == 200:
            messagebox.showinfo('Success', 'Upload successful. URL: ' + response.text)
        else:
            messagebox.showerror('Error', f'Upload failed. Status Code: {response.status_code}')
    except Exception as e:
        messagebox.showerror('Error', str(e))

# Create the main window
root = tk.Tk()
root.title("Catbox File Uploader")
root.geometry('400x200')  # Set the window size
root.resizable(False, False)  # Disable resizing

# Create the user hash entry with a label
hash_label = tk.Label(root, text="Catbox User Hash (optional):")
hash_label.pack()
user_hash = tk.Entry(root, width=40)
user_hash.pack()

# Create the file selection entry and button
file_label = tk.Label(root, text="Select the file to upload:")
file_label.pack()
file_entry = tk.Entry(root, width=40)
file_entry.pack()
select_button = tk.Button(root, text="Browse", command=select_file)
select_button.pack()

# Create the upload button
upload_button = tk.Button(root, text="Upload to Catbox", command=upload_file)
upload_button.pack(pady=20)

root.mainloop()
