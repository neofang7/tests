from re import split
import sys
import os
import types
from pathlib import Path
import csv


def merge_fio_csv(csv1, label1, csv2, label2, output_csv):
    csv1_path = Path(csv1)
    with csv1_path.open('r', encoding='utf-8') as data1_f:
        csv1_data = list(csv.reader(data1_f))
    csv2_path = Path(csv2)
    with csv2_path.open('r', encoding='utf-8') as data2_f:
        csv2_data = list(csv.reader(data2_f))

    output = []
    # create label
    # Write a new label line
    # WORKLOAD,bw_r,bw_r,bw_w,bw_w,IOPS_r,IOPS_r,IOPS_w,IOPS_w
    # ,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata
    label_line = []
    label_line_2 = []
    label_line.append(csv1_data[0][0])

    # set label_line_2[0] like 'libaio'
    # todo revoke the hardcode of 'libaio'.
    idx = csv1_data[1][0].find('-libaio')
    print(idx)
    if idx != -1:
        label_line_2.append('libaio')
    else:
        label_line_2.append("")
        idx = 0

    for i in range(1, len(csv1_data[0])):
        label_line.append(csv1_data[0][i])
        label_line.append(csv1_data[0][i])
        label_line_2.append(label1)
        label_line_2.append(label2)
    # writer.writerow(label_line)
    print(label_line)
    print(label_line_2)
    output.append(label_line)
    output.append(label_line_2)

    for i in range(1, len(csv1_data)):
        line = []
        idx = csv1_data[i][0].find('-libaio')
        line.append(csv1_data[i][0][:idx])
        for j in range(1, len(csv1_data[i])):
            line.append(csv1_data[i][j])
            line.append(csv2_data[i][j])

        output.append(line)

    output_path = Path(output_csv)
    with output_path.open('w', encoding='utf-8') as data3_f:
        writer = csv.writer(data3_f)
        for i in output:
            writer.writerow(i)

# To merge most of csv files.


def merge_csv(csv1, csv2, output_csv):
    csv1_path = Path(csv1)
    with csv1_path.open('r', encoding='utf-8') as data1_f:
        csv1_data = list(csv.reader(data1_f))
    csv2_path = Path(csv2)
    with csv2_path.open('r', encoding='utf-8') as data2_f:
        csv2_data = list(csv.reader(data2_f))

    output = []
    csv1_idx = 0
    for i in csv1_data:
        if i[0] == "Item":
            csv1_idx = csv1_idx + 1
            break
        output.append(i)
        csv1_idx = csv1_idx + 1

    # Write a new label line as "Env", "Tdx", "None-Tdx"
    label_line = ["WORKLOAD", "Tdx CC", "Legacy Kata", "Units"]
    # writer.writerow(label_line)
    output.append(label_line)

    csv2_idx = csv1_idx
    for i in range(csv1_idx, len(csv1_data)):
        line = []
        line.append(csv1_data[i][0])
        line.append(csv1_data[i][1])
        line.append(csv2_data[i][1])
        line.append(csv1_data[i][2])
        output.append(line)

    output_path = Path(output_csv)
    with output_path.open('w', encoding='utf-8') as data3_f:
        writer = csv.writer(data3_f)
        for i in output:
            writer.writerow(i)


if __name__ == '__main__':
    src1_dir = sys.argv[1]
    src2_dir = sys.argv[2]
    dst_dir = sys.argv[3]

    if not os.path.exists(src1_dir) or not os.path.exists(src2_dir):
        print("Error: {} or {} does not exist. Ignore it." %
              (src1_dir, src2_dir))
        exit

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    # parse and merge.
    for root, dirs, files in os.walk(src1_dir):
        for f in files:
            src1_filename = src1_dir + '/' + f
            src2_filename = src2_dir + '/' + f
            if not os.path.exists(src2_filename):
                print('Warning: {} does not exist'.format(src2_filename))
                continue
            dst_filename = dst_dir + '/' + f
            if f[:3] == "fio":
                merge_fio_csv(src1_filename, 'TDX CC',
                              src2_filename, 'Legacy Kata', dst_filename)
            else:
                merge_csv(src1_filename, src2_filename, dst_filename)

    # merge_csv('tdx-output/boot-times.csv', 'ccv0-output/boot-times.csv', 'merge-output/boot-times.csv')
    # merge_csv('tdx-output/memory-footprint.csv', 'ccv0-output/memory-footprint.csv', 'merge-output/memory-footprint.csv')
    # merge_csv('tdx-output/memory-footprint-inside-container.csv', 'ccv0-output/memory-footprint-inside-container.csv', 'merge-output/memory-footprint-inside-container.csv')
    # merge_csv('tdx-output/mlc.csv', 'ccv0-output/mlc.csv', 'merge-output/mlc.csv')
    # merge_csv('tdx-output/blogbench.csv', 'ccv0-output/blogbench.csv', 'merge-output/blogbench.csv')
    # merge_csv('tdx-output/memory-footprint-ksm.csv', 'ccv0-output/memory-footprint-ksm.csv', 'merge-output/memory-footprint-ksm.csv')
