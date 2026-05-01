"""
Start server and create public tunnel using npx
"""
import subprocess
import time
import sys
import os

os.chdir(r"C:\Users\MOHAMED\.qwenpaw\workspaces\default\lightline-investment")

print("Starting Flask server...")
flask_process = subprocess.Popen(
    [sys.executable, "app.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print("Waiting for server to start...")
time.sleep(4)

print("Creating public tunnel...")
try:
    lt_process = subprocess.Popen(
        ["npx", "localtunnel", "--port", "5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    for _ in range(15):
        line = lt_process.stdout.readline()
        if line and ("url" in line.lower() or "https" in line):
            print("\n" + "="*50)
            print("YOUR PUBLIC URL IS READY!")
            print("="*50)
            print(line.strip())
            print("="*50)
            break
        time.sleep(1)
    
    print("\nServer running at http://127.0.0.1:5000")
    print("Share the public URL above!")
    print("\nPress Ctrl+C to stop\n")
    
    lt_process.wait()
    
except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    print(f"Error: {e}")
finally:
    flask_process.terminate()
