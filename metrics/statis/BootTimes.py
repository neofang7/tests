from MetricsCase import MetricsCase
import csv
from TestInfor import TestInfor, Elem, ConfigList


class BootTimes:
    def __init__(self):
        self.MetricsCase = MetricsCase()

    def load_from_jsonfile(self, file_name):
        return self.MetricsCase.load_from_jsonfile(file_name, 'boot-times')

    def to_csv(self, file_name):
        # Need to calc average.
        # self.MetricsCase.to_csv(file_name)
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.MetricsCase.TestInfor.write_to_csv(writer)
            if self.MetricsCase.Configs != None:
                self.MetricsCase.Configs.write_to_csv(writer)

            label_line = ['Item', 'Result', 'Units']
            writer.writerow(label_line)

            keys = self.MetricsCase.Results[0].keys()

            res = {}
            res['total'] = 0.0
            res['to-workload'] = 0.0
            res['in-kernel'] = 0.0
            res['to-kernel'] = 0.0
            res['to-quit'] = 0.0

            for i in self.MetricsCase.Results:
                res['total'] = res['total'] + i['total']['Result']
                res['to-workload'] = res['to-workload'] + \
                    i['to-workload']['Result']
                res['in-kernel'] = res['in-kernel'] + i['in-kernel']['Result']
                res['to-kernel'] = res['to-kernel'] + i['to-kernel']['Result']
                res['to-quit'] = res['to-quit'] + i['to-quit']['Result']

            unit = self.MetricsCase.Results[0]['total']['Units']
            res['total'] = "{:.3f}".format(
                res['total']/len(self.MetricsCase.Results))
            row = []
            row.append('total')
            row.append(str(res['total']))
            row.append(unit)
            writer.writerow(row)

            res['to-workload'] = "{:.3f}".format(
                res['to-workload']/len(self.MetricsCase.Results))
            row.clear()
            row.append('to-workload')
            row.append(str(res['to-workload']))
            row.append(unit)
            writer.writerow(row)

            res['in-kernel'] = "{:.3f}".format(
                res['in-kernel']/len(self.MetricsCase.Results))
            row.clear()
            row.append('in-kernel')
            row.append(str(res['in-kernel']))
            row.append(unit)
            writer.writerow(row)

            res['to-kernel'] = "{:.3f}".format(
                res['to-kernel']/len(self.MetricsCase.Results))
            row.clear()
            row.append('to-kernel')
            row.append(str(res['to-kernel']))
            row.append(unit)
            writer.writerow(row)

            res['to-quit'] = "{:.3f}".format(res['to-quit'] /
                                             len(self.MetricsCase.Results))
            row.clear()
            row.append('to-quit')
            row.append(str(res['to-quit']))
            row.append(unit)
            writer.writerow(row)
