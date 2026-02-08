import shutil
import os
from pathlib import Path

class HaninRemover:
    def rem_dupes(self, save_to=None):
        if not self.dupes: return

        if save_to is None:
            self.log(f"Deleting {len(self.dupes)} duplicates...", "warn")
            if input("Enter 'confirm' to continue (anything else cancels) > ").lower() != "confirm":
                return

            self.perm_del()

        else:
            dest_root = Path(os.getcwd()) / save_to
            dest_root.mkdir(parents=True, exist_ok=True)

            self.log(f"Moving {len(self.dupes)} duplicates to {dest_root}")
            self.temp_del(dest_root)

    def perm_del(self):
        for _, path in self.dupes:
            try:
                path.unlink()
                self.log(f"Deleted {path}")
            except OSError as e:
                self.log(f"Error deleting {path}: {e}", "err")

    def temp_del(self, dest_root):
        for _, path in self.dupes:
            try:
                relative_path = path.relative_to(self.root)
                new_path = dest_root / relative_path

                new_path.parent.mkdir(parents=True, exist_ok=True)

                shutil.move(str(path), str(new_path))
                self.log(f"Moved {path}")
            except Exception as e:
                self.log(f"Error moving {path}: {e}", "err")
