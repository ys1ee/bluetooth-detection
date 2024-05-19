import asyncio
from bleak import BleakScanner

def rssi_to_distance(rssi, A=-59, n=2):
    if rssi == 0:
        return -1.0  # if we cannot determine distance, return -1.

    distance = 10 ** ((A - rssi) / (10 * n))
    return distance

async def discover_devices():
    print("Scanning for nearby Bluetooth devices...")
    devices = await BleakScanner.discover(return_adv=True)

    print(f"Found {len(devices)} devices")

    for device, data in devices.values():
        print(f"Addr: {device.address}, RSSI: {data.rssi} dBm, Dis: {rssi_to_distance(data.rssi)} m")
        # print(type(device), device)
        # print(type(data), data)
        # print()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_devices())
