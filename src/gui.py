import customtkinter as ctk
import threading
import time

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class OverlayApp(ctk.CTk):
    def __init__(self, submit_callback=None):
        super().__init__()

        self.submit_callback = submit_callback
        
        # Configure window
        self.title("Ctrl+AI Commander")
        self.geometry("600x60")
        
        # Make the window frameless
        self.overrideredirect(True)
        
        # Make it stay on top
        self.attributes('-topmost', True)
        self.resizable(False, False)

        # Center the window on the screen
        self.center_window()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Input Frame
        self.input_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e1e")
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Icon/Label (Left)
        self.label = ctk.CTkLabel(self.input_frame, text="✨ AI", font=("Arial", 14, "bold"), width=40)
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Entry Field
        self.entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Type a command (e.g., 'Fix grammar', 'Make professional')...",
            border_width=0,
            fg_color="transparent",
            font=("Arial", 14)
        )
        self.entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.entry.bind("<Return>", self.on_submit)
        self.entry.bind("<Escape>", self.hide_overlay)
        
        # Close on focus loss (optional, good for spotlight feel)
        # self.bind("<FocusOut>", self.hide_overlay)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 600
        height = 60
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 3) - (height // 2) # Slightly above center
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_overlay(self):
        self.deiconify()
        self.attributes('-topmost', True)
        self.entry.focus_set()
        self.entry.delete(0, 'end')

    def hide_overlay(self, event=None):
        self.withdraw()

    def on_submit(self, event=None):
        text = self.entry.get()
        if text and self.submit_callback:
            # Run callback in a separate thread if needed, or just call it. 
            # Ideally, the callback initiates the AI process.
            # We hide immediately to indicate action.
            self.hide_overlay()
            self.submit_callback(text)

    def start(self):
        self.withdraw() # Start hidden
        self.mainloop()

    def show_toast(self, message="Processing...", duration=None):
        """Displays a small toast notification near the center of the screen."""
        toast = ProcessingToast(self, message)
        if duration:
            self.after(int(duration * 1000), toast.destroy)
        return toast

class ProcessingToast(ctk.CTkToplevel):
    def __init__(self, master, message="Processing..."):
        super().__init__(master)
        
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        
        # Style
        self.configure(fg_color="#1e1e1e")
        
        # Content
        label = ctk.CTkLabel(self, text=f"⏳ {message}", font=("Arial", 12), text_color="white")
        label.pack(padx=20, pady=10)
        
        # Position (Center of screen for simplicity)
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) + 100 # Slightly below center
        self.geometry(f"+{x}+{y}")
        
    def hide(self):
        self.destroy()

# Test the UI standalone
if __name__ == "__main__":
    def mock_submit(text):
        print(f"Submitted: {text}")

    app = OverlayApp(submit_callback=mock_submit)
    # Simulate a trigger after 2 seconds
    def trigger():
        time.sleep(2)
        print("Showing overlay")
        app.show_overlay()
        
        time.sleep(2)
        print("Showing toast")
        # Use .after to run in main thread
        app.after(0, lambda: app.show_toast("Refactoring...", duration=2))
    
    threading.Thread(target=trigger).start()
    app.start()
