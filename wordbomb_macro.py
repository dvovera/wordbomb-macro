import re
# Enhanced region selection with mouse clicks and visual rectangle
def clean_input(text):
    # Keep only uppercase letters
    return re.sub(r'[^A-Z]', '', text.upper())


import pytesseract
print(pytesseract.__version__)
import cv2
import numpy as np
import pyautogui
from PIL import Image
import requests
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import keyboard


# GUI global state
region = None
typing_speed = 0.01  # Default typing speed (seconds per character)

# Set the path to Tesseract (Windows users)
import os
import sys

if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    tesseract_path = os.path.join(sys._MEIPASS, 'tesseract-OCR', 'tesseract.exe')
else:
    tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract-OCR', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path
# Function to let user select a region by clicking two corners (GUI)

# Enhanced region selection with mouse clicks and visual rectangle
def select_capture_region_gui():
    # Create a fullscreen transparent overlay window
    overlay = tk.Toplevel(root)
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-alpha', 0.3)
    overlay.attributes('-topmost', True)
    overlay.config(bg='black')
    overlay.lift()
    canvas = tk.Canvas(overlay, bg=None, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    coords = {'x1': None, 'y1': None, 'x2': None, 'y2': None, 'rect': None}
    instructions = tk.Label(overlay, text="Click and drag to select region", font=("Arial", 24), bg='yellow')
    instructions.place(relx=0.5, rely=0.05, anchor='n')

    def on_mouse_down(event):
        coords['x1'] = event.x
        coords['y1'] = event.y
        coords['x2'] = event.x
        coords['y2'] = event.y
        if coords['rect']:
            canvas.delete(coords['rect'])
        coords['rect'] = canvas.create_rectangle(coords['x1'], coords['y1'], coords['x2'], coords['y2'], outline='red', width=3)

    def on_mouse_move(event):
        if coords['x1'] is not None and coords['y1'] is not None:
            coords['x2'] = event.x
            coords['y2'] = event.y
            if coords['rect']:
                canvas.coords(coords['rect'], coords['x1'], coords['y1'], coords['x2'], coords['y2'])

    def on_mouse_up(event):
        coords['x2'] = event.x
        coords['y2'] = event.y
        overlay.after(100, overlay.destroy)

    canvas.bind('<Button-1>', on_mouse_down)
    canvas.bind('<B1-Motion>', on_mouse_move)
    canvas.bind('<ButtonRelease-1>', on_mouse_up)
    overlay.focus_set()
    overlay.grab_set()
    root.wait_window(overlay)

    x1, y1, x2, y2 = coords['x1'], coords['y1'], coords['x2'], coords['y2']
    if None in (x1, y1, x2, y2):
        messagebox.showwarning("Selection Cancelled", "No region selected.")
        return None
    # Normalize coordinates
    left, right = sorted([x1, x2])
    top, bottom = sorted([y1, y2])
    width = right - left
    height = bottom - top
    messagebox.showinfo("Region Selected", f"Selected region: ({left}, {top}, {width}, {height})")
    return (left, top, width, height)





def capture_and_read_text(region=None):
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if region:
        x, y, w, h = region
        img = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    custom_config = r'--psm 6'
    extracted_text = pytesseract.image_to_string(gray, config=custom_config)
    return extracted_text

# s

def find_words(sequence):
    # Build the URL with the wildcard (*) around the sequence
    url = f"https://api.datamuse.com/words?sp=*{sequence}*"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse JSON response
        words_data = response.json()

        return [word_info for word_info in words_data if ' ' not in word_info['word']]
    else:
        print("Error fetching data from the API.")
        return []


def main(syllable):
    syllable = syllable.strip()
    words = find_words(syllable)
    return words






def auto_read_and_type_word_gui():
    global region
    if not region:
        messagebox.showwarning("No Region", "Please select a region first.")
        return
    text = capture_and_read_text(region)
    cleaned_text = clean_input(text)
    extracted_text_box.delete(1.0, tk.END)
    extracted_text_box.insert(tk.END, cleaned_text)
    words = main(cleaned_text)
    found_words_box.delete(1.0, tk.END)
    interval = typing_speed_var.get()
    if words:
        for word in words[:15]:
            found_words_box.insert(tk.END, f"{word['word']} (score: {word.get('score',0)})\n")
        word = random.choice(words[:15])
        text_to_type = word['word'].strip()
        pyautogui.write(text_to_type, interval=interval)
        pyautogui.press('enter')
    else:
        found_words_box.insert(tk.END, "No words found.")





def manual_entry_gui():
    entry = simpledialog.askstring("Manual Entry", "Enter your letters:")
    if entry:
        cleaned_entry = clean_input(entry)
        words = main(cleaned_entry)
        found_words_box.delete(1.0, tk.END)
        interval = typing_speed_var.get()
        if words:
            for word in words[:10]:
                found_words_box.insert(tk.END, f"{word['word']} (score: {word.get('score',0)})\n")
            word = random.choice(words[:10])
            text_to_type = word['word'].strip()
            pyautogui.write(text_to_type, interval=interval)
            pyautogui.press('enter')
        else:
            found_words_box.insert(tk.END, "No words found.")

def finish_manual_entry():
    global typed_text
    global detecting

    if not detecting:
        return
    
    print("Running script...")
    keyboard.press_and_release('enter')

    print("Detected text:", typed_text)    
    words = main(typed_text)
    if words:
        word = random.choice(words[:10])
        text_to_type = word['word'].strip()
        print("Detected text:", typed_text)    
        print("\nTyping the word:", text_to_type, "\nScore:", word['score'])
        pyautogui.write(text_to_type, interval=0.01)  # Adjust interval for typing speed
        keyboard.press_and_release('enter')
    else:
        print("The list is empty. Cannot choose a random element")
    detecting = False


# --- GUI Setup ---


# --- Modern GUI Styling ---
BG_COLOR = "#23272e"
FG_COLOR = "#f8f8f2"
ACCENT_COLOR = "#6272a4"
BTN_COLOR = "#44475a"
BTN_ACTIVE = "#6272a4"
FONT = ("Segoe UI", 12)
HEADER_FONT = ("Segoe UI", 18, "bold")

root = tk.Tk()
root.title("Wordbomb Macro GUI")
root.attributes('-topmost', True)
root.configure(bg=BG_COLOR)


def select_region_button():
    global region
    region = select_capture_region_gui()
    if region:
        region_label.config(text=f"Region: {region}")
    else:
        region_label.config(text="Region: Not selected")


# --- Header ---
header = tk.Label(root, text="Wordbomb Macro", font=HEADER_FONT, bg=BG_COLOR, fg=ACCENT_COLOR)
header.pack(pady=(18, 8))

region_label = tk.Label(root, text="Region: Not selected", font=FONT, bg=BG_COLOR, fg=FG_COLOR)
region_label.pack(pady=(0, 8))

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=FONT, background=BTN_COLOR, foreground=FG_COLOR, borderwidth=0, focusthickness=3, focuscolor=ACCENT_COLOR, padding=8)
style.map('TButton', background=[('active', BTN_ACTIVE)])

