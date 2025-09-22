import pandas as pd
import warnings
from datetime import datetime
warnings.filterwarnings("ignore") 

def read_file(path:str)->dict:
    '''
    input file name in string
    output (type, pd.DataFrame, monthyear)
    '''
    try:
        return (path.split('-')[2][:4], pd.read_excel(path,header=0), path.split('-')[1]) #(type, df, monyear)

    except Exception as ex:
        print(f'Error: {ex}')
        return ('Error', ex)


class Df():
    def __init__(self, dataset:tuple):
        self.df = dataset[1]  # the pd.DataFrame
        self.type = dataset[0]  # 'Fuel' or 'Mile'
        self.month = dataset[2] # month string: MonYear

    def get_month(self):
        input_format  = "%b%Y"
        output_format = "%m-%d-%Y"
        date_object = datetime.strptime(self.month, input_format)
        month = date_object.strftime(output_format)
        return month

    def get_name(self):
        return self.type
    
    def get_columns(self):
        col = self.df.columns.tolist()
        del col[1]
        return col
    
    def get_state(self):
        state = self.df.columns.tolist()[2:]
        return state
    
    def get_type(self):
        return self.df.columns.tolist()[1]
    
    def total(self):
        return self.df[self.get_type()].sum()
    
    @staticmethod
    def gallon_l(gal):
        return gal * 3.78541 if gal>=0 else 0
    
    @staticmethod
    def mile_km(mile):
        return mile * 1.60934 if mile>=0 else 0


def ny_replace(df:pd.DataFrame):
    df['State'] = df['State'].replace({'NY Toll':'NY'}) #if fuel will be skipped
    return df

def get_df(read_file):
    return Df(read_file)

def transfrom_file(Df_)->pd.DataFrame:
    '''Input Df, out put unpivot data'''
    #df_ = Df(readfile)
    data_type = Df_.get_type()
    state = Df_.get_state()
    df1 = Df_.df.drop(columns=[data_type]) # remove total
    df_melt = ny_replace(pd.melt(df1,
                                 id_vars='Tractor',
                                 value_vars=state,
                                 var_name='State',
                                 value_name=data_type))
    df_melt = df_melt.groupby(['Tractor','State']).sum(data_type).reset_index()
    return (df_melt, Df_.get_name())


def imperial_metric(data):
    df = data[0]
    if data[1] == 'Fuel':
        df['Fuel Liters'] = df['Total Gallons'].apply(Df.gallon_l)
        return df[df['Total Gallons']!=0]  # remove none 0 rows
    elif data[1] == 'Mile':
        df['Total Kilometers'] = df['Total Miles'].apply(Df.mile_km)
        df['Taxable Kilometers'] = df['Total Miles'].apply(Df.mile_km)
        return df[df['Total Miles']!=0]    # remove none 0 rows
    else:
        return 'Error'


def static_col(df):
    df['Country'] = 'USA'
    df['revtype1'] = 'BISUSA'
    df['Toll Kilometers'] = 0
    df['Fuel Type'] = 'DSL' 
    return df

