# LEDSC Python library

Library for communicate with [ledsc](https://ledsc.eu).

## Examples

### Setting colors

```python
import time
import logging
from pymodbus.client import ModbusSerialClient
from ledsc import LedSC

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    modbus_client = ModbusSerialClient(port='/dev/ttyUSB1', baudrate=19200)
    lsc = LedSC(modbus_client=modbus_client, unit=1)
    lsc.set_transition_time(0.1)

    lsc.set_white(100)
    time.sleep(2)
    lsc.set_rgbw(red=100, green=20, blue=40, white=0)
```


