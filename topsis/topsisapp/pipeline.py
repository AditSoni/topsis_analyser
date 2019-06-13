import os 
from django.conf import settings

def pipeline():
	file=settings.MEDIA_ROOT+'/'+'data.csv'
	param=settings.MEDIA_ROOT+'/'+'parameters.txt'

	os.system("Rscript topsis.r %s %s"%(file,param))

	while True:
		if os.path.exists(settings.MEDIA_ROOT+'/'+'result.txt'):
			break

	return 

