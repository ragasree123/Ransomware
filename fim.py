import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

class CustomEventHandler(FileSystemEventHandler):
    """Custom event handler that logs all filesystem changes."""
    def on_modified(self, event):
        super().on_modified(event)
        logging.info(f"File {event.src_path} has been modified")

    def on_created(self, event):
        super().on_created(event)
        logging.info(f"File {event.src_path} has been created")

    def on_deleted(self, event):
        super().on_deleted(event)
        logging.info(f"File {event.src_path} has been deleted")

def monitor_directories(paths):
    logging.basicConfig(filename='fim_log.txt', level=logging.INFO,
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = CustomEventHandler()
    observer = Observer()

    for path in paths:
        observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # List of directories you want to monitor
    paths_to_monitor = ["/home/vboxuser/critical", "/home/vboxuser/critical/lab1", "/home/vboxuser/critical/lab2"]
    monitor_directories(paths_to_monitor)
