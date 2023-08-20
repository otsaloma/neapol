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

class Time(float): # s

    @classmethod
    def from_hms(cls, h, m, s):
        return cls(h*3600 + m*60 + s)

    @classmethod
    def from_string(cls, value):
        h, m, s = value.split(":")
        return cls.from_hms(int(h),
                            int(m),
                            float(s.replace(",", ".")))

    @classmethod
    def new(cls, value):
        if isinstance(value, str):
            return cls.from_string(value)
        if isinstance(value, tuple):
            return cls.from_hms(*value)
        return cls(value)

    def to_string(self):
        sign = "-" if self < 0 else ""
        h = self // 3600
        m = (self % 3600) // 60
        s = (self % 60)
        return f"{sign}{h:02.0f}:{m:02.0f}:{s:06.3f}"

class Subtitle:

    def __init__(self, start, end, text=""):
        self.start = Time.new(start)
        self.end = Time.new(end)
        self.text = text or ""

    def __str__(self):
        start = self.start.to_string()
        text = self.text.replace("\n", "|")
        return f"{start}: {text}"

    @property
    def duration(self):
        return Time(self.end - self.start)
