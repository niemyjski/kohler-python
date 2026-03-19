# kohler

[![CI](https://github.com/niemyjski/kohler-python/actions/workflows/ci.yml/badge.svg)](https://github.com/niemyjski/kohler-python/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/kohler.svg)](https://pypi.org/project/kohler/)
[![Python versions](https://img.shields.io/pypi/pyversions/kohler.svg)](https://pypi.org/project/kohler/)
[![License](https://img.shields.io/pypi/l/kohler.svg)](https://github.com/niemyjski/kohler-python/blob/main/LICENSE)

Python library for controlling **Kohler DTV+** shower systems over your local network.

## Features

- 🚿 Full shower control (start, stop, quick shower with valve configuration)
- 💡 Light module control with adjustable intensity
- 🎵 Music playback with volume control
- 🌧️ Chromatherapy rain effects (color or experience modes)
- ♨️ Steam control with temperature and duration
- 👤 User session management
- 🔧 System info, firmware updates, error logs, and factory reset
- 📤 Firmware upload via multipart POST
- ✅ Fully typed with inline type hints ([PEP 561](https://peps.python.org/pep-0561/))

## Installation

```bash
pip install kohler
```

**From source (development):**

```bash
git clone https://github.com/niemyjski/kohler-python.git
cd kohler-python
pip install -e ".[dev]"
```

## Quick Start

```python
import asyncio
from kohler import Kohler

async def main():
    kohler = Kohler(kohler_host="192.168.1.50")
    
    # Shower control
    await kohler.quick_shower()
    await kohler.stop_shower()
    
    # Lights
    await kohler.light_on(module=1, intensity=75)
    await kohler.light_off(module=1)

    # Music
    await kohler.music_on(volume=80)
    await kohler.music_off()

    # Steam
    await kohler.steam_on(temp=110, time=10)
    await kohler.steam_off()

    # Chromatherapy rain
    await kohler.rain_on(color=120)
    await kohler.rain_off()

asyncio.run(main())
```

## API Reference

### Initialization

| Method | Description |
|---|---|
| `Kohler(kohler_host, timeout=1.0)` | Create an asynchronous client. `kohler_host` is the IP or hostname of the DTV+ device. |

### Shower Control

| Method | Description |
|---|---|
| `quick_shower(valve_num, valve1_outlet, valve1_massage, valve1_temp, valve2_outlet, valve2_massage, valve2_temp)` | Start a quick shower with valve configuration. All params have sensible defaults. |
| `stop_shower()` | Stop the shower. |
| `start_user(user=1)` | Start a user session. |
| `stop_user()` | Stop the current user session. |
| `swap_valves()` | Swap valve 1 and valve 2 configurations. |

### Lighting

| Method | Description |
|---|---|
| `light_on(module=1, intensity=100)` | Turn on a light module (intensity: 0–100). |
| `light_off(module)` | Turn off a light module. |
| `light_module(module=2, intensity=100)` | Control a light module. |

### Music

| Method | Description |
|---|---|
| `music_on(volume=100)` | Turn on music (volume: 0–100). |
| `music_off(volume=100)` | Turn off music. |

### Steam & Rain

| Method | Description |
|---|---|
| `steam_on(temp=110, time=10)` | Turn on steam (temp in °F, time in minutes). |
| `steam_off()` | Turn off steam. |
| `rain_on(*, color=None, effect=None)` | Turn on rain — provide `color` (mode 1) **or** `effect` (mode 2), not both. |
| `rain_off()` | Turn off rain effect. |

### System & Configuration

| Method | Description |
|---|---|
| `system_info()` | Get system information. |
| `check_updates()` | Check for firmware updates. |
| `values()` | Get current device values. |
| `languages()` | Get available languages. |
| `ftp_status()` | Get FTP status. |
| `id_interface(index)` | Get interface identification. |
| `set_device(value)` | Set device configuration. |
| `save_variable(index, value, **kwargs)` | Save a variable. |
| `save_dt()` | Save DT configuration. |
| `save_ui(index)` | Save UI configuration. |
| `save_default()` | Save current settings as default. |
| `massage_toggle()` | Get massage toggle status. |
| `powerclean_check()` | Check PowerClean status. |
| `remove_module(module)` | Remove a module. |
| `reset_default()` | Reset to default settings. |
| `reset_factory()` | Reset to factory settings. |
| `reset_users()` | Reset all user settings. |
| `bt_disconnect()` | Disconnect Bluetooth. |
| `upload_firmware(file_path)` | Upload firmware file (multipart POST). |

### Diagnostics

| Method | Description |
|---|---|
| `controller_error_logs()` | Get controller error logs. |
| `konnect_error_logs()` | Get Konnect error logs. |
| `reset_controller_faults()` | Clear controller error logs. |
| `reset_konnect_faults()` | Clear Konnect error logs. |

### Error Handling

The library raises `KohlerError` when communication with the device fails unexpectedly:

```python
from kohler import Kohler, KohlerError

kohler = Kohler(kohler_host="192.168.1.50")

try:
    kohler.system_info()
except KohlerError as e:
    print(f"Device communication error: {e}")
```

## Contributing

```bash
# Clone and install dev dependencies
git clone https://github.com/niemyjski/kohler-python.git
cd kohler-python
pip install -e ".[dev]"

# Run checks
ruff check .          # Lint
ruff format --check . # Format check
mypy kohler/          # Type check
pytest -v             # Tests
```

## Disclaimer

**USE AT YOUR OWN RISK.** This library interacts with a physical water, steam, and electrical device (Kohler DTV+). The authors and contributors of this library are NOT affiliated with Kohler Co. and are NOT responsible for any damage, leaks, burns, flooding, or hardware failures that may occur from the use of this software. You are solely responsible for setting safe maximum temperatures and using this integration safely.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
