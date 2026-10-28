"""Decode a saved ASUS AURA configuration response. No device access."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
record = json.loads((root / 'artifacts' / 'aura-config.json').read_text(encoding='utf-8'))
data = bytes.fromhex(record['response_hex'])
if len(data) != 65 or data[0:2] != bytes([0xEC, 0x30]):
    raise SystemExit('Unexpected response marker/length')
table = data[4:64]
print(json.dumps({
    'argb_channels': table[2],
    'mainboard_leds': table[0x1B],
    'rgb_headers': table[0x1D],
    'raw_table_hex': table.hex(),
}, indent=2))
