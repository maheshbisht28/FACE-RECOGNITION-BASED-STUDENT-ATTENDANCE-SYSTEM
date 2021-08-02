from django.views import generic, View

#from .models import attendance1 , new1, new2
#from operator import attrgetter
from django.shortcuts import render
import numpy as np
from .forms import attformmytech, attform,Img ,Registrationformstudent , Registrationformteacher, createclass  , Editprofile,trainface
import  time
from django.http import HttpResponse
from imutils.video import VideoStream
import base64
from .models import User,Attendance ,createclasstime,course,subject
import os
import face_recognition
import argparse
import pickle
import cv2
import numpy as np
from PIL import Image
import io
import pandas as pd
from django.contrib import messages
import datetime
from django.db.models import Sum, Count
from itertools import chain
from django.core.files import File
from django.http import QueryDict
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT  = os.path.join(module_dir, 'media')


		
def studprofile(request):
	stud=User.objects.filter(is_student='True')
	cour=course.objects.all()
	subj=subject.objects.all()
	print("stud ",stud)

	return render(request,"studprofile.html",{'stud':stud,'cour':cour,'subj':subj})		

def studprofilecheck(request):
	print(request.POST)
	print(request.method =='POST')
	if request.method =='POST':	
		qry = request.POST
		print(qry)
		print(request.POST.get('User'))
		#mydict=qrydict.dict()
		subj=request.POST.get('subject')
		usr=request.POST.get('User')
		cour=request.POST.get('course')
		att=Attendance.objects.all()
		if usr == '0000':
			usr=User.objects.filter(is_student='True').values('id').distinct()
			test=[user for user in usr ]
			usr=[t['id'] for t in test ]
			# att=Attendance.objects.filter(user_id__in=test1)
			# print(att,"usr")
		if subj == '0000':
			subj=Attendance.objects.values('subject_id').distinct()
			test=[sub for sub in subj ]
			subj=[t['subject_id'] for t in test ]
			# att=Attendance.objects.filter(subject_id__in=test1)
			# print(att,"subj")
		if cour == '0000':
			cour=Attendance.objects.values('course_id').distinct()
			test=[cou for cou in cour ]
			cour=[t['course_id'] for t in test ]

		print("usr ",usr)
		print("cour ",cour)
		print("subj ",subj)
		#print(User.objects.filter(id__in=usr,course_id__in=cour).values('id','roll_no','first_name','last_name','course','email'))#.order_by('course'))
		student=User.objects.filter(id__in=usr,course_id__in=cour).values('id',
		'roll_no','first_name','last_name','course','email')#.order_by('course')
		print("student ",student)
		test=[]
		final=[]
		for st in student:
			print("st ",st)
			newdict={}
			
			# udata=User.objects.filter(id=t['user']).values('first_name','last_name','roll_no','course').first()
			# sdata=subject.objects.filter(id=t['subject']).values('s_name').first()
			cdata=course.objects.filter(id=st['course']).values('c_name').first()
			# print("udata ",udata)
			# print("sdata ",sdata)
			print("cdata ",cdata)
			newdict.update(st)
			# newdict.update(udata)
			# newdict.update(sdata)
			newdict.update(cdata)
			if bool(newdict):
				final.append(newdict)
			# test=[]
		print("final ",final)		
		# print("test ",test)					

		return render(request,"studprofilecheck.html",{'final':final})



		# test=[]
		# final=[]
		# for s in subj:
		# 	fi=Attendance.objects.filter(subject_id=s,user_id__in=usr,course_id__in=cour).values('user','subject','course').annotate(dcount=Count('subject'))
			
		# 	newdict={}
		# 	print("fi ",fi)
		# 	for t in fi:
		# 		print(t)
		# 		udata=User.objects.filter(id=t['user']).values('first_name','last_name','roll_no','course').first()
		# 		sdata=subject.objects.filter(id=t['subject']).values('s_name').first()
		# 		cdata=course.objects.filter(id=t['course']).values('c_name').first()
		# 		print("udata ",udata)
		# 		print("sdata ",sdata)
		# 		print("cdata ",cdata)
		# 		newdict.update(t)
		# 		newdict.update(udata)
		# 		newdict.update(sdata)
		# 		newdict.update(cdata)
		# 	if bool(newdict):
		# 		final.append(newdict)
		# 	# test=[]
		# print("final ",final)		
		# print("test ",test)					

		

	else:
		return render(request,"showatt.html")

		

