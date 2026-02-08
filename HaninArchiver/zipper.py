import py7zr

class HaninZipper:
    def zip7z(self, archive_name):
        """Compresses the cleaned root directory into a 7z file."""

        if not archive_name.endswith('.7z'):
            archive_name += '.7z'

        self.logger.info(f"Starting 7z compression: {archive_name}")

        try:
            with py7zr.SevenZipFile(archive_name, mode='w') as z:
                z.writeall(self.root, arcname=self.root.name)

            self.logger.info(f"Successfully zipped into {archive_name}")

        except Exception as e:
            self.logger.error(f"Failed to create 7z archive: {e}")
            raise
