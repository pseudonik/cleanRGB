"""Opt-in, query-only ASUS Aura HID probe. No lighting commands."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from aura_protocol import ProtocolError, query_packet, decode_config, decode_firmware

VID, PID, INTERFACE = 0x0B05, 0x1AA6, 2
QUERY = {'firmware': 0x82, 'config': 0xB0}


def run():
    ap = argparse.ArgumentParser()
    ap.add_argument('--query', choices=QUERY, help='Send one documented read-only query')
    ap.add_argument('--save-private', action='store_true', help='Save raw response locally under ignored artifacts/')
    args = ap.parse_args()
    try:
        import hid
    except ImportError as exc:
        raise SystemExit('Install hidapi in a local virtual environment first') from exc
    devices = [d for d in hid.enumerate(VID, PID) if d.get('interface_number') == INTERFACE]
    print('Compatible HID interfaces found:', len(devices))
    if not args.query:
        return
    if len(devices) != 1:
        raise SystemExit('Refusing query: expected exactly one matching interface')
    dev = hid.device()
    try:
        dev.open_path(devices[0]['path'])
        dev.set_nonblocking(1)
        written = dev.write(query_packet(QUERY[args.query]))
        if written != 65:
            raise ProtocolError('Incomplete HID query write')
        response = bytes(dev.read(65, 500))
        result = decode_firmware(response) if args.query == 'firmware' else decode_config(response)
        # Never print identifying firmware strings or observed topology by default.
        print('Response validated:', args.query)
        if args.save_private:
            record = {'time': datetime.now(timezone.utc).isoformat(), 'query': args.query,
                      'response_hex': response.hex(), 'decoded': result}
            output = Path(__file__).resolve().parents[1] / 'artifacts' / ('aura-' + args.query + '.json')
            output.parent.mkdir(exist_ok=True)
            output.write_text(json.dumps(record, indent=2), encoding='utf-8')
            print('Private result saved in ignored artifacts directory')
    finally:
        dev.close()


if __name__ == '__main__':
    run()
