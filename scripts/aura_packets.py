"""Offline packet construction only. This module never opens a HID device."""

from aura_protocol import ProtocolError, REPORT_ID, REPORT_LENGTH

MAX_LEDS_PER_PACKET = 20
MAX_CHANNEL = 3


def _report(command: int, body: bytes) -> bytes:
    if len(body) > 63:
        raise ProtocolError('Payload exceeds 64 bytes')
    packet = bytes([REPORT_ID, command]) + body.ljust(63, b'\x00')
    if len(packet) != REPORT_LENGTH:
        raise ProtocolError('Invalid report length')
    return packet


def direct_mode_packet(channel: int) -> bytes:
    if type(channel) is not int or not 0 <= channel <= MAX_CHANNEL:
        raise ProtocolError('Channel must be 0 through 3')
    body = bytearray(63)
    body[0] = channel
    body[3] = 0xFF
    return _report(0x35, body)


def static_color_packets(channel: int, rgb: tuple[int, int, int], leds: int) -> list[bytes]:
    if type(channel) is not int or not 0 <= channel <= MAX_CHANNEL:
        raise ProtocolError('Channel must be 0 through 3')
    if type(leds) is not int or not 1 <= leds <= 120:
        raise ProtocolError('LED count must be 1 through 120')
    if len(rgb) != 3 or any(type(v) is not int or not 0 <= v <= 255 for v in rgb):
        raise ProtocolError('RGB must be three integer values in 0..255')
    packets = []
    for offset in range(0, leds, MAX_LEDS_PER_PACKET):
        count = min(MAX_LEDS_PER_PACKET, leds - offset)
        body = bytearray(63)
        body[0] = channel | (0x80 if offset + count == leds else 0)
        body[1] = offset
        body[2] = count
        body[3:3 + count * 3] = bytes(rgb) * count
        packets.append(_report(0x40, body))
    return packets
