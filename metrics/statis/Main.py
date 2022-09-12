from re import split
import sys
import os
import types
from MemoryFootprint import MemoryFootprint
from Blogbench import Blogbench
from BootTimes import BootTimes
from NetworkIperf3 import NetworkIperf3
from MemoryFootprintInsideContainer import MemoryFootprintInsideContainer
from MemoryFootprintKsm import MemoryFootprintKsm
from Mlc import Mlc
from MlcFull import MlcFull
from Fio import FioCases


def filename_to_classname(file_name, postfix):
    #remove .py
    #file_name = file_name[:-3]
    strs = file_name[:-len(postfix)].split('-')
    class_name = ""
    for s in strs:
        class_name += s.capitalize()
    return class_name


if __name__ == '__main__':
    # parse folder and get the generated json files.
    args = sys.argv[1:]
    result_path = args[0]
    output_path = './output/'

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    root = ""
    for iter in next(os.walk(args[0])):
        print("next:{} {}".format(iter, type(iter)))
        if isinstance(iter, str):
            root = iter
            continue
        if len(iter) == 0:
            continue
        for f in iter:
            print(root+f)
            if f.endswith('.json'):
                class_name = filename_to_classname(f, '.json')
                if class_name not in globals().keys():
                    print('Unsupported class ', class_name)
                    continue
                class_type = globals()[class_name]
                obj = class_type()
                if obj.load_from_jsonfile(root+'/'+f) == 0:
                    obj.to_csv(output_path+f[:-5]+'.csv')

    # Handle results/fio_xx_xx
    fio = FioCases()
    fio.to_csv(result_path, output_path)

    # for root, dirs, files in os.walk(args[0]):
    #     for f in files:
    #         print(root)
    #         if not f.endswith('.json'):
    #             continue
    #         #class_type = (globals()['BootTimes'])
    #         class_name = filename_to_classname(f, '.json')
    #         if class_name not in globals().keys():
    #             print('Unsupported class ', class_name)
    #             continue
    #         class_type = globals()[class_name]
    #         obj = class_type()
    #         if obj.load_from_jsonfile(root+'/'+f) == 0:
    #             obj.to_csv(output_path+f[:-5]+'.csv')
