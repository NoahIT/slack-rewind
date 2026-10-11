# 5. Desktop window over loopback browser interface

Status: Accepted

Date: 2026-10-11

## Context

Local tools often ask the user to run a CLI script and navigate their browser to `http://localhost:8000`.

This experience feels technical, fragile, and unpolished for non-technical users. It exposes browser tab clutter, relies on memory of local port numbers, and makes lifecycle management awkward.

## Decision

The primary user interface is a native desktop window (pywebview wrapping a Vite + React UI). Double-clicking the app launches a dedicated window with an intuitive onboarding wizard, run progress indicators, and an accessible briefing document.

Python manages the window process and backend logic. React renders the UI with modern typography, sticky navigation, and WCAG 2.2 AA accessibility standards.

Any local communication server binds strictly to `127.0.0.1` and remains completely hidden from the user.

## Consequences

- The app feels like a standard desktop application.
- Windows is supported first, using the OS-native Edge WebView2 runtime. macOS support follows via WebKit.
- Packaging uses Python tooling (e.g. Briefcase / PyInstaller) without introducing a Rust/Tauri toolchain into the repository.

