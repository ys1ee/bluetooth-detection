import asyncio
from bleak import BleakScanner
from utils import *

def rssi_to_distance(rssi, A=-59, n=2):
    if rssi == 0:
        return -1.0  # if we cannot determine distance, return -1.

    distance = 10 ** ((A - rssi) / (10 * n))
    return distance

def checkAuth(device):
    while True:
        try:
            t = input('Is the BLE device authenticated? (0/1)')
            if len(t) != 1 or (not t.isnumeric()):
                #print(t)
                raise ValueError('Please input 0(False) or 1(True)!!')
            elif t.isnumeric() and (int(t) != 0 and int(t) != 1):
                raise ValueError('Please input 0(False) or 1(True)!!')
            else: 
                break
        except ValueError as msg:
            print(msg)
            continue
    device.isAuth = int(t)
    return device

async def discover_devices():
    print("Scanning for nearby Bluetooth devices...")
    devices = await BleakScanner.discover(return_adv=True)

    print(f"Found {len(devices)} devices")

    for device, data in devices.values():
        print(f"Addr: {device.address}, RSSI: {data.rssi} dBm, Dis: {rssi_to_distance(data.rssi)} m")
        temp = BLEDevice(device.address)
        temp = checkAuth(temp)
        print(temp.isAuth)
        # print(type(device), device)
        # print(type(data), data)
        # print()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_devices())
