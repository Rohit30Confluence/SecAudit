from analyzers import process_monitor
from utils.logger import log_event

def main():
    print("[+] SecAudit initialized...")
    log_event("SecAudit started")
    process_monitor.scan_processes()
    print("[+] Scanning completed. Check outputs/logs.csv")

if __name__ == "__main__":
    main()
