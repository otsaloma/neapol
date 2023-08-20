# -*- coding: utf-8-unix -*-

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

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk

class Row(GObject.Object):

    def __init__(self, *values):
        super().__init__()
        self.values = values

class View(Gtk.ColumnView):

    COLUMNS = ["#", "Start", "End", "Dur.", "Text"]

    def __init__(self):
        model = Gtk.MultiSelection(model=Gio.ListStore())
        GObject.GObject.__init__(self, model=model)
        self.add_css_class("neapol-view")
        self.set_enable_rubberband(True)
        self.set_reorderable(False)
        self.set_show_column_separators(True)
        self.set_show_row_separators(True)
        self.set_single_click_activate(False)
        self.init_columns()

    def init_columns(self):
        for i, title in enumerate(self.COLUMNS):
            factory = Gtk.SignalListItemFactory()
            factory.connect("setup", self.on_list_item_setup, title)
            factory.connect("bind", self.on_list_item_bind, i)
            column = Gtk.ColumnViewColumn(title=title, factory=factory)
            column.set_resizable(False)
            self.append_column(column)

    def on_list_item_setup(self, factory, item, title):
        label = Gtk.Label()
        label.set_selectable(False)
        if title == "Text":
            label.set_halign(Gtk.Align.START)
            label.set_valign(Gtk.Align.START)
            label.set_single_line_mode(False)
        else:
            label.set_halign(Gtk.Align.END)
            label.set_valign(Gtk.Align.START)
            label.set_single_line_mode(True)
        item.set_child(label)

    def on_list_item_bind(self, factory, item, i):
        label = item.get_child()
        value = item.get_item().values[i]
        label.set_label(value)

    def append(self, *subtitles):
        model = self.get_model().get_model()
        n = model.props.n_items
        for i, subtitle in enumerate(subtitles):
            model.append(Row(str(n+i+1),
                             subtitle.start.to_string(),
                             subtitle.end.to_string(),
                             f"{subtitle.duration:.3f}",
                             subtitle.text))
