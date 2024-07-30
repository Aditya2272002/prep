import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHandler(PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(patterns=["*.py"])

    def on_modified(self, event):
        print(f"{event.src_path} has been modified")
        run_flask()

def run_flask():
    global p
    if p:
        p.terminate()
    p = subprocess.Popen(["python", "main.py"])

if __name__ == "__main__":
    p = None
    run_flask()
    
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
