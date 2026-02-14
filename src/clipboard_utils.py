import time
import platform
import threading
import pyperclip
from pynput.keyboard import Key, Controller

# Initialize keyboard controller
keyboard = Controller()

def capture_selection(timeout=0.5):
    """
    Captures the currently selected text by manipulating the clipboard.
    
    1. Saves the current clipboard content.
    2. Clears the clipboard (to ensure we detect a new copy).
    3. Simulates the copy shortcut.
    4. Waits for the clipboard to populate.
    5. Restores the original clipboard if nothing was selected.
    """
    # 1. Save current clipboard
    try:
        temp_backup = pyperclip.paste()
    except Exception:
        temp_backup = ""

    # 2. Clear clipboard to detect new copy action
    try:
        pyperclip.copy("")
    except Exception:
        pass

    # 3. Simulate Copy
    # Determine OS modifier
    system = platform.system()
    if system == "Darwin":
        modifier = Key.cmd
    else:
        modifier = Key.ctrl

    # Small sleep to ensure the OS registers the key down if previously executing something
    time.sleep(0.05) 
    
    # Use pynput to simulate the hotkey
    with keyboard.pressed(modifier):
        keyboard.press('c')
        keyboard.release('c')
    
    # 4. Wait for clipboard to update
    start_time = time.time()
    captured_text = ""
    
    while time.time() - start_time < timeout:
        try:
            current_content = pyperclip.paste()
            if current_content != "":
                captured_text = current_content
                break
        except Exception:
            pass
        time.sleep(0.05) # Check every 50ms

    # 5. Handle result
    if captured_text:
        return captured_text
    else:
        # Timeout occurred (likely nothing selected)
        # Restore the original clipboard
        if temp_backup:
            pyperclip.copy(temp_backup)
        return ""

def paste_text(text):
    """
    Pastes the given text at the current cursor location.
    """
    pyperclip.copy(text)
    system = platform.system()
    if system == "Darwin":
        modifier = Key.cmd
    else:
        modifier = Key.ctrl
    
    with keyboard.pressed(modifier):
        keyboard.press('v')
        keyboard.release('v')
