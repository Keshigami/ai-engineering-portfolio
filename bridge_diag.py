import subprocess
import os

def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return f"COMMAND: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}\nRETURN CODE: {result.returncode}\n"
    except Exception as e:
        return f"COMMAND: {cmd}\nEXCEPTION: {str(e)}\n"

commands = [
    "whoami",
    "pwd",
    "git version",
    "git remote -v",
    "git status",
    "ls -la /Users/keshigami/ai-engineering-portfolio"
]

log_content = ""
for c in commands:
    log_content += run(c) + "\n---\n"

with open("/Users/keshigami/ai-engineering-portfolio/diag_log.txt", "w") as f:
    f.write(log_content)

print("Diagnostic complete.")