def showattbydate(request):
	print(request.POST)
	print(request.method =='POST')
	if request.method =='POST':
		if request.user.is_student:
			subid=request.POST.get('subject')
			att=Attendance.objects.filter(user_id=request.user.id,subject_id=subid).values('classtime','actualclasstime').order_by('-classtime')
			cltime=createclasstime.objects.filter(course_id=request.user.course_id,subject_id=subid).values('id','date').order_by('-date')
			#print(createclasstime.objects.filter(course_id=request.user.course_id,subject_id=subid).values('date').order_by('date'))
			print("cltime ",cltime)
			print("att ",att)
			finallist=[]
			for cl in cltime:
				flag=0
				for at in att:
					if cl['id'] == at['actualclasstime']:
						flag=1
						break
				if flag==1:
					finallist.append({'date':cl['date'],'status':True})
				else:
					finallist.append({'date':cl['date'],'status':False})
					
			print(finallist)	 		


			return render(request,"showattbydate.html",{'att':att,'cltime':cltime,'finallist':finallist})

		else:
			courid=request.POST.get('course')
			subid=request.POST.get('subject')
			userid=request.POST.get('user')
			print(type(courid))
			if len(subid)!=0:

				print(request.POST)
				
				
				
				print("sub ",subid)
				print("userid ",userid)
				print("courod ",courid)
				att=Attendance.objects.filter(user_id=userid,subject_id=subid).values('classtime','actualclasstime').order_by('-classtime')
				cltime=createclasstime.objects.filter(course_id=courid,subject_id=subid).values('id','date').order_by('-date')
				testing=createclasstime.objects.filter(course_id=courid,subject_id=subid).values('id','date')
				print("testing ",testing)
				#print(createclasstime.objects.filter(course_id=request.user.course_id,subject_id=subid).values('date').order_by('date'))
				print("att ",att)
				print("cltime ",cltime)
				finallist=[]
				for cl in cltime:
					flag=0
					for at in att:
						if cl['id'] == at['actualclasstime']:
							flag=1
							break
					if flag==1:
						finallist.append({'date':cl['date'],'status':True})
					else:
						finallist.append({'date':cl['date'],'status':False})
						
				print("final ",finallist)	 		

				return render(request,"showattbydate.html",{'finallist':finallist})
			else:
				messages.success(request,"No Class Attended ")
				return render(request,"showattbydate.html")

				

			

	else:
		return render(request,"showattbydate.html")
		
# def editprofile(request,pk):
# 	print("pk ",pk)
# 	objct = User.objects.get(pk=pk)
	
# 	form=Editprofile(instance=objct)
# 	print("form ",form)
# 	return render(request,"editprofile.html",{'form':form})
def editprofilebyteach(request):
	form=Editprofile(initial={'id':request.POST.get('id'),'first_name':request.POST.get('first_name'),'last_name':request.POST.get('last_name'),'email':request.POST.get('email')})
	print("from ",form)
	print("id ",request.POST.get('id'))
	return render(request,"editprofile.html",{'form':form})
def trainstudface(request,pk):
	if request.method == 'POST':
		knownEncodings=[]
		knownNames=[]
		print(Editprofile(request.POST))
		print("pk ",pk)
		form=Editprofile(request.POST,instance=User.objects.get(pk=pk))
		objct = User.objects.get(pk=pk)
		img1=request.POST.get('mydata1')
		img2=request.POST.get('mydata2')
		img3=request.POST.get('mydata3')
		img4=request.POST.get('mydata4')
		img5=request.POST.get('mydata5')
		# print(img1)

		print(img1 != None)
	
		if (img1 != None):
			lsimg=[]
			lsimg.append(request.POST.get('mydata1'))
			lsimg.append(request.POST.get('mydata2'))
			lsimg.append(request.POST.get('mydata3'))
			lsimg.append(request.POST.get('mydata4'))
			lsimg.append(request.POST.get('mydata5'))
			for img in lsimg:
				image_file = io.BytesIO(base64.b64decode(img))
				file = Image.open(image_file).convert('RGB')
				open_cv_image = np.array(file)
				open_cv_image = open_cv_image[:, :, ::-1].copy()
				rgb=cv2.cvtColor(open_cv_image,cv2.COLOR_BGR2RGB)
				boxes=face_recognition.face_locations(rgb,model='cnn')
				encodings=face_recognition.face_encodings(rgb,boxes)
				for encoding in encodings:
					knownEncodings.append(encodings)
					knownNames.append(objct.first_name)


			data={"encodings":knownEncodings,"names":knownNames} 		
			print("data ",data)
			f=open('encodingstesting',"wb")
			#print(f.read())
			f.write(pickle.dumps(data))
			f.close()
			file_path = os.path.join(module_dir,'encodingstesting')
			f=open(file_path,'rb')
			myfile = File(f)
			# print(myfile)
			user=User.objects.get(pk=pk)
			# print(user)
			# print(user.first_name)
			# user.first_name.save(request.POST.get('first_name'))
			#form.save()
			user.face_encoding.save('faceencodeing',myfile)
			print(file_path)
			messages.success(request,"Face Screen Shots are Successfully Submitted ")
		return render(request,"Stud_dashboard.html")	
	
	else:
		objct = User.objects.get(pk=pk)
		print("objct ",objct)
		form=Editprofile(instance=objct)
		return render(request,"trainstudface.html",{'form':form,'objct':objct})

