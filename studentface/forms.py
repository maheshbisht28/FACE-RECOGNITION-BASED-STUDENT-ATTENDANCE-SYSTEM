from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import User , Attendance,createclasstime,subject
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from api.widgets import DateTimeWidget

#class  DateInput(forms.DateTimeInput):
#	input_type='date'

class trainface(forms.ModelForm):
	class Meta:
		model = User
		fields=['face_encoding']

class Editprofile(UserChangeForm):
	last_name=forms.CharField(max_length=10,required=False)

	class Meta:
		model=User
		fields=['id','first_name','last_name','email','course']

class  TimeInput(forms.TimeInput):
	input_type='time'
	

class createclass(forms.ModelForm):
	time=forms.TimeField(widget=TimeInput())
	#date = forms.DateTimeField(
    #    input_formats=['%d/%m/%Y %H:%M'], 
    #    widget=DateTimeWidget()
    #)

	class Meta:
		model=createclasstime
		fields =['course','subject','date','time']
		widgets = {'date':forms.widgets.DateTimeInput(
		format="%d/%m/%Y %H:%M:%S",attrs={
		#'id':"datetimepicker",
		'placeholder':"DD/MM/DD HH:MM:SS",'type':"date"}),
		 
		}
		#,'time':forms.widgets.TimeInput()}

class attform(forms.ModelForm):
	#time=forms.TimeField(widget=TimeInput())
	#actualcltime=forms.ModelChoiceField(queryset=createclasstime.objects.all().values('id'))
	class Meta:
		model=Attendance
		fields=['user','course','subject','status','classtime','actualclasstime']# ,'time']
		widgets = {'classtime':forms.widgets.DateTimeInput(
		format="%d/%m/%Y %H:%M:%S",attrs={
		#'id':"datetimepicker",
		'placeholder':"DD/MM/DD HH:MM:SS",'type':"date"}),
		 
		}
class attformmytech(forms.ModelForm):
	time=forms.TimeField(widget=TimeInput())
	#actualcltime=forms.ModelChoiceField(queryset=createclasstime.objects.all().values('id'))
	class Meta:
		model=Attendance
		fields=['user','course','subject','status','classtime','actualclasstime' ,'time']
		widgets = {'classtime':forms.widgets.DateTimeInput(
		format="%d/%m/%Y %H:%M:%S",attrs={
		#'id':"datetimepicker",
		'placeholder':"DD/MM/DD HH:MM:SS",'type':"date"}),
		 
		}		
# class Createclass(ModelForm):
# 	class Meta:
# 		model=Attendance


class Registrationformstudent(ModelForm):

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model=User
		fields=['roll_no','first_name','last_name','email','year','is_staff','is_student','course']
	def clean_roll_no(self):
		roll = self.cleaned_data['roll_no']
		if User.objects.filter(roll_no=roll).exists():
			raise ValidationError("Roll already exists")
		return roll
			
		
	def clean_password2(self):
		pwd1 = self.cleaned_data.get('password1')
		pwd2 = self.cleaned_data.get('password2')
		if not pwd1 or not pwd2:
			raise forms.ValidationError('Password is empty')
		if pwd1 != pwd2:
			raise forms.ValidationError('Passwords do not match')
		return pwd2


	def save(self, commit=True):
		user = super(Registrationformstudent,self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
		    user.save()
		return user	

class Registrationformteacher(ModelForm):

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model=User
		fields=['first_name','last_name','email','is_staff','is_student']
	
			
		
	def clean_password2(self):
		pwd1 = self.cleaned_data.get('password1')
		pwd2 = self.cleaned_data.get('password2')
		if not pwd1 or not pwd2:
			raise forms.ValidationError('Password is empty')
		if pwd1 != pwd2:
			raise forms.ValidationError('Passwords do not match')
		return pwd2


	def save(self, commit=True):
		user = super(Registrationformteacher,self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
		    user.save()
		return user	




class Img(forms.Form):
	img=forms.ImageField() 