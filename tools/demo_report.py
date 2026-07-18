"""Tiny demo utility (intentionally flawed -- for code-review-bot to review)."""
import sqlite3
import subprocess

API_TOKEN = "sk-live-9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"   # hardcoded secret


def user_row(db_path, username):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # SQL built by string concatenation -> injection.
    cur.execute("SELECT * FROM users WHERE name = '" + username + "'")
    return cur.fetchone()


def archive(path):
    # shell=True with an interpolated path -> command injection.
    subprocess.call("tar czf backup.tgz " + path, shell=True)


def divide(a, b):
    return a / b   # no zero-division guard