def edituserprofile(request,pk):
	if request.method == 'POST':
		print(pk)
		form =Editprofile(request.POST,instance=User.objects.get(pk=pk))
		form1=Editprofile(request.POST)
		print("test ",form1)
		print(form)
		print("ob ",User.objects.get(pk=pk))
		obj=User.objects.get(pk=pk)
		print(obj)
		print(form.is_valid())
		


		print("form valid ",form.is_valid())

		if form.is_valid():
			form.save()
			print(form)
			messages.success(request,"Changes are Successfully Done")
			return render(request,"Stud_dashboard.html",)
		else:
			return render(request,"Stud_dashboard.html",)
			

	else:
		print("pk ",pk)
		objct = User.objects.get(pk=pk)
		print("obj ",objct)
		print("obj ",objct.is_student)
	
		form=Editprofile(instance=objct)
		print("form ",form)
		return render(request,"editprofile.html",{'form':form,'objct':objct})

def check(request):
	print("mahesh")
	print(request.POST)
	print(request.method =='POST')
	if request.method =='POST':
		if request.user.is_student:
			# print("mahesh",request.POST)
			qry = request.POST
			#mydict=qrydict.dict()
			print("qry",qry)
			print(request.user)
			subj=request.POST.get('subject')
			print("subjid",subj)
			if subj == '0000':
				subj=Attendance.objects.values('subject_id').distinct()
				print(subj)
				test=[sub for sub in subj ]
				print("test",test)
				subj=[t['subject_id'] for t in test ]
				print("subj",subj)

			att=Attendance.objects.filter(subject_id__in=subj,user_id=request.user.id,status='True').values('user','subject').annotate(dcount=Count('subject'))
			print("subj ",subj)
			print("att ",att)
			if att:
				
					
				subjid=[]	
				for sid in subj:
					test=Attendance.objects.filter(subject_id=sid,user_id=request.user.id,status='True').values('user','subject').annotate(dcount=Count('subject'))
					if test:
						subjid.append(test)
						print("test ",test)
				
				print(subjid)		


				student=[]
				count=[]
				test=[]
				sub=[]

				for (ur,sid) in  zip(att,subjid):
					print("ur ",ur)
					urr=User.objects.filter(id=ur['user']).values('first_name','last_name','roll_no')[0:1]
					sub=subject.objects.filter(id=ur['subject']).values('s_name')[0:1]
					#test=Attendance.objects.filter(subject_id=sid,user_id=request.user.id).values('user','subject').annotate(dcount=Count('subject'))
					print("urr ",urr)
					print("sub ",sub)
					print("sid ",sid)
					if sid:
						print("list ",list(chain(urr,sub,sid)))
					# qurydict=QueryDict('', mutable=True)
					# qurydict.update(ur)
					# print(qurydict)
						student.append(list(chain(urr,sub,sid)))

					count.append(ur['dcount'])
					#test.append(User.objects.filter())
					#print(Attendance.objects.filter(subject_id=sid,user_id=request.user.id).values('user','subject').annotate(dcount=Count('subject')))
				print(count)
				print(type(student))

				
				newstudent=[]

				for st in student:
					print(st)
					new_dict = {}
					for item in st:
						new_dict.update(item)
					print(new_dict)
					newstudent.append(new_dict)
				print("new ",newstudent)	
					



				classtimes=createclasstime.objects.filter(subject_id__in=subj,course_id=request.user.course_id)		
				return render(request,"showatt.html",{'newstudent':newstudent})

			
			else:
				messages.success(request,"No class attended or No Class Created ")
				return render(request,"showatt.html")
				

			
		else:
			print("bisht")
			qry = request.POST
			print(qry)
			print(request.POST.get('User'))
			#mydict=qrydict.dict()
			subj=request.POST.get('subject')
			usr=request.POST.get('User')
			cour=request.POST.get('course')
			att=Attendance.objects.all()
			if usr == '0000':
				#usr=Attendance.objects.values('user_id').distinct()
				usr=User.objects.filter(is_student='True').values('id')
				print("mahesh ID",usr)	
				test=[user for user in usr ]
				usr=[t['id'] for t in test ]
				# att=Attendance.objects.filter(user_id__in=test1)
				# print(att,"usr")
			if subj == '0000':
				#subj=Attendance.objects.values('subject_id').distinct()
				subj=subject.objects.values('id')
				test=[sub for sub in subj ]
				subj=[t['id'] for t in test ]
				# att=Attendance.objects.filter(subject_id__in=test1)
				# print(att,"subj")
			if cour == '0000':
				#cour=Attendance.objects.values('course_id').distinct()
				cour=course.objects.values('id')
				test=[cou for cou in cour ]
				cour=[t['id'] for t in test ]

			print("usr ",usr)
			print("cour ",cour)
			print("subj ",subj)


			# test=[]
			# final=[]
			# for s in subj:
			# 	print("test id",usr[0])
			# 	fi=Attendance.objects.filter(subject_id=s,user_id__in=usr,course_id__in=cour).values('user','subject','course','status').annotate(dcount=Count('subject'))
			# 	# test.append(fi)
			# 	mt=Attendance.objects.filter(subject_id=s,user_id=usr[2],course_id__in=cour).values('user','subject','course','status').annotate(dcount=Count('subject'))
			# 	print("mt ",mt)
			# 	#print("new ",Attendance.objects.filter(subject_id=s,user_id__in=usr,course_id__in=cour).values('user','subject').annotate(dcount=Count('subject')).first())
			# 	newdict={}
			# 	print("fi ",fi)
			# 	for t in fi:
			# 		print(t)
			# 		udata=User.objects.filter(id=t['user']).values('first_name','last_name','roll_no','course').first()
			# 		sdata=subject.objects.filter(id=t['subject']).values('s_name').first()
			# 		cdata=course.objects.filter(id=t['course']).values('c_name').first()
			# 		print("udata ",udata)
			# 		print("sdata ",sdata)
			# 		print("cdata ",cdata)
			# 		newdict.update(t)
			# 		newdict.update(udata)
			# 		newdict.update(sdata)
			# 		newdict.update(cdata)
			# 	if bool(newdict):
			# 		final.append(newdict)
			# 	# test=[]
			test=[]
			final=[]
			def Diff(list1, list2): 
 				return (list(list(set(list1)-set(list2)) + list(set(list2)-set(list1))))
			for ur in usr:
				print("ur ",ur)
				fi=Attendance.objects.filter(subject_id__in=subj,user_id=ur,course_id__in=cour,status='True').values('user','subject','course','status').annotate(dcount=Count('subject'))
				i=Attendance.objects.filter(subject_id__in=subj,user_id=ur,course_id__in=cour).values('user','subject','course','status').annotate(dcount=Count('subject'))
				print("i ",i)
				# test.append(fi)
				print("new if ",fi)

				#mt=Attendance.objects.filter(subject_id=s,user_id=usr[2],course_id__in=cour).values('user','subject','course','status').annotate(dcount=Count('subject'))
				#print("mt ",mt)
				#print("new ",Attendance.objects.filter(subject_id=s,user_id__in=usr,course_id__in=cour).values('user','subject').annotate(dcount=Count('subject')).first())
				couid=User.objects.filter(id=ur).values('course').first()
				print("courid ",couid)
				subid=subject.objects.filter(course_id=couid['course']).values('id')
				subid=[s['id'] for s in subid]
				print("subid ",subid)

				attcourid=Attendance.objects.filter(user_id=ur,status='True').values('subject').distinct()
				attcourid=[ar['subject']   for ar in attcourid]
				print("attcourid ",attcourid)
					

				if fi:
					
					#if len(fi) == 1 :

					for t in fi:
						newdict={}
						print(t)
						udata=User.objects.filter(id=t['user']).values('first_name','last_name','roll_no','course').first()
						sdata=subject.objects.filter(id=t['subject']).values('s_name').first()
						cdata=course.objects.filter(id=t['course']).values('c_name').first()
						print("udata ",udata)
						print("sdata ",sdata)
						print("cdata ",cdata)
						newdict.update(t)
						newdict.update(udata)
						newdict.update(sdata)
						newdict.update(cdata)
						print("newdict ",newdict)
						if bool(newdict):
							print("before final ",final)
							final.append(newdict)
							print("qwdqdqwdwwwwwwwwwwww")
							print("after final ",final)	
					if request.POST.get('subject') =='0000':

						if attcourid != subid:
							diff=Diff(subid,attcourid)
							
							for s in diff:
								newdict={}
								print("S",s)
								leftudata=User.objects.filter(id=ur).values('first_name','last_name','roll_no','course').first()
								leftsdata=subject.objects.filter(id=s).values('s_name').first()
								leftcdata=course.objects.filter(id=couid['course']).values('c_name').first()
								print("leftudata ",leftudata)
								print("leftsdata ",leftsdata)
								print("leftcdata ",leftcdata)
								
								newdict.update(leftudata)
								newdict.update(leftsdata)
								newdict.update(leftcdata)
								if bool(newdict):
									print("before final ",final)
									final.append(newdict)
									print("qwdqdqwdwwwwwwwwwwww")
									print("after final ",final)	

							print("newdict ",newdict)

							print("diff ",Diff(subid,attcourid))
							print("no")




				# test=[]
				else:
					print("mahesh lsit is emptry")
					print(ur)

					newdict={}
					
					udata=User.objects.filter(id=ur,course_id__in=cour).values('first_name','last_name','roll_no','course').first()
					print(udata)
					if udata:

						courses=course.objects.filter(id=udata['course']).values('c_name').first()
						#courlist=[courr['course'] for courr in udata]
						#print(courlist)
						#print(udata['course'])
						subjectt=subject.objects.filter(course_id=udata['course'],id__in=subj).values('s_name')
						print(subjectt)
						for subb in subjectt:
							newdict={}
							
							newdict.update(udata)
							newdict.update(courses)
							newdict.update(subb)
							print("newdict ",newdict)
							if bool(newdict):
								print("before final ",final)
								final.append(newdict)
								print("qwdqdqwdwwwwwwwwwwww")
								print("after final ",final)							

					# sdata=subject.objects.filter(id=t['subject']).values('s_name').first()
					# cdata=course.objects.filter(id=t['course']).values('c_name').first()
					# print("udata ",udata)
					# print("sdata ",sdata)
					# print("cdata ",cdata)
					# newdict.update(t)
					# newdict.update(udata)
					# newdict.update(sdata)
					# newdict.update(cdata)
					# print("newdict ",newdict)
					# if bool(newdict):
					# 	print("before final ",final)
					# 	final.append(newdict)
					# 	print("qwdqdqwdwwwwwwwwwwww")
					# 	print("after final ",final)

			print("final ",final)		
			print("test ",test)	
			for fi in final:
				print(fi)


			

			return render(request,"showatt.html",{'att':att,'final':final})
			
	else:
		#form=checkatt()
		return render(request,"checkattendance.html") #,{'form':form})
		
	




