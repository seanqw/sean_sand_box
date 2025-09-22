from pathlib import Path
import os
import pandas as pd

def get_fuel_file(path=os.getcwd()):
    '''
    input a path string like: C:\\Users\\sshan\\Notebook\\USA IRP
    output a file name in string
    '''
    fuel_suffix = 'FuelByStateByTractor.xlsx'
    if not path:
        folder_path = os.getcwd()
    else:
        folder_path = path


    for file_name in Path(folder_path).iterdir():
        if file_name.is_file() and file_name.name.endswith(fuel_suffix):
            return file_name.name
    else:
        return 'fuel file not found'
    


def get_mile_file(path=os.getcwd()):
    '''
    input a path string like: C:\\Users\\sshan\\Notebook\\USA IRP
    output a file name in string
    '''
    mile_suffix = 'MilesByStateByTractor.xlsx'
    if not path:
        folder_path = os.getcwd()
    else:
        folder_path = path

    for file_name in Path(folder_path).iterdir():
        if file_name.is_file() and file_name.name.endswith(mile_suffix):
            return file_name.name
    else:
        return 'mile file not found'


