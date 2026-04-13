## Python AI Agent

Compact Python AI agent inspired by Boot.dev's "Building an AI Agent" course. This toy project mimics a Claude/Gemini style CLI for learning and experimentation.

Quick start:
1. Clone the repo 
2. python -m venv .venv
3. uv install -r requirements.txt
4. python main.py


You should add your .env with your own API key like shown in .env.example 

How it works:

The agent parses prompts, selects helper functions in the functions package, executes them, and composes replies. Minimal file-based memory enables simple tool chaining.

It has calculator as an example to explore its usage. 

From the course: 

> Run your agent and ask it, "Fix the bug: 3 + 7 * 2 shouldn't be 20."


