import time
import watchdog

from os import path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

dirname = path.dirname(__file__)
watching = path.join(dirname, "..", "watching")

active_files = {}

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        srcpath = event.src_path
        if type(srcpath) is not str:
            srcpath = srcpath.decode("utf-8") 

        if not event.src_path.endswith(".mkv"):
            return

        if event.event_type == "modified":
            active_files[srcpath] = time.time()

event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, watching, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
        for file in active_files:
            if time.time() - active_files[file] > 10:
                del active_files[file]
                print(file)
finally:
    observer.stop()
    observer.join()
