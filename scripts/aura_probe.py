"""Read-only ASUS Aura Gen4 firmware/configuration query (explicit opt-in).
Only 0B05:1AA6 HID interface 2 is eligible. No lighting writes.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import hid

VID, PID, INTERFACE = 0x0B05, 0x1AA6, 2
REPORT_ID = 0xEC
QUERY = {'firmware': 0x82, 'config': 0xB0}


def discover():
    return [d for d in hid.enumerate(VID, PID) if d.get('interface_number') == INTERFACE]


def run():
    ap = argparse.ArgumentParser()
    ap.add_argument('--query', choices=['firmware', 'config'], help='Send one documented query')
    args = ap.parse_args()
    devices = discover()
    print('matching_hid_devices:', len(devices))
    for d in devices:
        print('device:', {k: d.get(k) for k in ('manufacturer_string', 'product_string', 'interface_number', 'usage_page', 'usage')})
    if not args.query:
        return
    if len(devices) != 1:
        raise SystemExit('Refusing query: expected exactly one matching device')
    dev = hid.device()
    try:
        dev.open_path(devices[0]['path'])
        dev.set_nonblocking(1)
        payload = bytes([REPORT_ID, QUERY[args.query]]) + bytes(63)
        written = dev.write(payload)
        response = dev.read(65, 500)
        record = {'time': datetime.now(timezone.utc).isoformat(), 'query': args.query,
                  'written_bytes': written, 'response_hex': bytes(response).hex(),
                  'response_length': len(response)}
        output = Path(__file__).resolve().parents[1] / 'artifacts' / ('aura-' + args.query + '.json')
        output.parent.mkdir(exist_ok=True)
        output.write_text(json.dumps(record, indent=2), encoding='utf-8')
        print(json.dumps(record, indent=2))
    finally:
        dev.close()


if __name__ == '__main__':
    run()
