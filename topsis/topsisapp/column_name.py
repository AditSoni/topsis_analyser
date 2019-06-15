

def get_columns(file,n=1):
	fp=open(file)
	name=[]
	if n==1:
		x=0
		for line in fp:
			if x==0:
				x=1
				continue
			l=line.split(',')
			name.append(l[0])
	else:
		for line in fp:
			l=line.strip()
			l=l.split(',')
			name=l[1:]
			name
			break

	return name