from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from topsisapp import column_name
import os



# Create your views here.
def index(request):
	context={}
	if request.method=='POST':

		uploaded_file = request.FILES['data']
		fs = FileSystemStorage()
		if os.path.exists(settings.MEDIA_ROOT+'/'+uploaded_file.name):#deletes pre existing file with same name
			os.remove(settings.MEDIA_ROOT+'/'+uploaded_file.name)
		fs.save(uploaded_file.name,uploaded_file)
		m=str(request.POST['m'])

		w=str(request.POST['w'])
		column=column_name.get_columns(settings.MEDIA_ROOT+'/'+uploaded_file.name)

		context['columns']=column

		print(m,w)

	return render(request,'topsisapp/index.html',context)
