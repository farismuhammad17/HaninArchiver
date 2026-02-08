from pathlib import Path

class HaninCleaner:
    def clean_empty_files(self, save_to=None):
        "Finds files with 0 bytes and removes/moves them."

        self.log("Searching for 0-byte files")

        empty_files = []
        for path in self.root.rglob('*'):
            if path.is_file() and path.stat().st_size == 0:
                empty_files.append(path)

        if not empty_files:
            self.log("No empty files found")
            return

        self.log(f"Found {len(empty_files)} empty file(s)")

        for file_path in empty_files:
            try:
                if save_to:
                    dest = Path(save_to) / file_path.relative_to(self.root)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    file_path.replace(dest)
                else:
                    file_path.unlink()
            except Exception as e:
                self.log(f"Failed to handle empty file {file_path}: {e}", "err")

        self.log("Empty file cleanup complete")

    def cleanup_junk(self):
        for path in self.root.rglob('*'):
            if path.is_file() and path.name in self.JUNK_FILES:
                try:
                    path.unlink()
                    self.log(f"Deleted OS Junk {path}")
                except OSError:
                    self.log(f"Could not delete {path}", "warn")

        self.log("OS Junk files cleanup complete")
