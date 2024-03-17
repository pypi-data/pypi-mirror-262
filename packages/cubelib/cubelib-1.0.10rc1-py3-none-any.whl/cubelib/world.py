__backend__ = "stream"

from typing import List, Dict, Tuple, NamedTuple, Optional
from numpy.typing import NDArray
from numpy import uint8, uint16

from io import BytesIO
from abc import ABC, abstractstaticmethod


# 16x16x16 of int (light, 0...15)
LightChunkType = NDArray[uint8]

# 16x16x16 of int (block 0...65535)
BlockChunkType = NDArray[uint16]

# 16x16 of int (biome 0...256)
BiomeMapType = NDArray[uint8]

# X, Z
FlatCoords = Tuple[int, int]

# X, Y, Z
Coords = Tuple[int, int, int]


class Block(NamedTuple):
    id: int
    damage: int

    @staticmethod
    def from1(v):
        return Block(v >> 4, v & 0x0F)
    
    def to1(self):
        return self.id << 4 | self.damage & 0x0F

class ChunkColumnType(NamedTuple):
    # up to 16 of 16x16x16
    block_chunk_array: List[Optional[BlockChunkType]]
    # up to 16 of 16x16x16
    blocklight_chunk_array: List[Optional[LightChunkType]]
    # up to 16 of 16x16x16 (if sent)
    skylight_chunk_array: Optional[List[Optional[LightChunkType]]]
    # 16x16 (256)
    biome_map: BiomeMapType

    x: Optional[int] = None
    z: Optional[int] = None

    @property
    def chunk_count(self):
        return len([None for i in self.block_chunk_array if i is not None])

    @property
    def bitmask(self):
        return int("".join(reversed(['0' if i is None else '1' for i in self.block_chunk_array])), 2)

    @property
    def skylight_sent(self):
        return self.skylight_chunk_array is not None
    
    @property
    def strbitmask(self):
        return str(bin(self.bitmask)[2:].zfill(16))

    def __repr__(self):
        return "ChunkColumn[{}, {}](SkyLight={}, StrBitmask={})".format(
            self.x,
            self.z,
            self.skylight_sent,
            self.strbitmask
        )

    @property
    def uniq_blocks(self):
        uniq_blocks = set()
        for block_chunk in self.block_chunk_array:
            if block_chunk is None:
                continue
            uniq_blocks.update(block_chunk.reshape(-1))
        return uniq_blocks

ChunkColumnMappingType = Dict[FlatCoords, ChunkColumnType]

class Chunk:
    height = 16
    width = 16
    depth = 16

    size = height * width * depth * 2
    HBsize = height * width * depth // 2

    dimensions = (height, width, depth)

class ChunkColumn(ABC):
    """
        Block:
            id: int
            damage:int

        BlockChunk:
            Array Y[16]:
                Array Z[16]
                    Array X[16]:
                        BlockID, Damage (Block)

        LightChunk:
            Array Y[16]:
                Array Z[16]
                    Array X[16]:
                        Light value (int)

        ChunkColumn:
            SkyLightSent: True/False
            BitMask: 0b00000000_00000000
            Array[0...16]: BlockChunk | None - block_chunk_array
            Array[0...16]: LightChunk | None - blocklight_chunk_array
            Array[0...16] | None: LightChunk | None - skylight_chunk_array

            Array Z[16]:              - biome_map
                Array X[16]: BiomeID (int)
    """

    height = 16
    width = 1
    depth = 1

    @abstractstaticmethod
    def destroy(
        bitmask: int, 
        chunk_column_buffer: BytesIO,
        skylight_sent: bool,
        x: Optional[int] = None,
        z: Optional[int] = None
    ) -> ChunkColumnType:
        ...

    @abstractstaticmethod
    def build(
        self,
        column: ChunkColumnType
    ) -> bytearray:
        ...


class BlockMeta:
    def __init__(self, cname, id, damage, id_name):
        self.cname = cname
        self.id = id
        self.damage = damage
        self.id_name = id_name

    @classmethod
    def _missing_(cls, value):
        base = None
        for block in cls:
            if isinstance(value, int):
                if block.id == value:
                    return block
            elif isinstance(value, tuple):
                if block.id == value[0] and block.damage == value[1]:
                    return block
                elif block.id == value[0]:
                    base = block
        return base

    def __repr__(self) -> str:
        return f'<{self.id}:{self.damage} {self.name} v{self.__proto__}>'