def checkattendance(request):
	print(request.user.is_student == 'True')
	if request.user.is_student:
		att=Attendance.objects.filter(course_id=request.user.course_id).values('subject')
		sub=subject.objects.filter(course_id=request.user.course_id)
		print(sub)
		print("mahesh")
	
		#print(att)

		
		
		return render(request,"checkattendance.html",{'sub':sub})
	else:		
		stud=User.objects.filter(is_student='True')
		cour=course.objects.all()
		subj=subject.objects.all()
		
		print(cour)
		return render(request,"checkattendance.html",{'stud':stud,'cour':cour,'subj':subj})		
		
def classtime(request):
	objt=createclasstime.objects.all()

	
	#print(type(objt.date))
	return render(request,"classtime.html",{'objt':objt})

def createclass_time(request):
	form=createclass()
	return render(request,"createclasstime.html",{'form':form})

def addclasstime(request):
	print(request.POST)
	if request.method =='POST':
		qrydict = request.POST
		print(request.POST.get('date'))
		mydict=qrydict.dict()
		mydict['date']=mydict['date']+' '+mydict['time']
		new_class_time=createclass(mydict)
		print(mydict['subject'])
		sid=mydict['subject']
		cid=mydict['course']
		print("date ",mydict['date'])
		uid=User.objects.filter(course_id=cid,is_student=True).values('id')
		print(uid)
		test=[]
		for ui in uid:
			test.append(ui['id'])
		print(test)	
		#print(Attendance.ob)

		
		if new_class_time.is_valid():
			#print(new_class_time.cleaned_data['date'])
			obj=new_class_time.save(True)
			print(obj.id)
			messages.success(request,"Class Time Successfully Created ")
			#temprol=new_stud.cleaned_data.get('roll_no')
			#print(type(temprol))
			#print(temprol)
			#form= attform()
			form=createclass()
			#context['form']= attform()
			#testform=attform() #initial={'user':test[0],'course':cid,'subject':sid,'status':False,'actualclasstime':obj.id})
			#print(attform(initial={'user':test,'course':cid,'subject':sid,'status':False,'actualclasstime':obj.id}))
			#testform['user']=test[0]
			# new_stud=attform(initial={'user':test[0],'course':cid,'subject':sid,'status':False,'actualclasstime':obj.id})
			# print(new_stud['user'])
			# new_stud.save(True)

			return render(request, "createclasstime.html",{'form':form}) 

		else:
			return render(request,'createclasstime.html',{'form':new_class_time} ) 
	else:

		new_class_time=createclass()
		return render(request,'createclasstime.html',{'form':new_class_time} )


