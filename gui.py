import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import shutil
import os
from PIL import Image, ImageTk

class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1="#6dd5ed", color2="#2193b0", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / height
        g_ratio = float(g2-g1) / height
        b_ratio = float(b2-b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.lower("gradient")

def upload_pdf():
    file_path = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF Files", "*.pdf")]
    )
    
    if file_path:
        program_folder = os.getcwd()
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(program_folder, file_name)
        try:
            shutil.copy(file_path, destination_path)
            messagebox.showinfo("File Uploaded", f"PDF uploaded and saved as: {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
    else:
        messagebox.showwarning("No File", "No file was selected.")

root = tk.Tk()
root.title("Dallani Program")
root.attributes("-fullscreen", True)

# Create gradient background
background = GradientFrame(root)
background.pack(fill="both", expand=True)

# Create title
title_label = tk.Label(background, text="Dallani Program", font=("Arial", 36, "bold"), bg="#6dd5ed", fg="#155724")
title_label.pack(pady=(20, 10))

# Create header frame with full-width background
header_frame = tk.Frame(background, bg="#2193b0")
header_frame.pack(fill="x", pady=10)

# Create centered menu buttons
menu_items = ["File", "Edit", "View", "Help"]
menu_frame = tk.Frame(header_frame, bg="#2193b0")
menu_frame.pack(expand=True)

for item in menu_items:
    menu_button = tk.Button(menu_frame, text=item, bg="#2193b0", fg="white", 
                            relief="flat", padx=20, pady=10, font=("Arial", 14))
    menu_button.pack(side="left", padx=10)

# Create main content frame
content_frame = tk.Frame(background, bg="")
content_frame.pack(expand=True)

# Add text above logo
image_text = tk.Label(content_frame, text="Your PDF Upload Center", font=("Arial", 18), bg="#6dd5ed", fg="#155724")
image_text.pack(pady=(20, 10))

# Load and display the logo
try:
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((200, 200), Image.LANCZOS)  # Resize the image
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(content_frame, image=logo_photo, bg="#6dd5ed")
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)
except FileNotFoundError:
    print("Logo file 'logo.png' not found. Displaying placeholder instead.")
    logo_label = tk.Label(content_frame, text="LOGO", font=("Arial", 36, "bold"), bg="#2193b0", fg="white", width=10, height=5)
    logo_label.pack(pady=10)

style = ttk.Style()
style.theme_use('clam')

style.configure("TButton",
                foreground="white",
                background="#28a745",
                font=("Arial", 12, "bold"),
                padding=10,
                borderwidth=0)
style.map("TButton", 
          background=[("active", "#218838")],
          relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

style.configure("TLabel",
                foreground="#155724", 
                background="",
                font=("Arial", 14))

label = ttk.Label(content_frame, text="Click the button below to upload a PDF file")
label.pack(pady=20)

upload_button = ttk.Button(content_frame, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=20)

# Add hover effect to the button
def on_enter(e):
    upload_button['style'] = 'Hover.TButton'

def on_leave(e):
    upload_button['style'] = 'TButton'

style.configure('Hover.TButton', background='#218838')
upload_button.bind("<Enter>", on_enter)
upload_button.bind("<Leave>", on_leave)

root.mainloop()