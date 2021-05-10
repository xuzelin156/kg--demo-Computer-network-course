import pandas as pd
import codecs
df = pd.read_csv('./disizhang_object.csv',encoding='utf-8')
title = df[' "x" '].values

with codecs.open('./disizhang_object.txt', 'w',encoding='utf-8') as f:
    for t in title[1:]:
        print(t)
        f.write(t + ' ' + 'nz' + '\n')