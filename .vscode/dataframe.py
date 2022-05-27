import pandas as pd

print('pd version:'+str(pd.__version__))

dic = {
    "col 1": [1, 2, 3], 
    "col 2": [10, 20, 30],
    "col 3": list('xyz'),
    "col 4": ['a', 'b', 'c'],
    "col 5": pd.Series(range(3))
}
df = pd.DataFrame(dic)
print(df)

rename_dic = {"col 1": "x", "col 2": "10x"}
df.rename(rename_dic, axis=1)

print(df)

df.columns = ['x(new)', '10x(new)'] + list(df.columns[2:])

print(df)



