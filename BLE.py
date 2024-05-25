import asyncio
from bleak import BleakScanner
from utils import *
import json
import argparse

AUTH_LIST_PATH = './private/authDeviceDict.json'

def get_auth_BLE_device():
    # 讀入 private/authDeviceDict.json -> dict
    # 如果是空檔案就回傳 empty dict
    try:
        with open(AUTH_LIST_PATH, 'r') as f:
            d = json.load(fp = f)
        return d
    except:
        return {}

def update_auth_BLE_device(authDict):
    # 寫入更新的 private/authDeviceDict.json
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
        # manchenlee: 我這邊的manufacturer_data只會有一個key，所以這樣寫
        if len(temp) == 1:
            company = temp[0]
        new = BLEDevice(device.address, device.name, company)
        new.printInfo(data.rssi)
        authDict = new.checkAuth(authDict)
    update_auth_BLE_device(authDict)
        

if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_devices())
