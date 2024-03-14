import logging
import pathlib
from dataclasses import dataclass
from datetime import datetime

from .utils import ConsoleFormatter, DebugFilter


@dataclass
class ItakelloLogging:

    debug_mode: bool
    logs_folder: pathlib.Path

    def __init__(self, debug: bool = False) -> None:
        self.debug_mode = debug
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.logs_folder = pathlib.Path("logs") / current_time
        self.logs_folder.mkdir(exist_ok=True, parents=True)
        handlers = self._get_handlers()
        logging.basicConfig(level=logging.DEBUG, handlers=handlers, force=True)

    def _get_handlers(self) -> list[logging.Handler]:
        handlers = [
            self._get_stream_handler(),
            self._get_main_file_handler(),
            self._get_debug_file_handler(),
        ]
        return handlers

    def _get_stream_handler(self) -> logging.StreamHandler:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        console_formatter = ConsoleFormatter(
            "%(asctime)s - %(filename)s - %(message)s", "%H:%M:%S"
        )
        stream_handler.setFormatter(console_formatter)
        return stream_handler

    def _get_debug_file_handler(self) -> logging.FileHandler:
        debug_file_handler = logging.FileHandler(self.logs_folder / "debug.log")
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.addFilter(DebugFilter())
        debug_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        return debug_file_handler

    def _get_main_file_handler(self) -> logging.FileHandler:
        main_file_handler = logging.FileHandler(self.logs_folder / "main.log")
        main_file_handler.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)
        main_file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
            )
        )
        return main_file_handler
