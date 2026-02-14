print("Main starting...")
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info("Main script starting...")

import time
import threading
from pynput import keyboard
from clipboard_utils import capture_selection, paste_text

class CtrlAIApp:
    def __init__(self):
        logging.info("Initializing App")
        self.running = True
        self.listener = None

    def on_commander(self):
        logging.info("[Commander] Triggered (Ctrl+Space)")
        print("[Commander] Triggered (Ctrl+Space)")
        # For Step 1/2, just test capture
        text = capture_selection()
        if text:
            print(f"[Commander] Captured: '{text}'")
            # Logic: Input bar -> Process -> Paste
            # This is deferred to UI step
        else:
            print("[Commander] No text selected or capture failed.")

    def on_refactor(self):
        logging.info("[Refactor] Triggered (Ctrl+Shift+H)")
        print("[Refactor] Triggered (Ctrl+Shift+H)")
        # 1. Grab text
        text = capture_selection()
        if not text:
            logging.warning("[Refactor] No text selected.")
            print("[Refactor] No text selected.")
            return

        logging.info(f"[Refactor] Processing text: '{text}'")
        print(f"[Refactor] Processing text: '{text}'")

        # 2. Send to LLM (Mock)
        # "Ghost Mode" - processing in background
        threading.Thread(target=self.process_refactor, args=(text,)).start()

    def process_refactor(self, text):
        # Mock processing
        logging.info("[Refactor] Sending to AI...")
        print("[Refactor] Sending to AI...")
        time.sleep(1) # Simulate API delay
        fixed_text = f"[Refactored] {text}"
        
        # 3. Auto-paste
        logging.info("[Refactor] Pasting result...")
        print("[Refactor] Pasting result...")
        paste_text(fixed_text)
        logging.info("[Refactor] Done.")
        print("[Refactor] Done.")

    def on_redactor(self):
        logging.info("[Redactor] Triggered (Ctrl+Shift+D)")
        print("[Redactor] Triggered (Ctrl+Shift+D)")
        text = capture_selection()
        if not text:
            logging.warning("[Redactor] No text selected.")
            print("[Redactor] No text selected.")
            return
            
        logging.info(f"[Redactor] Processing text: '{text}'")
        print(f"[Redactor] Processing text: '{text}'")
        threading.Thread(target=self.process_redactor, args=(text,)).start()

    def process_redactor(self, text):
        logging.info("[Redactor] Sanitizing...")
        print("[Redactor] Sanitizing...")
        time.sleep(1)
        redacted_text = f"[Redacted] {text}"
        logging.info("[Redactor] Pasting result...")
        print("[Redactor] Pasting result...")
        paste_text(redacted_text)
        logging.info("[Redactor] Done.")
        print("[Redactor] Done.")

    def start(self):
        # Define hotkeys
        # pynput format: <modifier>+<key>
        hotkeys = {
            '<ctrl>+<space>': self.on_commander,
            '<ctrl>+<shift>+h': self.on_refactor,
            '<ctrl>+<shift>+d': self.on_redactor
        }

        logging.info("Starting Ctrl+AI Listener...")
        print("Starting Ctrl+AI Listener...")
        print("Hotkeys:")
        print("  Commander: Ctrl+Space")
        print("  Refactor:  Ctrl+Shift+H")
        print("  Redactor:  Ctrl+Shift+D")
        print("Press Ctrl+C in this terminal to exit.")

        with keyboard.GlobalHotKeys(hotkeys) as self.listener:
            try:
                self.listener.join()
            except Exception as e:
                logging.error(f"Listener execution error: {e}")
                print(f"Listener error: {e}")

if __name__ == "__main__":
    app = CtrlAIApp()
    try:
        app.start()
    except KeyboardInterrupt:
        print("\nStopping...")
