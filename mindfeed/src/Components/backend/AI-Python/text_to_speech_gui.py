#11.7th - remove that audio speed modification and just use the original Code 2 approach
import tkinter as tk
from tkinter import messagebox, ttk
from gtts import gTTS
import os
import sys
import time
import re
import pygame
from googletrans import Translator
import atexit
import socket  # For internet connectivity check
import threading
import asyncio
from pydub import AudioSegment  # For local audio processing

TEMP_AUDIO_FILE = "temp_audio.mp3"

def cleanup_temp_file():
    # Only delete the file named exactly TEMP_AUDIO_FILE in the current working directory.
    if os.path.exists(TEMP_AUDIO_FILE):
        try:
            os.remove(TEMP_AUDIO_FILE)
            print("Temp file deleted at exit.")
        except Exception as e:
            print(f"Error deleting temp file at exit: {e}")

atexit.register(cleanup_temp_file)

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Check internet connectivity by attempting to connect to Google's DNS.
    Returns True if connection is successful, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print(f"Connection string(s): {s}, Host: {host}, Port: {port}")
        s.close()
        return True
    except Exception:
        return False

def run_async(coro):
    """Run an async coroutine in a separate thread and return its result."""
    result_container = []
    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coro)
        result_container.append(result)
        loop.close()
    t = threading.Thread(target=run_loop)
    t.start()
    t.join()
    return result_container[0]

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Converter v11.2")
        self.root.geometry("500x480")  # Increased height to accommodate extra buttons
        self.root.configure(bg="#2c3e50")  # Dark Blue Background

        # Font Styles
        self.label_font = ("Helvetica", 12, "bold")
        self.text_font = ("Arial", 12)
        self.button_font = ("Helvetica", 11, "bold")

        # Main Frame for Styling
        frame = tk.Frame(root, bg="#34495e", padx=10, pady=10, relief=tk.RIDGE, bd=3)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Title Label
        self.label = tk.Label(frame, text="Enter Text:", font=self.label_font, fg="white", bg="#34495e")
        self.label.pack(anchor="w", pady=(5, 0))

        # Text field
        self.text_field = tk.Text(frame, height=5, width=50, font=self.text_font, wrap=tk.WORD)
        self.text_field.pack(padx=5, pady=5, expand=True, fill='both')
        self.text_field.insert("1.0", self.input_text)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_field, command=self.text_field.yview)
        self.text_field.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        # Character Counter
        self.char_count_label = tk.Label(frame, text="Characters: 0", font=("Arial", 10), fg="white", bg="#34495e")
        self.char_count_label.pack(anchor="w", pady=(2, 0))
        self.text_field.bind("<KeyRelease>", self.update_char_count)

        # Language Selection Dropdown
        self.language_label = tk.Label(frame, text="Select Language:", font=self.label_font, fg="white", bg="#34495e")
        self.language_label.pack(anchor="w", pady=(10, 0))
        self.language_var = tk.StringVar(value='English')
        self.language_options = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it'
        }
        self.language_menu = ttk.Combobox(frame, textvariable=self.language_var,
                                          values=list(self.language_options.keys()), state='readonly')
        self.language_menu.pack(fill='x', pady=5)

        # Playback Speed Label (static text)
        self.speed_static_label = tk.Label(frame, text="Playback Speed:", font=self.label_font, fg="white", bg="#34495e")
        self.speed_static_label.pack(anchor="w", pady=(10, 0))
        # Create a frame to hold the radio buttons for binary speed option
        self.binary_radio_frame = tk.Frame(frame, bg="#34495e")
        self.binary_radio_frame.pack(fill='x', pady=5)
        # Playback Speed Variable (binary option: "Normal" or "Fast") - DO NOT MODIFY THIS LINE
        self.speed_var = tk.StringVar(value="Normal")
        self.normal_speed_button = tk.Radiobutton(self.binary_radio_frame, text="Normal", variable=self.speed_var, value="Normal", bg="#34495e", fg="white", selectcolor="black")
        self.fast_speed_button = tk.Radiobutton(self.binary_radio_frame, text="Fast", variable=self.speed_var, value="Fast", bg="#34495e", fg="white", selectcolor="black")
        self.normal_speed_button.pack(anchor="w")
        self.fast_speed_button.pack(anchor="w")

        # Convert Button
        self.convert_button = tk.Button(frame, text="Convert to Speech", command=self.convert_to_speech,
                                        font=self.button_font, fg="white", bg="#16a085", padx=10, pady=5,
                                        relief=tk.RAISED, cursor="hand2")
        self.convert_button.pack(pady=10, fill='x')
        # Automatically start the conversion
        self.convert_to_speech()


        # Playback Control Buttons Frame (initially hidden)
        self.control_frame = tk.Frame(frame, bg="#34495e")
        # Left slot: Pause/Resume button (using grid)
        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause_audio,
                                      font=self.button_font, fg="white", bg="#2980b9", padx=10, pady=5,
                                      relief=tk.RAISED, cursor="hand2")
        self.pause_button.grid(row=0, column=0, padx=5, sticky='ew')
        self.resume_button = tk.Button(self.control_frame, text="Resume", command=self.resume_audio,
                                       font=self.button_font, fg="white", bg="#2980b9", padx=10, pady=5,
                                       relief=tk.RAISED, cursor="hand2")
        # Right slot: Stop & Delete button (always fixed)
        self.stop_button = tk.Button(self.control_frame, text="Stop & Delete", command=self.stop_audio,
                                     font=self.button_font, fg="white", bg="#c0392b", padx=10, pady=5,
                                     relief=tk.RAISED, cursor="hand2")
        self.stop_button.grid(row=0, column=1, padx=5, sticky='ew')
        self.hide_control_buttons()

        # Toggle Theme Button
        self.theme_button = tk.Button(frame, text="Toggle Theme", command=self.toggle_theme,
                                      font=("Arial", 10, "bold"), fg="white", bg="#f39c12",
                                      relief=tk.RAISED, cursor="hand2")
        self.theme_button.pack(fill='x', pady=5)

        self.dark_mode = True
        self.paused = False
        self.audio_playing = False
        self.audio_filename = None
        self.monitor_id = None  # For storing the after() callback ID

        # For translation and speed change functionality
        self.original_audio = None  # To store the complete original AudioSegment
        self.pause_pos = 0  # In milliseconds

        # Bind the window close event to ensure TEMP_AUDIO_FILE is deleted.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Configure>", self.update_control_frame_widths)

    def update_char_count(self, event=None):
        text_length = len(self.text_field.get("1.0", tk.END)) - 1
        self.char_count_label.config(text=f"Characters: {text_length}")

    def normalize_backslashes(self, text):
        return re.sub(r'\\+', r'\\\\', text)

    def check_file_exists(self, directory, filename):
        file_path = os.path.join(directory, filename)
        file_path = self.normalize_backslashes(file_path)
        print("File path: ", file_path)
        return os.path.isfile(file_path)

    async def translate_text(self, text, language_code):
        # Asynchronously translate text using googletrans
        translator = Translator()
        translated = await translator.translate(text, dest=language_code)
        return translated.text

    def convert_to_speech(self):
        if not is_connected():
            messagebox.showinfo("Info", "No internet connection detected. Please ensure you are connected to the internet before using this feature.\n\nTip: To avoid this error, verify your network connection or use an offline text-to-speech solution like pyttsx3.")
            return

        language_code = self.language_options[self.language_var.get()]
        text = self.text_field.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return
        try:
            # Run the asynchronous translation in a separate thread
            translated_text = run_async(self.translate_text(text, language_code))
            print("Translated text: ", translated_text)
            # Use binary speed option: if "Normal" then slow=False, if "Fast" then slow=True
            slow_param = False if self.speed_var.get() == "Fast" else True
            tts = gTTS(text=translated_text, lang=language_code, slow=slow_param)
            directory = os.getcwd()
            if self.check_file_exists(directory, TEMP_AUDIO_FILE):
                os.remove(TEMP_AUDIO_FILE)
                print("*** Existing temp_audio.mp3 file deleted to avoid filename clash! ***\n")
            tts.save(TEMP_AUDIO_FILE)
            self.audio_filename = TEMP_AUDIO_FILE

            # Giving buffer time for 'Safe loading' of the audio file
            time.sleep(1)
            # Bring the application to the foreground
            self.root.attributes("-topmost", True)
            self.root.attributes("-topmost", False)

            # Play the audio file
            pygame.mixer.init()
            pygame.mixer.music.load(TEMP_AUDIO_FILE)
            pygame.mixer.music.play()
            self.audio_playing = True
            self.paused = False
            self.show_pause_button()  # Show Pause button and ensure Resume is hidden
            self.show_control_buttons()
            self.monitor_audio()

            self.original_audio = AudioSegment.from_file(TEMP_AUDIO_FILE, format="mp3")

            # Close the application after the audio finishes playing
            self.root.after(int(pygame.mixer.Sound(TEMP_AUDIO_FILE).get_length() * 1000), self.root.destroy)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Removed update_speed_label function as slider_value_label and speed_slider are not defined.

    def update_control_frame_widths(self, event=None):
        available_width = self.root.winfo_width() - 20
        half_width = available_width / 2
        new_width = int(half_width * 0.95)
        self.control_frame.grid_columnconfigure(0, minsize=new_width)
        self.control_frame.grid_columnconfigure(1, minsize=new_width)

    def monitor_audio(self):
        try:
            if self.paused:
                self.monitor_id = self.root.after(100, self.monitor_audio)
            elif pygame.mixer.get_init() is not None and pygame.mixer.music.get_busy():
                self.monitor_id = self.root.after(100, self.monitor_audio)
            else:
                self.cleanup_audio()
        except Exception as e:
            print(f"Error in monitor_audio: {e}")
            self.cleanup_audio()

    def cleanup_audio(self):
        try:
            pygame.mixer.quit()
        except Exception:
            pass
        if self.monitor_id is not None:
            try:
                self.root.after_cancel(self.monitor_id)
            except Exception as e:
                print(f"Error canceling monitor: {e}")
            self.monitor_id = None
        if self.audio_filename and os.path.exists(self.audio_filename):
            try:
                os.remove(self.audio_filename)
            except Exception as e:
                print(f"Error deleting audio file: {e}")
            self.audio_filename = None
        self.audio_playing = False
        self.hide_control_buttons()

    def pause_audio(self):
        if self.audio_playing and not self.paused:
            self.pause_pos = pygame.mixer.music.get_pos()  # in milliseconds
            pygame.mixer.music.pause()
            self.paused = True
            self.pause_button.grid_forget()
            self.resume_button.grid(row=0, column=0, padx=5, sticky='ew')
            self.stop_button.grid(row=0, column=1, padx=5, sticky='ew')

    def resume_audio(self):
        if self.audio_playing and self.paused:
            # Revert to original Code 2 behavior for Resume button:
            pygame.mixer.music.unpause()
            self.paused = False
            self.resume_button.grid_forget()
            self.pause_button.grid(row=0, column=0, padx=5, sticky='ew')

    def stop_audio(self):
        if self.audio_playing:
            pygame.mixer.music.stop()
            self.cleanup_audio()
            self.paused = False
            print("File Deleted through 'Stop & Delete' button")

    def show_control_buttons(self):
        self.control_frame.pack(pady=5, fill='x')

    def hide_control_buttons(self):
        self.control_frame.pack_forget()

    def show_pause_button(self):
        self.resume_button.grid_forget()
        if not self.pause_button.winfo_ismapped():
            self.pause_button.grid(row=0, column=0, padx=5, sticky='ew')

    def toggle_theme(self):
        if self.dark_mode:
            self.root.configure(bg="#ecf0f1")
            self.label.configure(bg="#ecf0f1", fg="#2c3e50")
            self.language_label.configure(bg="#ecf0f1", fg="#2c3e50")
            self.speed_static_label.configure(bg="#ecf0f1", fg="#2c3e50")
            self.char_count_label.configure(bg="#ecf0f1", fg="#2c3e50")
            self.theme_button.configure(bg="#2c3e50", fg="white")
            self.dark_mode = False
        else:
            self.root.configure(bg="#2c3e50")
            self.label.configure(bg="#34495e", fg="white")
            self.language_label.configure(bg="#34495e", fg="white")
            self.speed_static_label.configure(bg="#34495e", fg="white")
            self.char_count_label.configure(bg="#34495e", fg="white")
            self.theme_button.configure(bg="#f39c12", fg="white")
            self.dark_mode = True

    def on_closing(self):
        try:
            if self.audio_playing:
                pygame.mixer.music.stop()
        except Exception as e:
            print("Error stopping audio during close:", e)
        try:
            if os.path.exists(TEMP_AUDIO_FILE):
                os.remove(TEMP_AUDIO_FILE)
                print("Temp file deleted on window close.")
        except Exception as e:
            print("Error deleting temp file on close:", e)
        self.root.destroy()

if __name__ == "__main__":
    # Get the input text from the command
    input_text = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"Received input text: {input_text}")

    if not input_text:
        print("Error: No input text provided.")
        sys.exit(1)

    """
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
    """
    try:
        print("Starting text-to-speech conversion...")
        tts = gTTS(text=input_text, lang="en")
        tts.save(TEMP_AUDIO_FILE)
        print("Audio file created:", TEMP_AUDIO_FILE)

        # Play the audio file
        pygame.mixer.init()
        pygame.mixer.music.load(TEMP_AUDIO_FILE)
        pygame.mixer.music.play()
        print("Playing audio...")

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            continue

        print("Text-to-speech process completed successfully.")
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")
        sys.exit(1)
