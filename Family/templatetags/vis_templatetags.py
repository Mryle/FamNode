from django import template
import datetime
import time

register = template.Library()

@register.filter
def vis_timestamp(timestamp):
	#try:
	#	ts = float(timestamp)
	#except ValueError:
	#	return None
	return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp.timestamp()))