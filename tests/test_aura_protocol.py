"""Unit tests with synthetic packets. No RGB hardware required."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from aura_protocol import ProtocolError, query_packet, decode_config, decode_firmware


class ProtocolTests(unittest.TestCase):
    def test_firmware_query(self):
        p = query_packet(0x82)
        self.assertEqual(len(p), 65)
        self.assertEqual(p[:2], b'\xec\x82')
        self.assertEqual(p[2:], bytes(63))

    def test_reject_effect_commands(self):
        for opcode in (0x35, 0x3B, 0x40, 0xFF):
            with self.assertRaises(ProtocolError):
                query_packet(opcode)

    def test_decode_firmware(self):
        response = b'\xec\x02' + b'TEST-FW-1'.ljust(16, b'\x00') + bytes(47)
        self.assertEqual(decode_firmware(response), 'TEST-FW-1')

    def test_decode_config(self):
        table = bytearray(60)
        table[2], table[27], table[29] = 3, 5, 1
        response = b'\xec\x30\x00\x00' + bytes(table) + b'\x00'
        self.assertEqual(decode_config(response), {'argb_channels': 3, 'mainboard_leds': 5, 'rgb_headers': 1})

    def test_reject_malformed(self):
        with self.assertRaises(ProtocolError):
            decode_config(bytes(65))
        with self.assertRaises(ProtocolError):
            decode_firmware(bytes(64))


if __name__ == '__main__':
    unittest.main()
