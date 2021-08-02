from django.urls import path , include
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
	
    path('',index.as_view(), name="index"),
    path('stud_att',stud_att, name="stud_att"),
    path('att_check',att_check,name="att_check"),
    #path('test1',test1,name='test1'),
    path('clickimg',clickimg,name='clickimg'),
    path('upload_img',upload_img,name='upload_img'),
    path('Registerstudent',Registerstudent,name='Registerstudent'),
    path('Registerteacher',Registerteacher,name='Registerteacher'),
    path('login',login,name='login'),
    path('signuppagestudent',signuppagestudent,name='signuppagestudent'),
    path('signuppageteacher',signuppageteacher,name='signuppageteacher'),
    path('add_user_teacher',add_user_teacher,name='add_user_teacher'),
    path('add_user_student',add_user_student,name='add_user_student'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('Stud_dashboard/',Stud_dashboard , name='Stud_dashboard'),
    path('Teach_dashboard/',Teach_dashboard , name='Teach_dashboard'),
    path('createclass_time/',createclass_time, name='createclass_time'),
    path('addclasstime/',addclasstime, name='addclasstime'),
    path('classtime/',classtime, name='classtime'),
    path('checkattendance/',checkattendance, name='checkattendance'),
    path('check/',check, name='check'),
    # path('editprofile/',editprofile, name='editprofile'),
    path('showattbydate/',showattbydate, name='showattbydate'),
    path('add_att_by_teacher/',add_att_by_teacher, name='add_att_by_teacher'),
    
    # path('<int:pk>/',editprofile, name='editprofile'),
    path('<int:pk>/',edituserprofile, name='edituserprofile'),
    
    path('studprofile/',studprofile,name='studprofile'),
    path('studprofilecheck/',studprofilecheck,name='studprofilecheck'),
     
    path('editprofilebyteach',editprofilebyteach,name='editprofilebyteach'),
    path('addstudent',addstudent,name='addstudent'),
    path('trainstudface/<int:pk>/',trainstudface,name='trainstudface')




    #path('checkatt',checkatt,name='checkatt'),
    
    #path('teacher/',teacher.as_view(), name="teacher"),
    #path('subject/',subject.as_view(), name="subject"),
    #path('tablenew/',tablenew.as_view(), name="tablenew"),
    #path('addatt/',addatt, name="addatt"),
    #path('test2/',test2, name="test2"),
    #path('showtable/',showtable, name="showtable"),

    #path('check/',check, name="check")		
    #path('<int:pk>/',blogpost.as_view(), name="blogpost"),
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)