import asyncio
from bleak import BleakScanner
from utils import *
import json
import yaml

COMPANY_IDENTIFIER = './constants/company_identifiers.yaml'
AUTH_LIST_PATH = './private/AuthDeviceDict.json'

def get_auth_BLE_device() -> dict:
    """
    Reads the private/AuthDeviceDict.json file and returns its contents as a dictionary.

    Returns:
        dict: The contents of the private/AuthDeviceDict.json file as a dictionary.
        If the file does not exist, an empty dictionary is returned.
    """

    try:
        with open(AUTH_LIST_PATH, 'r') as f:
            d = json.load(fp = f)
        return d
    except:
        return {}

def update_auth_BLE_device(authDict):
    """
    Updates the authentication device dictionary and writes it to the private/authDeviceDict.json file.

    Parameters:
        authDict (dict): The authentication device dictionary to be updated.

    Returns:
        None
    """

    json.dump(authDict, open(AUTH_LIST_PATH,'w'))
    print('AuthDeviceDict UPDATED !!')

async def discover_devices(companyIdentifier):
    """
    Discovers nearby Bluetooth devices and updates the authentication device dictionary.

    Args:
        companyIdentifier (dict): A dictionary mapping company codes to company names.

    Returns:
        None
    """

    authDict = get_auth_BLE_device()
    print("Scanning for nearby Bluetooth devices...")
    devices = await BleakScanner.discover(return_adv=True)
    print(f"Found {len(devices)} devices")
    for device, data in devices.values():
        c_code = None
        temp = list(data.manufacturer_data.keys())
        # manchenlee: 我這邊的manufacturer_data只會有一個key，所以這樣寫

        if len(temp) == 1:
            c_code = temp[0]
        new = BLEDevice(device.address, device.name,
                        company = companyIdentifier[c_code] if c_code else c_code)
        new.printInfo(data.rssi)
        authDict = new.checkAuth(authDict)
    update_auth_BLE_device(authDict)

def add_auth_BLE_device(companyIdentifier):
    authDict = get_auth_BLE_device()
    try:
        addr = input('Please input MAC address of the BLE device: ')
        name = input('Please input Name of the BLE device: ')
        c_code = input('Please input Company Code of the BLE device: ')
        if not c_code.isnumeric():
            print('Warning: Company code should be an integer!! The value of company will be None.')
            c_code = None
        else:
            c_code = int(c_code)
        #print(type(c_code))
        #print(companyIdentifier)
        new = BLEDevice(addr, name,
                    company = companyIdentifier[c_code] if c_code else c_code)
        new.printInfo()
        authDict[new.addr] = {"Name": new.name, "Company": new.company}
        update_auth_BLE_device(authDict)
        return 1
    except:
        #print(msg)
        return 0

def delete_auth_BLE_device():
    authDict = get_auth_BLE_device()
    try:
        addr = input('Please input MAC address of the BLE device: ')
        authDict.pop(addr)
        update_auth_BLE_device(authDict)
        return 1
        #break
    except:
        print('Error: This MAC address is not in AuthDeviceDict !!')
        return 0
        #continue

def main():
    with open(COMPANY_IDENTIFIER, 'r', encoding="utf-8") as stream:
        f = yaml.safe_load(stream)
    f = f['company_identifiers']
    companyIdentifier = {}
    for i in range(len(f)):
        companyIdentifier[i] = f[i]['name']

    while True:
        print('===== Welcome to BLE tracker !! =====')
        print('1. Start scanning')
        print('2. Add authenticated BLE device')
        print('3. Remove unauthenticated BLE device')
        print('4. Exit')
        while True:
            try:
                choice = int(input('Your choice: '))
                if choice > 4 or choice < 1:
                    raise ValueError('Error: Please input an integer which ranges from 1 to 4 !!')
                break
            except ValueError as msg:
                print(msg)
                continue
        match choice:
            case 1:
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(discover_devices(companyIdentifier))
            case 2:
                    if add_auth_BLE_device(companyIdentifier):
                        print('===== Add successed !! =====')
                    else:
                        print("===== Add failed !! =====")
            case 3:
                    if delete_auth_BLE_device():
                        print('===== Remove successed !! =====')
                    else:
                        print("===== Remove failed !!=====")
            case 4:
                    print('===== Good bye !! =====')
                    exit(0)


if __name__ == "__main__":
    main()