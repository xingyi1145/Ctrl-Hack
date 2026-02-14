import customtkinter as ctk
import pyperclip
import threading
import time

# Set appearance mode and default color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Design Tokens ---
_BG_DEEP       = "#1a1a1a"
_BG_CARD       = "#2b2b2b"
_BG_HEADER     = "#202020"
_BG_INPUT      = "#1e1e1e"
_TEXT           = "#ececec"
_TEXT_DIM       = "#a0a0a0"
_ACCENT_BLUE   = "#3b8ed0"
_ACCENT_PURPLE  = "#9d46ff"
_ACCENT_RED    = "#e06060"
_ACCENT_GREEN  = "#60e060"
_BORDER_RED    = "#5c3a3a"
_BORDER_GREEN  = "#3a5c3a"
_FONT_BODY     = ("Segoe UI", 14)
_FONT_BODY_SM  = ("Segoe UI", 13)
_FONT_HEADER   = ("Segoe UI", 14, "bold")
_FONT_CODE     = ("Consolas", 13)
_FONT_INPUT    = ("Segoe UI", 16)
_FONT_LABEL    = ("Segoe UI", 15, "bold")
_FONT_BTN      = ("Segoe UI", 13, "bold")


class OverlayApp(ctk.CTk):
    def __init__(self, submit_callback=None):
        super().__init__()

        self.submit_callback = submit_callback
        self.history = []
        self.history_index = -1

        # Configure window
        self.title("Ctrl+AI Commander")
        self.geometry("640x70")

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
        self.input_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=_BG_INPUT,
                                        border_width=1, border_color="#333333")
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Icon/Label (Left)
        self.label = ctk.CTkLabel(self.input_frame, text="\u2728 AI", font=_FONT_LABEL,
                                  text_color=_ACCENT_BLUE, width=50)
        self.label.grid(row=0, column=0, padx=(14, 6), pady=14)

        # Entry Field
        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type a command (e.g., 'Fix grammar', 'Make professional')...",
            border_width=0,
            fg_color="transparent",
            text_color=_TEXT,
            font=_FONT_INPUT,
        )
        self.entry.grid(row=0, column=1, sticky="ew", padx=5, pady=14)
        self.entry.bind("<Return>", self.on_submit)
        self.entry.bind("<Escape>", self.hide_overlay)
        self.entry.bind("<Up>", self._history_up)
        self.entry.bind("<Down>", self._history_down)

        # Mode Badge (Right)
        self.mode_badge = ctk.CTkLabel(self.input_frame, text="CMD", font=("Segoe UI", 11, "bold"),
                                       text_color="#ffffff", fg_color=_ACCENT_BLUE,
                                       corner_radius=6, width=48, height=24)
        self.mode_badge.grid(row=0, column=2, padx=(4, 14), pady=14)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 640
        height = 70
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 3) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_overlay(self):
        self.deiconify()
        self.attributes('-topmost', True)
        self.lift()
        self.focus_force()
        self.entry.focus_set()
        self.entry.delete(0, 'end')
        self.history_index = -1

    def hide_overlay(self, event=None):
        self.withdraw()

    def on_submit(self, event=None):
        text = self.entry.get()
        if text and self.submit_callback:
            if not self.history or self.history[-1] != text:
                self.history.append(text)
            self.history_index = -1
            self.hide_overlay()
            self.submit_callback(text)

    def _history_up(self, event=None):
        if not self.history:
            return "break"
        if self.history_index == -1:
            self.history_index = len(self.history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        self.entry.delete(0, "end")
        self.entry.insert(0, self.history[self.history_index])
        return "break"

    def _history_down(self, event=None):
        if not self.history or self.history_index == -1:
            return "break"
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.entry.delete(0, "end")
            self.entry.insert(0, self.history[self.history_index])
        else:
            self.history_index = -1
            self.entry.delete(0, "end")
        return "break"

    def start(self):
        self.withdraw()
        self.mainloop()

    def show_toast(self, message="Processing...", duration=None):
        """Displays a small toast notification near the center of the screen."""
        toast = ProcessingToast(self, message)
        if duration:
            self.after(int(duration * 1000), toast.destroy)
        return toast

    def show_diff(self, original_text, new_text, on_accept_callback):
        """Opens the DiffWindow for human review before pasting."""
        DiffWindow(self, original_text, new_text, on_accept_callback)

    def show_explanation(self, content):
        """Opens the ExplanationWindow to display AI explanation (read-only)."""
        ExplanationWindow(self, content)

    def configure_mode(self, mode_name):
        """Switch the overlay appearance between 'commander' and 'explain' modes."""
        if mode_name == "explain":
            self.label.configure(text="\u2753 Ask", text_color=_ACCENT_PURPLE)
            self.entry.configure(placeholder_text="What do you want to know about this text?")
            self.mode_badge.configure(text="ASK", fg_color=_ACCENT_PURPLE)
        else:
            self.label.configure(text="\u2728 AI", text_color=_ACCENT_BLUE)
            self.entry.configure(placeholder_text="Type a command (e.g., 'Fix grammar', 'Make professional')...")
            self.mode_badge.configure(text="CMD", fg_color=_ACCENT_BLUE)


# ===========================================================================
#  DiffWindow - Side-by-side review
# ===========================================================================
class DiffWindow(ctk.CTkToplevel):
    """Human-in-the-loop review window showing original vs AI proposal side-by-side."""

    def __init__(self, master, original_text, new_text, on_accept_callback=None):
        super().__init__(master)

        self.on_accept_callback = on_accept_callback

        # --- Window setup ---
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(fg_color=_BG_DEEP)

        width, height = 860, 460
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # --- Header bar ---
        header = ctk.CTkFrame(self, height=40, fg_color=_BG_HEADER, corner_radius=0)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)
        title_label = ctk.CTkLabel(header, text="\U0001f50d  Review Changes",
                                   font=_FONT_HEADER, text_color=_TEXT)
        title_label.pack(side="left", padx=16, pady=8)

        # Dragging
        header.bind("<Button-1>", self._start_drag)
        header.bind("<B1-Motion>", self._on_drag)
        title_label.bind("<Button-1>", self._start_drag)
        title_label.bind("<B1-Motion>", self._on_drag)

        # --- Grid weights ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Left panel: Original ---
        left_frame = ctk.CTkFrame(self, fg_color=_BG_DEEP, border_width=2,
                                  border_color=_BORDER_RED, corner_radius=10)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        left_label = ctk.CTkLabel(left_frame, text="Original Text",
                                  font=_FONT_HEADER, text_color=_ACCENT_RED)
        left_label.grid(row=0, column=0, padx=14, pady=(10, 4), sticky="w")

        self.original_box = ctk.CTkTextbox(left_frame, fg_color=_BG_CARD, text_color=_TEXT,
                                           font=_FONT_BODY, wrap="word", corner_radius=8,
                                           border_width=0, spacing1=5)
        self.original_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.original_box.insert("1.0", original_text)
        self.original_box.configure(state="disabled")

        # --- Right panel: AI Proposal (editable) ---
        right_frame = ctk.CTkFrame(self, fg_color=_BG_DEEP, border_width=2,
                                   border_color=_BORDER_GREEN, corner_radius=10)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        right_label = ctk.CTkLabel(right_frame, text="AI Proposal  (editable)",
                                   font=_FONT_HEADER, text_color=_ACCENT_GREEN)
        right_label.grid(row=0, column=0, padx=14, pady=(10, 4), sticky="w")

        self.proposal_box = ctk.CTkTextbox(right_frame, fg_color=_BG_CARD, text_color=_TEXT,
                                           font=_FONT_BODY, wrap="word", corner_radius=8,
                                           border_width=0, spacing1=5)
        self.proposal_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.proposal_box.insert("1.0", new_text)

        # --- Bottom button bar ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(0, 12))

        reject_btn = ctk.CTkButton(btn_frame, text="\u2718  Reject (Esc)", width=170, height=36,
                                   fg_color="#4a2020", hover_color="#6a3030",
                                   text_color="#ff9090", font=_FONT_BTN,
                                   corner_radius=8, command=self._reject)
        reject_btn.pack(side="left", padx=10)

        accept_btn = ctk.CTkButton(btn_frame, text="\u2714  Accept (Enter)", width=170, height=36,
                                   fg_color="#204a20", hover_color="#306a30",
                                   text_color="#90ff90", font=_FONT_BTN,
                                   corner_radius=8, command=self._accept)
        accept_btn.pack(side="left", padx=10)

        # --- Key bindings ---
        self.bind("<Return>", lambda e: self._accept())
        self.bind("<Escape>", lambda e: self._reject())
        self.after(100, self.focus_force)

    # --- Drag support ---
    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag(self, event):
        x = self.winfo_x() + event.x - self._drag_x
        y = self.winfo_y() + event.y - self._drag_y
        self.geometry(f"+{x}+{y}")

    # --- Actions ---
    def _accept(self):
        final_text = self.proposal_box.get("1.0", "end-1c")

        # Hide window and return focus to underlying app
        self.withdraw()
        self.update_idletasks()
        time.sleep(0.2)

        if self.on_accept_callback:
            self.on_accept_callback(final_text)
        self.destroy()

    def _reject(self):
        self.destroy()


