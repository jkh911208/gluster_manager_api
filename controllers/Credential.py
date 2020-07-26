class Credential(object):
    def __init__(self, db):
        self.collection = db.set_collection("credential")
