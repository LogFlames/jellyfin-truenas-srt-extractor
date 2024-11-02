import glob
from main import process

if __name__ == "__main__":
    files = glob.glob("/home/watching/**/*.mkv", recursive=True)
    for i, file in enumerate(files):
        print(f"{i}/{len(files)}: {file}")
        process(file)


