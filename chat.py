#!/usr/bin/env python3
"""
Neon ChatGPT Terminal - Dinindu Vishwajith
"""

import os
import io
import asyncio

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import HSplit, Layout
from prompt_toolkit.widgets import TextArea, Frame, Label
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import ANSI, to_formatted_text
from prompt_toolkit.lexers.base import Lexer

from rich.console import Console
from rich.markdown import Markdown


# ANSI Escape Lexer (CORRECT IMPLEMENTATION)
class AnsiEscapeLexer(Lexer):
    def lex_document(self, document):
        lines = document.text.splitlines()

        def get_line(lineno):
            if lineno >= len(lines):
                return []
            # Convert ANSI -> fragment list (REQUIRED)
            return to_formatted_text(ANSI(lines[lineno]))

        return get_line


# OpenAI API
chatContent = []

def call_chat(prompt, model):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        chatContent.append({
            "role": "user",
            "content": prompt,
            "promptID": len(chatContent) + 1
        })

        resp = client.chat.completions.create(
            model=model,
            messages=chatContent,
        )
        return resp.choices[0].message.content

    except Exception as err:
        return f"OpenAI error: {err}"


# ANSI Theme
NEON_RED   = "\x1b[38;2;255;60;60m"
NEON_GREEN = "\x1b[38;2;0;255;140m"
NEON_BLUE  = "\x1b[38;2;0;210;255m"
NEON_PINK  = "\x1b[38;2;255;0;200m"
DIM        = "\x1b[2m"
RESET      = "\x1b[0m"



# Markdown to ANSI
def md_to_ansi(text: str) -> str:
    buf = io.StringIO()
    Console(
        file=buf,
        force_terminal=True,
        color_system="truecolor",
        width=100,
    ).print(Markdown(text, code_theme="monokai"))
    return buf.getvalue()


# Output Area (Scrollable + ANSI-rendered)
output_area = TextArea(
    text="",
    lexer=AnsiEscapeLexer(),
    read_only=False,
    wrap_lines=True,
    scrollbar=True,
    focusable=True,
)

def append_output(ansi_text: str):
    buf = output_area.buffer
    buf.insert_text(ansi_text)
    buf.cursor_down(count=10**6)
    get_app().invalidate()


# Input Area
input_area = TextArea(
    height=5,
    prompt=ANSI(f"{NEON_RED}●{RESET} "),
    multiline=True,
    wrap_lines=True,
)



# UI Elements
title = Label(
    ANSI(
        f"{NEON_BLUE}➤ {NEON_PINK}ChatGPT Terminal{RESET} "
        f"{DIM}Enter=Send • Alt+Enter=New line • Ctrl+C=Quit{RESET}"
    )
)

status = Label(ANSI(f"{NEON_GREEN}Status:{RESET} Ready"))

layout = Layout(
    HSplit([
        Frame(title),
        Frame(output_area, title=ANSI(f"{NEON_PINK}➤ [Response]{RESET}")),
        Frame(input_area, title=ANSI(f"{NEON_RED}➤ [Prompt]{RESET}")),
        status,
    ])
)


# Key Bindings
kb = KeyBindings()

@kb.add("enter")
def submit(event):
    event.app.create_background_task(handle_send())

@kb.add("escape", "enter")
def newline(event):
    input_area.buffer.insert_text("\n")

@kb.add("c-c")
def quit_(event):
    event.app.exit()


# Chat Logic
async def handle_send():
    prompt = input_area.text.strip()
    if not prompt:
        return

    input_area.text = ""

    append_output(
        f"\n{NEON_GREEN}➤ [You]:{RESET} {prompt}\n"
    )

    status.text = ANSI(f"{NEON_GREEN}Status:{RESET} Thinking…")

    loop = asyncio.get_running_loop()
    model = os.getenv("CHAT_MODEL", "gpt-4o-mini")

    response = await loop.run_in_executor(
        None, call_chat, prompt, model
    )

    append_output(
        f"{NEON_PINK}{'─'*60}{RESET}\n"
        f"{md_to_ansi(response)}\n"
        f"{NEON_PINK}{'─'*60}{RESET}\n"
    )

    status.text = ANSI(f"{NEON_GREEN}Status:{RESET} Ready")
    get_app().layout.focus(input_area)


# App
style = Style.from_dict({
    "frame.border": "#00ffff",
})

app = Application(
    layout=layout,
    key_bindings=kb,
    style=style,
    full_screen=True,
    mouse_support=True,
)

if __name__ == "__main__":
    app.run(pre_run=lambda: get_app().layout.focus(input_area))
