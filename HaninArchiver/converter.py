import shutil
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

class HaninConverter:
    def convert_images(self):
        extensions = {'.png', '.jpg', '.jpeg', '.jfif', '.bmp', '.tiff'}

        all_image_paths = [
            path for path in self.root.rglob('*')
            if path.is_file()
            and path.suffix.lower() in extensions
            and not path.name.startswith('._')
        ]

        total_files = len(all_image_paths)
        if total_files == 0:
            self.log("No images found to convert")
            return

        self.log(f"Converting {len(all_image_paths)} images to .webp")

        processed_count = 0
        lock = threading.Lock()

        def process_single_image(path):
            nonlocal processed_count

            try:
                with Image.open(path) as img:
                    info = img.info
                    new_path = path.with_suffix('.webp')

                    if path.suffix.lower() == '.png':
                        img.save(new_path, 'webp', lossless=True, **info)
                    else:
                        img.save(new_path, 'webp', quality=95, **info)

                path.unlink()
                self.log(f"Converted: {path} -> {new_path.name}")

            except Exception as e:
                print()
                self.log(f"Could not convert {path.name}: {e}", "err")

            finally:
                with lock:
                    processed_count += 1
                    print(f"\rConverted: {processed_count}/{total_files} images ", end="", flush=True)

        with ThreadPoolExecutor() as executor:
            executor.map(process_single_image, all_image_paths)

        print()
        self.log("Image conversion complete")

    def convert_videos(self):
        if not self.check_ffmpeg():
            self.log("Unable to convert videos (Could not locate FFMPEG)", "warn")
            return

        extensions = {'.avi', '.mov', '.mkv', '.wmv', '.mpg', '.mpeg'}

        all_video_paths = [
            path for path in self.root.rglob('*')
            if path.is_file()
            and path.suffix.lower() in extensions
            and not path.name.startswith('._')
        ]

        total_files = len(all_video_paths)
        if total_files == 0:
            self.log("No videos found to convert")
            return

        self.log(f"Optimizing {total_files} videos using HEVC (H.265)")

        processed_count = 0
        for path in all_video_paths:
            try:
                new_path = path.with_suffix('.mp4')

                if new_path.exists():
                    processed_count += 1
                    continue

                cmd = [
                    'ffmpeg', '-i', str(path),
                    '-c:v', 'libx265', '-crf', '28',
                    '-c:a', 'aac', '-map_metadata', '0',
                    str(new_path), '-y', '-loglevel', 'quiet'
                ]

                subprocess.run(cmd, check=True)

                path.unlink()
                self.log(f"Optimized: {path} -> {new_path.name}")

            except Exception as e:
                print()
                self.log(f"Could not convert {path.name}: {e}", "err")

            finally:
                processed_count += 1
                print(f"\rOptimized: {processed_count}/{total_files} videos ", end="", flush=True)

        print()
        self.log("Video optimization complete")

    def check_ffmpeg(self):
        ffmpeg_path = shutil.which("ffmpeg")

        if ffmpeg_path is None:
            return False

        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, OSError):
            return False
