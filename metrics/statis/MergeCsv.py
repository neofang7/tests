from re import split
import sys
import os
import types
from pathlib import Path
import csv


def merge_fio_bw_csv(legacy_csv, legacy_label, tdx_csv, tdx_label, output_csv):
    legacy_path = Path(legacy_csv)
    with legacy_path.open('r', encoding='utf-8') as data1_f:
        legacy_data = list(csv.reader(data1_f))
    tdx_path = Path(tdx_csv)
    with tdx_path.open('r', encoding='utf-8') as data2_f:
        tdx_data = list(csv.reader(data2_f))

    output = []
    column_ends = 3
    # create label
    # Write a new label line
    # WORKLOAD,bw_r,bw_r,bw_w,bw_w,IOPS_r,IOPS_r,IOPS_w,IOPS_w
    # ,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata
    workload_label_line = []
    container_label_line = []
    workload_label_line.append(legacy_data[0][0])

    # set label_line_2[0] like 'libaio'
    # todo revoke the hardcode of 'libaio'.
    idx = legacy_data[1][0].find('-libaio')
    print(idx)
    if idx != -1:
        container_label_line.append('libaio')
    else:
        container_label_line.append("")
        idx = 0

    # for i in range(1, len(legacy_data[0])):
    for i in range(1, column_ends):
        print(legacy_data[0][i])
        workload_label_line.append(legacy_data[0][i])
        workload_label_line.append(legacy_data[0][i])
        container_label_line.append(legacy_label)
        container_label_line.append(tdx_label)
        container_label_line.append('Ratio')
    # writer.writerow(label_line)
    print(f"workload label: {workload_label_line}")
    print(container_label_line)
    output.append(workload_label_line)
    output.append(container_label_line)

    for i in range(1, len(legacy_data)):
        line = []
        idx = legacy_data[i][0].find('-libaio')
        line.append(legacy_data[i][0][:idx])
        # for j in range(1, len(legacy_data[i])):
        for j in range(1, column_ends):
            line.append(legacy_data[i][j])
            line.append(tdx_data[i][j])
            if float(legacy_data[i][j]) < sys.float_info.epsilon:
                line.append(0.0)
            else:
                ratio = round(
                    float(tdx_data[i][j])/float(legacy_data[i][j]) * 100, 2)
                line.append(str(ratio)+"%")
        output.append(line)

    output_path = Path(output_csv)
    with output_path.open('w', encoding='utf-8') as data3_f:
        writer = csv.writer(data3_f)
        for i in output:
            writer.writerow(i)


def merge_fio_iops_csv(legacy_csv, legacy_label, tdx_csv, tdx_label, output_csv):
    legacy_path = Path(legacy_csv)
    with legacy_path.open('r', encoding='utf-8') as data1_f:
        legacy_data = list(csv.reader(data1_f))
    tdx_path = Path(tdx_csv)
    with tdx_path.open('r', encoding='utf-8') as data2_f:
        tdx_data = list(csv.reader(data2_f))

    output = []
    column_start = 3
    # create label
    # Write a new label line
    # WORKLOAD,bw_r,bw_r,bw_w,bw_w,IOPS_r,IOPS_r,IOPS_w,IOPS_w
    # ,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata
    workload_label_line = []
    container_label_line = []
    workload_label_line.append(legacy_data[0][0])

    # set label_line_2[0] like 'libaio'
    # todo revoke the hardcode of 'libaio'.
    idx = legacy_data[1][0].find('-libaio')
    print(idx)
    if idx != -1:
        container_label_line.append('libaio')
    else:
        container_label_line.append("")
        idx = 0

    for i in range(column_start, len(legacy_data[0])):
        print(legacy_data[0][i])
        workload_label_line.append(legacy_data[0][i])
        workload_label_line.append(legacy_data[0][i])
        container_label_line.append(legacy_label)
        container_label_line.append(tdx_label)
        container_label_line.append('Ratio')
    # writer.writerow(label_line)
    print(f"workload label: {workload_label_line}")
    print(container_label_line)
    output.append(workload_label_line)
    output.append(container_label_line)

    for i in range(1, len(legacy_data)):
        line = []
        idx = legacy_data[i][0].find('-libaio')
        line.append(legacy_data[i][0][:idx])
        for j in range(column_start, len(legacy_data[i])):

            line.append(round(float(legacy_data[i][j]), 2))
            line.append(round(float(tdx_data[i][j]), 2))
            if float(legacy_data[i][j]) < sys.float_info.epsilon:
                line.append(0.0)
            else:
                ratio = round(
                    float(tdx_data[i][j])/float(legacy_data[i][j]) * 100, 2)
                line.append(str(ratio)+"%")
        output.append(line)

    output_path = Path(output_csv)
    with output_path.open('w', encoding='utf-8') as data3_f:
        writer = csv.writer(data3_f)
        for i in output:
            writer.writerow(i)


