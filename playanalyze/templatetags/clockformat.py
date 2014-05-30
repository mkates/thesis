from django.template import Library
from datetime import datetime
register = Library()

@register.filter
def clockformat(value):
	minutes = int(value/60)
	seconds = int(value)%60
	if '.' in str(value):
		decimal = str(value).split('.')[1]
	else:
		decimal = ''
	if len(decimal) == 0:
		decimal = '00'
	elif len(decimal) == 1:
		decimal = '0'+decimal
	return str(minutes)+":"+str(seconds).zfill(2)+":"+ str(decimal)
