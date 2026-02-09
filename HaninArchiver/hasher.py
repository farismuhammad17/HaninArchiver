import xxhash
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

class HaninHasher:
    def get_fast_hash(self, path):
        "Hashes only the first 128KB of a file."

        hasher = xxhash.xxh64()

        try:
            with open(path, 'rb') as f:
                chunk = f.read(131072) # 128 KB
                hasher.update(chunk)
            return hasher.hexdigest()
        except OSError:
            return None

    def get_full_hash(self, path):
        "Hashes the entire file in chunks."

        hasher = xxhash.xxh128()
        try:
            with open(path, 'rb') as f:
                while chunk := f.read(131072):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except OSError:
            return None

    def get_hash_dupes(self):
        self.hash_dupes = defaultdict(list)

        self.log(f"Finding fast hash for {len(self.same_sized)} size groups")

        all_candidate_paths = [p for paths in self.same_sized.values() for p in paths]
        fast_hash_map = defaultdict(list)
        map_lock = threading.Lock()

        completed_count = 0

        def process_fast(path):
            nonlocal completed_count
            f_hash = self.get_fast_hash(path)

            if f_hash:
                try:
                    size = path.stat().st_size
                    with map_lock:
                        fast_hash_map[(size, f_hash)].append(path)
                        completed_count += 1

                    print(f"\rFast hashed: {completed_count}/{len(all_candidate_paths)} files", end="", flush=True)
                except Exception as e:
                    print()
                    self.log(f"Error getting size for {path}: {e}", level="ERROR")

        with ThreadPoolExecutor() as executor:
            executor.map(process_fast, all_candidate_paths)

        candidates_fast = []

        for (size, f_hash), paths in fast_hash_map.items():
            if len(paths) <= 1:
                continue
            elif len(paths) <= 3:
                self.hash_dupes[f"fast_{size}_{f_hash}"].extend(paths)
            else:
                candidates_fast.append(paths)

        print()

        if not candidates_fast:
            self.log("Hashing complete")
            return

        full_hash_lock = threading.Lock()

        all_full_candidates = [p for paths in candidates_fast for p in paths]

        self.log(f"Fast hash completed. Checking full hashes for {len(all_full_candidates)}")

        completed_count = 0

        def process_full(path):
            nonlocal completed_count
            full_hash = self.get_full_hash(path)

            if full_hash:
                with full_hash_lock:
                    self.hash_dupes[full_hash].append(path)
                    completed_count += 1

                print(f"\rHashed: {completed_count}/{len(all_full_candidates)} files", end="", flush=True)

        with ThreadPoolExecutor() as executor:
            executor.map(process_full, all_full_candidates)

        self.hash_dupes = {h: p for h, p in self.hash_dupes.items() if len(p) > 1}

        print()
        self.log(f"Found {len(self.hash_dupes)} hash duplicate groups.")
