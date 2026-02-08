import logging
from datetime import datetime

class HaninLogger:
    def setup_logger(self):
        log_filename = datetime.now().strftime("hanin_log_%Y%m%d_%H%M%S.log")

        self.logger = logging.getLogger("HaninArchiver")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info("Logger initialized.")

    def log(self, message, msg_type="info"):
        if not self.is_logging: return

        if msg_type == "info":
            self.logger.info(message)
        elif msg_type == "warn":
            self.logger.warning(message)
        elif msg_type == "err":
            self.logger.error(message)

        # DEV_REM
        else:
            raise Exception(f"Invalid logger type: {msg_type}")
