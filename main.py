import time
import subprocess
import os

from os import path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

dirname = path.dirname(__file__)
watching = path.join(dirname, "..", "watching")

SUPPORTED_LANGUAGES = {"eng", "swe", "spa", "nor", "dan", "fin", "fra", "deu", "isl"}

active_files = {}

def process(file):
    file_esc = file.replace("(", "\\(").replace(")", "\\)").replace(" ", "\\ ")
    output = subprocess.run(f'mkvinfo {file_esc}', shell=True, capture_output=True)
    lines = output.stdout.decode("utf-8").splitlines()
    tracks = []
    track = {"id": None, "language": "eng", "type": None}
    for line in lines:
        if line == '| + Track':
            if track["type"] == "subtitles":
                tracks.append(track)
            track = {"id": None, "language": "eng"}
        if line.startswith("|  + Track UID:"):
            track["id"] = int(line.split()[-1]) - 1
        if line.startswith("|  + Track type:"):
            track["type"] = line.split(": ")[-1]
        if line.startswith("|  + Language:"):
            track["language"] = line.split(": ")[-1]

    if track["type"] == "subtitles":
        tracks.append(track)

    subtitles_folder = path.join(path.dirname(file), "extracted_subtitles")
    if not path.exists(subtitles_folder):
        os.mkdir(subtitles_folder)

    target = path.join(path.dirname(file_esc), "extracted_subtitles", path.splitext(path.basename(file_esc))[0])

    for track in tracks:
        target_name = f"{target}_{track['id']}_{track['language']}"
        output = path.join(path.dirname(file_esc), path.splitext(path.basename(file_esc))[0] + "." + track["language"] + ".srt")

        if path.exists(output):
            continue

        print(f"Extracting tracks... {file_esc}")
        subprocess.run(f"mkvextract {file_esc} tracks {track['id']}:{target_name}", shell=True)

        if track["language"] not in SUPPORTED_LANGUAGES:
            print(f"{track['language']} not supported")
            continue

        subprocess.run(f"/root/.cargo/bin/vobsubocr {target_name}.idx --lang {track['language']} -o {output}", shell=True)


class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.event_type not in ("modified", "moved"):
            return

        fpath = event.src_path
        if event.event_type == "moved":
            fpath = event.dest_path

        if type(fpath) is not str:
            fpath = fpath.decode("utf-8") 

        fpath = path.normpath(fpath)

        if not event.src_path.endswith(".mkv"):
            return

        active_files[fpath] = time.time()

if __name__ == "__main__":
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, watching, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            to_clean = set()
            for file in active_files:
                if time.time() - active_files[file] > 10:
                    to_clean.add(file)
                    print(f"Processing: {file}")
                    process(file)

            for file in to_clean:
                del active_files[file]
    finally:
        observer.stop()
        observer.join()
