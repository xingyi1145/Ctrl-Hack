# Project Charter: Ctrl+AI v2.0

**Mission**: Eliminate the "Alt-Tab Tax" of using AI.  
**Tagline**: "Don't go to the AI. Bring the AI to your cursor."

## 1. The Problem & The Pivot (Why this matters)

**The Problem**: Current AI workflows are disjointed. Copying text, switching windows, pasting into ChatGPT, and copying back breaks the user's "flow state."  
**The Assumption to Attack**: "AI must be a destination (a website or app)."  
**The Solution**: AI as a utility layer over the OS. A background service that injects intelligence into any text field.

### The v2.0 Pivot
We shifted from "Ghost Mode" automation to "Human-in-the-Loop" interaction to build trust and prevent hallucinations. Earlier versions blindly accepted AI edits, which proved dangerous. We replaced blind automation with:
- **Diff Views**: A safety mechanism to review changes before applying them.
- **Active Inquiry**: A way to ask questions without modifying the source text.

## 2. Scope & Features

### Core Features (v2.0)

#### 1. The Commander
- **Trigger**: `Ctrl+Space`
- **Action**: Opens a spotlight-bar. User types instruction ("Make this professional").
- **Safety**: Result is shown in a **Diff Window**. User must click "Accept" to apply changes.

#### 2. The Analyst (Interactive Explain)
- **Trigger**: `Ctrl+Alt+E`
- **Action**: Active Inquiry. Select code or text and ask questions (e.g., "What does this Regex do?").
- **Result**: Displays analysis in a read-only insight window.

### Deprecated Features [DEPRECATED]
- **The Refactor (Ghost Mode)**: Removed due to safety concerns (blindly modifying code).
- **The Redactor (Ghost Mode)**: Removed due to lack of user control.

### Out of Scope (Do Not Build)
- Complex User Authentication (Hardcode a demo key or use a local .env).
- Chat History (This is transactional, not conversational).
- Cross-Platform Support (Focus on Windows for the Hackathon).

## 3. The Technical Stack (Optimized for Speed)

- **Core Logic**: Python (It has the best libraries for this).
- **GUI**: `customtkinter` (Modern UI), `tk` (Clipboard hooks).
- **AI Engine**: Google Gemini 2.5 Flash / Groq API.
- **Packaging**: `PyInstaller` (To turn your script into an .exe).

## 4. Roadmap

- [x] **Phase 1: Basic Hook** (Global Hotkey -> Hello World)
- [x] **Phase 2: The "Ghost" MVP** (Text Selection -> OpenAI -> Paste)
- [x] **Phase 3: The Pivot (v2.0)** (Diff View, Interactive Explain, Safety First)
- [ ] **Phase 4: Polish & Packaging** (Installer, EXE, README)
- [ ] **Phase 5: Public Release** (GitHub Releases)
