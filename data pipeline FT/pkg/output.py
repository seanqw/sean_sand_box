import pandas as pd
import os

def save_csv(data:pd.DataFrame, month:str, path:str=None):
    name = f'Tractor_Summary_BISUSA-{month}.csv'
    data.to_csv(name, index=False)
    return name
    # if not path: # save to current folder
    #     df.to_csv(name, index=False)
    
    # else:
    #     if not os.path.exists(path):  #create folder if not exist
    #         os.makedirs(path)
    #         print(f"Created output folder: {path}")

    #     output_full_path = os.path.join(path, name)
    #     df.to_csv(output_full_path, index=False)

if __name__ == '__main__':
    test = pd.read_csv('test.csv')
    save_csv(test, 'test')