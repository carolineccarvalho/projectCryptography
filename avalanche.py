import pandas as pd

df = pd.read_csv('teste.csv',on_bad_lines='skip', sep=",")

print(df['anonimizado'])