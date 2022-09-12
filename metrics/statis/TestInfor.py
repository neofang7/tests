from ast import List


class TestInfor:
    def __init__(self):
        self.Contents = {}

    def print_myself(self):
       for k in self.Contents:
            print('{}:{}'.format(k, self.Contents[k]))

    # json_dict: load the json file inside a dict.
    def load_from_dict(self, json_dict):
        if type(json_dict) is not dict:
            print("Invalid data format of json, not a dict")
            return

        for k in json_dict['env'].keys():
            self.Contents[k] = json_dict['env'][k]
        self.Contents['Date'] = json_dict['date']['Date']
        self.Contents['runtime'] = json_dict['test']['runtime']
        self.Contents['testname'] = json_dict['test']['testname']
        return

    def write_to_csv(self, writer):
        writer.writerow(['Env', 'Value'])
        for k in self.Contents:
            writer.writerow([k, self.Contents[k]])


class Elem:
    def __init__(self, name):
        self.Name = name
        self.Result = 0.0
        self.Units = ""

    def print_myself(self):
        print('{}: {}{}'.format(self.Name, self.Result, self.Units))


class Config:
    def __init__(self):
       self.Contents = {}


class ConfigList:
    def __init__(self):
        self.configs = []

    def load_from_dict(self, json_list):
        if type(json_list) is not list:
            print('Not a list.', type(json_list))
            return
        print(json_list)
        self.configs = json_list
        return

    def write_to_csv(self, writer):
        #print(self.configs)
        writer.writerow(self.configs[0].keys())
        for i in self.configs:
            writer.writerow(i.values())
        return
