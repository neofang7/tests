from asyncore import write
from re import split
import sys
import os
import types

import csv
from fpdf import FPDF

# Merge tdx and ccv0 csvs to pdf.
# One case one page at least
# Two csv files of one case should be merged column by column or line by line.


def write_info_to_pdf(csv_file, pdf):
    with open(csv_file) as f:
        contents = list(csv.reader(f))
        page_width = pdf.w - 2*pdf.l_margin
        pdf.set_font('Times', '', 14.0)
        pdf.cell(page_width, 0.0, "Test Report", align='C')
        th = pdf.font_size
        pdf.ln(th)
        col_width = page_width/3
        for line in contents:
            if line[0] == "WORKLOAD":
                break
            pdf.cell(col_width, th, line[0], border=0)
            pdf.cell(col_width, th, line[1], border=0)
            pdf.ln(th)


def write_to_pdf(csv_file, head, pdf):
    try:
        f = open(csv_file, 'r')
    except FileNotFoundError as e:
        print("Ign: No such firle or directory: {}.".format(csv_file))
        return
    contents = list(csv.reader(f))
    page_width = pdf.w - 2*pdf.l_margin
    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(page_width, 0.0, head, align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
    col_width = page_width/3

    start = 0
    for line in contents:
        if line[0] == "WORKLOAD":
            break
        start = start + 1

    pdf.set_font('Courier', 'B', 13)
    th = pdf.font_size
    row = contents[start]
    for i in range(0, len(row)-1):
        pdf.cell(col_width, th, row[i], border=1)
    pdf.ln(th)

    for idx in range(start+1, len(contents)):
        pdf.set_font('Courier', 'B', 12)
        th = pdf.font_size
        row = contents[idx]
        # set cell format for row[0]
        pdf.cell(col_width, th, row[0] + '(' + row[-1] + ')', border=1)
        # pdf.ln(th)
        for j in range(1, len(row) - 1):
            pdf.set_font('Courier', '', 12)
            th = pdf.font_size
            pdf.cell(col_width, th, row[j], border=1)
        pdf.ln(th)

    pdf.ln(10)

def write_fio_to_pdf(csv_file, head, pdf):
    try:
        f = open(csv_file, 'r')
    except FileNotFoundError as e:
        print("Ign: No such firle or directory: {}.".format(csv_file))
        return
    contents = list(csv.reader(f))
    page_width = pdf.w - 2*pdf.l_margin
    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(page_width, 0.0, head, align='C')
    pdf.ln(10)

    start = 0
    label_line = contents[0]
    columns = len(label_line)
    cc_line = contents[1]
    col_width = int(page_width/columns)

    pdf.set_font('Courier', 'B', 11)
    th = pdf.font_size
    pdf.cell(col_width, th, label_line[0], border=1)
    for i in range(1, len(label_line)):
        if i%2 == 0:
            continue
        pdf.cell(col_width*2, th, label_line[i], border=1, align='C')

    pdf.ln(th)
    pdf.set_font('Courier', 'B', 8)
    for i in cc_line:
        pdf.cell(col_width, th, i, border=1, align='C')
    pdf.ln(th)
    #pdf.cell(col_width, th, cc_line, border=1)

    for idx in range(2, len(contents)):
        pdf.set_font('Courier', 'B', 10)
        th = pdf.font_size
        row = contents[idx]
        # set cell format for row[0]
        pdf.cell(col_width, th, row[0], border=1)
        # pdf.ln(th)
        for j in range(1, len(row)):
            pdf.set_font('Courier', '', 10)
            th = pdf.font_size
            data = str(round(float(row[j]), 2))
            pdf.cell(col_width, th, data, border=1, align = 'R')
        pdf.ln(th)

    pdf.ln(10)

if __name__ == '__main__':
    # parse folder and get the generated json files.
    args = sys.argv[1:]
    pdf = FPDF()
    # example to write boot-times csv to a pdf.
    pdf.add_page()
    write_info_to_pdf('merge-output/boot-times.csv', pdf)
    pdf.add_page()
    write_to_pdf('merge-output/boot-times.csv', 'Boot Time', pdf)
    write_to_pdf('merge-output/blogbench.csv', 'Blogbench', pdf)
    write_to_pdf('merge-output/memory-footprint.csv', 'Memory Footprint', pdf)
    write_to_pdf('merge-output/memory-footprint-inside-container.csv',
                 'Memory Footprint Inside Container', pdf)
    write_to_pdf('merge-output/memory-footprint-ksm.csv',
                 'Memory Footprint KSM', pdf)
    pdf.add_page()
    write_to_pdf('merge-output/mlc.csv', 'MLC', pdf)
    write_to_pdf('merge-output/mlc-full.csv', 'MLC Full', pdf)

    pdf.add_page()
    write_fio_to_pdf('merge-output/fio_64_4k.csv', 'Fio 64 4K Metrics', pdf)
    write_fio_to_pdf('merge-output/fio_64_64k.csv', 'Fio 64 64K Metrics', pdf)

    pdf.output('Metrics_Test_Report.pdf', 'F')
