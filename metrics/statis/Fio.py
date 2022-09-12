import os
import csv
import pandas as pd


class FioCases:
    def __init__(self):
        pass

    # fio test case has generated the csv file.
    # we need to rename different fio case csv file like fio_64_64k.csv, and set vertical table.
    # deprecated.
    def to_csv(self, in_dir, out_dir):
        for iter in next(os.walk(in_dir)):
            if isinstance(iter, list):
                for i in iter:
                    print(i)
                    if i[0:4] == "fio_":
                        in_csv = in_dir+i+'/results.csv'
                        out_csv = out_dir+i+'.csv'
                        print(out_csv)
                        # read the csv file, set table as vertical, write to fio_*.csv
                        try:
                            with open(in_csv, 'r', encoding='utf-8') as in_f:
                                f_data = list(csv.reader(in_f))
                        except FileNotFoundError as e:
                            print(e)

                        out_f = open(out_csv, 'w+', encoding='utf-8')
                        wr = csv.writer(out_f)

                        for row in f_data:
                            wr.writerow(row[1:])

    def to_csv_vertical(self, directory, out_dir):
        for iter in next(os.walk(directory)):
            if isinstance(iter, list):
                for i in iter:
                    print(i)
                    if i[0:4] == "fio_":
                        in_csv = directory+i+'/results.csv'
                        out_csv = out_dir+i+'.csv'
                        print(out_csv)
                        # read the csv file, set table as vertical, write to fio_*.csv
                        df = pd.read_csv(in_csv)
                        data = df.values
                        data = list(map(list, zip(*data)))
                        data = pd.DataFrame(data)
                        data.to_csv(out_csv, header=0, index=0)
