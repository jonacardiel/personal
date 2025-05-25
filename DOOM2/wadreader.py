import struct
from pygame.math import Vector2 as vec2 
from data_types import *  # Ensure Linedef is defined or imported in this module

class WADReader:
    def __init__(self, wad_path):
        self.wad_file = open(wad_path, 'rb')
        self.header = self.read_header()
        self.directory = self.read_directory()
        self.map_data = self.load_map_data()  # Add this line

    def read_vertex(self, offset):
        # Read vertex data from the WAD file
        x = self.read_2_bytes(offset, byte_format="<h")
        y = self.read_2_bytes(offset + 2, byte_format="<h")
        return vec2(x, y)

    def read_directory(self):
        directory = []
        for i in range(self.header['num_lumps']):
            offset = self.header['init_offset'] + i * 16
            lump_info = {
                'offset': self.read_4_bytes(offset),
                'size': self.read_4_bytes(offset + 4),
                'name': self.read_string(offset + 8, num_bytes=8),
            }
            directory.append(lump_info)
        return directory

    def read_header(self):
        return {
            'wad_type': self.read_string(offset=0, num_bytes=4),
            'num_lumps': self.read_4_bytes(offset=4),
            'init_offset': self.read_4_bytes(offset=8),
        }
    
    def read_1_byte(self, offset, byte_format="<B"):
        return self.read_bytes(offset, num_bytes=1, byte_format=byte_format)[0]
    
    def read_2_bytes(self, offset, byte_format):
        return self.read_bytes(offset, num_bytes=2, byte_format=byte_format)[0]

    def read_4_bytes(self, offset, byte_format="<i"):
        return self.read_bytes(offset, num_bytes=4, byte_format=byte_format)[0]

    def read_string(self, offset, num_bytes):
        # Read bytes and decode, strip nulls, and uppercase
        raw = self.read_bytes(offset, num_bytes, byte_format='{}s'.format(num_bytes))[0]
        return raw.decode('ascii', errors='ignore').rstrip('\0').upper()

    def read_bytes(self, offset, num_bytes, byte_format):
        self.wad_file.seek(offset)
        buffer = self.wad_file.read(num_bytes)
        return struct.unpack(byte_format, buffer)

    def close(self):
        self.wad_file.close()

    def load_map_data(self):
        """
        Loads map data (vertexes, linedefs, etc.) from the WAD file.
        This is a minimal example; you may need to expand it for full WAD support.
        """
        from wad_data import WADData, Vertex, Linedef  # Local import to avoid circular import
        map_data = WADData(engine=None, map_name="Unnamed")  # Replace with actual values if available
        # Find lumps for VERTEXES and LINEDEFS
        vertex_lump = next((d for d in self.directory if d['name'] == 'VERTEXES'), None)
        linedef_lump = next((d for d in self.directory if d['name'] == 'LINEDEFS'), None)

        # Load vertexes
        if vertex_lump:
            count = vertex_lump['size'] // 4  # Each vertex is 4 bytes (2 shorts)
            for i in range(count):
                offset = vertex_lump['offset'] + i * 4
                v = self.read_vertex(offset)
                map_data.vertexes.append(Vertex(v.x, v.y))

        # Load linedefs
        if linedef_lump:
            count = linedef_lump['size'] // 14  # Each linedef is 14 bytes
            for i in range(count):
                offset = linedef_lump['offset'] + i * 14
                ldef = self.read_linedef(offset)
                map_data.linedefs.append(ldef)

        return map_data

    def read_linedef(self, offset):
        # Minimal Linedef definition (if not imported)
        try:
            from wad_data import Linedef
        except ImportError:
            class Linedef:
                def __init__(self, start_vertex_id, end_vertex_id):
                    self.start_vertex_id = start_vertex_id
                    self.end_vertex_id = end_vertex_id
        read_2_bytes = self.read_2_bytes
        linedef = Linedef(
            start_vertex_id=read_2_bytes(offset, byte_format="<H"),
            end_vertex_id=read_2_bytes(offset + 2, byte_format="<H")
        )
        return linedef
