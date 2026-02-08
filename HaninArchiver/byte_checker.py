import os
import ctypes
from pathlib import Path

class HaninByteChecker:
    def verify_so(self):
        ext = ".dll" if os.name == 'nt' else ".so"
        lib_path = Path(__file__).parent / "core" / f"byte_checker{ext}"

        if not lib_path.exists():
            raise FileNotFoundError(f"Could not find compiled library at {lib_path}. Did you run 'make'?")

        self._lib = ctypes.CDLL(str(lib_path))

        self._lib.check_if_identical.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self._lib.check_if_identical.restype = ctypes.c_int

    def get_dupes(self):
        self.dupes = []

        total_comparisons = sum(len(paths) - 1 for paths in self.hash_dupes.values())
        completed_count = 0

        self.log(f"C++: Checking {total_comparisons} pairs Byte-by-Byte")

        for file_hash, paths in self.hash_dupes.items():
            original = paths[0]
            orig_bytes = str(original).encode('utf-8')

            for candidate in paths[1:]:
                cand_bytes = str(candidate).encode('utf-8')

                result = self._lib.check_if_identical(orig_bytes, cand_bytes)
                completed_count += 1

                if result == 1:
                    self.dupes.append((original, candidate))
                    self.log(f"Duplicate found: {candidate}")
                elif result == -1:
                    print()
                    self.log(f"Could not open files for comparison: {candidate}", "err")

                print(f"\rChecked: {completed_count}/{total_comparisons} pairs ", end="", flush=True)

        print()
        self.log(f"Found {len(self.dupes)} duplicates.")