def merge_fio_csv(legacy_csv, legacy_label, tdx_csv, tdx_label, output_csv):
    legacy_path = Path(legacy_csv)
    with legacy_path.open('r', encoding='utf-8') as data1_f:
        legacy_data = list(csv.reader(data1_f))
    tdx_path = Path(tdx_csv)
    with tdx_path.open('r', encoding='utf-8') as data2_f:
        tdx_data = list(csv.reader(data2_f))

    output = []
    # create label
    # Write a new label line
    # WORKLOAD,bw_r,bw_r,bw_w,bw_w,IOPS_r,IOPS_r,IOPS_w,IOPS_w
    # ,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata,TDX CC,Legacy Kata
    workload_label_line = []
    container_label_line = []
    workload_label_line.append(legacy_data[0][0])

    # set label_line_2[0] like 'libaio'
    # todo revoke the hardcode of 'libaio'.
    idx = legacy_data[1][0].find('-libaio')
    print(idx)
    if idx != -1:
        container_label_line.append('libaio')
    else:
        container_label_line.append("")
        idx = 0

    for i in range(1, len(legacy_data[0])):
        workload_label_line.append(legacy_data[0][i])
        workload_label_line.append(legacy_data[0][i])
        container_label_line.append(legacy_label)
        container_label_line.append(tdx_label)
        container_label_line.append('Ratio')
    # writer.writerow(label_line)
    print(workload_label_line)
    print(container_label_line)
    output.append(workload_label_line)
    output.append(container_label_line)

    for i in range(1, len(legacy_data)):
        line = []
        idx = legacy_data[i][0].find('-libaio')
        line.append(legacy_data[i][0][:idx])
        for j in range(1, len(legacy_data[i])):
            line.append(legacy_data[i][j])
            line.append(round(tdx_data[i][j], 2))
            if float(legacy_data[i][1]) < sys.float_info.epsilon:
                line.append(0.0)
            else:
                ratio = round(
                    float(tdx_data[i][1])/float(legacy_data[i][1]) * 100, 2)
                line.append(str(ratio)+"%")
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
    label_line = ["WORKLOAD", "Legacy Kata", "Tdx CC", "Ratio", "Units"]
    # writer.writerow(label_line)
    output.append(label_line)

    csv2_idx = csv1_idx
    for i in range(csv1_idx, len(csv1_data)):
        line = []
        line.append(csv1_data[i][0])
        line.append(csv1_data[i][1])
        line.append(csv2_data[i][1])
        print(csv1_data[i][1])
        if float(csv2_data[i][1]) < sys.float_info.epsilon:
            line.append(0.0)
        else:
            ratio = round(float(csv2_data[i][1]) /
                          float(csv1_data[i][1]) * 100, 2)
            line.append(str(ratio)+"%")
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
            if f[:3] == "fio":
                dst_filename = dst_dir + '/bw_' + f
                merge_fio_bw_csv(src1_filename, 'Legacy',
                                 src2_filename, 'TDX', dst_filename)
                dst_filename = dst_dir + '/iops_' + f
                merge_fio_iops_csv(src1_filename, 'Legacy',
                                   src2_filename, 'TDX', dst_filename)
            else:
                dst_filename = dst_dir + '/' + f
                merge_csv(src1_filename, src2_filename, dst_filename)

    # merge_csv('tdx-output/boot-times.csv', 'ccv0-output/boot-times.csv', 'merge-output/boot-times.csv')
    # merge_csv('tdx-output/memory-footprint.csv', 'ccv0-output/memory-footprint.csv', 'merge-output/memory-footprint.csv')
    # merge_csv('tdx-output/memory-footprint-inside-container.csv', 'ccv0-output/memory-footprint-inside-container.csv', 'merge-output/memory-footprint-inside-container.csv')
    # merge_csv('tdx-output/mlc.csv', 'ccv0-output/mlc.csv', 'merge-output/mlc.csv')
    # merge_csv('tdx-output/blogbench.csv', 'ccv0-output/blogbench.csv', 'merge-output/blogbench.csv')
    # merge_csv('tdx-output/memory-footprint-ksm.csv', 'ccv0-output/memory-footprint-ksm.csv', 'merge-output/memory-footprint-ksm.csv')
