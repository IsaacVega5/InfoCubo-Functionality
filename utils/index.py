import pandas as pd
def read_idex_list():
    index_file = pd.read_csv('./indexTable.csv', sep=';')
    keys = index_file.keys()
    print(keys[0])