from MetricsCase import MetricsCase

class Mlc:
    def __init__(self):
        self.MetricsCase = MetricsCase()
        
    def load_from_jsonfile(self, file_name):
        return self.MetricsCase.load_from_jsonfile(file_name, 'mlc')
        
    def to_csv(self, file_name):
        self.MetricsCase.to_csv(file_name)