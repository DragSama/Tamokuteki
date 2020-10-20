from telethon import TelegramClient

import logging
from pathlib import Path
import importlib.util as importlib

class TamokutekiClient(TelegramClient):
    """Custom Telethon client with extra attributes."""

    def __init__(self, *args, **kwargs) -> None:
        """Start client and import plugins."""
        self.__plugins__ = {}
        super().__init__(*args, **kwargs)

        core_plugin =  Path(__file__).parent / "core.py"
        help_plugin = Path(__file__).parent / "help.py"
        self.load_plugin(core_plugin)
        self.load_plugin(help_plugin)

        for plugin in Path(__file__).parent.glob(f"plugins/*.py"):
            self.load_plugin(plugin)
        logging.info("Loaded all plugins.")

    def load_plugin(self, path) -> None:
        """Load plugin from given path."""

        path = Path(path)
        stem = path.stem
        spec = importlib.spec_from_file_location(stem, path)
        module = importlib.module_from_spec(spec)
        module.Tamokuteki = self
        spec.loader.exec_module(module)
        self.__plugins__[stem] = module
        logging.info(f"Loaded plugin {stem}")

    def unload_plugin(self, plugin: str) -> None:
        """Unload plugin."""

        try:
            name = self.__plugins__[plugin].__name__
        except KeyError:
            return False
        for i in range(len(self._event_builders)):
            ev, cb = self._event_builders[i]
            if cb.__module__ == name:
                del self._event_builders[i]

        del self.__plugins__[name]
        logging.info(f"Removed plugin {name}")

    def list_plugins(self) -> list:
        """List all plugins that are loaded."""

        return list(self.__plugins__.keys())

    def get_plugin(self, plugin: str):
        return self.__plugins__.get(plugin, None)
