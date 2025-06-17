import requests
import json
from tkinter import *
import tkinter.ttk as ttk
import pandas as pd
from pandas import json_normalize

url : str = "http://127.0.0.1:8000/post-list"
response = requests.get(url)

contents = response.text
json_ob = json.loads(contents)
#print(json_ob)
body = json_ob['posts']
dataframe = json_normalize(body)
print(dataframe)

columns_data = dataframe.columns.tolist()
tree = ttk.Treeview()

tree['show'] = 'headings'
tree['columns'] = columns_data
for i in columns_data:
    tree.column(i,width=60,minwidth=60,anchor=CENTER)
    tree.heading(i,text=i,anchor=CENTER)
i=0

for ro in range(len(dataframe)):
    insert_data = []
    for column in range(len(columns_data)):
        insert_data.append(dataframe.iloc[ro][column])
    tree.insert('',i,text="",values=insert_data)
    i += 1

tree.pack()
mainloop()
