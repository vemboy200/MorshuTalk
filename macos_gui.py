import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import os

from morshutalk import Morshu
from sounddevice import play

morshu = Morshu()

def speak():
    text = entry.get()
    if not text.strip():
        return
    def run():
        try:
            audio = morshu.load_text(text)
            play(audio.get_array_of_samples(), audio.frame_rate)
        except Exception as e:
            messagebox.showerror("MorshuTalk Error", str(e))
    threading.Thread(target=run, daemon=True).start()

def save_audio():
    text = entry.get()
    if not text.strip():
        messagebox.showinfo("MorshuTalk", "Type some text first.")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("WAV audio", "*.wav"), ("MP3 audio", "*.mp3")],
        title="Save Morshu audio as...",
    )
    if not path:
        return

    ext = os.path.splitext(path)[1].lower().lstrip(".")
    fmt = "mp3" if ext == "mp3" else "wav"

    def run():
        try:
            audio = morshu.load_text(text)
            audio.export(path, format=fmt)
            messagebox.showinfo("MorshuTalk", f"Saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("MorshuTalk Error", str(e))
    threading.Thread(target=run, daemon=True).start()

root = tk.Tk()
root.title("MorshuTalk")
root.geometry("420x200")

tk.Label(root, text="Enter text for Morshu to speak:").pack(pady=10)

entry = tk.Entry(root, width=45)
entry.pack(pady=5)
entry.bind("<Return>", lambda e: speak())
entry.focus()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Speak", command=speak, width=15).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Save Audio", command=save_audio, width=15).pack(side=tk.LEFT, padx=5)

root.mainloop()
