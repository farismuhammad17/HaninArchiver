import sys
from pathlib import Path

from Hanin import HaninArchiver

def main():
    root, save_dupes_folder, save_7z_name, is_logging, no_rem_empty_files, no_rem_dupes, no_convert_img, no_convert_vid, no_zip, view_dupes = get_args()

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
    args = sys.argv[1:]

    if args[0].lower() == "docs":
        docs()
        quit()

    if len(args) < 1:
        raise AttributeError("Usage: python HaninArchiver <args> | For documentation: python HaninArchiver docs")

    target_dir = args[args.index("-dir") + 1]
    root = Path(target_dir)

    if not root.is_dir():
        raise NotADirectoryError(f"Error: {target_dir} is not a valid directory.")

    if "-save-to" in args:
        save_dupes_folder = args[args.index("-save-to") + 1]
    else:
        save_dupes_folder = None

    if "-zip" in args:
        save_7z_name = args[args.index("-zip") + 1]
    else:
        save_7z_name = "hanin_archive.7z"

    is_logging = "--no-log" not in args
    if not is_logging:
        args.remove("--no-log")

    no_rem_empty_files = "--no-rem-empty-files" in args
    if no_rem_empty_files:
        args.remove("--no-rem-empty-files")

    no_rem_dupes = "--no-rem-dupes" in args
    if no_rem_dupes:
        args.remove("--no-rem-dupes")

    no_convert_img = "--no-convert-img" in args
    if no_convert_img:
        args.remove("--no-convert-img")

    no_convert_vid = "--no-convert-vid" in args
    if no_convert_vid:
        args.remove("--no-convert-vid")

    no_zip = "--no-zip" in args
    if no_zip:
        args.remove("--no-zip")

    view_dupes = "--view-dupes" in args
    if view_dupes:
        args.remove("--view-dupes")

    for arg in args:
        if arg[0] == '-':
            print(f"Unidentified argument: {arg}")

    return root, save_dupes_folder, save_7z_name, is_logging, no_rem_empty_files, no_rem_dupes, no_convert_img, no_convert_vid, no_zip, view_dupes

def docs():
    print("python HaninArchiver <args>")
    print("Valid args:")
    print("\t* -dir: Directory to archive")
    print("\t* -save-to: Folder to save duplicates to")
    print("\t* -zip: Name of the 7z files you want to compress to")
    print("\t* - --no-log: To disable logging everything being done")
    print("\t* - --no-rem-empty-files: Disable removal of empty files")
    print("\t* - --no-rem-dupes: Disable removal of duplicates")
    print("\t* - --no-convert-img: Disable image conversion to .webp")
    print("\t* - --no-convert-vid: Disable video conversion to .mp4")
    print("\t* - --no-zip: Disable compressing to .7z")
    print("\t* - --view-dupes: View each dupe in a window")

main()
