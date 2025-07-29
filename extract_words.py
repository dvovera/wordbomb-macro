import pytesseract
import cv2
import numpy as np
import pyautogui

from PIL import Image

import requests
import time
import keyboard

import random

# Set the path to Tesseract (Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define the coordinates of the area to capture (x, y, width, height)
x1, y1, x2, y2 = -989, 282, -920, 318

region = (720, 600, 80, 50)  # Example: (x=100, y=200, width=800, height=400)

# Create an empty string to store the typed keys
typed_text = ""
detecting = False

def capture_and_read_text(region=None):
    
    # while True:
    #   print(pyautogui.position())

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Convert screenshot to a NumPy array (for OpenCV)
    img = np.array(screenshot)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)



    # Crop the image to the specified region
    if region:
        x, y, w, h = region
        img = img[y:y+h, x:x+w]  # Crop to (y1:y2, x1:x2)


    # Convert to grayscale for better OCR results
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to enhance text visibility
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # SHOW IMAGE
    # cv2.imshow("Screenshot", gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Use Tesseract to extract text
    custom_config = r'--psm 6' 
    extracted_text = pytesseract.image_to_string(gray, config=custom_config)

    return extracted_text



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
    
    if words:
        print(f"Words containing '{syllable}':")
        print(words)
        # for word in words:
        #     print(word)
    else:
        print(f"No words found containing '{syllable}'.")
      
    return words



def on_spacebar():
    print("Running script...")

    print("Capturing screen and extracting text from specific area...")
    text = capture_and_read_text(region)
    print("\nExtracted Text:\n", text)
    words = main(text)
    if words:
      word = random.choice(words[:10])
      text_to_type = word['word'].strip()
      print("\nExtracted Text:\n", text)
      print("\nTyping the word:", text_to_type, "\nScore:", word['score'])
      pyautogui.write(text_to_type, interval=0.05)  # Adjust interval for typing speed
      keyboard.press_and_release('enter')
    else:
      print("The list is empty. Cannot choose a random element.")


def manual_entry():
    global typed_text
    global detecting

    print("Running manual script... Type your letters and press enter.")
    
    typed_text = ""
    detecting = True

typing = False

def finish_manual_entry():
    global typed_text
    global detecting
    global typing
    detecting = False

    # if not detecting:
    #     return
    
    print("Running script...")
    keyboard.press_and_release('enter')

    print("Detected text:", typed_text)    
    words = main(typed_text)
    word = random.choice(words[:10])
    text_to_type = word['word'].strip()
    print("Detected text:", typed_text)    
    print("\nTyping the word:", text_to_type, "\nScore:", word['score'])

    pyautogui.write(text_to_type, interval=0.03)  # Adjust interval for typing speed

    keyboard.press_and_release('enter')
    time.sleep(1)
    typed_text = ""

    detecting = True

# Listen for spacebar keypress and call function
keyboard.add_hotkey("ctrl", on_spacebar)

# Listen for spacebar keypress and call function
keyboard.add_hotkey("shift", manual_entry)
keyboard.add_hotkey("enter", finish_manual_entry)

# keyboard.add_hotkey("enter", )

print("Press the cntrl to trigger the script or shift to manual entry. Press ESC to exit.")

# Function to record typed text
def record_keys(keyboard_event):
    global typed_text
    global detecting

    if detecting:
      if keyboard_event.event_type == keyboard.KEY_DOWN:
        if keyboard_event.name not in ['shift', 'ctrl', 'alt', 'enter', 'esc', 'tab', 'caps lock', 'backspace', 'space',"-"]:
          typed_text += keyboard_event.name  # Add the key to the string
          print(f"Recorded: {typed_text}")  # Optional: print each key typed

# Hook the keyboard events to call the function when a key is pressed
keyboard.hook(record_keys)

print("Recording... Press 'esc' to stop.")

# Keep the script running
keyboard.wait("esc")  # Stops when ESC is pressed