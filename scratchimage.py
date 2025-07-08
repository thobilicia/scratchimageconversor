import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def convert_image():
    global output_path  # vamos usar essa var depois no botão de copiar
    file_path = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )

    if not file_path:
        return  # cancelado

    try:
        width, height = 480, 360

        img = Image.open(file_path).convert("RGB")
        img = img.resize((width, height))

        values = []
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                number = r * 65536 + g * 256 + b
                values.append(str(number))

        output_path = os.path.join(os.path.dirname(file_path), "pixels.txt")
        with open(output_path, "w") as f:
            f.write(" ".join(values))

        copy_button.config(state="normal")  # ativa botão de copiar
        feedback_label.config(text="pixels.txt generated!", fg="green")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def copy_to_clipboard():
    try:
        with open(output_path, "r") as f:
            data = f.read()
            janela.clipboard_clear()
            janela.clipboard_append(data)
            feedback_label.config(text="Text copied to clipboard!", fg="blue")
            janela.after(3000, lambda: feedback_label.config(text=""))  # limpa após 3s
    except:
        messagebox.showerror("Error", "You need to convert an image first.")


# Janela principal
janela = tk.Tk()
janela.title("thobiw scratch image conversor")
janela.geometry("420x240")

title = tk.Label(janela, text="Click below to select an image", font=("Arial", 13))
title.pack(pady=15)

convert_button = tk.Button(
    janela, text="Select image", command=convert_image,
    font=("Arial", 11), bg="#4CAF50", fg="white", padx=10, pady=5
)
convert_button.pack()

copy_button = tk.Button(
    janela, text="Copy pixel text to clipboard", command=copy_to_clipboard,
    font=("Arial", 11), bg="#2196F3", fg="white", padx=10, pady=5
)
copy_button.pack(pady=10)
copy_button.config(state="disabled")  # só ativa depois de gerar o arquivo

feedback_label = tk.Label(janela, text="", font=("Arial", 10))
feedback_label.pack()

janela.mainloop()
