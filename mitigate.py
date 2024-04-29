import subprocess
import psutil

def terminate_processes(pattern):
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info['cmdline'] and any(pattern in cmd for cmd in proc.info['cmdline']):
            proc.terminate()
            print(f"Terminated suspicious process {proc.info['name']} with PID {proc.pid}")
