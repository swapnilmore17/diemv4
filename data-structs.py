class TimeoutInfo:
    def __init__(self,round,high_qc):
        self.round = round
        self.high_qc = high_qc
        ###
        self.sender=u
        self.signature = hash(round,high_qc.round)
    
class TC:
    def __init__(self,round):
        #####
        self.round=round