import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from topsisapp import column_name,topsis,mailer




# Create your views here.
def index(request):
	context={}
	if request.method=='POST':

		uploaded_file = request.FILES['data']
		fs = FileSystemStorage()
		if os.path.exists(settings.MEDIA_ROOT+'/'+uploaded_file.name):#deletes pre existing file with same name
			os.remove(settings.MEDIA_ROOT+'/'+uploaded_file.name)
		fs.save('data.csv',uploaded_file)
		
		context['file']='done'

	return render(request,'topsisapp/index.html',context)


def setpara(request):
	
	column=column_name.get_columns(settings.MEDIA_ROOT+'/'+'data.csv',2)
	context={}
	
	
	param=list(enumerate(column))
	context['column']=param
	
	if request.method=='POST':
		i1=[]
		w1=[]
		for i in range(len(column)):
			i1.append(float(request.POST['m%d'%i]))
			w1.append(float(request.POST['w%d'%i]))

		email=request.POST['email']
		with open(settings.MEDIA_ROOT+'/'+'emails.txt','a') as fe:
	 		fe.write(email+'\n')

		score=topsis.topsys(settings.MEDIA_ROOT+'/'+'data.csv',w1,i1)
		mnames=column_name.get_columns(settings.MEDIA_ROOT+'/'+'data.csv',1)
		temp_list=score
		temp_list=sorted(temp_list)
		ranks={}
		temp_list=list(set(temp_list))
		temp_list=list(enumerate(temp_list))
		for i,r in temp_list:
			s=str(r)
			ranks[s]=i+1

		zipped=zip(mnames,score)
		#creating file to be mailed
		with open(settings.MEDIA_ROOT+'/'+'TopsisResult.csv','w') as fp:
			fp.write('Model_Name,Score,Rank\n')

			for i,j in zipped:
				print(i,j)
				s1=i+','+str(j)+','+str(ranks[str(j)])+'\n'
				fp.write(s1)



		mailer.mail(email)
		context['score']=score
		

		




		
	return render(request,'topsisapp/setpara.html',context) 