select_region_btn = ttk.Button(root, text="Select Region", command=select_region_button, style='TButton')
select_region_btn.pack(pady=6, ipadx=8, ipady=2)


# Typing speed slider
typing_speed_var = tk.DoubleVar(value=0.01)
def update_speed_label(val):
    speed_val = float(val)
    speed_label.config(text=f"Typing Speed: {speed_val:.3f} sec/char")

speed_frame = tk.Frame(root, bg=BG_COLOR)
speed_frame.pack(pady=(0, 10))
speed_label = tk.Label(speed_frame, text=f"Typing Speed: {typing_speed_var.get():.3f} sec/char", font=FONT, bg=BG_COLOR, fg=ACCENT_COLOR)
speed_label.pack(side=tk.LEFT, padx=(0, 10))
speed_slider = ttk.Scale(speed_frame, from_=0.001, to=0.1, orient=tk.HORIZONTAL, variable=typing_speed_var, command=update_speed_label, length=200)
speed_slider.pack(side=tk.LEFT)

ctrl_label = tk.Label(root, text="Press Ctrl to Capture & Extract (global hotkey)", font=FONT, bg=BG_COLOR, fg=ACCENT_COLOR)
ctrl_label.pack(pady=(0, 10))

def on_ctrl_keyboard():
    auto_read_and_type_word_gui()
keyboard.add_hotkey('ctrl', on_ctrl_keyboard)

manual_btn = ttk.Button(root, text="Manual Entry", command=manual_entry_gui, style='TButton')
manual_btn.pack(pady=6, ipadx=8, ipady=2)

tk.Label(root, text="Extracted Text:", font=FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=(10, 0))
extracted_text_box = ScrolledText(root, height=4, width=50, font=FONT, bg=BTN_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, borderwidth=0)
extracted_text_box.pack(pady=5)

tk.Label(root, text="Found Words:", font=FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=(10, 0))
found_words_box = ScrolledText(root, height=10, width=50, font=FONT, bg=BTN_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, borderwidth=0)
found_words_box.pack(pady=5)

root.mainloop()