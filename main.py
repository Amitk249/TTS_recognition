import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from gtts import gTTS
import pygame
import tempfile
import os

class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Text-to-Speech Application")
        master.geometry("500x400")

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "temp.mp3")

        self.create_widgets()

    def create_widgets(self):
        # Text input
        self.text_label = ttk.Label(self.master, text="Enter text:")
        self.text_label.pack(pady=5)
        
        self.text_entry = tk.Text(self.master, height=10, width=50)
        self.text_entry.pack(pady=5)

        # Language selection
        self.lang_label = ttk.Label(self.master, text="Select language:")
        self.lang_label.pack(pady=5)
        
        self.lang_var = tk.StringVar()
        self.lang_combo = ttk.Combobox(self.master, textvariable=self.lang_var)
        self.lang_combo['values'] = ('en', 'fr', 'es', 'de', 'it')
        self.lang_combo.set('en')
        self.lang_combo.pack(pady=5)

        # Speed control
        self.speed_label = ttk.Label(self.master, text="Speech speed:")
        self.speed_label.pack(pady=5)
        
        self.speed_var = tk.DoubleVar()
        self.speed_scale = ttk.Scale(self.master, from_=0.5, to=2.0, orient='horizontal', 
                                     variable=self.speed_var, length=200)
        self.speed_scale.set(1.0)
        self.speed_scale.pack(pady=5)

        # Buttons
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=20)

        self.speak_button = ttk.Button(self.button_frame, text="Speak", command=self.speak_text)
        self.speak_button.pack(side='left', padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save Audio", command=self.save_audio)
        self.save_button.pack(side='left', padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self.clear_text)
        self.clear_button.pack(side='left', padx=5)

    def speak_text(self):
        text = self.text_entry.get("1.0", 'end-1c')
        lang = self.lang_var.get()
        speed = self.speed_var.get()

        if not text:
            messagebox.showwarning("Warning", "Please enter some text to speak.")
            return

        tts = gTTS(text=text, lang=lang, slow=False)
        try:
            tts.save(self.temp_file)
        except PermissionError:
            messagebox.showerror("Error", "Permission denied while saving the temporary audio file.")
            return

        pygame.mixer.music.load(self.temp_file)
        pygame.mixer.music.play()

    def save_audio(self):
        text = self.text_entry.get("1.0", 'end-1c')
        lang = self.lang_var.get()

        if not text:
            messagebox.showwarning("Warning", "Please enter some text to save as audio.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])

        if file_path:
            tts = gTTS(text=text, lang=lang, slow=False)
            try:
                tts.save(file_path)
                messagebox.showinfo("Success", f"Audio saved successfully to {file_path}")
            except PermissionError:
                messagebox.showerror("Error", "Permission denied while saving the audio file.")
    
    def clear_text(self):
        self.text_entry.delete("1.0", 'end')

    def __del__(self):
        # Clean up the temporary file and directory
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            if os.path.exists(self.temp_dir):
                os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
