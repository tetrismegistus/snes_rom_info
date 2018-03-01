#!/usr/bin/env python3

import os
import argparse

import hexview

# My two main sources for this are:
# https://en.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map
# http://www.emulatronia.com/doctec/consolas/snes/sneskart.html#embededcartridge


class Header(object):

    HEADER_SIZE = int('40', 16)  # 64 byte header
    LOROM_HEADER = int('7FC0', 16)  # Lowrom bank ends at 7FFF, with no smc header
    HIROM_HEADER = int('FFC0', 16)  # hirom  bank ends at FFFF, with no smc header

    ROM_TYPES = {0: 'ROM',
                 1: 'ROM and RAM',
                 2: 'ROM and Save RAM',
                 3: 'ROM and DSP1 chip',
                 4: 'ROM, RAM, and DSP1 Chip',
                 5: 'ROM, Save RAM and DSP1 Chip',
                 19: 'ROM and Super FX chip',
                 227: 'ROM, RAM and GameBoy data',
                 246: 'ROM and DSP2 chip'}

    COUNTRY_TABLE = {0: 'Japan',
                     1: 'USA',
                     2: 'Australia, Europe, Oceania, and Asia ',
                     3: 'Sweden',
                     4: 'Finland',
                     5: 'Denmark',
                     6: 'France',
                     7: 'Holland',
                     8: 'Spain',
                     9: 'Germany, Austria, and Switzerland',
                     10: 'Italy',
                     11: 'Hong Kong and China',
                     12: 'Indonesia',
                     13: 'Korea'}

    LICENSEES = {1: 'Nintendo', 3:  'Imagineer-Zoom', 5:  'Zamuse', 6:  'Falcom', 8:  'Capcom', 9:  'HOT-B',
                      10:  'Jaleco', 11:  'Coconuts', 12:  'Rage Software', 14:  'Technos', 15:  'Mebio Software',
                      18:  'Gremlin Graphics', 19:  'Electronic Arts', 21:  'COBRA Team', 22:  'Human/Field',
                      23:  'KOEI', 24:  'Hudson Soft', 26:  'Yanoman', 28:  'Tecmo', 30:  'Open System',
                      31:  'Virgin Games', 32:  'KSS', 33:  'Sunsoft', 34:  'POW', 35:  'Micro World',
                      38:  'Enix', 39:  'Loriciel/Electro Brain', 40:  'Kemco', 41:  'Seta Co.,Ltd.',
                      45:  'Visit Co.,Ltd.', 49:  'Carrozzeria', 50:  'Dynamic', 51:  'Nintendo', 52:  'Magifact',
                      53:  'Hect', 60:  'Empire Software', 61:  'Loriciel', 64:  'Seika Corp.', 65:  'UBI Soft',
                      70:  'System 3', 71:  'Spectrum Holobyte', 73:  'Irem', 75:  'Raya Systems/Sculptured Software',
                      76:  'Renovation Products', 77:  'Malibu Games/Black Pearl', 79:  'U.S. Gold',
                      80:  'Absolute Entertainment', 81:  'Acclaim', 82:  'Activision', 83:  'American Sammy',
                      84:  'GameTek', 85:  'Hi Tech Expressions', 86:  'LJN Toys', 90:  'Mindscape', 93:  'Tradewest',
                      95:  'American Softworks Corp.', 96:  'Titus', 97:  'Virgin Interactive Entertainment',
                      98:  'Maxis', 103:  'Ocean', 105:  'Electronic Arts', 107:  'Laser Beam', 110:  'Elite',
                      111:  'Electro Brain', 112:  'Infogrames', 113:  'Interplay', 114:  'LucasArts',
                      115:  'Parker Brothers', 117:  'STORM', 120:  'THQ Software', 121:  'Accolade Inc.',
                      122:  'Triffix Entertainment', 124:  'Microprose', 127:  'Kemco', 128:  'Misawa', 129:  'Teichio',
                      130:  'Namco Ltd.', 131:  'Lozc', 132:  'Koei', 134:  'Tokuma Shoten Intermedia',
                      136:  'DATAM-Polystar', 139:  'Bullet-Proof Software', 140:  'Vic Tokai', 142:  'Character Soft',
                      143:  'I\'Max', 144:  'Takara', 145:  'CHUN Soft', 146:  'Video System Co., Ltd.', 147:  'BEC',
                      149:  'Varie', 151:  'Kaneco', 153:  'Pack in Video', 154:  'Nichibutsu', 155:  'TECMO',
                      156:  'Imagineer Co.', 160:  'Telenet', 164:  'Konami', 165:  'K.Amusement Leasing Co.',
                      167:  'Takara', 169:  'Technos Jap.', 170:  'JVC', 172:  'Toei Animation', 173:  'Toho',
                      175:  'Namco Ltd.', 177:  'ASCII Co. Activison', 178:  'BanDai America', 180:  'Enix',
                      182:  'Halken', 186:  'Culture Brain', 187:  'Sunsoft', 188:  'Toshiba EMI',
                      189:  'Sony Imagesoft', 191:  'Sammy', 192:  'Taito', 194:  'Kemco', 195:  'Square',
                      196:  'Tokuma Soft', 197:  'Data East', 198:  'Tonkin House', 200:  'KOEI', 202:  'Konami USA',
                      203:  'NTVIC', 205:  'Meldac', 206:  'Pony Canyon', 207:  'Sotsu Agency/Sunrise',
                      208:  'Disco/Taito', 209:  'Sofel', 210:  'Quest Corp.', 211:  'Sigma', 214:  'Naxat',
                      216:  'Capcom Co., Ltd.', 217:  'Banpresto', 218:  'Tomy', 219:  'Acclaim', 221:  'NCS',
                      222:  'Human Entertainment', 223:  'Altron', 224:  'Jaleco', 226:  'Yutaka', 228:  'T&ESoft',
                      229:  'EPOCH Co.,Ltd.', 231:  'Athena', 232:  'Asmik', 233:  'Natsume', 234:  'King Records',
                      235:  'Atlus', 236:  'Sony Music Entertainment', 238:  'IGS', 241:  'Motown Software',
                      242:  'Left Field Entertainment', 243:  'Beam Software', 244:  'Tec Magik', 249:  'Cybersoft',
                      255:  'Hudson Soft'}

    def __init__(self, filename):
        self.filename = filename
        self.smc_offset = self.get_smc_offset(filename)
        self.calculated_checksum = self.calculate_checksum()

        for f in (self.LOROM_HEADER, self.HIROM_HEADER):
            rom_segment = hexview.read_file(filename, self.HEADER_SIZE, f + self.smc_offset)
            checksum_and_complement_verfication = self.check_checksum_and_complement(rom_segment)
            potential_rom_mapping = self.get_specified_rom_mapping(rom_segment)

            if f == self.LOROM_HEADER:
                possible_types = [32, 48, 50]
            else:
                possible_types = [33, 35, 49, 53]

            if (checksum_and_complement_verfication == 'ffff') and (potential_rom_mapping[0] in possible_types):
                self.header = rom_segment
                self.rom_mapping = potential_rom_mapping[1]
                self.header_address = f + self.smc_offset

        self.game_title = str(self.header[0:20])
        self.rom_type = self.ROM_TYPES.get(self.header[22])
        self.rom_size = 1 << (self.header[23] - 7)
        self.sram_size = 1 << (self.header[24] + 3)
        self.country = self.COUNTRY_TABLE.get(self.header[25])
        self.licensee = self.LICENSEES.get(self.header[26])
        self.version = self.header[27]
        self.checksum_complement = '{:02x}{:02x}'.format(self.header[29], self.header[28])
        self.header_checksum = '{:02x}{:02x}'.format(self.header[31], self.header[30])

    def calculate_checksum(self):
        f = open(self.filename, 'rb')
        f.seek(self.smc_offset)
        chunk_sums = []
        for chunk in read_in_chunks(f):
            total = 0
            for byte in chunk:
                total += byte
            chunk_sums.append(total)

        total = 0

        for csum in chunk_sums:
            total += csum

        return '{:04x}'.format(total & int('FFFF', 16))

    @staticmethod
    def check_checksum_and_complement(header):
        complement = int('{:02x}{:02x}'.format(header[29], header[28]), 16)
        checksum = int('{:02x}{:02x}'.format(header[31], header[30]), 16)
        return '{:04x}'.format(complement | checksum)

    @staticmethod
    def get_specified_rom_mapping(header):
        mapping_type = header[21]
        # yeah, I know a lookup table is lame when this is basically a bitmask
        # problem is, I have trouble resolving some of the values based on the
        # bitmask described https://en.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map
        # such as SA-1 ROM.  For now I'll return both the value and description
        # and the last bit of the value may still be used to verify lo-rom / hi-rom label
        mappings = {32: 'LoROM',
                    33: 'HiRom',
                    35: 'SA-1 ROM',
                    48: 'LoROM + FastROM',
                    49: 'HiRom + FastROM',
                    50: 'ExLoROM',
                    53: 'ExHiRom'}
        return [mapping_type, mappings.get(mapping_type)]

    @staticmethod
    def get_smc_offset(filename):
        size = os.path.getsize(filename)
        # https://en.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map
        # Before you try to load in these informations, you have to determine
        # the size of the SMC, may it be there or not. The length of the ROM
        # modulo 1024 (ROM size % $400) gives you the size of the SMC header.
        # If it's 0, there is no header. If it's not 512, the header is malformed
        return size % 1024


def read_in_chunks(file_object, chunk_size=500000):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def main(args):
    header = Header(args.filename)
    print()

    if header.smc_offset > 0:
        smc = 'Yes'
    else:
        smc = 'No'
    print('Game Title: {}'.format(header.game_title))
    print('SMC Header: {}'.format(smc))
    print('Rom Mapping: {}'.format(header.rom_mapping))
    print('Rom Type: {}'.format(header.rom_type))
    print('Rom Size: {} MegaBits'.format(header.rom_size))
    print('SRAM Size: {} Kilobits'.format(header.sram_size))
    print('Country: {}'.format(header.country))
    print('Licensee: {}'.format(header.licensee))
    print('Game Version: {}'.format(header.version))
    print('Checksum Complement: {}'.format(header.checksum_complement))
    print('Specified Checksum: {}'.format(header.header_checksum))
    print('Calculated checksum: {}'.format(header.calculated_checksum))

    print()
    hexview.print_canonical(header.header, header.header_address)
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='snes_rom_info.py', usage='%(prog)s filename')
    parser.add_argument('filename', help="The ROM you wish to analyze")
    args = parser.parse_args()
    main(args)
