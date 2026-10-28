"""ASUS Aura HID protocol parsing; no device access or lighting writes."""
REPORT_ID = 0xEC
REPORT_LENGTH = 65
FIRMWARE_MARKER = 0x02
CONFIG_MARKER = 0x30


class ProtocolError(ValueError):
    pass


def query_packet(opcode: int) -> bytes:
    if opcode not in (0x82, 0xB0):
        raise ProtocolError('Only firmware and configuration queries are permitted')
    return bytes((REPORT_ID, opcode)) + bytes(REPORT_LENGTH - 2)


def response_payload(response: bytes, marker: int) -> bytes:
    if len(response) != REPORT_LENGTH:
        raise ProtocolError('Unexpected HID response length')
    if response[0] != REPORT_ID or response[1] != marker:
        raise ProtocolError('Unexpected HID response marker')
    return response[1:]


def decode_firmware(response: bytes) -> str:
    payload = response_payload(response, FIRMWARE_MARKER)
    raw = payload[1:17]
    if any(byte > 0x7F for byte in raw):
        raise ProtocolError('Firmware string contains non-ASCII bytes')
    return raw.decode('ascii').rstrip('\x00').strip()


def decode_config(response: bytes) -> dict[str, int]:
    payload = response_payload(response, CONFIG_MARKER)
    table = payload[3:63]
    if len(table) != 60:
        raise ProtocolError('Unexpected configuration table length')
    return {
        'argb_channels': table[0x02],
        'mainboard_leds': table[0x1B],
        'rgb_headers': table[0x1D],
    }
