from django.db import models
import datetime 
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager


YEARS = (    
    ('1', 1),
    ('2', 2),
    ('3', 3),    
    ('4', 4),    
    ('5', 5),
    ('NA','NA')    
)

CATEGORY_CHOICES2 = (
    ('0', 0),
    ('1', 1),
    ('2', 2),
    
)
 

class studentManage(BaseUserManager):
    def create_user(self,email,first_name,password=None):
        if not email:
            raise ValueError("users must have an email")
        
        if not first_name:
            raise ValueError("users must have an first_name")
        user = self.model(
               email=self.normalize_email(email),
               first_name = first_name,
               roll_no = 00,
               )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,first_name,password):
        user=self.create_user(
            email=self.normalize_email(email),
            first_name =first_name,
            password = password
            )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

         
class User(AbstractBaseUser):
    roll_no= models.IntegerField(default='000')
    img = models.ImageField(upload_to='file/',default='file/S.jpg')
    #username=models.CharField(max_length=10,unique=True)
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    course=models.ForeignKey(course,on_delete=models.CASCADE,null=True,blank=True)
    year=models.CharField(choices=YEARS, max_length=2,default='NA')
    email=models.EmailField(verbose_name='email', max_length=20, unique=True)
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    face_encoding=models.FileField(upload_to='file/',default='not applicable', null=True, blank=True)
    #img=models.ImageField(upload_to='image/',default='')
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['first_name',]


    objects= studentManage()
    def __str__(self):
        return str(self.roll_no)

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class course(models.Model):
    #roll_no=models.OnetoOne
    code=models.CharField(max_length=10, unique=True)
    c_name=models.CharField(max_length=10,unique=True)
    total_years=models.CharField(choices=YEARS, max_length=2)

    def __str__(self):
        return self.c_name

class subject(models.Model):
    course=models.ForeignKey(course,on_delete=models.CASCADE)
    s_name=models.CharField(max_length=10)
    s_code=models.CharField(max_length=10)
    year=models.CharField(choices=YEARS, max_length=2)

    def __str__(self):
        return self.s_name 

class createclasstime(models.Model):
    course=models.ForeignKey(course,on_delete=models.CASCADE)
    subject=models.ForeignKey(subject,on_delete=models.CASCADE)
    date=models.DateTimeField(verbose_name='date')
    def __str__(self):
        return '{} {} {}'.format(self.course, self.subject,self.date)
            

class Attendance(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(course,on_delete=models.CASCADE,null=True)
    subject=models.ForeignKey(subject,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    classtime=models.DateTimeField(null=True)
    actualclasstime=models.ForeignKey(createclasstime,on_delete=models.CASCADE,null=True)
    









#class attendance1(models.Model):
#    roll_no= models.CharField(primary_key=True,    max_length=11,unique=True)
#    name = models.CharField(max_length=20)
    #Date = models.DateField()
    #slug = models.SlugField(max_length=200, unique=True)
    #author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    #updated_on = models.DateTimeField(auto_now= True)
    #content = models.TextField()
    #created_on = models.DateTimeField(auto_now_add=True)
    #roll_no = models.IntegerField(default=0,max_length=11, unique=True)
    
#    year = models.CharField(max_length=12,default="", choices=CATEGORY_CHOICES,)
    #name = models.CharField(max_length=20)
    #Date = models.DateField()
    #slug = models.SlugField(max_length=200, unique=True)
    #author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    #updated_on = models.DateTimeField(auto_now= True)
    #content = models.TextField()
    #created_on = models.DateTimeField(auto_now_add=True)
    #roll_no = models.IntegerField(default=0,max_length=11, unique=True)
    #roll_no= models.CharField(max_length=11)
    #atten=models.TextField(max_length=2,default="", choices=CATEGORY_CHOICES2)
    
    #class Meta:
     #   ordering = ['-created_on']

    #def __str__(self):
     #   return self.title


