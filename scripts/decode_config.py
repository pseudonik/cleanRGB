"""Decode a locally saved ASUS Aura configuration response, without device access."""
import json
from pathlib import Path
from aura_protocol import decode_config

root = Path(__file__).resolve().parents[1]
record = json.loads((root / 'artifacts' / 'aura-config.json').read_text(encoding='utf-8'))
print(json.dumps(decode_config(bytes.fromhex(record['response_hex'])), indent=2))
