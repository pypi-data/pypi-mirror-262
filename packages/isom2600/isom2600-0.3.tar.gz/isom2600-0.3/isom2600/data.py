import pandas as pd
import numpy as np

def stockindex():
    url = 'https://drive.google.com/file/d/1EpczybaLAzV053G8pG-kB38IXT7NC580/view?usp=sharing'
    data_path = 'https://drive.google.com/uc?export=download&id=' + url.split('/')[-2]
    df = pd.read_csv(data_path,index_col=0)
    df.index=pd.to_datetime(df.index)
    return df