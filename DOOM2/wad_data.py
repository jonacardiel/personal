from wadreader import WADReader

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Linedef:
    def __init__(self, start_vertex_id, end_vertex_id):
        self.start_vertex_id = start_vertex_id
        self.end_vertex_id = end_vertex_id

class WADData:
    LUMP_INDICES = {
        'THINGS': 1, 'LINEDEFS': 2, 'SIDEDEFS': 3, 'VERTEXES': 4,
        'SEGS': 5, 'SSECTORS': 6, 'NODES': 7, 'SECTORS': 8, 'REJECT': 9,
        'BLOCKMAP': 10
    }
    
    def __init__(self, engine, map_name):
        self.wad_reader = WADReader(WADReader)
        self.wad_reader.close()
        self.map_index = self.get_lump_index(lump_name=map_name)
        if self.map_index is not None:
            self.vertexes = self.get_lump_data(
                reader_func=self.wad_reader.read_vertex,
                Lump_index=self.map_index + self.LUMP_INDICES['VERTEXES'],
                num_bytes=4,
            )
        if self.map_index is not None:
            self.linedefs = self.get_lump_data(
                reader_func=self.wad_reader.read_linedef,  # Use the correct method name
                Lump_index=self.map_index + self.LUMP_INDICES['LINEDEFS'],
                num_bytes=14,
            )
            [self.print_attrs(i) for i in self.linedefs]
        else:
            self.linedefs = []

        self.wad_reader.close()

    @staticmethod
    def print_attrs(obj):
        print()
        for attr in obj.__slots__:
            print(eval(f'obj.{attr}'), end=' ')
        
    def get_lump_data(self, reader_func, Lump_index, num_bytes, header_length=0):
        lump_info = self.wad_reader.directory[Lump_index]
        count= lump_info['size'] // num_bytes
        data = []
        for i in range(count):
            offset = lump_info['offset'] + header_length + i * num_bytes
            data.append(reader_func(offset))
        return data
        

    def get_lump_index(self, lump_name):
        """
        Get the index of a lump by its name.
        """
        for index, lump_info in enumerate(self.wad_reader.directory):
            if lump_name in lump_info.values():
                return index