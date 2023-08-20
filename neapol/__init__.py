# -*- coding: utf-8 -*-

# Copyright (C) 2023 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

__version__ = "0.0"

import gi

gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
gi.require_version("GObject", "2.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Pango", "1.0")

from gi.repository import GLib
from pathlib import Path

CONFIG_HOME = Path(GLib.get_user_config_dir()) / "neapol"
DATA_HOME = Path(GLib.get_user_data_dir()) / "neapol"

# Default to the source directory, overwritten when installing.
DATA_DIR = Path(__file__).parent.parent.joinpath("data").resolve()
LOCALE_DIR = Path(__file__).parent.parent.joinpath("locale").resolve()

from neapol.subtitle import Time # noqa
from neapol.subtitle import Subtitle # noqa
from neapol import files # noqa
from neapol.view import View # noqa
from neapol.window import Window # noqa
from neapol.app import Application # noqa

def main(args):
    global app
    app = Application(args)
    raise SystemExit(app.run())
