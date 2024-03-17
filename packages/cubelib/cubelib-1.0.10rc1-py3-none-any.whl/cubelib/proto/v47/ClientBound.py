from .types import *
from cubelib.p import Night
from cubelib.proto.version_independent.ClientBound import ClassicLogin
from .enums import *
from cubelib.mcenums import *

from cubelib.world import ChunkColumnType, ChunkColumnMappingType, FlatCoords
from .world import ChunkColumn_v47

from typing import List


class Login(ClassicLogin):
    pass

class Play:

    class JoinGame(Night):

        Dimension = JoinGameDimensionEnum

        EntityID: Int
        Gamemode: UnsignedByte
        Dimension: JoinGameDimensionEnum
        Difficulty: UnsignedByte
        MaxPlayers: UnsignedByte
        LevelType: String
        ReducedDebugInfo: Bool

    class PluginMessage(Night):

        Channel: String
        Data: ByteArray

    class ServerDifficulty(Night):

        Difficulty: UnsignedByte

    class SpawnPosition(Night):

        Location: Position

    class UpdateHealth(Night):

        Health: Float
        Food: VarInt
        FoodSaturating: Float
    
    class Respawn(Night):

        Dimension: Int
        Difficulty: UnsignedByte
        Gamemode: UnsignedByte
        LevelType: String

    class PlayerAbilities(Night):

        Flags: Byte
        FlyingSpeed: Float
        FOVModifier: Float

    class ChatMessage(Night):

        Message: Json
        Position: ChatMessagePositionEnum

    class KeepAlive(Night):

        KeepAliveID: VarInt

    class PlayerPositionAndLook(Night):

        X: Double
        FeetY: Double
        Z: Double
        Yaw: Float
        Pitch: Float
        Flags: Byte
    
    class HeldItemChange(Night):

        Slot: Byte

    class TimeUpdate(Night):

        WorldAge: Long
        TimeOfDay: Long

    class WindowItems(Night):

        WindowID: UnsignedByte        
        SlotData: FiniteLengthArray(Short)[Slot]

    class EntityRelativeMove(Night):

        EntityID: VarInt
        DeltaX: FixedPointB
        DeltaY: FixedPointB
        DeltaZ: FixedPointB
        OnGround: Bool

    class EntityLook(Night):

        EntityID: VarInt
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class EntityLookAndRelativeMove(Night):

        EntityID: VarInt
        DeltaX: Byte
        DeltaY: Byte
        DeltaZ: Byte
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class EntityHeadLook(Night):

        EntityID: VarInt
        HeadYaw: Angle

    class EntityVelocity(Night):

        EntityID: VarInt
        VelocityX: Short
        VelocityY: Short
        VelocityZ: Short

    class EntityStatus(Night):

        EntityID: Int
        EntityStatus: Byte

    class Disconnect(Night):
        Reason: String

    class EntityEquipment(Night):

        EntityID: VarInt
        Slot: Short
        Item: ByteArray  # ?slot
    
    class UseBed(Night):

        EntityID: VarInt
        Location: Position

    class Animation(Night):

        EntityID: VarInt
        Animation: UnsignedByte

    class SpawnPlayer(Night):

        EntityID: VarInt
        PlayerUUID: UUID
        X: Int
        Y: Int
        Z: Int
        Yaw: Angle
        Pitch: Angle
        CurrentItem: Short
        Metadata: Metadata
    
    class CollectItem(Night):

        CollectedEntityID: VarInt
        CollectorEntityID: VarInt

    class SpawnObject(Night):

        EntityID: VarInt
        Type: Object
        X: FixedPoint
        Y: FixedPoint
        Z: FixedPoint
        Pitch: Angle
        Yaw: Angle
        Data: Int
        VelocityX: Optional('Data', 0, equals=False)[Short]
        VelocityY: Optional('Data', 0, equals=False)[Short]
        VelocityZ: Optional('Data', 0, equals=False)[Short]

    class SpawnMob(Night):

        EntityID: VarInt
        Type: Mob
        X: FixedPoint
        Y: FixedPoint
        Z: FixedPoint
        Yaw: Angle
        Pitch: Angle
        HeadPitch: Angle
        VelocityX: Short
        VelocityY: Short
        VelocityZ: Short
        Metadata: Metadata
    
    class SpawnPainting(Night):

        EntityID: VarInt
        Title: String[13]
        Location: Position
        Direction: UnsignedByte

    class SpawnExperienceOrb(Night):

        EntityID: VarInt
        X: FixedPoint
        Y: FixedPoint
        Z: FixedPoint
        Count: Short

    class DestroyEntities(Night):

        EntityIDs: FiniteLengthArray(VarInt)[VarInt]

    class Entity(Night):

        EntityID: VarInt
    
    class EntityTeleport(Night):

        EntityID: VarInt
        X: Int
        Y: Int
        Z: Int
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class AttachEntity(Night):

        EntityID: Int
        VehicleID: Int
        Leash: Bool
    
    class EntityMetadata(Night):

        EntityID: VarInt
        Metadata: Metadata
    
    class EntityEffect(Night):

        EntityID: VarInt
        EffectID: Byte
        Amplifier: Byte
        Duration: VarInt
        HideParticles: Bool

    class RemoveEntityEffect(Night):

        EntityID: VarInt
        EffectID: Byte

    class SetExperience(Night):

        ExperienceBar: Float
        Level: VarInt
        TotalExperience: VarInt

    class EntityProperties(Night):

        EntityID: VarInt
        Properties: FiniteLengthArray(Int)[Property]
    
    class ChunkData(Night):

        ChunkX: Int
        ChunkZ: Int
        GroundUpCont: Bool
        PrimaryBitMask: UnsignedShort
        Data: FiniteLengthByteArray

        def analyze(self, overworld: bool = True) -> ChunkColumnType:
            return Chunk.destroy(
                bitmask=self.PrimaryBitMask,
                chunk_column_buffer=SafeBuff(self.Data, strictly_exhausted=True),
                skylight_sent=overworld
            )

        def regen(self, ChunkColumnType) -> bytes:
            self.Data = Chunk.build(
                ChunkColumnType
            )
            return self

    class MultiBlockChange(Night):

        ChunkX: Int
        ChunkZ: Int
        Data: ByteArray

    class BlockChange(Night):

        Location: Position
        BlockID: BlockID

    class BlockAction(Night):

        Location: Position
        Byte1: UnsignedByte
        Byte2: UnsignedByte
        BlockType: VarInt

    class BlockBreakAnimation(Night):

        EntityID: VarInt
        Location: Position
        DestroyStage: Byte

    class MapChunkBulk(Night):

        SkyLightSent: Bool
        ChunkMeta: FiniteLengthArray(VarInt)[ChunkMeta]
        Data: ByteArray

        @property
        def Columns(self) -> ChunkColumnMappingType:
            output = dict()
            buffer = SafeBuff(self.Data, strictly_exhausted=True)

            for column in self.ChunkMeta:
                output[tuple(column[:2])] = ChunkColumn_v47.destroy(
                    bitmask=column[2],
                    chunk_column_buffer=buffer,
                    skylight_sent=self.SkyLightSent,
                    x=column[0],
                    z=column[1]
                )
            return output


        @Columns.setter
        def Columns(self, columns: ChunkColumnMappingType):
            self.SkyLightSent = columns[next(iter(columns))].skylight_sent

            self.ChunkMeta = list()
            data = bytearray()

            for pos, column in columns.items():
                self.ChunkMeta.append((*pos, column.bitmask))
                data.extend(
                    ChunkColumn_v47.build(
                        column
                    )
                )
            self.Data = bytes(data)
            return self
        
        @property
        def included_coords(self) -> List[FlatCoords]:
            return [i[:2] for i in self.ChunkMeta]
            
        def is_presented(self, coords: FlatCoords) -> bool:
            return coords in self.included_coords

    class Explosion(Night):

        X: Float
        Y: Float
        Z: Float
        Radius: Float
        Data: ByteArray
    
    class Effect(Night):

        EffectID: Int
        Location: Position
        Data: Int
        DisableRelativeVolume: Bool

    class SoundEffect(Night):

        SoundName: Sound
        EffectPositionX: Int
        EffectPositionY: Int
        EffectPositionZ: Int
        Volume: Float
        Pitch: UnsignedByte

    class Particle(Night):

        ParticleID: Int
        LongDistance: Bool
        X: Float
        Y: Float
        Z: Float
        OffsetX: Float
        OffsetY: Float
        OffsetZ: Float
        ParticleData: Float
        ParticleCount: Int
        Data: ByteArray

    class ChangeGameState(Night):

        Reason = ChangeGameStateReasonEnum

        Reason: Reason
        Value: Float
    
    class SpawnGlobalEntity(Night):

        EntityID: VarInt
        Type: Byte
        X: FixedPoint
        Y: FixedPoint
        Z: FixedPoint
    
    class OpenWindow(Night):
        
        WindowID: UnsignedByte
        WindowType: String
        Data: ByteArray
    
    class CloseWindow(Night):

        WindowID: UnsignedByte
    
    class SetSlot(Night):

        WindowID: Byte
        Slot: Short
        SlotData: Slot

    class WindowProperty(Night):

        WindowID: UnsignedByte
        Property: Short
        Value: Short
    
    class ConfirmTransaction(Night):

        WindowID: Byte
        ActionNumber: Short
        Accepted: Bool
    
    class UpdateSign(Night):

        Location: Position
        Line1: String
        Line2: String
        Line3: String
        Line4: String
    
    class Map(Night):

        MapID: VarInt
        Scale: Byte
        Data: ByteArray

    class UpdateBlockEntity(Night):

        Location: Position
        Action: UpdateBlockEntityActionEnum
        NBTData: NBT
    
    class OpenSignEditor(Night):

        Location: Position
    
    class Statistics(Night):

        Statistics: FiniteLengthArray(VarInt)[StatisticsElement]

    class PlayerListItem(Night):
        
        Action = PlayerListItemData.Action

        Data: PlayerListItemData

    class TabComplete(Night):

        Matches: FiniteLengthArray(VarInt)[String]
    
    class ScoreboardObjective(Night):

        Mode = ScoreboardObjectiveModeEnum

        ObjectiveName: String
        Mode: ScoreboardObjectiveModeEnum
        ObjectiveValue: Optional("Mode", (Mode.Create, Mode.Update))[String]
        Type: Optional("Mode", (Mode.Create, Mode.Update))[String]

    class UpdateScore(Night):

        Action = UpdateScoreActionEnum

        ScoreName: String
        Action: UpdateScoreActionEnum
        ObjectiveName: String
        Value: Optional("Action", Action.Update)[VarInt]
    
    class DisplayScoreboard(Night):

        Position: Byte
        Name: String
    
    class Teams(Night):

        TeamName: String
        Mode: Byte
        TeamDisplayName: Optional("Mode", (0, 2))[String]
        #Data: ByteArray

    class ServerDifficulty(Night):

        Difficulty: UnsignedByte
    
    class CombatEvent(Night):

        Event: VarInt
        Duration: Optional("Event", 1)[VarInt]
        PlayerID: Optional("Event", 2)[VarInt]
        EntityID: Optional("Event", (1, 2))[Int]
        Message: Optional("Event", 2)[String]

    class Camera(Night):

        CameraID: VarInt
    
    class WorldBorder(Night):

        Action: VarInt
        Data: ByteArray
    
    class Title(Night):

        Action: VarInt
        Data: ByteArray

    class SetCompression(Night):

        Threshold: VarInt #warn
    
    class PlayerListHeaderAndFooter(Night):

        Header: String
        Footer: String

    class ResourcePackSend(Night):
        
        URL: String
        Hash: String[[40]]

    class UpdateEntityNBT(Night):

        EntityID: VarInt
        Tag: ByteArray

    map = {
        0x00: KeepAlive,
        0x01: JoinGame,
        0x02: ChatMessage,
        0x03: TimeUpdate,
        0x04: EntityEquipment,
        0x05: SpawnPosition,
        0x06: UpdateHealth,
        0x07: Respawn,
        0x08: PlayerPositionAndLook,
        0x09: HeldItemChange,
        0x0A: UseBed,
        0x0B: Animation,
        0x0C: SpawnPlayer,
        0x0D: CollectItem,
        0x0E: SpawnObject,
        0x0F: SpawnMob,
        0x10: SpawnPainting,
        0x11: SpawnExperienceOrb,
        0x12: EntityVelocity,
        0x13: DestroyEntities,
        0x14: Entity,
        0x15: EntityRelativeMove,
        0x16: EntityLook,
        0x17: EntityLookAndRelativeMove,
        0x18: EntityTeleport,
        0x19: EntityHeadLook,
        0x1A: EntityStatus,
        0x1B: AttachEntity,
        0x1C: EntityMetadata,
        0x1D: EntityEffect,
        0x1E: RemoveEntityEffect,
        0x1F: SetExperience,
        0x20: EntityProperties,
        0x21: ChunkData,
        0x22: MultiBlockChange,
        0x23: BlockChange,
        0x24: BlockAction,
        0x25: BlockBreakAnimation,
        0x26: MapChunkBulk,
        0x27: Explosion,
        0x28: Effect,
        0x29: SoundEffect,
        0x2A: Particle,
        0x2B: ChangeGameState,
        0x2C: SpawnGlobalEntity,
        0x2D: OpenWindow,
        0x2E: CloseWindow,
        0x2F: SetSlot,
        0x30: WindowItems,
        0x31: WindowProperty,
        0x32: ConfirmTransaction,
        0x33: UpdateSign,
        0x34: Map,
        0x35: UpdateBlockEntity,
        0x36: OpenSignEditor,
        0x37: Statistics,
        0x38: PlayerListItem,
        0x39: PlayerAbilities,
        0x3A: TabComplete,
        0x3B: ScoreboardObjective,
        0x3C: UpdateScore,
        0x3D: DisplayScoreboard,
        0x3E: Teams,
        0x3f: PluginMessage,
        0x40: Disconnect,
        0x41: ServerDifficulty,
        0x42: CombatEvent,
        0x43: Camera,
        0x44: WorldBorder,
        0x45: Title,
        0x46: SetCompression,
        0x47: PlayerListHeaderAndFooter,
        0x48: ResourcePackSend,
        0x49: UpdateEntityNBT
    }
    inv_map = {v: k for k, v in map.items()}
