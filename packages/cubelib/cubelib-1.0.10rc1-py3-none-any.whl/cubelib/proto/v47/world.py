from cubelib.world import (
    ChunkColumnType,
    ChunkColumn,
    Chunk,
)
from cubelib.types import SafeBuff

from typing import List, Union, BinaryIO, Iterator, Iterable, Tuple

from numpy.typing import NDArray
import numpy as np


class Chunk_v47(Chunk):
    @staticmethod
    def read(
        buff: SafeBuff
    ) -> NDArray:
        return np.ndarray(
            shape=Chunk.dimensions,
            dtype=np.uint16,
            buffer=buff.read(Chunk.size)
        )

    @staticmethod
    def readHB(
        buff: SafeBuff
    ) -> NDArray:
        arr = np.frombuffer(buff.read(Chunk.HBsize), dtype=np.uint8)
        return np.column_stack((arr >> 4, arr & 0x0f)).reshape(Chunk.dimensions)

class ChunkColumn_v47(ChunkColumn):
    @staticmethod
    def destroy(
        bitmask: int, 
        chunk_column_buffer: SafeBuff, 
        skylight_sent: bool,
        x: Union[int, None] = None,
        z: Union[int, None] = None
    ) -> ChunkColumnType:

        
        # up to 16 of 16x16x16 (positioned)
        block_chunk_array: List = [
            None for _ in range(0, ChunkColumn.height)
        ]

        # up to 16 of 16x16x16 (positioned)
        blocklight_chunk_array: List = [
            None for _ in range(0, ChunkColumn.height)
        ]

        # up to 16 of 16x16x16 (positioned) (if sent)
        skylight_chunk_array: Union[List, None] = [
            None for _ in range(0, ChunkColumn.height)
        ] if skylight_sent else None

        # 16x16 (256)
        biome_map: NDArray
        
        # read all block arrays (up to 16 of 16x16x16 (positioned))
        for chunk_number in range(0, ChunkColumn.height):
            if not bitmask & (1 << chunk_number):
                # if chunk is empty (air)
                continue
            block_chunk_array[chunk_number] = Chunk_v47.read(chunk_column_buffer)
    
        # read all blight arrays (up to 16 of 16x16x16 (positioned))
        for chunk_number in range(0, ChunkColumn.height):
            if not bitmask & (1 << chunk_number):
                # if chunk is empty (air)
                continue
            blocklight_chunk_array[chunk_number] = Chunk_v47.readHB(chunk_column_buffer)

        if skylight_sent:
            # read all blight arrays (up to 16 of 16x16x16 (positioned))
            for chunk_number in range(0, ChunkColumn.height):
                if not bitmask & (1 << chunk_number):
                    # if chunk is empty (air)
                    continue
                skylight_chunk_array[chunk_number] = Chunk_v47.readHB(chunk_column_buffer)

        biome_map = np.ndarray(shape=(16,16), dtype=np.uint8, buffer=chunk_column_buffer.read(16*16))
        
        return ChunkColumnType(
            block_chunk_array,
            blocklight_chunk_array,
            skylight_chunk_array,
            biome_map,
            x,
            z
        )
    
    @staticmethod
    def build(
        chunk_column: ChunkColumnType
    ) -> bytearray:
        """encode chunk column
        """
        output = bytearray()

        for block_chunk in chunk_column.block_chunk_array:
            if block_chunk is None:
                continue
            output.extend(block_chunk.tobytes())

        for blocklight_chunk in chunk_column.blocklight_chunk_array:
            if blocklight_chunk is None:
                continue
            arr = blocklight_chunk.reshape(-1)
            output.extend((arr[0::2] << 4 | arr[1::2] & 0x0f).tobytes())

        if chunk_column.skylight_chunk_array is not None:
            for skylight_chunk in chunk_column.skylight_chunk_array:
                if skylight_chunk is None:
                    continue
                arr = skylight_chunk.reshape(-1)
                output.extend((arr[0::2] << 4 | arr[1::2] & 0x0f).tobytes())

        output.extend(chunk_column.biome_map.tobytes())
        return output

def load_columns_1(
    buffer: BinaryIO, 
    metadata: List[dict],
    skylight: bool
) -> Iterator[ChunkColumnType]:
    """metadata: [(-3, 8, 15), (-2, 8, 15), (-12, 18, 63), ...
    """

    for column in metadata:
        yield ChunkColumn_v47.destroy(
            bitmask=column[2],
            chunk_column_buffer=buffer,
            skylight_sent=skylight,
            x=column[0],
            z=column[1]
        )

def dump_columns_2(
    columns: Iterable[ChunkColumnType]
) -> Tuple[List[dict], bytearray]:
    metadata = list()
    data = bytearray()

    for column in columns:
        metadata.append([column.x, column.z, column.bitmask])
        data.extend(
            ChunkColumn_v47.build(
                column
            )
        )
    return metadata, data
