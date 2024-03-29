# libraries to be imported 
import smtplib 
from django.conf import settings
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 




def mail(mail):   
	fromaddr = "TopsisAnalyser"
	toaddr = mail
	   
	# instance of MIMEMultipart 
	msg = MIMEMultipart() 
	  
	# storing the senders email address   
	msg['From'] = fromaddr 
	  
	# storing the receivers email address  
	msg['To'] = toaddr 
	  
	# storing the subject  
	msg['Subject'] = "Topsis Analysis"
	  
	# string to store the body of the mail 
	body = "We make choosing the best model easier.\nThank you for Using our services.\n\nHere is the result file\n"
	  
	# attach the body with the msg instance 
	msg.attach(MIMEText(body, 'plain')) 
	  
	# open the file to be sent  
	filename = "TopsisResult.csv"
	attachment = open(settings.MEDIA_ROOT+'/results/'+'TopsisResult.csv', "rb") 
	  
	# instance of MIMEBase and named as p 
	p = MIMEBase('application', 'octet-stream') 
	  
	# To change the payload into encoded form 
	p.set_payload((attachment).read()) 
	  
	# encode into base64 
	encoders.encode_base64(p) 
	   
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
	  
	# attach the instance 'p' to instance 'msg' 
	msg.attach(p) 
	  
	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	  
	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login("yourmail", "password") 
	  
	# Converts the Multipart msg into a string 
	text = msg.as_string() 
	  
	# sending the mail 
	s.sendmail(fromaddr, toaddr, text) 
	  
	# terminating the session 
	s.quit()