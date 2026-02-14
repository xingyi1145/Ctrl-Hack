print("Main starting...")
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info("Main script starting...")

import time
import threading
from pynput import keyboard
from clipboard_utils import capture_selection, paste_text
from ai_handler import AIHandler

# Try importing GUI; gracefully handle if tkinter is missing (e.g. on headless/some Linux)
try:
    from gui import OverlayApp
    GUI_AVAILABLE = True
except ImportError as e:
    logging.error(f"GUI Import failed: {e}")
    print(f"WARNING: GUI not available ({e}). Commander mode will be disabled.")
    GUI_AVAILABLE = False
    OverlayApp = None

class CtrlAIApp:
    def __init__(self):
        logging.info("Initializing App")
        self.running = True
        self.listener = None
        self.ai = AIHandler()
        self.gui = None
        self.captured_text_for_commander = ""
        self.active_toast = None

        if GUI_AVAILABLE:
            self.gui = OverlayApp(submit_callback=self.on_commander_submit)

    def show_progress(self, message):
        if self.gui:
            self.gui.after(0, lambda: self._gui_show_toast(message))
            
    def _gui_show_toast(self, message):
        if self.active_toast:
            try:
                self.active_toast.hide()
            except: 
                pass
        self.active_toast = self.gui.show_toast(message)
        
    def hide_progress(self):
        if self.gui:
            self.gui.after(0, self._gui_hide_toast)
            
    def _gui_hide_toast(self):
        if self.active_toast:
            try:
                self.active_toast.hide()
            except:
                pass
            self.active_toast = None

    def on_commander(self):
        logging.info("[Commander] Triggered (Ctrl+Space)")
        print("[Commander] Triggered (Ctrl+Space)")
        
        if not self.gui:
            print("Commander mode requires GUI (tkinter missing).")
            return

        # 1. Capture text first (The "Context")
        text = capture_selection()
        if text:
            print(f"[Commander] Context captured: '{text[:20]}...'")
            self.captured_text_for_commander = text
            # 2. Show UI
            # Use `after` to schedule GUI update safely in main thread if possible, 
            # or relying on ctk thread safety. Best practice is `after`.
            # Since self.gui is running in main thread and we are in listener thread:
            self.gui.after(0, self.gui.show_overlay)
        else:
            print("[Commander] No text selected.")

    def on_commander_submit(self, prompt):
        print(f"[Commander] Prompt: {prompt}")
        threading.Thread(target=self.process_commander, args=(prompt,)).start()

    def process_commander(self, prompt):
        logging.info(f"Processing Commander: {prompt}")
        self.show_progress(f"Commander: {prompt}...")
        try:
            result = self.ai.process_text(self.captured_text_for_commander, mode="commander", prompt_instruction=prompt)
            print("[Commander] Pasting result...")
            paste_text(result)
            logging.info("Commander done.")
        finally:
            self.hide_progress()

    def on_refactor(self):
        logging.info("[Refactor] Triggered (Ctrl+Shift+H)")
        print("[Refactor] Triggered (Ctrl+Shift+H)")
        # 1. Grab text
        text = capture_selection()
        if not text:
            logging.warning("[Refactor] No text selected.")
            print("[Refactor] No text selected.")
            # Show a quick failure toast?
            self.show_progress("No text selected")
            threading.Timer(1.0, self.hide_progress).start()
            return

        logging.info(f"[Refactor] Processing text: '{text[:50]}...'")
        print(f"[Refactor] Processing text: '{text[:50]}...'")

        # 2. Send to LLM
        # "Ghost Mode" - processing in background
        threading.Thread(target=self.process_refactor, args=(text,)).start()

    def process_refactor(self, text):
        # Mock processing
        logging.info("[Refactor] Sending to AI...")
        print("[Refactor] Sending to AI...")
        self.show_progress("Refactoring...")
        
        try:
            result = self.ai.process_text(text, mode="refactor")
            
            # 3. Auto-paste
            logging.info("[Refactor] Pasting result...")
            print("[Refactor] Pasting result...")
            paste_text(result)
            logging.info("[Refactor] Done.")
            print("[Refactor] Done.")
        finally:
            self.hide_progress()

    def on_redactor(self):
        logging.info("[Redactor] Triggered (Ctrl+Shift+D)")
        print("[Redactor] Triggered (Ctrl+Shift+D)")
        text = capture_selection()
        if not text:
            logging.warning("[Redactor] No text selected.")
            print("[Redactor] No text selected.")
            self.show_progress("No text selected")
            threading.Timer(1.0, self.hide_progress).start()
            return
            
        logging.info(f"[Redactor] Processing text: '{text[:50]}...'")
        print(f"[Redactor] Processing text: '{text[:50]}...'")
        threading.Thread(target=self.process_redactor, args=(text,)).start()

    def process_redactor(self, text):
        logging.info("[Redactor] Sanitizing...")
        print("[Redactor] Sanitizing...")
        self.show_progress("Redacting...")
        
        try:
            result = self.ai.process_text(text, mode="redactor")
            
            logging.info("[Redactor] Pasting result...")
            print("[Redactor] Pasting result...")
            paste_text(result)
            logging.info("[Redactor] Done.")
            print("[Redactor] Done.")
        finally:
            self.hide_progress()

    def start_listener(self):
        # Define hotkeys
        # pynput format: <modifier>+<key>
        hotkeys = {
            '<ctrl>+<space>': self.on_commander,
            '<ctrl>+<shift>+h': self.on_refactor,
            '<ctrl>+<shift>+d': self.on_redactor
        }
        
        logging.info("Starting Hotkey Listener...")
        # Non-blocking start if we want to join manually, but listener.join() is blocking
        with keyboard.GlobalHotKeys(hotkeys) as self.listener:
            try:
                self.listener.join()
            except Exception as e:
                logging.error(f"Listener execution error: {e}")
                print(f"Listener error: {e}")

    def start(self):
        print("Starting Ctrl+AI...")
        print("Hotkeys:")
        print("  Commander: Ctrl+Space")
        print("  Refactor:  Ctrl+Shift+H")
        print("  Redactor:  Ctrl+Shift+D")
        print("Press Ctrl+C to exit.")

        # Start listener in a separate thread so GUI can run in main thread
        listener_thread = threading.Thread(target=self.start_listener)
        listener_thread.daemon = True
        listener_thread.start()

        if self.gui:
            # Blocks main thread
            try:
                self.gui.start()
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print(f"GUI Error: {e}")
        else:
            # If no GUI, just keep main thread alive or join listener thread
            try:
                listener_thread.join()
            except KeyboardInterrupt:
                print("\nStopping...")

if __name__ == "__main__":
    app = CtrlAIApp()
    try:
        app.start()
    except KeyboardInterrupt:
        print("\nStopping...")
