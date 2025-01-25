import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
import os

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image
def grayify(image):
    return image.convert("L")
def pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    ascii_str = ""
    num_chars = len(ascii_chars)
    for pixel in pixels:
        intensity = pixel
        index = int(intensity / 256 * (num_chars - 1))
        ascii_str += ascii_chars[index]
    return ascii_str
def image_to_ascii(image_path, new_width=100, ascii_chars=None):
    try:
        image = Image.open(image_path)
        image = resize_image(image, new_width)
        image = grayify(image)
        ascii_str = pixels_to_ascii(image, ascii_chars)
        img_width = image.width
        ascii_str_len = len(ascii_str)
        ascii_img = ""
        for i in range(0, ascii_str_len, img_width):
            ascii_img += ascii_str[i:i + img_width] + "\n"
        return ascii_img
    except Exception as e:
        print("Error:", e)
        return None
def save_ascii_image(ascii_img):
    custom_filename = simpledialog.askstring("Save File", "Enter the custom filename (with extension, e.g., 'my_ascii_art.txt'): ")
    if not custom_filename:
        custom_filename = "output.txt"
    with open(custom_filename, "w") as f:
        f.write(ascii_img)
    print(f"The ASCII art has been saved to '{custom_filename}'.")
def get_ascii_symbols():
    num_symbols = simpledialog.askinteger("Symbols", "Enter the number of symbols (e.g., 2, 4, 6, 8):", minvalue=2)
    available_symbols = ['.', ',', '-', '+', '*', '%', '#', '@', '&', '$']
    symbols = []
    for i in range(num_symbols):
        symbol = simpledialog.askstring(f"Symbol {i + 1}", f"Enter symbol {i + 1}: (Leave empty for default)")
        if not symbol:
            symbol = available_symbols[i % len(available_symbols)]
        symbols.append(symbol)
    return symbols
def process_image():
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp")]
    )
    if not image_path:
        print("No image selected. Exiting process.")
        return
    try:
        image = Image.open(image_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
        new_width = simpledialog.askinteger("Width", "Enter the desired width for the ASCII art:", minvalue=10)
        ascii_chars = get_ascii_symbols()
        ascii_image = image_to_ascii(image_path, new_width, ascii_chars)
        if ascii_image:
            ascii_text.delete(1.0, tk.END)
            ascii_text.insert(tk.END, ascii_image)
            save_ascii_image(ascii_image)
    except Exception as e:
        print(f"Error opening image: {e}")
def toggle_theme():
    global dark_mode
    if dark_mode:
        root.configure(bg="#f0f0f0")
        process_button.config(bg="#d1d1d1", fg="black", activebackground="#a0a0a0")
        image_label.config(bg="#f0f0f0")
        ascii_text.config(bg="#ffffff", fg="black", insertbackground="black")
        dark_mode = False
    else:
        root.configure(bg="#2e2e2e")
        process_button.config(bg="#3e3e3e", fg="white", activebackground="#505050")
        image_label.config(bg="#2e2e2e")
        ascii_text.config(bg="#333333", fg="white", insertbackground="white")
        dark_mode = True
dark_mode = True
root = tk.Tk()
root.title("Image to ASCII Art")
root.configure(bg="#2e2e2e")
process_button = tk.Button(root, text="Generate ASCII Art", command=process_image, bg="#3e3e3e", fg="white", activebackground="#505050", font=("Arial", 12))
process_button.pack(pady=10)
image_label = tk.Label(root, bg="#2e2e2e")
image_label.pack(padx=10, pady=10)
ascii_text = tk.Text(root, width=80, height=20, bg="#333333", fg="white", font=("Courier", 10), insertbackground="white", wrap="word")
ascii_text.pack(padx=10, pady=10)
theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg="#3e3e3e", fg="white", activebackground="#505050", font=("Arial", 12))
theme_button.pack(side="bottom", pady=10)
root.mainloop()
