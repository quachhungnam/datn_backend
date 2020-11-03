import pandas as pd
from pandas import ExcelFile


# def add_student_db(file_student):
#     try:
#         df = pd.read_excel(file_student, sheet_name=0)
#         return df
#     except:
#         print('error')
#         pass

Cars_Path = 'D:/ds10a2.xlsx'
df = pd.read_excel(Cars_Path, sheet_name=0, index_col=0)

# df = add_student_db(Cars_Path)

print(df)
print(df.head(4))  # lay 4 dong dau tien
row_col=df.shape #in ra so luong dong va cot
print(row_col[0])
print(df.at[0,'A'])
# df.to_excel('D:/output.xlsx')