def signuppageteacher(request):
	form=Registrationformteacher()
	form = Registrationformteacher(initial={'is_staff':True})
	
	return render(request, "signuppage.html",{'form':form})
def signuppagestudent(request):
	form=Registrationformstudent()
	form = Registrationformstudent(initial={'is_student':True})
	
	return render(request, "signuppage.html",{'form':form})
def login(request):
	return render(request,"login.html")
def Registerstudent(request):
	return render(request,"Registerstudent.html")


def Registerteacher(request):
	return render(request,"Registerteacher.html")
		

def stud_att(request):
	form= attformmytech()
	classtime=createclasstime.objects.all()
	print(form)	
	#context['form']= attform()
	return render(request, "test.html",{'form':form,'classtime':classtime}) 


def upload_img(request):
	if request.method == 'POST':
		print("mahesh")
		new_form=Img(request.POST)
		img=request.POST.get('mydata')
		#img = base64.b64decode(img)
		
	return render(request,"clickimg.html",{'img':img})


def clickimg(request):
	return render(request,"clickimg2.html")
def test1(request):
	if request.method == 'POST':
		print("mahesh")
		video_capture = cv2.VideoCapture(0)

		while True:
			ret, frame = video_capture.read()
			
			cv2.imshow('Video', frame)
		

		print("mahesh is the only boss")
	return render(request,"check.html")

