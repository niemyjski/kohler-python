# kohler-python

Python library for talking to Kohler devices (DTV+)

## Installation

```cmd
pip3 install kohler
```

## Usage

```python
from kohler import Kohler
kohler = Kohler(bondIp='192.168.1.50')

kohler.lightOn(1, 50)
kohler.musicOn()
kohler.quickShower()
kohler.stopShower()
kohler.steamOn()
kohler.steamOff()
```
