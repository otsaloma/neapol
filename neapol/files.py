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

import neapol
import re

from pathlib import Path

class SubRip:

    TIME_LINE_PATTERN = (r"^(-?\d{1,2}:\d{1,2}:\d{1,2},\d{1,3}) -->"
                         r" (-?\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})")

    @classmethod
    def read(self, path, encoding="utf-8"):
        matches_time = lambda x: re.match(self.TIME_LINE_PATTERN, x)
        lines = path.read_text(encoding).splitlines()
        for i in list(range(len(lines))):
            if matches_time(lines[i]):
                # Remove numbers and blank lines above them.
                if lines[i-1].strip().isdigit():
                    lines[i-1] = None
                    if not lines[i-2].strip():
                        lines[i-2] = None
        lines = list(filter(None, lines))
        for i in range(len(lines)):
            if match := matches_time(lines[i]):
                start, end = match.groups()
                subtitle = neapol.Subtitle(start, end)
                for j in range(i+1, len(lines)):
                    if matches_time(lines[j]): break
                    if subtitle.text:
                        subtitle.text += "\n"
                    subtitle.text += lines[j]
                yield subtitle

def read(path):
    path = Path(path)
    if path.suffix == ".srt":
        return list(SubRip.read(path))
    raise NotImplementedError
