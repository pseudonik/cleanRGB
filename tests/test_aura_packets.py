"""Offline ASUS Aura packet tests; no hardware writes."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from aura_packets import direct_mode_packet, static_color_packets
from aura_protocol import ProtocolError


class PacketTests(unittest.TestCase):
    def test_direct_mode_layout(self):
        p = direct_mode_packet(2)
        self.assertEqual(len(p), 65)
        self.assertEqual(p[:6], bytes([0xEC, 0x35, 2, 0, 0, 0xFF]))

    def test_single_led(self):
        p = static_color_packets(0, (1, 2, 3), 1)[0]
        self.assertEqual(len(p), 65)
        self.assertEqual(p[:9], bytes([0xEC, 0x40, 0x80, 0, 1, 1, 2, 3, 0]))

    def test_chunk_boundaries(self):
        p = static_color_packets(3, (4, 5, 6), 41)
        self.assertEqual(len(p), 3)
        self.assertEqual([(x[2], x[3], x[4]) for x in p], [(3, 0, 20), (3, 20, 20), (0x83, 40, 1)])
        self.assertTrue(all(len(x) == 65 for x in p))

    def test_reject_invalid_inputs(self):
        for channel, rgb, count in ((4, (1, 2, 3), 1), (0, (256, 0, 0), 1), (0, (1, 2, 3), 0), (0, (1, 2, 3), 121)):
            with self.assertRaises(ProtocolError):
                static_color_packets(channel, rgb, count)
        with self.assertRaises(ProtocolError):
            direct_mode_packet(-1)


if __name__ == '__main__':
    unittest.main()
