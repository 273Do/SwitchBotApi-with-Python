import binascii
import asyncio
from bleak import BleakClient
import sys


def get_command(operation):
    """指定された操作に基づいてコマンドバイナリを返す"""
    if operation == "turnoff":
        return b"\x57\x0f\x50\x01\x01\x00"
    elif operation == "turnon":
        return b"\x57\x0f\x50\x01\x01\x80"
    elif operation == "toggle":
        return b"\x57\x0f\x50\x01\x02\x80"
    elif operation == "readstate":
        return b"\x57\x0f\x51\x01"
    else:
        return None

def switchbotplugmini(address, operation):
    """! switchbotplugmini brief.
    Turn Off, Turn On, Toggle, Read State the SwitchBot Plug Mini
    @param address  : BLE MAC Address
    @param operation: turnoff/turnon/toggle/readstate
    @return         : result(True/False)
                      resp(RESP message(0x0100:Off, 0x0180:On) or 0x0000)
    """

    #RX characteristic UUID of the message from the Terminal to the Device
    RX_CHARACTERISTIC_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
    #TX characteristic UUID of the message from the Device to the Terminal
    TX_CHARACTERISTIC_UUID = "cba20003-224d-11e6-9fb8-0002a5d5c51b"
    
    result = True
    resp = b"\x00\x00"

    def callback(sender: int, data: bytearray):
        #print(f"{sender}: {data}")
        nonlocal resp
        resp = data

    async def run(loop):
        async with BleakClient(address, loop=loop) as client:
            await client.start_notify(TX_CHARACTERISTIC_UUID, callback)
            await client.write_gatt_char(RX_CHARACTERISTIC_UUID, bytearray(command), response=True)
            await asyncio.sleep(0.5)
            await client.stop_notify(TX_CHARACTERISTIC_UUID)

    command = get_command(operation)
    if command is None:
        print("ERROR, <turnoff/turnon/toggle/readstate>")
        return False, resp[0]

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run(loop))
    except:
        print(sys.exc_info())
        result = False
    finally:
        asyncio.set_event_loop(None)
        loop.close()
        return result, resp

def main():
    # if len(sys.argv) != 3:
    #     print("ERROR, python switchbotplugmini.py <BLE ADDRESS> <turnoff/turnon/toggle/readstate>")
    #     sys.exit(1)

    address = "DEVICE_BLE_MAC_ADDRESS"
    operation = "toggle" # on off の切り替え

    result, resp = switchbotplugmini(address, operation)
    if result:
        if resp == b"\x01\x80":
            print(result, binascii.hexlify(resp), "on")
        elif resp == b"\x01\x00":
            print(result, binascii.hexlify(resp), "off")
        else:
            print(result, binascii.hexlify(resp)) 
        sys.exit(0) #result==True, exit(0)
    else:
        print(result, binascii.hexlify(resp))
        sys.exit(1)

if __name__ == "__main__":
    main()
