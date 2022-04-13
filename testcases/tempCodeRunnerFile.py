file = 'fcomparaison.xlsx'
data = pd.ExcelFile(file)
print(data.sheet_names)  # this returns the all the sheets in the excel file
