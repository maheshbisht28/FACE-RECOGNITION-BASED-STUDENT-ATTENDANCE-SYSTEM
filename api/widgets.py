from django.forms import DateTimeInput

class DateTimeWidget(DateTimeInput):
	import os
	print('----------')
	print(os.getcwd())
	print('----------')
	template_name = 'widgets/datetimepicker.html'