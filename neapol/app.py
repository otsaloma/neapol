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

import neapol

from argparse import ArgumentParser
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk
from pathlib import Path

class Application(Gtk.Application):

    def __init__(self, args):
        GObject.GObject.__init__(self)
        self.window = None
        self.set_application_id("io.otsaloma.neapol")
        self.set_flags(Gio.ApplicationFlags.NON_UNIQUE)
        self.connect("activate", self.on_activate, args)

    def on_activate(self, app, args):
        args = self.parse_arguments(args)
        self.window = neapol.Window()
        self.add_window(self.window)
        self.window.set_visible(True)
        for path in args.paths:
            self.window.open(path)

    def parse_arguments(self, args):
        parser = ArgumentParser(usage="neapol [OPTION...] [FILE...]")
        parser.add_argument("files",
                            metavar="FILE...",
                            nargs="*",
                            default=[],
                            help="subtitle files to open")

        parser.add_argument("--version",
                            action="version",
                            version=f"neapol {neapol.__version__}")

        args = parser.parse_args()
        args.paths = [Path(x) for x in args.files]
        return args
