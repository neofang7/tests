#!/bin/sh

TDX_RESULTS="tdx-results"
LEGACY_RESULTS="legacy-results"
TDX_OUTPUT="tdx-output"
LEGACY_OUTPUT="legacy-output"

if [ -d ${TDX_OUTPUT} ];
then
    rm -rf ${TDX_OUTPUT}
fi

if [ -d ${LEGACY_OUTPUT} ];
then
    rm -rf ${LEGACY_OUTPUT}
fi

python3 statis/GenCsv.py tdx-results/
python3 statis/GenCsv.py legacy-results/
python3 statis/MergeCsv.py legacy-output/ tdx-output/ merge-output/
python3 statis/WriteToPdf.py