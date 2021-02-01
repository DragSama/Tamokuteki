# Copyright (C) 2020-2021 DragSama. All rights reserved. Source code available under the AGPL.
#
# This file is part of TamokutekiBot.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from TamokutekiBot import NO_LOAD, SUDO_USERS

from telethon import TelegramClient
import aiohttp
import re
import logging
from pathlib import Path
import importlib.util as importlib

def check_event(event):
    if event.sender.is_self:
        event.send = event.edit
    else:
        event.send = event.reply
    return True

class TamokutekiClient(TelegramClient):
    """Custom Telethon client with extra attributes."""

    def __init__(self, *args, **kwargs) -> None:
        """Start client and import plugins."""
        self.__plugins__ = {}
        super().__init__(*args, **kwargs)
        self.aio_session = aiohttp.ClientSession()
        self.failed_plugins = {}
        core_plugin = Path(__file__).parent / "core.py"
        help_plugin = Path(__file__).parent / "help.py"
        self.load_plugin(core_plugin)
        self.load_plugin(help_plugin)
        for plugin in Path(__file__).parent.glob(f"plugins/*.py"):
            if Path(plugin).stem in NO_LOAD:
                continue
            self.load_plugin(plugin)
        logging.info("Loaded all plugins.")

    def load_plugin(self, path) -> None:
        """Load plugin from given path."""

        path = Path(path)
        stem = path.stem
        try:
            spec = importlib.spec_from_file_location(stem, path)
            module = importlib.module_from_spec(spec)
            module.Tamokuteki = self
            module.session = self.aio_session
            spec.loader.exec_module(module)
            if hasattr(module, "__type__") and module.__type__ == "IGNORE":
                return
            self.__plugins__[stem] = module
            logging.info(f"Loaded plugin {stem}")
        except Exception as e:
            self.failed_plugins[stem] = e
            logging.error(f"Failed to load plugin{stem}\n{e}")

    def unload_plugin(self, plugin: str) -> None:
        """Unload plugin."""
        if plugin in ["core", "help"]:
            return False
        try:
            name = self.__plugins__[plugin].__name__
        except KeyError:
            return False
        for i in reversed(range(len(self._event_builders))):
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

    def command(self, pattern, outgoing=True, allow_sudo=True):
        def _command(func):
            if allow_sudo:
                return self.on(events.NewMessage(
                    pattern=re.compile(f"^\.{pattern}( .*)?$"), outgoing=outgoing, func=check_event
                ))
            return self.on(events.NewMessage(
                pattern=re.compile(f"^\.{pattern}( .*)?$"), outgoing=outgoing
            ))
        return _command
