"""Converts FontDat models back into the binary format used by the game"""
#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

from skytemple_files.common.util import *
from skytemple_files.graphics.fonts import *
from skytemple_files.graphics.fonts.font_dat.model import FontDat


class FontDatWriter:
    def __init__(self, model: FontDat):
        self.model = model

    def write(self) -> bytes:
        buffer = bytearray(FONT_ENTRY_LEN * len(self.model.entries))
        write_uintle(buffer, len(self.model.entries), 0x00, 4)
        
        for i, e in enumerate(self.model.entries):
            off_start = 0x4 + (i * FONT_ENTRY_LEN)
            write_uintle(buffer, e.char, off_start + 0x00)
            write_uintle(buffer, e.table, off_start + 0x01)
            write_uintle(buffer, e.width, off_start + 0x02)
            write_uintle(buffer, e.bprow, off_start + 0x03)
            buffer[off_start + 0x04:off_start + FONT_ENTRY_LEN] = e.data

        return buffer
