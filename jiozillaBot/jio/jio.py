import hashlib

class Jio:
    def __init__(self, creatorId, jioName, jioStart, jioEnd, jioLocation, orgId):
        self.orgId = orgId
        self.creatorId = creatorId
        self.jioName = jioName
        self.jioId = int(hashlib.sha1(jioName.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        self.jioStart = jioStart
        self.jioEnd = jioEnd
        self.jioLocation = jioLocation

