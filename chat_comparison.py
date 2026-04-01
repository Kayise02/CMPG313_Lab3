"""
Chat Comparison GUI — ELIZA vs LLM
CMPG 313 Lab: AI The Past and the Present

Side-by-side comparison of rule-based AI (ELIZA) and a modern LLM.
"""

import threading
import tkinter as tk
from tkinter import scrolledtext

from eliza import get_eliza_response
from LLM import get_llm_response


class ChatComparisonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Past vs Present AI — ELIZA vs LLM")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0f172a")
        self.build_ui()

    # ─────────────────────────────────────────
    # UI construction
    # ─────────────────────────────────────────
    def build_ui(self):
        # Title
        tk.Label(
            self.root,
            text="AI Comparison Lab: ELIZA vs LLM",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#0f172a",
        ).pack(pady=(15, 3))

        tk.Label(
            self.root,
            text="Compare rule-based AI and modern generative AI side by side",
            font=("Segoe UI", 11),
            fg="#cbd5e1",
            bg="#0f172a",
        ).pack(pady=(0, 12))

        # Chat panels
        top_frame = tk.Frame(self.root, bg="#0f172a")
        top_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.eliza_frame = tk.Frame(top_frame, bg="#1e293b")
        self.eliza_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.llm_frame = tk.Frame(top_frame, bg="#1e293b")
        self.llm_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

        # ELIZA panel
        tk.Label(
            self.eliza_frame,
            text="🕰  ELIZA  (Rule-Based — Past AI)",
            font=("Segoe UI", 14, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(pady=8)

        self.eliza_chat = self._make_textbox(self.eliza_frame)
        self._append(self.eliza_chat, "ELIZA ready. Type a message below.\n")

        # LLM panel
        tk.Label(
            self.llm_frame,
            text="🤖  LLM  (Qwen2.5 — Present AI)",
            font=("Segoe UI", 14, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(pady=8)

        self.llm_chat = self._make_textbox(self.llm_frame)
        self._append(self.llm_chat, "LLM ready. Type a message below.\n")

        # Input area
        bottom = tk.Frame(self.root, bg="#0f172a")
        bottom.pack(fill="x", padx=20, pady=(4, 18))

        tk.Label(
            bottom,
            text="Your message:",
            font=("Segoe UI", 10),
            fg="#cbd5e1",
            bg="#0f172a",
        ).pack(anchor="w", pady=(0, 4))

        self.input_box = tk.Entry(
            bottom,
            font=("Segoe UI", 13),
            bg="#1e293b",
            fg="white",
            insertbackground="white",
            relief="flat",
        )
        self.input_box.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.input_box.bind("<Return>", self.send_message)
        self.input_box.focus_set()

        tk.Button(
            bottom,
            text="Compare ▶",
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            command=self.send_message,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            bottom,
            text="Clear",
            font=("Segoe UI", 12, "bold"),
            bg="#475569",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            command=self.clear_chats,
        ).pack(side="left")

    def _make_textbox(self, parent):
        box = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#0b1220",
            fg="#e2e8f0",
            insertbackground="white",
            relief="flat",
            padx=10,
            pady=10,
        )
        box.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        box.config(state="disabled")
        return box

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────
    def _append(self, widget, text):
        widget.config(state="normal")
        widget.insert(tk.END, text + "\n")
        widget.see(tk.END)
        widget.config(state="disabled")

    # ─────────────────────────────────────────
    # Message handling
    # ─────────────────────────────────────────
    def send_message(self, event=None):
        user_text = self.input_box.get().strip()
        if not user_text:
            return
        self.input_box.delete(0, tk.END)

        self._append(self.eliza_chat, f"You: {user_text}")
        self._append(self.llm_chat,   f"You: {user_text}")

        # ELIZA — synchronous (instant)
        eliza_reply = get_eliza_response(user_text)
        self._append(self.eliza_chat, f"ELIZA: {eliza_reply}")

        # LLM — run in background thread to keep GUI responsive
        self._append(self.llm_chat, "LLM: ⏳ Thinking…")
        threading.Thread(
            target=self._llm_worker,
            args=(user_text,),
            daemon=True,
        ).start()

    def _llm_worker(self, user_text):
        try:
            reply = get_llm_response(user_text)
        except Exception as exc:
            reply = f"[Error: {exc}]"
        self.root.after(0, self._replace_thinking, reply)

    def _replace_thinking(self, new_text):
        self.llm_chat.config(state="normal")
        content = self.llm_chat.get("1.0", tk.END).rstrip()
        marker = "LLM: ⏳ Thinking…"
        if content.endswith(marker):
            content = content[: -len(marker)].rstrip()
        self.llm_chat.delete("1.0", tk.END)
        self.llm_chat.insert(tk.END, content + "\n\n")
        self.llm_chat.insert(tk.END, f"LLM: {new_text}\n\n")
        self.llm_chat.see(tk.END)
        self.llm_chat.config(state="disabled")

    def clear_chats(self):
        for widget, starter in [
            (self.eliza_chat, "ELIZA ready. Type a message below.\n"),
            (self.llm_chat,   "LLM ready. Type a message below.\n"),
        ]:
            widget.config(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, starter)
            widget.config(state="disabled")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    ChatComparisonGUI(root)
    root.mainloop()
