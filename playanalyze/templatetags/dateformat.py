from django.template import Library
from datetime import datetime
register = Library()

@register.filter
def dateformat(value):
	value = str(value)
	year = value[0:4]
	month = value[4:6]
	day = value[6:8]
	date = datetime.strptime(month+" "+day+" "+year, '%m %d %Y')
	return date

@register.filter
def integer(value):
	for i in range(len(value)):
		value[i] = float(value[i])
	return value