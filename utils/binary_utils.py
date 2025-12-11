
class ByteUtils:
    @staticmethod
    def pack_u16(n):
        """Pack an unsigned 16-bit integer into 2 bytes (little-endian)."""
        return bytes([n & 0xFF, (n >> 8) & 0xFF])

    @staticmethod
    def pack_u32(n):
        """Pack an unsigned 32-bit integer into 4 bytes (little-endian)."""
        return bytes([
            n & 0xFF,
            (n >> 8) & 0xFF,
            (n >> 16) & 0xFF,
            (n >> 24) & 0xFF
        ])

    @staticmethod
    def unpack_u16(data, offset):
        """Unpack 2 bytes starting at offset into a 16-bit unsigned integer."""
        return data[offset] | (data[offset + 1] << 8)

    @staticmethod
    def unpack_u32(data, offset):
        """Unpack 4 bytes starting at offset into a 32-bit unsigned integer."""
        return (
            data[offset] |
            (data[offset + 1] << 8) |
            (data[offset + 2] << 16) |
            (data[offset + 3] << 24)
        )
