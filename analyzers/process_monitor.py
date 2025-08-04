import psutil
from utils.logger import log_event

SUSPICIOUS_PATHS = ["/tmp", "/dev", "/var/tmp", "/run/shm"]

def is_suspicious_process(proc):
    try:
        exe_path = proc.exe()
        if any(path in exe_path for path in SUSPICIOUS_PATHS):
            return True, "Executed from suspicious path"
        if proc.status() == psutil.STATUS_ZOMBIE:
            return True, "Zombie process"
        if proc.ppid() == 1 and proc.pid > 1000:
            return True, "Orphaned process (parent is init)"
        if proc.cpu_percent(interval=0.1) > 70:
            return True, "High CPU usage"
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False, None
    return False, None

def scan_processes():
    print("[*] Scanning processes...")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            suspicious, reason = is_suspicious_process(proc)
            if suspicious:
                log_event(f"Suspicious process detected: PID={proc.pid}, Name={proc.name()}, Reason={reason}")
        except Exception as e:
            log_event(f"Error scanning process {proc.pid}: {str(e)}")
