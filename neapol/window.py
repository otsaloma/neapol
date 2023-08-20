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

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

class Window(Gtk.Window):

    def __init__(self):
        GObject.GObject.__init__(self)
        self.notebook = Gtk.Notebook()
        self.set_default_size(700, 600)
        label = Gtk.Label()
        label.set_justify(Gtk.Justification.CENTER)
        label.set_markup("<b>Neapol</b>")
        header = Gtk.HeaderBar(title_widget=label)
        self.set_titlebar(header)
        self.set_child(self.notebook)
        controller = Gtk.EventControllerKey()
        controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        self.add_controller(controller)
        controller.connect("key-pressed", self.on_key_pressed)
        self.load_css()

    def load_css(self):
        css = (neapol.DATA_DIR / "neapol.css").read_text("utf-8")
        style = self.get_style_context()
        display = Gdk.Display.get_default()
        provider = Gtk.CssProvider()
        try:
            # The call signature of 'load_from_data' seems to have changed
            # in some GTK version. Also, the whole function is deprecated
            # and since GTK 4.12 we should use 'load_from_string'.
            provider.load_from_data(css, -1)
        except Exception:
            provider.load_from_data(bytes(css.encode()))
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        style.add_provider_for_display(display, provider, priority)

    def on_key_pressed(self, event_controller_key, keyval, keycode, state, user_data=None):
        if keyval == Gdk.KEY_Escape:
            self.close()
            return True
        control = state & Gdk.ModifierType.CONTROL_MASK
        if control and keyval in [Gdk.KEY_w, Gdk.KEY_q]:
            if self.notebook.get_n_pages() > 1:
                page = self.notebook.get_current_page()
                self.notebook.remove_page(page)
                return True
            self.close()
            return True

    def open(self, path, encoding="utf-8"):
        subtitles = neapol.files.read(path, encoding)
        view = neapol.View()
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroller.set_child(view)
        title = path.name
        if len(title) > 16:
            title = title[:16] + "..."
        label = Gtk.Label.new(title)
        self.notebook.append_page(scroller, label)
        view.append(*subtitles)
