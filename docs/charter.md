Project Charter: Ctrl+AI
Mission: Eliminate the "Alt-Tab Tax" of using AI.
Tagline: "Don't go to the AI. Bring the AI to your cursor."

1. The Problem & The Pivot (Why this matters)
The Problem: Current AI workflows are disjointed. Copying text, switching windows, pasting into ChatGPT, and copying back breaks the user's "flow state."
The Assumption to Attack: "AI must be a destination (a website or app)."
The Solution: AI as a utility layer over the OS. A background service that injects intelligence into any text field (VS Code, Slack, Google Docs, Notion).

2. The "MVP" Scope (The Non-Negotiables)
To win, you must demo these three features perfectly. Cut everything else.
Feature
The "Ctrl+Hack+Del" Hook
Functionality
1. The Commander
CTRL (Control)
Trigger: Cmd+Space (or custom).

Action: Opens a spotlight-bar. User types instruction ("Make this professional").

Result: Text is replaced in-place.
2. The Refactor
HACK (Modify)
Trigger: Cmd+Shift+H.

Action: Detects code/text. Sends to LLM with "Fix/Optimize" prompt.

Result: Returns cleaned code or corrected grammar.
3. The Redactor
DEL (Delete)
Trigger: Cmd+Shift+D.

Action: Identifies PII (Personal Identifiable Information) or "fluff."

Result: Returns a sanitized or summarized version.

Out of Scope (Do Not Build):
Complex User Authentication (Hardcode a demo key or use a local .env).
Chat History (This is transactional, not conversational).
Cross-Platform Support (Pick ONE OS: Windows or macOS. Trying to do both in 36 hours is a death sentence for system-level tools).

3. The Technical Stack (Optimized for Speed)
Core Logic: Python (It has the best libraries for this).
pynput or keyboard: For global hotkey listening.
pyperclip: For hijacking the clipboard (Copy/Paste).
tkinter or PyQt: For the overlay UI (keep it minimal).
AI Engine: Groq API (Recommended over OpenAI for the demo).
Why: Groq is near-instant. In a live demo, waiting 3 seconds for GPT-4 looks like a bug. Groq returns text in milliseconds.
Packaging: PyInstaller (To turn your script into an .exe or .app for the judges).

4. The 36-Hour Battle Plan
Phase 1: The "Skeleton" (Hours 0–6)
Goal: A script that detects a keypress, copies selected text to the clipboard, prints it to the console, and pastes a hardcoded string back.
Critical Check: If you can't get permission to control the clipboard/keyboard on your laptop by Hour 4, PIVOT. Switch to a Chrome Extension immediately.
Phase 2: The "Brain" (Hours 6–18)
Goal: Connect the skeleton to the API.
Task: Write the prompt engineering.
Challenge: The LLM will be chatty ("Here is your fixed code..."). You need to write a parser that strips everything except the raw output so the paste function works cleanly.
Phase 3: The "Face" (Hours 18–30)
Goal: Build the UI Overlay.
Task: Instead of just pasting, pop up a small "Loading..." spinner near the mouse cursor. Visual feedback is crucial.
Polish: Add a "Diff View" (Show Original vs. AI Version) if time permits.
Phase 4: The "Pitch" (Hours 30–36)
Goal: Rehearse the demo.
Task: Create a "Demo Script" document. Do not type live queries. Have a text file ready with specific, pre-tested examples (e.g., a broken JSON block, a rude email draft) that you know the AI handles perfectly.

5. Roles & Responsibilities
Member 1 (The System Architect):
Owns the keyboard / clipboard loop.
Battles OS permissions (Accessibility Access on Mac, Defender on Windows).
Ensures the app doesn't crash when no text is selected.
Member 2 (The Prompt Engineer):
Writes the system prompts for the 3 modes (Ctrl, Hack, Del).
Tests the API with edge cases (code vs. text).
Implements the "Groq" or "OpenAI" client.
Member 3 (The Frontend/Pitch):
Designs the floating UI (must look modern, not like a Windows 95 app).
Builds the slide deck.
Crucial: Records a backup video of the tool working (in case the live demo fails).

Sparring Partner Review (Potential Weaknesses)
The "Malware" Vibe: A background app that logs keystrokes and reads clipboards is functionally identical to a keylogger.
Defense: Be upfront about this in the pitch. "We run locally. We only send data when the hotkey is triggered. Privacy by design."
The "Hallucination" Risk: If the AI hallucinates while refactoring code, it breaks the user's trust instantly.
Defense: Add a "Review" step in the UI before it pastes back over the user's work.
