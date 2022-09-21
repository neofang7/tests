import csv
from MetricsCase import MetricsCase

class Mlc:
    def __init__(self):
        self.MetricsCase = MetricsCase()
        
    def load_from_jsonfile(self, file_name):
        return self.MetricsCase.load_from_jsonfile(file_name, 'mlc')
        
    def to_csv(self, file_name):
        #self.MetricsCase.to_csv(file_name)
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.MetricsCase.TestInfor.write_to_csv(writer)
            if self.MetricsCase.Configs != None:
                self.MetricsCase.Configs.write_to_csv(writer)

            label_line = ['Item', 'Result', 'Units']
            writer.writerow(label_line)

            # for r in self.Results:
            r = self.MetricsCase.Results[0]
            #print(len(self.Results))

            for i in r.keys():
                workload = i.replace('Local', 'L')
                row = [workload]
                row.append(str(r[i]['Result']))
                row.append(r[i]['Units'])
                writer.writerow(row)