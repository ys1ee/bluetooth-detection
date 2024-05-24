class BLEDevice():
    def __init__(self, addr, isAuth=None):
        self.addr = addr
        self.isAuth = isAuth