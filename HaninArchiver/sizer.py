from collections import defaultdict

class HaninSizer:
    def get_same_sized(self):
        size_map = defaultdict(list)

        self.log("Finding files of same size")

        for path in self.root.rglob('*'):
            if path.is_file():
                try:
                    file_size = path.stat().st_size
                    size_map[file_size].append(path)

                except OSError:
                    self.log(f"Could not check {path} for size", "err")

        self.same_sized = {size: paths for size, paths in size_map.items() if len(paths) > 1}

        self.log(f"Found files of same size")
