from MetricsCase import MetricsCase

class Blogbench:
    def __init__(self):
        self.MetricsCase = MetricsCase()
        
    def load_from_jsonfile(self, file_name):
        return self.MetricsCase.load_from_jsonfile(file_name, 'blogbench')
        
    def to_csv(self, file_name):
        self.MetricsCase.to_csv_with_labels_vertical(file_name, ['write', 'read'])
