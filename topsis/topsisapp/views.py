import os
import time
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from topsisapp import column_name,topsis,mailer




# Create your views here.
def index(request):
	context={}

	context['sample']=settings.MEDIA_ROOT+'\\sample\\'+'data.csv'


	
	if request.method=='POST':
		

		if 'data' in request.FILES.keys(): # for uploading!!!
			
			uploaded_file = request.FILES['data']
			fs = FileSystemStorage()
			try:
				if os.path.exists(settings.MEDIA_ROOT+'/uploads/'+'data.csv'):#deletes pre existing file with same name
					os.remove(settings.MEDIA_ROOT+'/uploads/'+'data.csv')
					os.remove(settings.MEDIA_ROOT+'/uploads/'+'dat1.csv')

			except:
				pass
			
			fs.save('./uploads/data.csv',uploaded_file)

			column=column_name.get_columns(settings.MEDIA_ROOT+'/uploads/'+'data.csv',2)
			param=list(enumerate(column))
			context['column']=param
			context['upload']='done'
			



		if 'email' in request.POST.keys(): # parametersss
			
		# extracting max/min and weights from form
			column=column_name.get_columns(settings.MEDIA_ROOT+'/uploads/'+'data.csv',2)
			param=list(enumerate(column))
			i1=[]
			w1=[]
			for i in range(len(column)):
				i1.append(float(request.POST['m%d'%i]))
				w1.append(float(request.POST['w%d'%i]))

			email=request.POST['email']
			with open(settings.MEDIA_ROOT+'/'+'emails.txt','a') as fe:
				fe.write(email+'\n')
				# passing the uploaded file nad weights into our topsis function
			score=topsis.topsys(settings.MEDIA_ROOT+'/uploads/'+'data.csv',w1,i1)
			mnames=column_name.get_columns(settings.MEDIA_ROOT+'/uploads/'+'data.csv',1)
			temp_list=score

			ranks={}
			temp_list=list(set(temp_list))
			temp_list=sorted(temp_list,reverse=True)
			temp_list=list(enumerate(temp_list))
			for i,r in temp_list:
				s=str(r)
				ranks[s]=i+1

			zipped=zip(mnames,score)
			#creating file to be mailed
			with open(settings.MEDIA_ROOT+'/results/'+'TopsisResult.csv','w') as fp:
				fp.write('Model_Name,Score,Rank\n')

				for i,j in zipped:
					s1=i+','+str(j)+','+str(ranks[str(j)])+'\n'
					fp.write(s1)



			mailer.mail(email)
			context['alert']='email sent'
		
			

	return render(request,'topsisapp/index.html',context)
