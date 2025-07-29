# Wordbomb Macro

![demo](https://github.com/user-attachments/assets/7f7d0522-e93a-4f01-973b-87312b36ed7b)
(in the gif above i was fartmaster and i got banned)



A Python macro with a modern GUI for automating word extraction and typing in the Wordbomb game using OCR (Tesseract) and Datamuse API.

## Features
- Select screen region for OCR with a visual overlay
- Adjustable typing speed
- Manual entry and auto-capture modes
- Modern tkinter GUI
- Bundles Tesseract-OCR for offline OCR

## Requirements
- Python 3.8+
- Tesseract-OCR (not included in repo, see below)

## Setup
1. **Clone this repository**
2. **Download Tesseract-OCR**
   - Download the `Tesseract-OCR` Windows folder (not included here due to size)
   - Place it in the project root so the path is: `wordbomb-macro/Tesseract-OCR/tesseract.exe`
3. **Install dependencies**
   - Create and activate a virtual environment (optional but recommended):
     ```
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - Install requirements:
     ```
     pip install -r requirements.txt
     ```

## Usage
- Run the script:
  ```
  python wordbomb_macro.py
  ```
- Use the GUI to select a region, adjust typing speed, and start automation.

## Building the EXE
1. Make sure all dependencies are installed in your venv.
2. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
3. Build the executable:
   ```
   pyinstaller --onefile --noconsole --add-data "Tesseract-OCR;Tesseract-OCR" wordbomb_macro.py
   ```
4. The `.exe` will be in the `dist` folder. Do **not** push this file to GitHub.

## Sharing the EXE
- Upload the `.exe` and `Tesseract-OCR` folder to a file sharing service (Google Drive, Dropbox, etc.)
- Share the download link with users.

## Notes
- `.exe` size is large due to Python, dependencies, and Tesseract-OCR.
- Do **not** push `Tesseract-OCR/` or `.exe` files to GitHub (see `.gitignore`).

## License
MIT
