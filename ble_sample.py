import asyncio
from bleak import BleakScanner
import pprint

async def run():
    devices = await BleakScanner.discover(timeout=60)
    for d in devices:
        if d.address.lower()=="DEVICE_BLE_MAC_ADDRESS".lower():
            print(d)
            print(d.address, d.name, d.rssi)
            pprint.pprint(d.metadata)
        
asyncio.run(run())
