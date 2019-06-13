import pandas as p

def get_columns(file):
	file=p.read_csv(file)
	file=file.drop([file.columns[0]],axis=1) # renoving first column
	column=list(file.columns)
	
	return column
