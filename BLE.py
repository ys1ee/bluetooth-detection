import asyncio
from bleak import BleakScanner
from utils import *
import json
import argparse

AUTH_LIST_PATH = './private/authDeviceList.json'

def get_auth_BLE_device():
    try:
        with open(AUTH_LIST_PATH, 'r') as f:
            d = json.load(fp = f)
        return d
    except:
        return {}

def update_auth_BLE_device(authDict):
    json.dump(authDict, open(AUTH_LIST_PATH,'w'))
    print('authDeviceList UPDATED !!')

async def discover_devices():
    authDict = get_auth_BLE_device()
    print("Scanning for nearby Bluetooth devices...")
    devices = await BleakScanner.discover(return_adv=True)
    print(f"Found {len(devices)} devices")
    for device, data in devices.values():
        company = None
        temp = list(data.manufacturer_data.keys())
        if len(temp) == 1:
            company = temp[0]
        new = BLEDevice(device.address, device.name, company)
        new.printInfo(data.rssi)
        authDict = new.checkAuth(authDict)
    update_auth_BLE_device(authDict)
        

if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_devices())
