class ScanConfirmation:
    def __init__(self):
        self.PIN = None
        self.ProviderID = None
        self.UserID = None
        self.Status = None

    def getPIN(self):
        return self.PIN

    def setPIN(self, PIN):
        self.PIN = PIN

    def getProviderID(self):
        return self.ProviderID

    def setProviderID(self, providerID):
        self.ProviderID = providerID

    def getUserID(self):
        return self.UserID

    def setUserID(self, userID):
        self.UserID = userID

    def getStatus(self):
        return self.Status

    def setStatus(self, status):
        self.Status = status

    def __str__(self):
        return f"ScanConfirmation{{'PIN': '{self.PIN}', 'ProviderID': '{self.ProviderID}', 'UserID': '{self.UserID}', 'Status': '{self.Status}'}}"
