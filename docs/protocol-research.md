# ASUS Aura protocol references

The open-source Hypercolor implementation includes ASUS Aura motherboard-class HID devices, including the product-family identifier `0B05:1AA6`.

- Implementation: https://github.com/hyperb1iss/hypercolor (Apache-2.0)
- Reference modules: `crates/hypercolor-hal/src/drivers/asus/` (`devices.rs`, `protocol.rs`, `types.rs`)
- HID report ID: `0xEC`; protocol payload length: 64 bytes.
- Documented query opcodes: firmware `0x82` and configuration `0xB0`.
- Protocol configuration parser uses offsets `0x02`, `0x1B`, and `0x1D` for advertised ARGB channels, motherboard LED count, and RGB headers.

These are public protocol constants, not a record of any particular user's hardware or test results. Never commit firmware strings, observed channel counts, raw responses, serial numbers, or local inventory.

A separate SignalRGB community plugin may provide background reading, but device compatibility and licensing must be independently verified.
