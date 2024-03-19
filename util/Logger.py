import logging

class Logger:
    def __init__(self):
        logging.DATA = 15
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        file_handler = logging.FileHandler("./logs/test.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, message: str):
        return self.logger.info(message)
        