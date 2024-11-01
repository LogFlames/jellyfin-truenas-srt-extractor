import time
import watchdog

from os import path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

dirname = path.dirname(__file__)
watching = path.join(dirname, "..", "watching")

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        print(event)

event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, watching, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()
