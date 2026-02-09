import sys
import argparse
from pathlib import Path

from Hanin import HaninArchiver

CLR_CONVERSION = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37
}

def clr(text: str, colour: str, bg: bool = False):
    "Formats the text for a specific colour"

    if not colour: return text

    bright = colour.startswith('br')
    colour = colour.removeprefix('br')

    out = CLR_CONVERSION[colour]
    out = out + (10 if bg and not bright else 0)
    out = out + (60 if not bg and bright else 0)
    out = out + (70 if bg and bright else 0)

    return f"\033[{out}m{text}\033[0m"

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "docs":
        docs()
        return

    arguments = get_args()
    verify_args(arguments)

    root, save_dupes_folder, save_7z_name, is_logging, no_rem_empty_files, no_rem_dupes, no_convert_img, no_convert_vid, no_zip, view_dupes = arguments

    HaninArchiver(root, is_logging=is_logging).archive(
        save_dupes_to=save_dupes_folder,
        save_7z_name=save_7z_name,
        no_rem_empty_files=no_rem_empty_files,
        no_rem_dupes=no_rem_dupes,
        no_convert_img=no_convert_img,
        no_convert_vid=no_convert_vid,
        no_zip=no_zip,
        view_dupes=view_dupes
    )

def get_args():
    parser = argparse.ArgumentParser(description="HaninArchiver")

    parser.add_argument("-dir", required=True, help="Target directory to archive")

    parser.add_argument("-save-to", default=None, help="Folder to save duplicates")
    parser.add_argument("-zip", default="hanin_archive.7z", help="Name of the final zip")

    parser.add_argument("--no-log", action='store_false', dest='is_logging', help="Disable logging")
    parser.add_argument("--no-rem-empty-files", action='store_true')
    parser.add_argument("--no-rem-dupes", action='store_true')
    parser.add_argument("--no-convert-img", action='store_true')
    parser.add_argument("--no-convert-vid", action='store_true')
    parser.add_argument("--no-zip", action='store_true')
    parser.add_argument("--view-dupes", action='store_true')

    args = parser.parse_args()

    root = Path(args.dir)
    if not root.is_dir():
        raise NotADirectoryError(f"Error: {args.dir} is not a valid directory.")

    return (root, args.save_to, args.zip, args.is_logging,
            args.no_rem_empty_files, args.no_rem_dupes,
            args.no_convert_img, args.no_convert_vid,
            args.no_zip, args.view_dupes)

def verify_args(arguments):
    root, save_dupes_folder, save_7z_name, is_logging, no_rem_empty_files, no_rem_dupes, no_convert_img, no_convert_vid, no_zip, view_dupes = arguments

    def status(val):
        return clr("ENABLED", "green") if val else clr("DISABLED", "red")

    print(clr("\n--- Hanin configuration ---", "cyan"))
    print(f"Folder: {clr(str(root), 'yellow')}")
    print(f"Duplicates: {clr(save_dupes_folder, 'blue') if save_dupes_folder else clr('Delete Permanently', 'brred')}")
    print(f"7z file: {clr(save_7z_name, 'yellow')}")
    print(f"Logging: {status(is_logging)}")
    print(f"Remove empty files: {status(not no_rem_empty_files)}")
    print(f"Remove duplicates: {status(not no_rem_dupes)}")
    print(f"Convert images: {status(not no_convert_img)}")
    print(f"Convert videos: {status(not no_convert_vid)}")
    print(f"Zip final archive: {status(not no_zip)}")
    print(f"GUI Dupe Viewer: {status(view_dupes)}")
    print(clr("---------------------------", "cyan"))

    try:
        input(f"\nPress {clr('ENTER', 'brgreen')} to start ({clr('CTRL+C', 'red')} to terminate) ")
    except KeyboardInterrupt:
        print(clr("\n\nOperation aborted", "yellow"))
        sys.exit(0)

def docs():
    DOCS = {
        "-dir": "Directory to archive",
        "-save-to": "Folder to save duplicates to",
        "-zip": "Name of the 7z files you want to compress to",
        "--no-log": "To disable logging everything being done",
        "--no-rem-empty-files": "Disable removal of empty files",
        "--no-rem-dupes": "Disable removal of duplicates",
        "--no-convert-img": "Disable image conversion to .webp",
        "--no-convert-vid": "Disable video conversion to .mp4",
        "--no-zip": "Disable compressing to .7z",
        "--view-dupes": "View each dupe in a window"
    }

    print(f"{clr('Usage', 'green')}: python HaninArchiver <args>")
    print("Valid args:")

    for doc_name, doc_desc in DOCS.items():
        print(f"\t* {clr(doc_name, 'magenta')}: {doc_desc}")

main()
