from pkg.file_path import get_fuel_file, get_mile_file
from pkg.read_file import read_file, Df, transfrom_file, imperial_metric, static_col, get_df
from pkg.sql_conn import query
from pkg.output import save_csv
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import pandas as pd
import numpy as np
import os


# get files name
def get_data():
    fuel_path = get_fuel_file()  
    fuel = read_file(fuel_path) #(,df,)

    mile_path = get_mile_file()
    mile = read_file(mile_path) #(,df,)

    #fuel_df = Df(fuel)
    #mile_df = Df(mile)
    return fuel, mile

def get_Df(fuel, mile):

    return get_df(fuel), get_df(mile)

# month on file name
def check_month(fuel_df, mile_df):
    '''
    input fuel, mile data class; output monyr and mon abb strings
    '''
    if fuel_df.get_month() == mile_df.get_month():
        month_start = fuel_df.get_month()
        month_abb = fuel_df.month
        return month_start, month_abb
    else:
        print('Unmathced month')

# Transfrom & merge data

def transfrom_merge(fuel, mile):
    f = imperial_metric(transfrom_file(fuel))
    m = imperial_metric(transfrom_file(mile))
    fuel_mile = pd.merge(f, 
                         m, 
                         how='outer',
                         on=['Tractor','State']).fillna(0)

    fuel_mile['KPL'] = fuel_mile.groupby('Tractor')['Total Kilometers'].transform('sum') / fuel_mile.groupby('Tractor')['Fuel Liters'].transform('sum')
    fuel_mile['KPL'] = fuel_mile['KPL'].replace([np.inf, -np.inf], 0).fillna(0)

    fuel_mile['Litres Burned'] = (fuel_mile['Total Kilometers'] / fuel_mile['KPL']).replace([np.inf, -np.inf], 0).fillna(0)

    fuel_mile = static_col(fuel_mile)
    return fuel_mile

# IFTA
def get_tax_rate(month_start):
    ifta = query(month_start)
    ifta['Tax Rate'] = ifta['Tax Rate'].astype('float64')
    return ifta

def main():
    try:
        print('Reading Data...')
        fuel, mile = get_data()
        print('Instanciate Dataframe...')
        fuel_df, mile_df = get_Df(fuel, mile)
        print('Checking File...')
        month_start, month_abb = check_month(fuel_df, mile_df)
        print('Transfrom and Merge...')
        fuel_mile = transfrom_merge(fuel_df, mile_df)
        print('Query Tax Rate...')
        ifta = get_tax_rate(month_start=month_start)
        print('Consolidate Tax Rate...')
        fuel_mile = pd.merge(fuel_mile, ifta, how='left', left_on='State', right_on='state')
        fuel_mile = fuel_mile.fillna(0)
        print('Calculate Tax Amount...')
        fuel_mile['Tax Amount'] = fuel_mile['Litres Burned'] * fuel_mile['Tax Rate']
        print('Generating Output Dataframe...')
        output_columns = ['Tractor', 'Country', 'State', 'Tax Rate', 'Total Kilometers', 'Taxable Kilometers','Toll Kilometers','Fuel Liters','Litres Burned','Fuel Type','Tax Amount','KPL','revtype1']
        output = fuel_mile[output_columns]
        print('Save File...')
        file_name = save_csv(data=output, month=month_abb)
        print('File In Place \n')
        print(f'Report: {file_name}')
        print(f'Output path: {os.getcwd()}')
        print(f'IFTA month {month_start}')
        print(f'Output KM {int(output['Total Kilometers'].sum())}; Original KM {int(Df.mile_km(mile_df.total()))}')
        print(f'Output Liters {int(output['Fuel Liters'].sum())}; Original Liter {int(Df.gallon_l(fuel_df.total()))}')
        print(f'Please scrutinize output data, such as null and error value before import to system \nEND')
    except Exception as ex:
        print(f'Error Encountered: {ex}')
        raise ex # for GUI


if __name__ == '__main__':
    main()