def add_user_teacher(request):
	if request.method =='POST':
		new_stud=Registrationformteacher(request.POST)
		
		print(new_stud.is_valid())
		if new_stud.is_valid():
			new_stud.save(True)
			print(new_stud)
			messages.success(request,"Successfully Created ")
			#temprol=new_stud.cleaned_data.get('roll_no')
			#print(type(temprol))
			#print(temprol)
			form= attform()
			#context['form']= attform()
			return render(request, "test.html",{'form':form}) 

		else:
			return render(request,'signuppage.html',{'form':new_stud} ) 
	else:

		new_stud=Registrationformteacher()
		return render(request,'signuppage.html',{'form':new_stud} )

def addstudent(request):
	if request.method =='POST':
		new_stud=Registrationformstudent(request.POST)
		
		print(new_stud.is_valid())
		if new_stud.is_valid():
			new_stud.save(True)
			print(new_stud)
			#temprol=new_stud.cleaned_data.get('roll_no')
			#print(type(temprol))
			#print(temprol)
			form= attform()
			#context['form']= attform()
			return render(request, "Stud_dashboard.html") 

		else:
			return render(request,'Stud_dashboard.html',{'form':new_stud} ) 
	else:

		form=Registrationformstudent(initial={'is_student':True})
		return render(request,'addstudent.html',{'form':form} )	
def add_user_student(request):
	if request.method =='POST':
		new_stud=Registrationformstudent(request.POST)
		
		print(new_stud.is_valid())
		if new_stud.is_valid():
			new_stud.save(True)
			print(new_stud)
			#temprol=new_stud.cleaned_data.get('roll_no')
			#print(type(temprol))
			#print(temprol)
			form= attform()
			#context['form']= attform()
			return render(request, "test.html",{'form':form}) 

		else:
			return render(request,'signuppage.html',{'form':new_stud} ) 
	else:

		new_stud=Registrationformstudentr()
		return render(request,'signuppage.html',{'form':new_stud} )

def add_att_by_teacher(request):
	if request.method== 'POST':
		# print(request.user.id)
		qrydict = request.POST
		mydict=qrydict.dict()
		print(type(mydict))
		print(mydict)
		mydict['classtime']=mydict['classtime']+' '+mydict['time']

		#print(datetime.datetime.now,"mahesh")
		# mydict['user']=request.user.id
		# mydict['course']=request.user.course_id
		print(mydict)

		# #print(mydict['user'])
		new_object=attform(mydict)
		print(new_object)
		# cid=new_object.data['course']
		# sid=new_object.data['subject']
		# #cid=cid['course']
		# #print("course id",cid)
		# #print("subject id",sid)
		# print(type(new_object.data['time']))
		# print(type(new_object.data['classtime']))
		# new_object.data['classtime']=datetime.datetime.now()
		if new_object.is_valid():
			attend=new_object.save(commit=False)
			attend.save()
			messages.success(request,"Successfully Created ")
			return render(request,"test.html")

		else:
			messages.error(request, 'Complete All field')
			classtime=createclasstime.objects.all()
			return render(request, "test.html", {'form':new_object,'classtime':classtime})
	else:
		new_object=attform()
		classtime=createclasstime.objects.all()
		return render(request,"test.html")


		

			
