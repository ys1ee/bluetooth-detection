

def rssi_to_distance(rssi, A=-59, n=2):
        if rssi == 0:
            return -1.0  # if we cannot determine distance, return -1.
        distance = 10 ** ((A - rssi) / (10 * n))
        return distance

class BLEDevice():
    def __init__(self, addr, name="", company=0, isAuth=None):
        self.addr = addr
        self.name = name
        self.company = company
        self.isAuth = isAuth
    
    def printInfo(self, rssi):
        print(f"Addr: {self.addr}\n Name: {self.name}\n RSSI: {rssi} dBm\n Dis: {rssi_to_distance(rssi)} m")

    def checkAuth(self, authDict):
        if self.addr in authDict:
            print("The BLE device \"{}\" has been in authDeviceList!!".format(self.addr))
            self.isAuth = 1
            return authDict
        else:
            while True:
                try:
                    t = input('Is the BLE device \"{}\" authenticated? (0/1)'.format(self.addr))
                    if len(t) != 1 or not t.isnumeric():
                        #print(t)
                        raise ValueError('Error: Please input 0(False) or 1(True)!!')
                    elif t.isnumeric() and (int(t) != 0 and int(t) != 1):
                        raise ValueError('Error: Please input 0(False) or 1(True)!!')
                    else: 
                        break
                except ValueError as msg:
                    print(msg)
                    continue
            isAuth = int(t)
            self.isAuth = isAuth
            if isAuth:
                authDict[self.addr] = {"Name": self.name, "Company": self.company}
            return authDict
            