# ===========================================================================
#  ExplanationWindow - Read-only AI insight
# ===========================================================================
class ExplanationWindow(ctk.CTkToplevel):
    """Read-only card window displaying the AI's explanation."""

    def __init__(self, master, content):
        super().__init__(master)
        self._content = content

        # --- Window setup ---
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(fg_color=_BG_DEEP)

        width, height = 660, 440
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # --- Header (40px) ---
        header = ctk.CTkFrame(self, height=40, fg_color=_BG_HEADER, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)
        title_label = ctk.CTkLabel(header, text="\U0001f4a1  AI Insight",
                                   font=_FONT_HEADER, text_color=_TEXT)
        title_label.pack(side="left", padx=16, pady=8)

        # Dragging
        header.bind("<Button-1>", self._start_drag)
        header.bind("<B1-Motion>", self._on_drag)
        title_label.bind("<Button-1>", self._start_drag)
        title_label.bind("<B1-Motion>", self._on_drag)

        # --- Grid ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Body card ---
        body_card = ctk.CTkFrame(self, fg_color=_BG_DEEP, border_width=2,
                                 border_color="#3a4a6a", corner_radius=10)
        body_card.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        body_card.grid_rowconfigure(0, weight=1)
        body_card.grid_columnconfigure(0, weight=1)

        self.text_box = ctk.CTkTextbox(body_card, fg_color=_BG_CARD, text_color=_TEXT,
                                       font=_FONT_BODY, wrap="word", corner_radius=8,
                                       border_width=0, spacing1=5)
        self.text_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.text_box.insert("1.0", content)
        self.text_box.configure(state="disabled")

        # --- Footer buttons ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(0, 12))

        copy_btn = ctk.CTkButton(btn_frame, text="\U0001f4cb  Copy", width=140, height=36,
                                 fg_color=_ACCENT_BLUE, hover_color="#2d7abc",
                                 text_color="#ffffff", font=_FONT_BTN,
                                 corner_radius=8, command=self._copy)
        copy_btn.pack(side="left", padx=10)

        done_btn = ctk.CTkButton(btn_frame, text="\u2714  Done (Esc)", width=140, height=36,
                                 fg_color="#333333", hover_color="#444444",
                                 text_color=_TEXT_DIM, font=_FONT_BTN,
                                 corner_radius=8, command=self.destroy)
        done_btn.pack(side="left", padx=10)

        # --- Key binding ---
        self.bind("<Escape>", lambda e: self.destroy())
        self.after(100, self.focus_force)

    # --- Copy ---
    def _copy(self):
        try:
            pyperclip.copy(self._content)
        except Exception:
            pass

    # --- Drag support ---
    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag(self, event):
        x = self.winfo_x() + event.x - self._drag_x
        y = self.winfo_y() + event.y - self._drag_y
        self.geometry(f"+{x}+{y}")


# ===========================================================================
#  ProcessingToast
# ===========================================================================
class ProcessingToast(ctk.CTkToplevel):
    def __init__(self, master, message="Processing..."):
        super().__init__(master)

        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(fg_color=_BG_INPUT)

        label = ctk.CTkLabel(self, text=f"\u23f3 {message}", font=_FONT_BODY_SM, text_color=_TEXT)
        label.pack(padx=20, pady=10)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) + 100
        self.geometry(f"+{x}+{y}")

    def hide(self):
        self.destroy()


# ===========================================================================
#  Standalone test
# ===========================================================================
if __name__ == "__main__":
    def mock_submit(text):
        print(f"Submitted: {text}")

    app = OverlayApp(submit_callback=mock_submit)

    def trigger():
        time.sleep(2)
        print("Showing overlay")
        app.show_overlay()

        time.sleep(2)
        print("Showing toast")
        app.after(0, lambda: app.show_toast("Processing...", duration=2))

    threading.Thread(target=trigger).start()
    app.start()
