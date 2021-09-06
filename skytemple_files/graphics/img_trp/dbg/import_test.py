#  Copyright 2020-2021 Capypara and the SkyTemple Contributors
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

import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.types.file_types import FileType
from skytemple_files.common.util import get_ppmdu_config_for_rom
from skytemple_files.graphics.img_trp.handler import ImgTrpHandler

try:
    from PIL import Image
except ImportError:
    from pil import Image

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')
out_dir = os.path.join(os.path.dirname(__file__), 'dbg_output')

rom = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us.nds'))
config = get_ppmdu_config_for_rom(rom)
dungeon_bin = FileType.DUNGEON_BIN.deserialize(rom.getFileByName('DUNGEON/dungeon.bin'), config)

for i, file in enumerate(dungeon_bin):
    fn = dungeon_bin.get_filename(i)
    if fn.endswith('.trp.img'):
        file_serialize = ImgTrpHandler.serialize(file)
        print(f'dungeon.bin:{fn}')
        for x in range(len(file.sprites)):
            img = Image.open(os.path.join(out_dir, 'dungeon.bin__' + fn.replace('/', '_') + f'.{x}.png'), 'r')
            file.from_pil(x, img)
        print(file)
        assert file == ImgTrpHandler.deserialize(file_serialize)