def att_check(request):
	
	print("Reached here with data %r"%request)
	if request.method == 'POST':
		print(request.user.id)
		qrydict = request.POST
		mydict=qrydict.dict()
		print(type(mydict))
		print(datetime.datetime.now,"mahesh")
		mydict['user']=request.user.id
		mydict['course']=request.user.course_id

		print(mydict['user'])
		new_object=attform(mydict)
		# print(mydict['user'])
		# print(mydict['course'])
		# print(new_object.is_valid())
		# print(type(new_object.data['user']))
		# print(type(new_object.data['course']))
		# print(new_object.data['subject'])
		# print(new_object.data['status'])
		cid=new_object.data['course']
		sid=new_object.data['subject']
		#cid=cid['course']
		print("course id",cid)
		print("subject id",sid)
		new_object.data['classtime']=datetime.datetime.now()
		#new_object.data['time']=datetime.datetime.now()


		latestclasstime=createclasstime.objects.filter(course_id=cid,subject_id=sid).latest('date')
		print("tets, ",createclasstime.objects.filter(course_id=cid,subject_id=sid))
		print(latestclasstime)
		print(latestclasstime.date)
		print(request.POST.get('classtime'))
		print(new_object)
		temprol=request.user.roll_no #filter(roll_no=new_object.cleaned_data['roll']).values('first_name')
		print(temprol)
		temp=User.objects.filter(roll_no=str(temprol)).values('face_encoding')
		print(temp)		
		if new_object.is_valid():
			
			img=request.POST.get('mydata')
			print(request.user.course)
			
			temprol=request.user.roll_no #filter(roll_no=new_object.cleaned_data['roll']).values('first_name')
			print(temprol)
			temp=User.objects.filter(roll_no=str(temprol)).values('face_encoding')
			firstname=User.objects.filter(roll_no=str(temprol)).values('first_name')
			timeclass=User.objects.filter(roll_no=str(temprol)).values('course')
			print("mahesh classtime" ,timeclass)
			realname=firstname[0]['first_name']
			print(temp)
			#print(temp[0]['face_encoding'])
			face=temp[0]['face_encoding']
			#print(face)
			file_path = os.path.join(MEDIA_ROOT,face)
			print(file_path)
			
			objects = []
			with (open(file_path, "rb")) as openfile:
				while True:
					try:
						objects.append(pickle.load(openfile))
					except EOFError:
						break

			object1 = pd.read_pickle(file_path)	
			print(type(object1))
			encodings=object1['encodings']					
			image_file = io.BytesIO(base64.b64decode(img))
			file = Image.open(image_file).convert('RGB')
			open_cv_image = np.array(file)
			open_cv_image = open_cv_image[:, :, ::-1].copy()
			names=[]
			
			rgb=cv2.cvtColor(open_cv_image,cv2.COLOR_BGR2RGB)
			#rgb=cv2.cvtColor(np.float32(data1),cv2.COLOR_BGR2RGB)
			boxes=face_recognition.face_locations(rgb,model='cnn')
			encodingsface=face_recognition.face_encodings(rgb,boxes)
			print(type(encodingsface))
		
			for encoding in encodingsface:
				
				temp=len(encodings)
				matches=[]
				indx= [ matches.append(face_recognition.compare_faces(encodings[i], encoding,tolerance=0.6)) for i in range(temp)  ]
				
				name = "Unknown"
				matches=np.array(matches)
				
				if matches.any():
					print("face_matches_with_snap")
					matchesIndex = [ i for (i, b) in enumerate(matches) if b ]
					counts ={}
					#print(matchesIndex)
					for i in matchesIndex: 
					    name=object1["names"][i]
					    counts[name] = counts.get(name,0)+1
					    #print(counts)
					    name= max(counts , key=counts.get)
					names.append(name)

		
			print(name)
			#print(new_object.cleaned_data['classtime'])
			stud=User.objects.filter(roll_no=str(temprol)).values()
			marktime=new_object.cleaned_data['classtime']
			#print(latestclasstime+datetime.timedelta(hours=5,minutes=10))
			#print(latestclasstime.date)
			#print(latestclasstime.date+datetime.timedelta(hours=5,minutes=30))
			print("marktime ",marktime)
			#print(((datetime.timedelta(minutes=10).seconds)%3600)//60)
			#print(datetime.timedelta(minutes=10))
			print("atestclasstime ",latestclasstime)
			print("atestclasstime ",latestclasstime.date)
			latestcltime=latestclasstime.date #+datetime.timedelta(hours=5,minutes=30)
			print("atestcltime ",latestcltime)
			# print(datetime.datetime.date(latestcltime)+' '+datetime.datetime.time(latestcltime))
			maxminute=latestclasstime.date+datetime.timedelta(minutes=29)
			# if maxminute.hour >
			print("maxminute ",maxminute)
			print(latestcltime.minute <= marktime.minute <= maxminute.minute)
			print(latestcltime.hour == marktime.hour)
			print(latestcltime.hour == marktime.hour and (latestcltime.minute <= marktime.minute <= maxminute.minute))
			print(latestclasstime.date <= marktime)
			print(type(marktime))
			print(type(latestclasstime.date))
			print(marktime <= maxminute)
			print(type(maxminute))

			# print("compaer ",latestclasstime <= marktime)
			# print("compare",marktime <= maxminute)

			# print(attstatus.classtime)
			# print(latestclasstime.date)
			# print(latestclasstime.date<attstatus.classtime)
			# print(latestclasstime.date.time())
			# print(attstatus.classtime.minute)
			# newlatestcltime = datetime.datetime.strptime(str(latestcltime), "%Y-%m-%d %H:%M:%S%z")
			# print("newatestcltime ",newlatestcltime)
			# newmarktime = datetime.datetime.strptime(str(marktime), "%Y-%m-%d %H:%M:%S.%f%z")
			# print("newmarktime ",newmarktime)
			# newmaxminute = datetime.datetime.strptime(str(maxminute), "%Y-%m-%d %H:%M:%S%z")
			# print("newmaxminute ",newmaxminute)
			# test=str(maxminute)

			# print("compaer ",newlatestcltime >= newmarktime)
			# print("compare",newmarktime <= newmaxminute)
			if len(encodingsface) != 0:
				if realname in name:

					print(type(realname),' ',realname)
					print(type(name),' ',name)

					# if latestcltime.hour == marktime.hour and (latestcltime.minute <= marktime.minute <= maxminute.minute):
					if latestclasstime.date <= marktime and marktime <= maxminute:
						attend=new_object.save(commit=False)
						attend.save()
						print(attend)
					else:
						#new_object.data=[status]
						print("status ",new_object.data['status'])
						messages.error(request,"You cannot mark your attendacne because your are out of time")
						print("You cannot mark your attendacn")
						classtime=createclasstime.objects.all()
						print("latestclasstime",latestcltime)
						print("marktime",marktime)
						#new_object['status']='False'
						print("new_objecttt ",new_object)
						return render(request, "test.html", {'form':new_object,'classtime':classtime})


				else:
					messages.error(request,"face_doesnot_matches_with_snap")
					print("face_doesnot_matches_with_snap")
					classtime=createclasstime.objects.all()
					return render(request, "test.html", {'form':new_object,'classtime':classtime}) 
			else:
				messages.error(request, 'Complete All field')
				classtime=createclasstime.objects.all()
				return render(request, "test.html", {'form':new_object,'classtime':classtime})

						

			

		
			# print("-----------------------")
			# print(attstatus.classtime)
			# print(latestclasstime.date)
			# print(latestclasstime.date<attstatus.classtime)
			# print(latestclasstime.date.time())
			# print(attstatus.classtime.minute)
			# print(type(Attendance.objects.filter(user__roll_no=str(temprol))))
			
			    
			attstatus=Attendance.objects.filter(user__roll_no=str(temprol)).latest('classtime')

			return render(request, "clickimg.html", {'stud':stud,'attstatus':attstatus })
		else:
			messages.error(request, 'Complete All field')
			classtime=createclasstime.objects.all()
			return render(request, "test.html", {'form':new_object,'classtime':classtime}) 
			
	else:
		new_object=attform()
		classtime=createclasstime.objects.all()
		return render(request,"test.html",{'form':new_object,'classtime':classtime})
			

def Stud_dashboard(request):
	return render(request, "Stud_dashboard.html")
def Teach_dashboard(request):
	return render(request, "Teach_dashboard.html")

class index(View):
	#model=Post
	def get(self,request):
		#sset = Post.objects.filter(category='travel').order_by('-created_on')
		#posts=Post.objects.all()[0:3]
		#freqs=Post.objects.values('category').order_by().annotate(Count('category'))
		return render(request,'index.html') #,{'sset':sset,'freqs':freqs,'posts':posts,})

