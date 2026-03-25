# SkyrimTalker
Overlay tool that displays LLM-generated NPC dialogue in real time from logs when in-game rendering fails (Skyrim CHIM integration).
This tool displays LLM-generated NPC dialogue in real time when in-game rendering fails.

## Background

In CHIM (a system where LLM generates NPC dialogue and behavior in real time), dialogue may not appear due to TTS timeout or processing errors.

This tool solves that problem by reading log output and overlaying dialogue directly on the screen.

## Features

- Real-time log monitoring
- JSON parsing of LLM output
- Overlay display using PySide6
- Duplicate message filtering

## Tech Stack

- Python
- PySide6 (GUI)
- JSON parsing
- Log monitoring

## Usage

1. Set log file path in the script
2. Run:

```bash
python skyrimtalker.py
