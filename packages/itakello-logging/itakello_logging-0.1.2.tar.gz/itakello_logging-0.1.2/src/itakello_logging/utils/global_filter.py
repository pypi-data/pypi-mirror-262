import logging


class GlobalFilter(logging.Filter):

    def __init__(self, excluded_modules: list[str]):
        super().__init__()
        self.excluded_modules = excluded_modules

    def filter(self, record: logging.LogRecord) -> bool:
        return not record.filename in self.excluded_modules
