from MetricsCase import MetricsCase

class MemoryFootprintKsm:
    def __init__(self):
        self.MetricsCase = MetricsCase()
        
    def load_from_jsonfile(self, file_name):
        return self.MetricsCase.load_from_jsonfile(file_name, 'memory-footprint-ksm')
        
    def to_csv(self, file_name):
        self.MetricsCase.to_csv(file_name)