import zipfile

class HaninUnzipper:
    def unzip_all_zip(self):
        zip_files = list(self.root.rglob('*.zip'))

        self.log(f"Unzipping {len(zip_files)} ZIP files")

        for zip_path in zip_files:
            base_name = f"{zip_path.stem}_extracted"
            extract_path = zip_path.with_name(base_name)

            i = 2
            while extract_path.exists():
                extract_path = zip_path.with_name(f"{base_name}_{i}")
                i += 1

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                zip_path.unlink()

                self.log(f"Unzipped {zip_path}")
            except zipfile.BadZipFile:
                self.log(f"{zip_path} is corrupt.", "warn")

        self.log("Unzipping complete")
