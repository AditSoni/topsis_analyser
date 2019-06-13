from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from topsisapp import column_name,pipeline
import os



# Create your views here.
def index(request):
	context={}
	if request.method=='POST':

		uploaded_file = request.FILES['data']
		fs = FileSystemStorage()
		if os.path.exists(settings.MEDIA_ROOT+'/'+uploaded_file.name):#deletes pre existing file with same name
			os.remove(settings.MEDIA_ROOT+'/'+uploaded_file.name)
		fs.save('data.csv',uploaded_file)
		m=str(request.POST['m'])

		w=str(request.POST['w'])
		column=column_name.get_columns(settings.MEDIA_ROOT+'/'+'data.csv')

		context['columns']=column

		file=open(settings.MEDIA_ROOT+'/'+'parameters.txt','w+')
		file.write(m+'\n')
		file.write(w)
		file.close()

		result=pipeline.pipeline()


		context['result']=result

	return render(request,'topsisapp/index.html',context)
