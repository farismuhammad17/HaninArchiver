from unzipper import HaninUnzipper
from cleanup import HaninCleaner
from sizer import HaninSizer
from hasher import HaninHasher
from byte_checker import HaninByteChecker
from remover import HaninRemover
from zipper import HaninZipper
from converter import HaninConverter

from logger import HaninLogger
from view_dupes import HaninViewer

class HaninArchiver(
    HaninUnzipper,
    HaninCleaner,
    HaninSizer,
    HaninHasher,
    HaninByteChecker,
    HaninRemover,
    HaninZipper,
    HaninConverter,

    HaninLogger,
    HaninViewer
):
    def __init__(self, root, is_logging=False):
        self.root       = root
        self.is_logging = is_logging

        self.logger = None

        self.JUNK_FILES = {
            '.DS_Store',    # macOS folder attributes
            '.localized',   # macOS localization
            'Thumbs.db',    # Windows thumbnail cache
            'desktop.ini',  # Windows folder customization
        }

        self.same_sized = None
        self.hash_dupes = None
        self.dupes      = None

        if is_logging:
            self.setup_logger()

    def archive(self,
        save_dupes_to="dupes",
        save_7z_name="hanin_archive.7z",
        no_rem_empty_files=False,
        no_rem_dupes=False,
        no_convert_img=False,
        no_convert_vid=False,
        no_zip=False,
        view_dupes=False
    ):
        if not no_rem_empty_files:
            self.clean_empty_files(save_dupes_to)

        if not no_rem_dupes:
            self.verify_so()

            self.unzip_all_zip()
            self.cleanup_junk()
            self.get_same_sized()
            self.get_hash_dupes()
            self.get_dupes()

            if view_dupes:
                self.view_dupes()

            self.rem_dupes(save_dupes_to)

        if not no_convert_img:
            self.convert_images()

        if not no_convert_vid:
            self.convert_videos()

        if not no_zip:
            self.zip7z(save_7z_name)

        self.log("Task finished")
