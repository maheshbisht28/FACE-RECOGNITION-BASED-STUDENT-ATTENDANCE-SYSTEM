from django.contrib import admin


from .models import course , subject, User, Attendance, createclasstime

class Usertable(admin.ModelAdmin):
	list_display = ("id","roll_no","first_name","last_name","course","email","face_encoding","is_student","is_staff","is_superuser")


class coursetable(admin.ModelAdmin):
	list_display = ("id","code","c_name","total_years")


class subjecttable(admin.ModelAdmin):
	list_display = ("id","course","s_name","s_code","year")


class attendancetable(admin.ModelAdmin):
	list_display = ("id","user","subject","status","classtime","actualclasstime")

class classtimetable(admin.ModelAdmin):
	list_display = ("id","course","subject","date")


    #search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}
  
    #search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}

#admin.site.register(attendance1, Att)
admin.site.register(User,Usertable)
admin.site.register(course, coursetable)
admin.site.register(subject, subjecttable)
admin.site.register(Attendance,attendancetable)
admin.site.register(createclasstime,classtimetable)
