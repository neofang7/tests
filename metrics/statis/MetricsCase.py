import json
import csv
from pathlib import Path
from TestInfor import TestInfor, Elem, ConfigList


class Result:
    def __init__(self):
        self.results = {}


class MetricsCase:
    def __init__(self):
        self.TestInfor = TestInfor()
        self.Configs = None
        self.Results = []

    def load_from_jsonfile(self, file_name, result_label):
        json_path = Path(file_name)
        with json_path.open('r', encoding='utf-8') as data_f:
            try:
                data = json.loads(data_f.read())
            except ValueError:
                print("Decoding json failure.")
                return -1
        self.TestInfor.load_from_dict(data)

        self.load_from_dict(data[result_label])
        return 0

    def load_from_dict(self, json_dict):
        if 'Config' in json_dict.keys():
            self.Configs = ConfigList()
            self.Configs.load_from_dict(json_dict['Config'])

        if 'Results' not in json_dict.keys() == 0:
            print(json_dict.keys())
            return

        self.Results = json_dict['Results']

        # for d in self.Results:
        #     row = []
        #     for i in d.keys():
        #         if 'Units' not in d[i].keys():
        #             row.append(str(d[i]['Result']))
        #         else:
        #             row.append(str(d[i]['Result']) + d[i]['Units'])
        #     print(row)

        return

    def to_csv(self, file_name):
        # with open(file_name, 'a') as csv_file:
        #     writer = csv.writer(csv_file)
        #     self.TestInfor.write_to_csv(writer)
        #     if self.Configs != None:
        #         self.Configs.write_to_csv(writer)

        #     # write label:
        #     writer.writerow(self.Results[0].keys())
        #     # write contents:
        #     for d in self.Results:
        #         row = []
        #         for i in d.keys():
        #             if 'Units' not in d[i].keys():
        #                 row.append(str(d[i]['Result']))
        #             else:
        #                 row.append(str(d[i]['Result']) + d[i]['Units'])
        #         writer.writerow(row)
        #self.to_csv_with_labels(file_name, None)
        self.to_csv_vertical(file_name)

    def to_csv_with_labels(self, file_name, labels):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            if self.Configs != None:
                self.Configs.write_to_csv(writer)

            # write label:
            label_line = []
            if labels != None:
                for l in self.Results[0].keys():
                    if l in labels:
                        label_line.append(l)
            else:
                label_line = self.Results[0].keys()
            writer.writerow(label_line)
            # write contents:
            for d in self.Results:
                row = []
                for i in d.keys():
                    if labels is not None and i not in labels:
                        continue
                    if 'Units' not in d[i].keys():
                        row.append(str(d[i]['Result']))
                    else:
                        row.append(str(d[i]['Result']) + d[i]['Units'])
                writer.writerow(row)

    def to_csv_vertical(self, file_name):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            if self.Configs != None:
                self.Configs.write_to_csv(writer)

            label_line = ['Item', 'Result', 'Units']
            writer.writerow(label_line)

            # for r in self.Results:
            r = self.Results[0]
            #print(len(self.Results))

            for i in r.keys():
                row = [i]
                row.append(str(r[i]['Result']))
                row.append(r[i]['Units'])
                writer.writerow(row)

    def to_csv_with_labels_vertical(self, file_name, labels):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.TestInfor.write_to_csv(writer)
            if self.Configs != None:
                self.Configs.write_to_csv(writer)

            # write label:
            writer.writerow(['Item', 'Result', 'Units'])

            for r in self.Results:
                for l in labels:
                    if l in r.keys():
                        row = []
                        row.append(l)
                        row.append(str(r[l]['Result']))
                        row.append(r[l]['Units'])
                        writer.writerow(row)

            # if labels != None:
            #     for l in self.Results[0].keys():
            #         if l in labels:
            #             label_line.append(l)
            # else:
            #      label_line = self.Results[0].keys()
            # #writer.writerow(label_line)
            # # write contents:

            # for d in self.Results:
            #     row = []
            #     for i in d.keys():
            #         if labels is not None and i not in labels:
            #             continue
            #         if 'Units' not in d[i].keys():
            #             row.append(str(d[i]['Result']))
            #         else:
            #             row.append(str(d[i]['Result']) + d[i]['Units'])
            #     writer.writerow(row)
