class User:
    def __init__(self, user_id, name, registered_on, email, rfid= None, lineToken = None):
        self.user_id = user_id
        self.name = name
        self.lineToken  = lineToken
        self.registered_on = registered_on
        self.email = email
        self.rfid = rfid

    def getName(self):
        return self.name

    def getID(self):
        return self.user_id

    def getLineNotifyToken(self):
        return self.lineToken

    def setLineNotifyToken(self,token):
        self.lineToken = tokenuser


