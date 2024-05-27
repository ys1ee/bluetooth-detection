def rssi_to_distance(rssi, A=-59, n=2):
    """
    Calculate the distance based on the received signal strength indicator (RSSI) value.

    Parameters:
        rssi (int): The received signal strength indicator value.
        A (float, optional): The reference signal strength value. Defaults to -59.
        n (float, optional): The exponent value. Defaults to 2.

    Returns:
        float: The calculated distance in meters. If the RSSI value is 0, returns -1.0.
    """

    if rssi == 0:
        return -1.0  # if we cannot determine distance, return -1.
    distance = 10 ** ((A - rssi) / (10 * n))
    return distance

class BLEDevice():
    def __init__(self, addr, name="", company=0, dis=0):
        self.addr = addr
        self.name = name
        self.company = company
        # self.isAuth = 0
        self.dis = dis
        self.sus = 1

    def printInfo(self, rssi=None):
        print(f"Addr: {self.addr}\nName: {self.name}\nCompany: {self.company}")
        if rssi:
            print(f"RSSI: {rssi} dBm\nEstimated Dis: {rssi_to_distance(rssi)} m")

    def addFind(self, findDict, rssi) -> dict:
        new_dis = rssi_to_distance(rssi)
        if self.addr in findDict:
            new_dis = rssi_to_distance(rssi)
            ratio = (new_dis-self.dis)/self.dis*100
            if new_dis > 10:
                findDict[self.addr]["Sus"] = 0
                findDict[self.addr]["Dis"] = 0

            if new_dis <= 5 or -10 <= ratio <= 10:
                findDict[self.addr]["Sus"] += 1
            else:
                findDict[self.addr]["Sus"] -= 1

            findDict[self.addr]["Dis"] = new_dis

        if self.addr not in findDict and new_dis <= 10:
            findDict[self.addr] = {"Name": self.name, "Company": self.company, "Dis": self.dis, "Sus": 1}

        return findDict


    def checkAuth(self, authDict) -> bool:
        return self.addr in authDict
